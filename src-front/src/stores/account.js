import { reactive } from 'vue';
import { defineStore } from 'pinia';

export const useAccountStore = defineStore('account', () => {
  const accounts = reactive([]);

  return {
    accounts,
  };
});
