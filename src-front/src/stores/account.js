import { reactive } from 'vue';
import { defineStore } from 'pinia';
import { DateTime } from 'luxon';

export const useAccountStore = defineStore('account', () => {
  const accounts = reactive([]);
  const lastUpdated = DateTime.now();

  return {
    accounts,
    lastUpdated,
  };
});
