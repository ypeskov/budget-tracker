<script setup>
import {computed, onMounted, ref} from 'vue';
import {usePlannedTransactionsStore} from '@/stores/plannedTransactions';
import {useAccountStore} from '@/stores/account';
import {useCategoriesStore} from '@/stores/categories';
import {useUserStore} from '@/stores/user';
import {PlannedTransactionsService} from '@/services/plannedTransactions';
import {AccountService} from '@/services/accounts';
import {CategoriesService} from '@/services/categories';
import {SettingsService} from '@/services/settings';
import BalanceProjectionChart from '@/components/planning/BalanceProjectionChart.vue';
import StatisticsPanel from '@/components/planning/StatisticsPanel.vue';
import UpcomingTransactionsList from '@/components/planning/UpcomingTransactionsList.vue';
import PlannedTransactionModal from '@/components/planning/PlannedTransactionModal.vue';
import ConfirmDialog from '@/components/utils/ConfirmDialog.vue';

const store = usePlannedTransactionsStore();
const accountStore = useAccountStore();
const categoryStore = useCategoriesStore();
const userStore = useUserStore();

const plannedTxService = new PlannedTransactionsService(userStore, accountStore);
const accountService = new AccountService(accountStore, userStore);
const categoriesService = new CategoriesService(categoryStore, userStore);
const settingsService = new SettingsService(userStore);

const showModal = ref(false);
const selectedTransaction = ref(null);
const modalLoading = ref(false);
const balanceProjection = ref(null);
const futureBalanceData = ref(null);
const showDeleteConfirm = ref(false);
const transactionToDelete = ref(null);
const showInactive = ref(false);

// Projection settings
const getDefaultEndDate = () => {
  // Check user settings first
  const savedDate = userStore.settings?.projectionEndDate;
  if (savedDate) {
    // Validate that saved date is in the future
    const saved = new Date(savedDate);
    const now = new Date();
    if (saved > now) {
      return savedDate;
    }
  }

  // Default: 30 days from now
  const date = new Date();
  date.setDate(date.getDate() + 30);
  return date.toISOString().split('T')[0];
};

const getDefaultPeriod = () => {
  // Check user settings first
  const savedPeriod = userStore.settings?.projectionPeriod;
  if (savedPeriod && ['daily', 'weekly', 'monthly'].includes(savedPeriod)) {
    return savedPeriod;
  }
  // Default: daily
  return 'daily';
};

const projectionSettings = ref({
  endDate: getDefaultEndDate(),
  period: getDefaultPeriod(),
});

// Computed properties
const baseCurrency = computed(() => {
  // First check localStorage (user is already logged in)
  const storedBaseCurrency = localStorage.getItem('baseCurrency');
  if (storedBaseCurrency) {
    return storedBaseCurrency;
  }
  // Fallback to store
  return userStore.baseCurrency || 'USD';
});

const totalCurrentBalance = computed(() => {
  return accountStore.accounts
    .filter(acc => acc.showInReports !== false) // Only include accounts shown in reports
    .reduce((sum, acc) => sum + parseFloat(acc.balanceInBaseCurrency || 0), 0);
});

const projectedBalance = computed(() => {
  if (!balanceProjection.value || !balanceProjection.value.projectionPoints) {
    return totalCurrentBalance.value;
  }
  const points = balanceProjection.value.projectionPoints;
  return points.length > 0 ? points[points.length - 1].balance : totalCurrentBalance.value;
});

const totalPlannedIncome = computed(() => {
  return futureBalanceData.value?.totalPlannedIncome || 0;
});

const totalPlannedExpenses = computed(() => {
  return futureBalanceData.value?.totalPlannedExpenses || 0;
});

const incomeTransactionsCount = computed(() => {
  return futureBalanceData.value?.incomeCount || 0;
});

const expenseTransactionsCount = computed(() => {
  return futureBalanceData.value?.expensesCount || 0;
});

const inactiveCount = computed(() => {
  return store.plannedTransactions.filter(t => !t.isActive).length;
});

onMounted(async () => {
  await Promise.all([
    loadAccounts(),
    loadCategories(),
    loadPlannedTransactions(),
    loadUpcomingOccurrences(),
    loadBalanceProjection(),
    loadFutureBalance(),
  ]);
});

async function loadAccounts() {
  try {
    // Always load fresh data with balanceInBaseCurrency
    await accountService.getUserAccounts({
      includeHidden: false,
      includeArchived: false,
      shouldUpdate: true, // Force refresh
    });
  } catch (error) {
    console.error('Failed to load accounts:', error);
  }
}

