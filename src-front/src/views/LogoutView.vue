<script setup>
import {useRouter} from 'vue-router';

import { Services } from '../services/servicesConfig';

Services.userService.logOutUser();

const router = useRouter();
router.push({name: 'login'});

</script>

<template>
  <div>
    <h1>Logging out...</h1>
  </div>
</template>
