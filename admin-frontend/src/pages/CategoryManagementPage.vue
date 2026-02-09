<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold">카테고리 관리</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <div class="mb-4">
        <button
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + 카테고리 추가
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="category in categories"
          :key="category.id"
          class="bg-white rounded-lg shadow p-4"
        >
          <h3 class="font-bold text-lg mb-2">{{ category.name }}</h3>
          <p class="text-sm text-gray-600 mb-4">순서: {{ category.display_order }}</p>
          <div class="flex gap-2">
            <button
              @click="editCategory(category)"
              class="flex-1 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 text-sm"
            >
              수정
            </button>
            <button
              @click="deleteCategory(category.id)"
              class="flex-1 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 카테고리 추가 모달 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">카테고리 추가</h2>
        
        <form @submit.prevent="addCategory">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">카테고리명</label>
            <input
              v-model="newCategory.name"
              type="text"
              required
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="예: 메인 요리"
            />
          </div>
          
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">표시 순서</label>
            <input
              v-model.number="newCategory.display_order"
              type="number"
              required
              min="1"
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="1"
            />
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

const categories = ref([])
const showAddModal = ref(false)
const newCategory = ref({
  name: '',
  display_order: 1
})

const loadCategories = async () => {
  try {
    const response = await apiClient.get('/api/admin/category/list')
    categories.value = response.data.categories || response.data
  } catch (err) {
    alert('카테고리 목록을 불러오는데 실패했습니다')
  }
}

const addCategory = async () => {
  try {
    const response = await apiClient.post('/api/admin/category/create', newCategory.value)
    categories.value.push(response.data)
    showAddModal.value = false
    // 폼 초기화
    newCategory.value = {
      name: '',
      display_order: 1
    }
    alert('카테고리가 추가되었습니다')
  } catch (err) {
    alert(err.response?.data?.detail || '카테고리 추가에 실패했습니다')
  }
}

const editCategory = (category) => {
  alert('카테고리 수정 기능은 구현 예정입니다')
}

const deleteCategory = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  
  try {
    await apiClient.delete(`/api/admin/category/${id}`)
    categories.value = categories.value.filter(c => c.id !== id)
  } catch (err) {
    alert('삭제에 실패했습니다')
  }
}

onMounted(() => {
  loadCategories()
})
</script>
