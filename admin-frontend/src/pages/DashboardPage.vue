<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold">주문 관리 대시보드</h1>
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-600">{{ username }}</span>
          <button
            @click="logout"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            로그아웃
          </button>
        </div>
      </div>
    </header>

    <!-- Navigation -->
    <nav class="bg-white border-b">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex gap-4">
          <router-link
            to="/dashboard"
            class="px-4 py-3 border-b-2 border-blue-600 text-blue-600 font-medium"
          >
            주문 관리
          </router-link>
          <router-link
            to="/tables"
            class="px-4 py-3 text-gray-600 hover:text-gray-900"
          >
            테이블 관리
          </router-link>
          <router-link
            to="/menus"
            class="px-4 py-3 text-gray-600 hover:text-gray-900"
          >
            메뉴 관리
          </router-link>
          <router-link
            to="/categories"
            class="px-4 py-3 text-gray-600 hover:text-gray-900"
          >
            카테고리 관리
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-6">
      <!-- Status Filter -->
      <div class="mb-6 flex gap-2">
        <button
          v-for="status in statuses"
          :key="status.value"
          @click="filterStatus = status.value"
          :class="[
            'px-4 py-2 rounded-lg transition',
            filterStatus === status.value
              ? 'bg-blue-600 text-white'
              : 'bg-white text-gray-700 hover:bg-gray-50'
          ]"
        >
          {{ status.label }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">주문 목록을 불러오는 중...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <!-- Orders Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition"
        >
          <div class="flex justify-between items-start mb-3">
            <div>
              <p class="text-sm text-gray-600">주문번호</p>
              <p class="font-bold">{{ order.order_number }}</p>
            </div>
            <span
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                getStatusClass(order.status)
              ]"
            >
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <div class="mb-3">
            <p class="text-sm text-gray-600">테이블</p>
            <p class="font-medium">{{ order.table_number }}</p>
          </div>

          <div class="mb-3">
            <p class="text-sm text-gray-600 mb-1">주문 항목</p>
            <div class="space-y-1">
              <p
                v-for="item in order.items"
                :key="item.id"
                class="text-sm"
              >
                {{ item.menu_name }} x {{ item.quantity }}
              </p>
            </div>
          </div>

          <div class="mb-4 pt-3 border-t">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">합계</span>
              <span class="font-bold">{{ formatPrice(order.total_amount) }}원</span>
            </div>
          </div>

          <div class="flex gap-2">
            <button
              v-if="order.status === 'pending'"
              @click="updateStatus(order.id, 'preparing')"
              class="flex-1 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              준비 시작
            </button>
            <button
              v-if="order.status === 'preparing'"
              @click="updateStatus(order.id, 'completed')"
              class="flex-1 px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
            >
              완료
            </button>
            <button
              v-if="order.status !== 'cancelled'"
              @click="updateStatus(order.id, 'cancelled')"
              class="flex-1 px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              취소
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredOrders.length === 0" class="text-center py-12">
        <p class="text-gray-600">주문이 없습니다</p>
      </div>

      <!-- WebSocket Status -->
      <div class="fixed bottom-4 right-4">
        <div
          :class="[
            'px-4 py-2 rounded-lg shadow-lg',
            wsConnected ? 'bg-green-500' : 'bg-red-500'
          ]"
        >
          <span class="text-white text-sm">
            {{ wsConnected ? '실시간 연결됨' : '연결 끊김' }}
          </span>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()
const username = ref(sessionStorage.getItem('admin_username') || 'Admin')
const loading = ref(true)
const error = ref('')
const orders = ref([])
const filterStatus = ref('all')
const wsConnected = ref(false)
let ws = null

const statuses = [
  { value: 'all', label: '전체' },
  { value: 'pending', label: '대기중' },
  { value: 'preparing', label: '준비중' },
  { value: 'completed', label: '완료' },
  { value: 'cancelled', label: '취소됨' }
]

const filteredOrders = computed(() => {
  if (filterStatus.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === filterStatus.value)
})

const formatPrice = (price) => {
  return price.toLocaleString()
}

const getStatusLabel = (status) => {
  const statusMap = {
    'pending': '대기중',
    'preparing': '준비중',
    'completed': '완료',
    'cancelled': '취소됨'
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const classMap = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'preparing': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'cancelled': 'bg-red-100 text-red-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

const loadOrders = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await apiClient.get('/api/admin/order/list')
    orders.value = response.data.orders || response.data
  } catch (err) {
    error.value = err.response?.data?.detail || '주문 목록을 불러오는데 실패했습니다'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (orderId, newStatus) => {
  try {
    await apiClient.patch(`/admin/orders/${orderId}/status`, {
      status: newStatus
    })
    
    // Update local state
    const order = orders.value.find(o => o.id === orderId)
    if (order) {
      order.status = newStatus
    }
    
    // Play notification sound
    playNotificationSound()
  } catch (err) {
    alert(err.response?.data?.detail || '상태 변경에 실패했습니다')
  }
}

const connectWebSocket = () => {
  const wsUrl = 'ws://localhost:8000/ws'
  ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    wsConnected.value = true
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    
    if (data.type === 'new_order') {
      // Add new order to list
      orders.value.unshift(data.order)
      playNotificationSound()
    } else if (data.type === 'order_updated') {
      // Update existing order
      const index = orders.value.findIndex(o => o.id === data.order.id)
      if (index !== -1) {
        orders.value[index] = data.order
      }
    }
  }
  
  ws.onclose = () => {
    wsConnected.value = false
    console.log('WebSocket disconnected')
    // Reconnect after 3 seconds
    setTimeout(connectWebSocket, 3000)
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
}

const playNotificationSound = () => {
  // Simple beep sound using Web Audio API
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  
  oscillator.connect(gainNode)
  gainNode.connect(audioContext.destination)
  
  oscillator.frequency.value = 800
  oscillator.type = 'sine'
  
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5)
  
  oscillator.start(audioContext.currentTime)
  oscillator.stop(audioContext.currentTime + 0.5)
}

const logout = () => {
  sessionStorage.clear()
  router.push('/login')
}

onMounted(() => {
  loadOrders()
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
</script>
