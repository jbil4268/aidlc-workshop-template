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
          <p class="text-sm text-gray-600 mb-2">또는 테이블 번호 직접 입력</p>
          <input
            v-model="manualTableId"
            type="number"
            placeholder="테이블 ID"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'
import apiClient from '@/api/client'

const router = useRouter()
const scanning = ref(false)
const manualTableId = ref('')
const error = ref('')
let html5QrCode = null

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
  if (!manualTableId.value) {
    error.value = '테이블 ID를 입력해주세요'
    return
  }
  
  await loginWithTableId(parseInt(manualTableId.value))
}

const loginWithTableId = async (tableId) => {
  try {
    error.value = ''
    const response = await apiClient.post('/customer/auth/login', { table_id: tableId })
    
    sessionStorage.setItem('table_id', tableId)
    sessionStorage.setItem('session_id', response.data.session_id)
    sessionStorage.setItem('access_token', response.data.access_token)
    
    router.push('/menu')
  } catch (err) {
    error.value = err.response?.data?.detail || '로그인에 실패했습니다'
  }
}
</script>
