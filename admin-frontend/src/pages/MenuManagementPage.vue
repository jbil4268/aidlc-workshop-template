<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold">메뉴 관리</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <div class="mb-4">
        <button
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + 메뉴 추가
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="menu in menus"
          :key="menu.id"
          class="bg-white rounded-lg shadow p-4"
        >
          <h3 class="font-bold text-lg mb-2">{{ menu.name }}</h3>
          <p class="text-sm text-gray-600 mb-2">{{ menu.description }}</p>
          <p class="text-blue-600 font-bold mb-2">{{ formatPrice(menu.price) }}원</p>
          <p class="text-sm mb-4">
            <span
              :class="[
                'px-2 py-1 rounded text-xs',
                menu.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]"
            >
              {{ menu.is_available ? '판매중' : '품절' }}
            </span>
          </p>
          <div class="flex gap-2">
            <button
              @click="editMenu(menu)"
              class="flex-1 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 text-sm"
            >
              수정
            </button>
            <button
              @click="deleteMenu(menu.id)"
              class="flex-1 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 메뉴 추가 모달 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">메뉴 추가</h2>
        
        <form @submit.prevent="addMenu">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">메뉴명</label>
            <input
              v-model="newMenu.name"
              type="text"
              required
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="예: 김치찌개"
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">설명</label>
            <textarea
              v-model="newMenu.description"
              rows="3"
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="메뉴 설명을 입력하세요"
            ></textarea>
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">가격 (원)</label>
            <input
              v-model.number="newMenu.price"
              type="number"
              required
              min="0"
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="10000"
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">카테고리 ID</label>
            <input
              v-model.number="newMenu.category_id"
              type="number"
              required
              min="1"
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="1"
            />
          </div>
          
          <div class="mb-6">
            <label class="flex items-center">
              <input
                v-model="newMenu.is_available"
                type="checkbox"
                class="mr-2"
              />
              <span class="text-sm">판매 가능</span>
            </label>
          </div>
          
          <div class="flex gap-2">
            <button
              type="button"
              @click="showAddModal = false"
              class="flex-1 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              취소
            </button>
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              추가
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const menus = ref([])
const showAddModal = ref(false)
const newMenu = ref({
  name: '',
  description: '',
  price: 0,
  category_id: 1,
  is_available: true
})

const formatPrice = (price) => {
  return price.toLocaleString()
}

const loadMenus = async () => {
  try {
    const response = await apiClient.get('/api/admin/menu/list')
    menus.value = response.data.menus || response.data
  } catch (err) {
    alert('메뉴 목록을 불러오는데 실패했습니다')
  }
}

const addMenu = async () => {
  try {
    const response = await apiClient.post('/api/admin/menu/create', newMenu.value)
    menus.value.push(response.data)
    showAddModal.value = false
    // 폼 초기화
    newMenu.value = {
      name: '',
      description: '',
      price: 0,
      category_id: 1,
      is_available: true
    }
    alert('메뉴가 추가되었습니다')
  } catch (err) {
    alert(err.response?.data?.detail || '메뉴 추가에 실패했습니다')
  }
}

const editMenu = (menu) => {
  alert('메뉴 수정 기능은 구현 예정입니다')
}

const deleteMenu = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  
  try {
    await apiClient.delete(`/api/admin/menu/${id}`)
    menus.value = menus.value.filter(m => m.id !== id)
  } catch (err) {
    alert('삭제에 실패했습니다')
  }
}

onMounted(() => {
  loadMenus()
})
</script>
