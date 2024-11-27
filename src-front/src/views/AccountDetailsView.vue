<script setup>
import { onBeforeMount, reactive, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { DateTime } from 'luxon';

import { Services } from '../services/servicesConfig';
import { processError } from '@/errors/errorHandlers';

import TransactionsListView from './TransactionsListView.vue';
import newAccount from '../components/account/newAccount.vue';
import { CREDIT_CARD_ACC_TYPE_ID } from '@/constants.js';

const route = useRoute();
const router = useRouter();
const t = useI18n().t;

let accountDetails = reactive({});
const showConfirmation = ref(false);
const showEditAccForm = ref(false);

onBeforeMount(async () => {
  await loadAccountDetails();
});

async function loadAccountDetails() {
  try {
    const details = await Services.accountsService.getAccountDetails(route.params.id);
    if (details) {
      accountDetails = Object.assign(accountDetails, details);
    }
  } catch (e) {
    await processError(e, router);
  }
}

const handleDeleteClick = () => {
  showConfirmation.value = true; // Show the confirmation popup
}

const formattedBalance = computed(() => {
  if (!accountDetails.balance) return '0.00';
  return accountDetails.balance.toLocaleString('ru-UA', {
    style: 'decimal',
    maximumFractionDigits: 2,
    minimumFractionDigits: 2
  })
})

const handleUpdateAccount = () => {
  loadAccountDetails();
  closeEditAccForm();
}

const handleEditClick = () => {
  showEditAccForm.value = true;
}

const closeEditAccForm = () => {
  showEditAccForm.value = false;
}

const confirmDelete = async () => {
  try {
    await Services.accountsService.deleteAccount(accountDetails.id);
    await router.push({name: 'accounts'});
  } catch (e) {
    await processError(e, router);
  } finally {
    showConfirmation.value = false; // Hide popup regardless of outcome
  }
}

const availableBalanceCC = computed(() => {
  return accountDetails.balance + accountDetails.creditLimit;
})
</script>

<template>
  <main>
    <div class="container">
      <div class="account-row">
        <div class="account-name">
          <span>{{$t('message.account')}}: <strong>{{ accountDetails.name }}</strong></span>
          <a class="edit-acc-icon" href="" @click.prevent="handleEditClick">
            <img src="/images/icons/edit-icon.svg" alt="Edit account"
                 width="24" height="24" :title="t('message.editAccount')" />
          </a>
        </div>

        <div class="account-balance">
          <span>
            {{$t('message.balance')}}: <b>{{ formattedBalance }}
            <span v-if="accountDetails.accountType==CREDIT_CARD_ACC_TYPE_ID">({{ availableBalanceCC }})</span>
            &nbsp;{{ accountDetails?.currency?.code }}</b>
          </span>
          <a class="edit-acc-icon" href="" @click.prevent="handleDeleteClick">
            <img src="/images/icons/delete-icon.svg" alt="Delete account" width="24" height="24"
              :title="t('message.deleteAccount')" />
          </a>
        </div>
        <div class="account-open-date">
          <span>{{$t('message.created')}}: <b>{{ DateTime.fromISO(accountDetails?.openingDate).toISODate() }}</b></span>
        </div>
      </div>
    </div>

    <div v-if="showEditAccForm" class="row">
      <div class="col">
        <newAccount
            :account-created="handleUpdateAccount"
            :close-new-acc-form="closeEditAccForm"
            :account-details="accountDetails"
        />
      </div>
    </div>

    <TransactionsListView :account-id="route.params.id" :is-account-details="true" />

    <div v-if="showConfirmation" class="confirmation-popup-overlay">
      <div class="confirmation-popup">
        <p>Are you sure want to delete this account?</p>
        <a @click="confirmDelete" class="btn btn-primary">Yes</a>
        <a @click="showConfirmation = false" class="btn btn-secondary">No</a>
      </div>
    </div>


  </main>
</template>

<style scoped>
.container {
  margin: 0 auto;
}

.account-row {
  background-color: #e2e0e0;
  padding: 5px 10px;
  border-radius: 5px;
  margin: 0.5rem 0 0.5rem 0.5rem;
}

.account-name,
.account-balance {
  font-size: 1em;
  color: #333;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.delete-acc-icon {
  display: inline-block;
  text-decoration: none;
}

.confirmation-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.confirmation-popup {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  width: 90%;
  max-width: 400px;
}

.btn-primary {
  margin-right: 8px;
}
</style>
