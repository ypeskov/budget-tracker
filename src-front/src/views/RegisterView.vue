<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';

let registerEmail = ref('');
let registerPassword = ref('');
let firstName = ref('');
let lastName = ref('');
let errorMessage = ref(''); // Add this line for the error message
const showForm = ref(true);
const showSuccess = ref(false);

const router = useRouter();

function updateEmail(event) {
  registerEmail.value = event.target.value;
  errorMessage.value = ''; // Clear error message when email is changed
}

async function submitRegistration() {
  try {
    await Services.userService.registerUser(registerEmail.value,
      registerPassword.value,
      firstName.value,
      lastName.value);
    registerEmail.value = '';
    registerPassword.value = '';
    firstName.value = '';
    lastName.value = '';
    showForm.value = false;
    showSuccess.value = true;
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
    <div class="row">
      <div v-if="showForm" class="col">
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
            <label for="emailInput" class="form-label">
              Email Address <span class="text-danger">*</span> <!-- Red asterisk for required field -->
            </label>
            <input type="email" class="form-control" id="emailInput" :value="registerEmail" @change="updateEmail"
                   ref="emailInputRef" placeholder="Enter Email" required /> <!-- 'required' attribute added -->
            <div v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</div>
          </div>

          <div class="mb-3">
            <label for="passwordInput" class="form-label">
              Password <span class="text-danger">*</span> <!-- Red asterisk for required field -->
            </label>
            <input type="password" class="form-control" id="passwordInput" v-model="registerPassword"
                   placeholder="Password" required /> <!-- 'required' attribute added -->
          </div>
          <button type="submit" class="btn btn-primary">Register</button>
        </form>
      </div>
      <div v-if="showSuccess" class="col">
        <div class="alert alert-success" role="alert">
          Registration successful! Please check your email to verify your account.
        </div>
        <button @click="router.push('/login')" class="btn btn-primary">Login</button>
      </div>
    </div>

  </div>
</template>

