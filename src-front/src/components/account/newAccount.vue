<script setup>
import { ref } from 'vue';

const accountType = ref(2);
const currency = ref(2);
const name = ref('');
const balance = ref(1000);
const openingDate = ref('');
const comment = ref('');
const isHidden = ref(false);

function createAccount() {
  const newAccount = {
    account_type_id: accountType.value,
    currency_id: currency.value,
    name: name.value,
    balance: balance.value,
    opening_date: openingDate.value,
    comment: comment.value,
    is_hidden: isHidden.value
  };
  // Send newAccount to server or perform other actions
}
</script>

<template>
  <form @submit.prevent="createAccount">
    <div>
      <label for="account_type_id">Account Type ID:</label>
      <input type="number" id="account_type_id" v-model="accountType" required>
    </div>
    <div>
      <label for="currency_id">Currency ID:</label>
      <input type="number" id="currency_id" v-model="currency" required>
    </div>
    <div>
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="name" required>
    </div>
    <div>
      <label for="balance">Balance:</label>
      <input type="number" id="balance" v-model="balance" required>
    </div>
    <div>
      <label for="opening_date">Opening Date:</label>
      <input type="datetime-local" id="opening_date" v-model="openingDate" required>
    </div>
    <div>
      <label for="comment">Comment:</label>
      <textarea id="comment" v-model="comment"></textarea>
    </div>
    <div>
      <label for="is_hidden">Is Hidden:</label>
      <input type="checkbox" id="is_hidden" v-model="isHidden">
    </div>
    <button type="submit">Create Account</button>
  </form>
</template>

<style scoped>
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
  }

  label {
    font-weight: bold;
  }

  input[type="number"],
  input[type="text"],
  input[type="datetime-local"],
  textarea {
    padding: 0.5rem;
    border-radius: 0.25rem;
    border: 1px solid #ccc;
    width: 100%;
    box-sizing: border-box;
  }

  input[type="checkbox"] {
    margin-left: 0.5rem;
  }

  button[type="submit"] {
    background-color: #4caf50;
    color: #fff;
    border: none;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button[type="submit"]:hover {
    background-color: #3e8e41;
  }
</style>