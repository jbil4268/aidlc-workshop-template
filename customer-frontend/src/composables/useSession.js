import { ref, computed } from 'vue'

export function useSession() {
  const tableId = ref(sessionStorage.getItem('table_id'))
  const sessionToken = ref(sessionStorage.getItem('session_token'))

  const isAuthenticated = computed(() => {
    return !!(tableId.value && sessionToken.value)
  })

  const setSession = (data) => {
    tableId.value = data.table_id
    sessionToken.value = data.session_token

    sessionStorage.setItem('table_id', data.table_id)
    sessionStorage.setItem('session_token', data.session_token)
    if (data.table_number) {
      sessionStorage.setItem('table_number', data.table_number)
    }
  }

  const clearSession = () => {
    tableId.value = null
    sessionToken.value = null

    sessionStorage.removeItem('table_id')
    sessionStorage.removeItem('session_token')
    sessionStorage.removeItem('table_number')
  }

  return {
    tableId,
    sessionToken,
    isAuthenticated,
    setSession,
    clearSession
  }
}
