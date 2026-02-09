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
          <p class="text-sm text-gray-600 mb-2">수용 인원: {{ table.capacity }}명</p>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const tables = ref([])
const showAddModal = ref(false)

const loadTables = async () => {
  try {
    const response = await apiClient.get('/api/admin/table/list')
    tables.value = response.data.tables || response.data
  } catch (err) {
    alert('테이블 목록을 불러오는데 실패했습니다')
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
