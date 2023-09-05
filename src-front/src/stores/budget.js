import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useBudgetStore = defineStore('budget', () => {
  const email = ref('');
  const accessToken = ref('');

  return { email, accessToken }
})
