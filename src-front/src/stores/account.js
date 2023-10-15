import { reactive, ref } from 'vue';
import { defineStore } from 'pinia';
import { DateTime } from 'luxon';

export const useAccountStore = defineStore('account', () => {
  const accounts = reactive([]);
  const lastUpdated = DateTime.now();
  const shouldUpdate = ref(true);
  return {
    accounts,
    lastUpdated,
    shouldUpdate,
  };
});
