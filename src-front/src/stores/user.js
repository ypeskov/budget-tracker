import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const id = ref(null)
  const firstName = ref(null)
  const lastName = ref(null)
  const email = ref(null)
  const accessToken = ref(null)
  const iat = ref(null)
  const exp = ref(null)

  return { id, firstName, lastName, email, accessToken, iat, exp }
})
