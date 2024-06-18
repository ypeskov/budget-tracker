import { ref, reactive } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
  const user = reactive({});
  const accessToken = ref(null);
  const isLoggedIn = ref(false);

  const currencies = reactive([]);
  const categories = reactive([]);
  const settings = reactive({});
  const baseCurrency = ref('');

  return {
    user,
    accessToken,
    isLoggedIn,
    currencies,
    categories,
    settings,
    baseCurrency,
  };
});
