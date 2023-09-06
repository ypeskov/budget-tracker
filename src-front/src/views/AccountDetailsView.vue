<script setup>
// import { onBeforeMount, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountStore } from '../stores/account';

const route = useRoute();
console.log(route.params);

</script>

<template>

</template>