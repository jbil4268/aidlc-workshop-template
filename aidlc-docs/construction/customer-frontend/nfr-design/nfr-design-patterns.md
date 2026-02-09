# Customer Frontend - NFR Design Patterns

## 1. Component Architecture Pattern

### Pattern: Atomic Design (Simplified)
**Purpose**: 재사용 가능한 컴포넌트 구조

**Structure**:
```
components/
├── atoms/           # 기본 UI 요소
│   ├── Button.vue
│   ├── Badge.vue
│   ├── Spinner.vue
│   └── Input.vue
├── molecules/       # 조합된 컴포넌트
│   ├── MenuCard.vue
│   ├── OrderCard.vue
│   └── CategoryTab.vue
├── organisms/       # 복잡한 컴포넌트
│   ├── MenuList.vue
│   ├── OrderSummary.vue
│   └── TipSelector.vue
└── templates/       # 페이지 레이아웃
    └── MainLayout.vue
```

**Benefits**:
- 컴포넌트 재사용성 향상
- 일관된 UI/UX
- 유지보수 용이

---

## 2. State Management Pattern

### Pattern: Composition API + SessionStorage
**Purpose**: 간단하고 효율적인 상태 관리

**Implementation**:
```javascript
// composables/useSession.js
import { ref, computed } from 'vue'

const sessionToken = ref(sessionStorage.getItem('sessionToken'))
const tableNumber = ref(sessionStorage.getItem('tableNumber'))

export function useSession() {
  const setSession = (token, table) => {
    sessionToken.value = token
    tableNumber.value = table
    sessionStorage.setItem('sessionToken', token)
    sessionStorage.setItem('tableNumber', table)
  }
  
  const clearSession = () => {
    sessionToken.value = null
    tableNumber.value = null
    sessionStorage.clear()
  }
  
  const isAuthenticated = computed(() => !!sessionToken.value)
  
  return { sessionToken, tableNumber, setSession, clearSession, isAuthenticated }
}
```

**Benefits**:
- 전역 상태 관리 간편
- 페이지 새로고침 시 세션 유지
- 외부 라이브러리 불필요

---

## 3. API Communication Pattern

### Pattern: Axios Instance + Interceptors
**Purpose**: 일관된 API 호출 및 에러 처리

**Implementation**:
```javascript
// api/client.js
import axios from 'axios'
import { useSession } from '@/composables/useSession'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const { sessionToken } = useSession()
    if (sessionToken.value) {
      config.params = { ...config.params, session_token: sessionToken.value }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Session expired
      const { clearSession } = useSession()
      clearSession()
      router.push('/scan')
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

**Benefits**:
- 중복 코드 제거
- 자동 인증 토큰 추가
- 통합 에러 처리

---

## 4. Error Handling Pattern

### Pattern: Try-Catch + User Feedback
**Purpose**: 사용자 친화적 에러 처리

**Implementation**:
```javascript
// composables/useApi.js
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'

export function useApi(apiCall) {
  const loading = ref(false)
  const error = ref(null)
  const { showError } = useToast()
  
  const execute = async (...args) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await apiCall(...args)
      return result
    } catch (err) {
      error.value = err.message
      showError(err.response?.data?.detail || '오류가 발생했습니다.')
      throw err
    } finally {
      loading.value = false
    }
  }
  
  return { execute, loading, error }
}
```

**Benefits**:
- 일관된 로딩 상태 관리
- 자동 에러 메시지 표시
- 재사용 가능한 API 호출 로직

---

## 5. Routing Pattern

### Pattern: Route Guards + Lazy Loading
**Purpose**: 인증 체크 및 성능 최적화

**Implementation**:
```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useSession } from '@/composables/useSession'

const routes = [
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('@/pages/QRScanPage.vue')
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/pages/MenuListPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('@/pages/OrderPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/status',
    name: 'Status',
    component: () => import('@/pages/OrderStatusPage.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useSession()
  
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/scan')
  } else if (to.path === '/scan' && isAuthenticated.value) {
    next('/menu')
  } else {
    next()
  }
})

export default router
```

**Benefits**:
- 자동 인증 체크
- 코드 스플리팅으로 번들 크기 감소
- 보안 강화

---

## 6. Responsive Design Pattern

### Pattern: Mobile-First + Tailwind Breakpoints
**Purpose**: 모바일 우선 반응형 디자인

**Implementation**:
```vue
<template>
  <!-- Mobile first, then tablet/desktop -->
  <div class="p-4 md:p-6 lg:p-8">
    <h1 class="text-2xl md:text-3xl lg:text-4xl">메뉴</h1>
    
    <!-- Grid layout -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <MenuCard v-for="menu in menus" :key="menu.id" :menu="menu" />
    </div>
  </div>
