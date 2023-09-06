<script setup>
import {useRouter} from 'vue-router';
import { useUserStore } from '../stores/user';

const userStore = useUserStore();


userStore.isLoggedIn = false;
userStore.authToken = '';
userStore.logOutUser();

const router = useRouter();
router.push('/login');

</script>

<template></template>