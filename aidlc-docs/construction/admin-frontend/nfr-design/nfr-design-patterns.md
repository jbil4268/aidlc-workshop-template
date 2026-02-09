# Admin Frontend - NFR Design Patterns

## Key Patterns (Similar to Customer Frontend)

### 1. Component Architecture
- Atomic Design pattern
- Reusable components

### 2. State Management
- Composition API
- SessionStorage for JWT token

### 3. WebSocket Pattern
```javascript
// composables/useWebSocket.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket(storeId) {
  const connected = ref(false)
  const messages = ref([])
  let ws = null
  
  const connect = () => {
    ws = new WebSocket(`ws://localhost:8000/ws/admin/${storeId}`)
    
    ws.onopen = () => {
      connected.value = true
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      messages.value.push(data)
    }
    
    ws.onclose = () => {
      connected.value = false
      // Reconnect after 3 seconds
      setTimeout(connect, 3000)
    }
  }
  
  const send = (message) => {
    if (ws && connected.value) {
      ws.send(JSON.stringify(message))
    }
  }
  
  onMounted(connect)
  onUnmounted(() => {
    if (ws) ws.close()
  })
  
  return { connected, messages, send }
}
```

### 4. Authentication Pattern
```javascript
// composables/useAuth.js
import { ref, computed } from 'vue'

const token = ref(sessionStorage.getItem('adminToken'))

export function useAuth() {
  const setToken = (newToken) => {
    token.value = newToken
    sessionStorage.setItem('adminToken', newToken)
  }
  
  const clearToken = () => {
    token.value = null
    sessionStorage.removeItem('adminToken')
  }
  
  const isAuthenticated = computed(() => !!token.value)
  
  return { token, setToken, clearToken, isAuthenticated }
}
```

### 5. Form Handling Pattern
- Vue Composition API
- Validation with computed properties
- Optimistic updates

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
