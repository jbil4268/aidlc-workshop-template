import { ref, computed } from 'vue'

export function useSession() {
  const tableId = ref(sessionStorage.getItem('table_id'))
  const sessionId = ref(sessionStorage.getItem('session_id'))
  const accessToken = ref(sessionStorage.getItem('access_token'))

  const isAuthenticated = computed(() => {
    return !!(tableId.value && sessionId.value && accessToken.value)
  })

  const setSession = (data) => {
    tableId.value = data.table_id
    sessionId.value = data.session_id
    accessToken.value = data.access_token

    sessionStorage.setItem('table_id', data.table_id)
    sessionStorage.setItem('session_id', data.session_id)
    sessionStorage.setItem('access_token', data.access_token)
  }

  const clearSession = () => {
    tableId.value = null
    sessionId.value = null
    accessToken.value = null

    sessionStorage.removeItem('table_id')
    sessionStorage.removeItem('session_id')
    sessionStorage.removeItem('access_token')
  }

  return {
    tableId,
    sessionId,
    accessToken,
    isAuthenticated,
    setSession,
    clearSession
  }
}
