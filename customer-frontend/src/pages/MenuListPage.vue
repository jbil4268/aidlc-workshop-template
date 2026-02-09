<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-xl font-bold">메뉴</h1>
        <button
          @click="goToCart"
          class="relative bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          장바구니
          <span v-if="cartCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
            {{ cartCount }}
          </span>
        </button>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-6">
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">메뉴를 불러오는 중...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <div v-else>
        <div v-for="category in categories" :key="category.id" class="mb-8">
          <h2 class="text-lg font-bold mb-4">{{ category.name }}</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="menu in getMenusByCategory(category.id)"
              :key="menu.id"
              class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition cursor-pointer"
              @click="viewMenuDetail(menu)"
            >
              <div class="flex gap-4">
                <img
                  v-if="menu.image_url"
                  :src="menu.image_url"
                  :alt="menu.name"
                  class="w-24 h-24 object-cover rounded"
                />
                <div class="flex-1">
                  <h3 class="font-bold text-lg">{{ menu.name }}</h3>
                  <p class="text-sm text-gray-600 mt-1">{{ menu.description }}</p>
                  <p class="text-blue-600 font-bold mt-2">{{ formatPrice(menu.price) }}원</p>
                  <div v-if="menu.allergens" class="mt-2 flex flex-wrap gap-1">
                    <span
                      v-for="allergen in menu.allergens.split(',')"
                      :key="allergen"
                      class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded"
                    >
                      {{ allergen.trim() }}
                    </span>
                  </div>
                  <span v-if="!menu.is_available" class="inline-block mt-2 text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                    품절
                  </span>
                </div>
              </div>
            </div>
          </div>
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
const loading = ref(true)
const error = ref('')
const categories = ref([])
const menus = ref([])
const cart = ref(JSON.parse(sessionStorage.getItem('cart') || '[]'))

const cartCount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.quantity, 0)
})

const getMenusByCategory = (categoryId) => {
  return menus.value.filter(menu => menu.category_id === categoryId)
}

const formatPrice = (price) => {
  return price.toLocaleString()
}

const viewMenuDetail = (menu) => {
  if (!menu.is_available) {
    alert('품절된 메뉴입니다')
    return
  }
  
  const existingItem = cart.value.find(item => item.menu_id === menu.id)
  if (existingItem) {
    existingItem.quantity++
  } else {
    cart.value.push({
      menu_id: menu.id,
      name: menu.name,
      price: menu.price,
      quantity: 1
    })
  }
  
  sessionStorage.setItem('cart', JSON.stringify(cart.value))
}

const goToCart = () => {
  router.push('/order')
}

const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const [categoriesRes, menusRes] = await Promise.all([
      apiClient.get('/customer/menu/categories'),
      apiClient.get('/customer/menu')
    ])
    
    categories.value = categoriesRes.data
    menus.value = menusRes.data
  } catch (err) {
    error.value = err.response?.data?.detail || '메뉴를 불러오는데 실패했습니다'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
