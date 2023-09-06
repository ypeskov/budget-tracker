import { ref, reactive } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
  const user = reactive({});
  const accessToken = ref(null);
  const isLoggedIn = ref(false);

  return {
    user,
    accessToken,
    isLoggedIn,
  };
});
