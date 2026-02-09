<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <h1 class="text-xl font-bold">주문 현황</h1>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-6">
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">주문 내역을 불러오는 중...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <div v-else-if="orders.length === 0" class="text-center py-12">
        <p class="text-gray-600 mb-4">주문 내역이 없습니다</p>
        <button
          @click="goToMenu"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          메뉴 보러가기
        </button>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="order in orders"
          :key="order.id"
          class="bg-white rounded-lg shadow p-6"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <p class="text-sm text-gray-600">주문번호: {{ order.order_number }}</p>
              <p class="text-xs text-gray-500">{{ formatDate(order.created_at) }}</p>
            </div>
            <span
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                getStatusClass(order.status)
              ]"
            >
              {{ getStatusText(order.status) }}
            </span>
          </div>

          <div class="space-y-2 mb-4">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="flex justify-between text-sm"
            >
              <span>{{ item.menu_name }} x {{ item.quantity }}</span>
              <span>{{ formatPrice(item.price * item.quantity) }}원</span>
            </div>
          </div>

          <div class="border-t pt-3 space-y-1">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">소계</span>
              <span>{{ formatPrice(order.subtotal_amount) }}원</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">팁</span>
              <span>{{ formatPrice(order.tip_amount) }}원</span>
            </div>
            <div class="flex justify-between font-bold">
              <span>합계</span>
              <span class="text-blue-600">{{ formatPrice(order.total_amount) }}원</span>
            </div>
          </div>
        </div>

        <button
          @click="endSession"
          class="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 transition"
        >
          세션 종료
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()
const loading = ref(true)
const error = ref('')
const orders = ref([])
let pollingInterval = null

const formatPrice = (price) => {
  return price.toLocaleString()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR')
}

const getStatusText = (status) => {
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

const goToMenu = () => {
  router.push('/menu')
}

const loadOrders = async () => {
  try {
    const sessionToken = sessionStorage.getItem('session_token')
    console.log('session_token:', sessionToken)
    
    if (!sessionToken) {
      error.value = '세션이 만료되었습니다. 다시 로그인해주세요.'
      router.push('/qr-scan')
      return
    }
    
    const response = await apiClient.get(`/api/customer/order/list?session_token=${sessionToken}`)
    orders.value = response.data.orders || response.data
    loading.value = false
  } catch (err) {
    error.value = err.response?.data?.detail || '주문 내역을 불러오는데 실패했습니다'
    loading.value = false
  }
}

const endSession = async () => {
  if (!confirm('세션을 종료하시겠습니까?')) {
    return
  }
  
  try {
    const sessionToken = sessionStorage.getItem('session_token')
    
    if (!sessionToken) {
      alert('세션 정보가 없습니다')
      sessionStorage.clear()
      router.push('/qr-scan')
      return
    }
    
    await apiClient.post('/api/customer/auth/logout', null, {
      params: { session_token: sessionToken }
    })
    
    sessionStorage.clear()
    router.push('/qr-scan')
  } catch (err) {
    console.error('세션 종료 에러:', err)
    alert(err.response?.data?.detail || '세션 종료에 실패했습니다')
  }
}

onMounted(() => {
  loadOrders()
  
  // Poll every 5 seconds
  pollingInterval = setInterval(() => {
    loadOrders()
  }, 5000)
})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>
