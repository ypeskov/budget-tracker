<script setup>
import { onBeforeMount, reactive, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { Services } from '@/services/servicesConfig';
import { HttpError } from '@/errors/HttpError';

import TransactionsListView from './TransactionsListView.vue';

const route = useRoute();
const router = useRouter();

let accountDetails = reactive({});
const showConfirmation = ref(false);

onBeforeMount(async () => {
  try {
    const details = await Services.accountsService.getAccountDetails(route.params.id);
    accountDetails = Object.assign(accountDetails, details);
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      console.log(e.message);
      await router.push({name: 'login'});
      return;
    } else {
      console.log(e);
    }
    await router.push({name: 'home'});
  }
});

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

const confirmDelete = async () => {
  try {
    await Services.accountsService.deleteAccount(accountDetails.id);
    console.log("Account deleted successfully");
    router.push({ name: 'accounts' });
  } catch (e) {
    console.error("Failed to delete account:", e);
    // Handle error, e.g., display an error message to the user
  } finally {
    showConfirmation.value = false; // Hide popup regardless of outcome
  }
}
</script>

<template>
  <main>
    <div class="container">
      <div class="account-row">
        <div class="account-name">
          <span>Account: <strong>{{ accountDetails.name }}</strong></span>
          <a class="delete-acc-icon" href="" @click.prevent="handleDeleteClick">
            <img src="/images/icons/edit-icon.svg" alt="Edit account" width="24" height="24" title="Edit account" />

          </a>
        </div>
        <div class="account-balance">
          <span>Balance: <b>{{ formattedBalance }}&nbsp;{{ accountDetails?.currency?.code }}</b></span>
          <a class="edit-acc-icon" href="" @click.prevent="">
            <img src="/images/icons/delete-icon.svg" alt="Delete account" width="24" height="24"
              title="Delete account" />
          </a>
        </div>
        <div class="account-open-date">
          <span>Created: <b>{{ DateTime.fromISO(accountDetails?.openingDate).toISODate() }}</b></span>
        </div>
      </div>
    </div>

    <TransactionsListView :account-id="accountDetails.id" :is-account-details="true" />

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
