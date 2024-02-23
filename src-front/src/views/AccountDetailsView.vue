<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';

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
      router.push({ name: 'login' });
      return;
    } else {
      console.log(e);
    }
    router.push({ name: 'home' });
  }
});

const handleDeleteClick = () => {
  showConfirmation.value = true; // Show the confirmation popup
}

const confirmDelete = async () => {
  try {
    await Services.accountsService.deleteAccount(accountDetails.id);
    console.log("Account deleted successfully");
    router.push({ name: 'home' });
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
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="red"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 6h18" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              <line x1="10" y1="11" x2="10" y2="17" />
              <line x1="14" y1="11" x2="14" y2="17" />
            </svg>
          </a>
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
  display: flex;
  /* Добавлено для flexbox */
  justify-content: space-between;
  /* Распределяет пространство между элементами */
  align-items: center;
  /* Центрирует элементы по вертикали */
}

.account-name {
  font-size: 1em;
  color: #333;
  display: flex;
  /* Обеспечивает гибкое расположение для дочерних элементов */
  justify-content: space-between;
  /* Располагает элементы на противоположных концах */
  width: 100%;
  /* Занимает всю доступную ширину */
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