async function loadCategories() {
  // Only load if categories are not already in store
  if (categoryStore.categories.length === 0) {
    try {
      await categoriesService.getUserCategories();
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  }
}

async function loadPlannedTransactions() {
  try {
    store.setLoading(true);
    const transactions = await plannedTxService.getPlannedTransactions({
      isExecuted: false,
      includeInactive: true, // Load all to count inactive
    });
    store.setPlannedTransactions(transactions);
  } catch (error) {
    store.setError(error.message || 'Failed to load planned transactions');
  } finally {
    store.setLoading(false);
  }
}

async function loadUpcomingOccurrences() {
  try {
    const days = Math.ceil((new Date(projectionSettings.value.endDate) - new Date()) / (1000 * 60 * 60 * 24));
    const occurrences = await plannedTxService.getUpcomingOccurrences({
      days: Math.max(days, 30),
      includeInactive: showInactive.value,
    });
    store.setUpcomingOccurrences(occurrences);
  } catch (error) {
    console.error('Failed to load upcoming occurrences:', error);
  }
}

async function loadBalanceProjection() {
  try {
    const projection = await plannedTxService.getBalanceProjection({
      endDate: new Date(projectionSettings.value.endDate).toISOString(),
      period: projectionSettings.value.period,
      accountIds: null,
      includeInactive: false, // Always exclude inactive from projections
    });

    balanceProjection.value = projection;
  } catch (error) {
    console.error('Failed to load balance projection:', error);
  }
}

async function loadFutureBalance() {
  try {
    const futureBalance = await plannedTxService.calculateFutureBalance({
      targetDate: new Date(projectionSettings.value.endDate).toISOString(),
      accountIds: null,
      includeInactive: showInactive.value,
    });

    futureBalanceData.value = futureBalance;
  } catch (error) {
    console.error('Failed to load future balance:', error);
  }
}

async function onShowInactiveChange() {
  // Reload all data when checkbox changes
  Promise.all([
    loadBalanceProjection(),
    loadFutureBalance(),
    loadUpcomingOccurrences(),
  ]);
}

async function onProjectionSettingsChange() {
  // Save settings to user settings
  try {
    const updatedSettings = {
      ...userStore.settings,
      projectionEndDate: projectionSettings.value.endDate,
      projectionPeriod: projectionSettings.value.period,
    };
    await settingsService.saveUserSettings(updatedSettings);
    Object.assign(userStore.settings, updatedSettings);
  } catch (error) {
    console.error('Failed to save projection settings:', error);
  }

  // Reload data when settings change
  Promise.all([
    loadBalanceProjection(),
    loadFutureBalance(),
    loadUpcomingOccurrences(),
  ]);
}

async function resetProjectionSettings() {
  // Reset to default (30 days, daily period)
  const date = new Date();
  date.setDate(date.getDate() + 30);
  projectionSettings.value = {
    endDate: date.toISOString().split('T')[0],
    period: 'daily',
  };

  // Save reset values to user settings
  try {
    const updatedSettings = {
      ...userStore.settings,
      projectionEndDate: projectionSettings.value.endDate,
      projectionPeriod: projectionSettings.value.period,
    };
    await settingsService.saveUserSettings(updatedSettings);
    Object.assign(userStore.settings, updatedSettings);
  } catch (error) {
    console.error('Failed to save projection settings:', error);
  }

  // Reload data
  Promise.all([
    loadBalanceProjection(),
    loadFutureBalance(),
    loadUpcomingOccurrences(),
  ]);
}

function showCreateModal() {
  selectedTransaction.value = null;
  showModal.value = true;
}

async function editPlanned(plannedTransactionId) {
  try {
    selectedTransaction.value = await plannedTxService.getPlannedTransaction(plannedTransactionId);
    showModal.value = true;
  } catch (error) {
    store.setError(error.message || 'Failed to load planned transaction');
  }
}

async function handleModalSubmit(data) {
  modalLoading.value = true;
  try {
    if (data.id) {
      // Update existing
      const updated = await plannedTxService.updatePlannedTransaction(data.id, data);
      store.updatePlannedTransaction(updated);
    } else {
      // Create new
      const created = await plannedTxService.createPlannedTransaction(data);
      store.addPlannedTransaction(created);
    }

    showModal.value = false;
    await Promise.all([
      loadBalanceProjection(),
      loadFutureBalance(),
      loadUpcomingOccurrences(),
    ]);
  } catch (error) {
    store.setError(error.message || 'Failed to save planned transaction');
  } finally {
    modalLoading.value = false;
  }
}

function deletePlanned(id) {
  transactionToDelete.value = id;
  showDeleteConfirm.value = true;
}

async function confirmDelete() {
  if (!transactionToDelete.value) return;

  try {
    await plannedTxService.deletePlannedTransaction(transactionToDelete.value);
    store.removePlannedTransaction(transactionToDelete.value);
    await Promise.all([
      loadBalanceProjection(),
      loadFutureBalance(),
      loadUpcomingOccurrences(),
    ]);
  } catch (error) {
    store.setError(error.message || 'Failed to delete planned transaction');
  } finally {
    transactionToDelete.value = null;
  }
}

</script>


<template>
  <div class="financial-planning-view container-fluid mt-4">
    <div class="page-header mb-4">
      <h1 class="page-title">
        <i class="bi bi-graph-up-arrow"></i>
        {{ $t('financialPlanning.title') }}
      </h1>
      <button class="btn btn-primary btn-lg" @click="showCreateModal">
        <i class="bi bi-plus-circle"></i>
        {{ $t('financialPlanning.createPlanned') }}
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="store.loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">{{ $t('common.loading') }}</span>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="store.error" class="alert alert-danger alert-dismissible fade show">
      <i class="bi bi-exclamation-triangle"></i>
      {{ store.error }}
      <button type="button" class="btn-close" @click="store.clearError()"></button>
    </div>

    <!-- Main content -->
    <div v-else>
      <!-- Projection Settings -->
      <div class="row mb-3">
        <div class="col-12">
          <div class="card settings-card">
            <div class="card-body">
              <div class="row align-items-end g-3">
                <div class="col-md-3">
                  <label class="form-label">{{ $t('financialPlanning.projectionEndDate') }}</label>
                  <input
                    type="date"
                    class="form-control"
                    v-model="projectionSettings.endDate"
                    @change="onProjectionSettingsChange"
                  />
                </div>
                <div class="col-md-3">
                  <label class="form-label">{{ $t('financialPlanning.projectionPeriod') }}</label>
                  <select
                    class="form-select"
                    v-model="projectionSettings.period"
                    @change="onProjectionSettingsChange"
                  >
                    <option value="daily">{{ $t('financialPlanning.periods.daily') }}</option>
                    <option value="weekly">{{ $t('financialPlanning.periods.weekly') }}</option>
                    <option value="monthly">{{ $t('financialPlanning.periods.monthly') }}</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <div class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="showInactiveCheckbox"
                      v-model="showInactive"
                      @change="onShowInactiveChange"
                    />
                    <label class="form-check-label" for="showInactiveCheckbox">
                      {{ $t('financialPlanning.showInactive') }}
                      <span v-if="inactiveCount > 0" class="badge bg-secondary ms-1">{{ inactiveCount }}</span>
                    </label>
                  </div>
                </div>
                <div class="col-md-3">
                  <button class="btn btn-outline-secondary w-100" @click="resetProjectionSettings">
                    <i class="bi bi-arrow-clockwise"></i>
                    {{ $t('financialPlanning.resetSettings') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top section: Chart and Statistics -->
      <div class="row mb-4">
        <!-- Balance Projection Chart -->
        <div class="col-lg-7 mb-4">
          <div class="card chart-card">
            <div class="card-body">
              <h5 class="card-title">
                <i class="bi bi-graph-up"></i>
                {{ $t('financialPlanning.balanceProjection') }}
              </h5>
              <BalanceProjectionChart
                v-if="balanceProjection"
                :projection-data="balanceProjection"
                :current-balance="totalCurrentBalance"
                :currency="balanceProjection?.baseCurrencyCode || baseCurrency"
              />
              <div v-else class="projection-placeholder">
                <p class="text-muted">{{ $t('financialPlanning.loadingProjection') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Statistics Panel -->
        <div class="col-lg-5 mb-4">
          <StatisticsPanel
            :current-balance="totalCurrentBalance"
            :projected-balance="projectedBalance"
            :total-income="totalPlannedIncome"
            :total-expenses="totalPlannedExpenses"
            :income-count="incomeTransactionsCount"
            :expenses-count="expenseTransactionsCount"
            :currency="futureBalanceData?.baseCurrencyCode || baseCurrency"
            :projection-end-date="projectionSettings.endDate"
          />
        </div>
      </div>

      <!-- Upcoming Transactions -->
      <div class="row">
        <div class="col-12">
          <div class="card transactions-card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-calendar-check"></i>
                {{ $t('financialPlanning.upcomingTransactions') }}
              </h5>
            </div>
            <div class="card-body">
              <UpcomingTransactionsList
                :transactions="store.upcomingOccurrences"
                :currency="futureBalanceData?.baseCurrencyCode || baseCurrency"
                @edit="editPlanned"
                @delete="deletePlanned"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Create/Edit -->
    <PlannedTransactionModal
      v-model="showModal"
      :transaction="selectedTransaction"
      :loading="modalLoading"
      @submit="handleModalSubmit"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      :title="$t('financialPlanning.confirmDelete')"
      :message="$t('financialPlanning.confirmDeleteMessage')"
      :confirm-text="$t('common.delete')"
      :cancel-text="$t('common.cancel')"
      @confirm="confirmDelete"
    />
  </div>
</template>


<style scoped>
.financial-planning-view {
  max-width: 1400px;
  padding-bottom: 3rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-title i {
  color: #0d6efd;
}

.card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.settings-card .card-body {
  padding: 1rem 1.5rem;
}

.settings-card .form-label {
  font-weight: 500;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: #495057;
}

.settings-card .form-control,
.settings-card .form-select {
  border-radius: 8px;
}

.chart-card {
  height: 100%;
}

.chart-card .card-body {
  padding: 1.5rem;
}

.chart-card .card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.projection-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.transactions-card .card-header {
  background: white;
  border-bottom: 2px solid #f1f3f5;
  padding: 1.25rem 1.5rem;
}

.transactions-card .card-title {
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alert {
  border-radius: 12px;
}

@media (max-width: 992px) {
  .page-title {
    font-size: 1.5rem;
  }

  .btn-lg {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-lg {
    width: 100%;
  }
}
</style>
