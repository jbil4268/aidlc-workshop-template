<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
        <button @click="goBack" class="text-gray-600 hover:text-gray-900">
          ← 뒤로
        </button>
        <h1 class="text-xl font-bold">주문하기</h1>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-6">
      <div v-if="cart.length === 0" class="text-center py-12">
        <p class="text-gray-600 mb-4">장바구니가 비어있습니다</p>
        <button
          @click="goBack"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          메뉴 보러가기
        </button>
      </div>

      <div v-else>
        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <h2 class="font-bold text-lg mb-4">주문 내역</h2>
          
          <div v-for="(item, index) in cart" :key="index" class="flex justify-between items-center py-3 border-b">
            <div class="flex-1">
              <p class="font-medium">{{ item.name }}</p>
              <p class="text-sm text-gray-600">{{ formatPrice(item.price) }}원</p>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="decreaseQuantity(index)"
                class="w-8 h-8 bg-gray-200 rounded hover:bg-gray-300"
              >
                -
              </button>
              <span class="w-8 text-center">{{ item.quantity }}</span>
              <button
                @click="increaseQuantity(index)"
                class="w-8 h-8 bg-gray-200 rounded hover:bg-gray-300"
              >
                +
              </button>
              <button
                @click="removeItem(index)"
                class="ml-2 text-red-600 hover:text-red-700"
              >
                삭제
              </button>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <h2 class="font-bold text-lg mb-4">팁 선택</h2>
          
          <div class="grid grid-cols-5 gap-2">
            <button
              v-for="rate in tipRates"
              :key="rate"
              @click="selectedTipRate = rate"
              :class="[
                'py-3 rounded-lg border-2 transition',
                selectedTipRate === rate
                  ? 'border-blue-600 bg-blue-50 text-blue-600'
                  : 'border-gray-300 hover:border-gray-400'
              ]"
            >
              {{ rate }}%
            </button>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">소계</span>
              <span>{{ formatPrice(subtotal) }}원</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">팁 ({{ selectedTipRate }}%)</span>
              <span>{{ formatPrice(tipAmount) }}원</span>
            </div>
            <div class="flex justify-between text-lg font-bold pt-2 border-t">
              <span>합계</span>
              <span class="text-blue-600">{{ formatPrice(total) }}원</span>
            </div>
          </div>
        </div>

        <button
          @click="submitOrder"
          :disabled="submitting"
          class="w-full bg-blue-600 text-white py-4 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
        >
          {{ submitting ? '주문 중...' : '주문하기' }}
        </button>

        <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {{ error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()
const cart = ref([])
const selectedTipRate = ref(0)
const tipRates = [0, 5, 10, 15, 20]
const submitting = ref(false)
const error = ref('')

const subtotal = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

const tipAmount = computed(() => {
  return Math.round(subtotal.value * selectedTipRate.value / 100)
})

const total = computed(() => {
  return subtotal.value + tipAmount.value
})

const formatPrice = (price) => {
  return price.toLocaleString()
}

const goBack = () => {
  router.push('/menu')
}

const increaseQuantity = (index) => {
  cart.value[index].quantity++
  saveCart()
}

const decreaseQuantity = (index) => {
  if (cart.value[index].quantity > 1) {
    cart.value[index].quantity--
    saveCart()
  }
}

const removeItem = (index) => {
  cart.value.splice(index, 1)
  saveCart()
}

const saveCart = () => {
  sessionStorage.setItem('cart', JSON.stringify(cart.value))
}

const submitOrder = async () => {
  try {
    submitting.value = true
    error.value = ''
    
    const sessionToken = sessionStorage.getItem('session_token')
    if (!sessionToken) {
      error.value = '세션이 만료되었습니다. 다시 로그인해주세요.'
      router.push('/qr-scan')
      return
    }
    
    const orderData = {
      items: cart.value.map(item => ({
        menu_id: item.menu_id,
        quantity: item.quantity
      })),
      tip_rate: selectedTipRate.value
    }
    
    await apiClient.post(`/api/customer/order/create?session_token=${sessionToken}`, orderData)
    
    sessionStorage.removeItem('cart')
    
    // 주문 완료 메시지 표시
    alert('주문이 완료되었습니다! 5초 후 메뉴 화면으로 이동합니다.')
    
    // 5초 후 메뉴 화면으로 이동
    setTimeout(() => {
      router.push('/menu')
    }, 5000)
    
  } catch (err) {
    error.value = err.response?.data?.detail || '주문에 실패했습니다'
    submitting.value = false
  }
}

onMounted(() => {
  cart.value = JSON.parse(sessionStorage.getItem('cart') || '[]')
})
</script>