</template>
```

**Breakpoints**:
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (desktops)

**Benefits**:
- 모바일 성능 우선
- 일관된 반응형 동작
- Tailwind 유틸리티 활용

---

## 7. Performance Optimization Pattern

### Pattern: Lazy Loading + Image Optimization
**Purpose**: 빠른 페이지 로드 및 렌더링

**Implementation**:
```vue
<template>
  <!-- Lazy load images -->
  <img 
    :src="menu.image_url || '/placeholder.png'" 
    :alt="menu.name"
    loading="lazy"
    class="w-full h-48 object-cover"
  />
  
  <!-- Virtual scrolling for long lists (optional) -->
  <RecycleScroller
    v-if="menus.length > 50"
    :items="menus"
    :item-size="200"
  >
    <template #default="{ item }">
      <MenuCard :menu="item" />
    </template>
  </RecycleScroller>
</template>
```

**Techniques**:
- Image lazy loading
- Route-based code splitting
- Component lazy loading
- Virtual scrolling (for large lists)

**Benefits**:
- 초기 로드 시간 단축
- 메모리 사용량 감소
- 부드러운 스크롤

---

## 8. Form Handling Pattern

### Pattern: v-model + Computed Validation
**Purpose**: 실시간 폼 검증

**Implementation**:
```vue
<script setup>
import { ref, computed } from 'vue'

const quantity = ref(1)

const isValid = computed(() => quantity.value >= 1 && quantity.value <= 99)
const errorMessage = computed(() => {
  if (quantity.value < 1) return '수량은 1 이상이어야 합니다.'
  if (quantity.value > 99) return '수량은 99 이하여야 합니다.'
  return ''
})

const increment = () => {
  if (quantity.value < 99) quantity.value++
}

const decrement = () => {
  if (quantity.value > 1) quantity.value--
}
</script>

<template>
  <div>
    <button @click="decrement" :disabled="quantity <= 1">-</button>
    <input v-model.number="quantity" type="number" min="1" max="99" />
    <button @click="increment" :disabled="quantity >= 99">+</button>
    <p v-if="!isValid" class="text-red-500">{{ errorMessage }}</p>
  </div>
</template>
```

**Benefits**:
- 실시간 검증
- 사용자 피드백 즉시 제공
- 간단한 구현

---

## 9. Polling Pattern

### Pattern: setInterval + Cleanup
**Purpose**: 주문 상태 실시간 업데이트

**Implementation**:
```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getOrders } from '@/api/orders'

const orders = ref([])
let pollingInterval = null

const fetchOrders = async () => {
  try {
    const response = await getOrders()
    orders.value = response.data.orders
  } catch (error) {
    // Silent fail for polling
    console.error('Polling error:', error)
  }
}

onMounted(() => {
  fetchOrders() // Initial fetch
  pollingInterval = setInterval(fetchOrders, 5000) // Poll every 5 seconds
})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>
```

**Benefits**:
- 실시간 데이터 업데이트
- 자동 정리 (메모리 누수 방지)
- 에러 시 계속 폴링

---

## 10. Toast Notification Pattern

### Pattern: Event Bus + Composable
**Purpose**: 전역 알림 시스템

**Implementation**:
```javascript
// composables/useToast.js
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  const showToast = (message, type = 'info', duration = 3000) => {
    const id = toastId++
    toasts.value.push({ id, message, type })
    
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }
  
  const showSuccess = (message) => showToast(message, 'success')
  const showError = (message) => showToast(message, 'error')
  const showInfo = (message) => showToast(message, 'info')
  
  return { toasts, showToast, showSuccess, showError, showInfo }
}
```

```vue
<!-- ToastContainer.vue -->
<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="[
        'p-4 rounded shadow-lg',
        toast.type === 'success' ? 'bg-green-500' : '',
        toast.type === 'error' ? 'bg-red-500' : '',
        toast.type === 'info' ? 'bg-blue-500' : ''
      ]"
      class="text-white"
    >
      {{ toast.message }}
    </div>
  </div>
</template>
```

**Benefits**:
- 일관된 알림 UI
- 자동 사라짐
- 여러 알림 동시 표시 가능

---

## Pattern Summary

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| Atomic Design | Component structure | Low |
| Composition API | State management | Low |
| Axios Interceptors | API communication | Medium |
| Try-Catch + Feedback | Error handling | Low |
| Route Guards | Authentication | Low |
| Mobile-First | Responsive design | Low |
| Lazy Loading | Performance | Medium |
| v-model Validation | Form handling | Low |
| Polling | Real-time updates | Low |
| Toast Notifications | User feedback | Low |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
