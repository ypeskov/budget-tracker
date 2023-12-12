<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';

let registerEmail = ref('');
let registerPassword = ref('');
let firstName = ref('');
let lastName = ref('');
let errorMessage = ref(''); // Add this line for the error message

const router = useRouter();

function updateEmail(event) {
  registerEmail.value = event.target.value;
  errorMessage.value = ''; // Clear error message when email is changed
}

async function submitRegistration() {
  try {
    await Services.userService.registerUser(registerEmail.value, registerPassword.value, firstName.value, lastName.value);
    registerEmail.value = '';
    registerPassword.value = '';
    firstName.value = '';
    lastName.value = '';
    router.push('/login');
  } catch (error) {
    errorMessage.value = `Registration failed: ${error.message}`; 
  }
}

const emailInputRef = ref(null);

onMounted(() => {
  if (emailInputRef.value) {
    emailInputRef.value.focus();
  }
});
</script>

<template>
  <div class="container mt-5">
    <main>
      <form @submit.prevent="submitRegistration" autocomplete="on">
        <div class="mb-3">
          <label for="firstNameInput" class="form-label">First Name</label>
          <input type="text" class="form-control" id="firstNameInput" v-model="firstName" placeholder="First Name" />
        </div>
        <div class="mb-3">
          <label for="lastNameInput" class="form-label">Last Name</label>
          <input type="text" class="form-control" id="lastNameInput" v-model="lastName" placeholder="Last Name" />
        </div>
        <div class="mb-3">
          <label for="emailInput" class="form-label">Email Address</label>
          <input type="email" class="form-control" id="emailInput" :value="registerEmail" @change="updateEmail"
            ref="emailInputRef" placeholder="Enter Email" />
          <div v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</div> <!-- Error message display -->
        </div>
        <div class="mb-3">
          <label for="passwordInput" class="form-label">Password</label>
          <input type="password" class="form-control" id="passwordInput" v-model="registerPassword"
            placeholder="Password" />
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </main>
  </div>
</template>
