<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold">테이블 관리</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <div class="mb-4">
        <button
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + 테이블 추가
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="table in tables"
          :key="table.id"
          class="bg-white rounded-lg shadow p-4"
        >
          <h3 class="font-bold text-lg mb-2">{{ table.table_number }}</h3>
          <p class="text-sm text-gray-600 mb-1">수용 인원: {{ table.capacity }}명</p>
          <p class="text-sm text-gray-600 mb-2">QR: {{ table.qr_code }}</p>
          <p class="text-sm mb-4">
            <span
              :class="[
                'px-2 py-1 rounded text-xs',
                table.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              ]"
            >
              {{ table.is_active ? '활성' : '비활성' }}
            </span>
          </p>
          <div class="flex gap-2">
            <button
              @click="editTable(table)"
              class="flex-1 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 text-sm"
            >
              수정
            </button>
            <button
              @click="deleteTable(table.id)"
              class="flex-1 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 테이블 추가 모달 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">테이블 추가</h2>
        
        <form @submit.prevent="addTable">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">테이블 번호</label>
            <input
              v-model="newTable.table_number"
              type="text"
              required
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="예: T-01"
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">수용 인원</label>
            <input
              v-model="newTable.capacity"
              type="number"
              required
              min="1"
              max="20"
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="예: 4"
            />
          </div>
          
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">QR 코드</label>
            <input
              v-model="newTable.qr_code"
              type="text"
              required
              class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="예: QR-T01-STORE1"
            />
            <p class="text-xs text-gray-500 mt-1">고유한 QR 코드 식별자를 입력하세요</p>
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

const tables = ref([])
const showAddModal = ref(false)
const newTable = ref({
  table_number: '',
  capacity: '',
  qr_code: ''
})

const loadTables = async () => {
  try {
    const response = await apiClient.get('/api/admin/table/list')
    tables.value = response.data.tables || response.data
  } catch (err) {
    alert('테이블 목록을 불러오는데 실패했습니다')
  }
}

const addTable = async () => {
  try {
    // capacity를 숫자로 변환
    const tableData = {
      table_number: newTable.value.table_number,
      capacity: parseInt(newTable.value.capacity, 10),
      qr_code: newTable.value.qr_code
    }
    
    const response = await apiClient.post('/api/admin/table/create', tableData)
    tables.value.push(response.data)
    showAddModal.value = false
    // 폼 초기화
    newTable.value = {
      table_number: '',
      capacity: '',
      qr_code: ''
    }
    alert('테이블이 추가되었습니다')
  } catch (err) {
    alert(err.response?.data?.detail || '테이블 추가에 실패했습니다')
  }
}

const editTable = (table) => {
  alert('테이블 수정 기능은 구현 예정입니다')
}

const deleteTable = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  
  try {
    await apiClient.delete(`/api/admin/table/${id}`)
    tables.value = tables.value.filter(t => t.id !== id)
  } catch (err) {
    alert('삭제에 실패했습니다')
  }
}

onMounted(() => {
  loadTables()
})
</script>
