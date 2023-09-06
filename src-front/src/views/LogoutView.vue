<script setup>
import {useRouter} from 'vue-router';
import { useUserStore } from '../stores/user';
import { UserService } from '../services/users';

const userStore = useUserStore();
const userService = new UserService();

userStore.isLoggedIn = false;
userStore.authToken = '';
userService.logOutUser();

const router = useRouter();
router.push('/login');

</script>

<template></template>