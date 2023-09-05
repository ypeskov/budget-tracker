<script setup>
import {useRouter} from 'vue-router';
import { useUserStore } from '../stores/user';

const userStore = useUserStore();
userStore.setUser({
  id: null,
  firstName: null,
  lastName: null,
  email: null,
  iat: null,
  exp: null
}, true);

userStore.isLoggedIn = false;
userStore.authToken = null;

const router = useRouter();
router.push('/');

</script>

<template></template>