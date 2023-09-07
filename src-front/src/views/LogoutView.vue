<script setup>
import {useRouter} from 'vue-router';
import { useUserStore } from '../stores/user';
import { UserService } from '../services/users';

const userStore = useUserStore();
const userService = new UserService(userStore);

userService.logOutUser();

const router = useRouter();
router.push({name: 'login'});

</script>

<template></template>