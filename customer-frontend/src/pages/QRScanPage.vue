<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
      <h1 class="text-2xl font-bold text-center mb-6">테이블 QR 스캔</h1>
      
      <div v-if="!scanning" class="text-center">
        <button
          @click="startScan"
          class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition"
        >
          QR 코드 스캔 시작
        </button>
        
        <div class="mt-6">
          <p class="text-sm text-gray-600 mb-2">또는 테이블 선택</p>
          <select
            v-model="manualTableId"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">테이블을 선택하세요</option>
            <option 
              v-for="table in tables" 
              :key="table.id" 
              :value="table.id"
            >
              {{ table.table_number }} ({{ table.capacity }}명)
            </option>
          </select>
          <button
            @click="loginManual"
            class="w-full mt-2 bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition"
          >
            입장하기
          </button>
        </div>
      </div>
      
      <div v-else>
        <div id="qr-reader" class="w-full"></div>
        <button
          @click="stopScan"
          class="w-full mt-4 bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition"
        >
          스캔 중지
        </button>
      </div>
      
      <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'
import apiClient from '@/api/client'

const router = useRouter()
const scanning = ref(false)
const manualTableId = ref('')
const tables = ref([])
const error = ref('')
let html5QrCode = null

// 테이블 목록 로드
const loadTables = async () => {
  try {
    const response = await apiClient.get('/api/admin/table/list')
    tables.value = response.data.tables || response.data
  } catch (err) {
    console.error('테이블 목록 로드 실패:', err)
  }
}

onMounted(() => {
  loadTables()
})

const startScan = async () => {
  try {
    scanning.value = true
    error.value = ''
    
    html5QrCode = new Html5Qrcode('qr-reader')
    
    await html5QrCode.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: 250 },
      onScanSuccess
    )
  } catch (err) {
    error.value = 'QR 스캔을 시작할 수 없습니다: ' + err.message
    scanning.value = false
  }
}

const stopScan = async () => {
  if (html5QrCode) {
    await html5QrCode.stop()
    scanning.value = false
  }
}

const onScanSuccess = async (decodedText) => {
  await stopScan()
  
  try {
    const tableId = parseInt(decodedText)
    await loginWithTableId(tableId)
  } catch (err) {
    error.value = 'QR 코드 형식이 올바르지 않습니다'
  }
}

const loginManual = async () => {
  console.log('loginManual 시작')
  console.log('manualTableId:', manualTableId.value)
  
  if (!manualTableId.value) {
    error.value = '테이블을 선택해주세요'
    return
  }
  
  // 선택한 테이블의 qr_code 찾기
  const selectedTable = tables.value.find(t => t.id === parseInt(manualTableId.value))
  console.log('selectedTable:', selectedTable)
  
  if (!selectedTable) {
    error.value = '선택한 테이블을 찾을 수 없습니다'
    return
  }
  
  console.log('loginWithQRCode 호출:', selectedTable.qr_code, selectedTable.id)
  await loginWithQRCode(selectedTable.qr_code, selectedTable.id)
}

const loginWithTableId = async (tableId) => {
  // QR 스캔으로 로그인 시 - qr_code가 tableId로 전달됨
  await loginWithQRCode(tableId.toString(), null)
}

const loginWithQRCode = async (qrCode, tableId = null) => {
  console.log('loginWithQRCode 시작:', qrCode, tableId)
  try {
    error.value = ''
    console.log('API 호출 시작')
    const response = await apiClient.post('/api/customer/auth/login', { qr_code: qrCode })
    console.log('API 응답:', response.data)
    
    const actualTableId = tableId || response.data.table_id
    sessionStorage.setItem('table_id', actualTableId)
    sessionStorage.setItem('session_token', response.data.session_token)
    sessionStorage.setItem('table_number', response.data.table_number)
    
    console.log('router.push 호출')
    router.push('/menu')
  } catch (err) {
    console.error('로그인 에러:', err)
    error.value = err.response?.data?.detail || '로그인에 실패했습니다'
  }
}
</script>
