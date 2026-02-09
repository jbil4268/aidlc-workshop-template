<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <h1 class="text-3xl font-bold text-center mb-8">관리자 로그인</h1>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            사용자명
          </label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="admin"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            비밀번호
          </label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="••••••••"
          />
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
        >
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
        
        <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>
      </form>
      
      <div class="mt-6 text-center text-sm text-gray-600">
        <p>기본 계정: admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()
const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await apiClient.post('/api/admin/auth/login', {
      username: username.value,
      password: password.value
    })
    
    sessionStorage.setItem('admin_token', response.data.access_token)
    sessionStorage.setItem('admin_username', username.value)
    
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || '로그인에 실패했습니다'
  } finally {
    loading.value = false
  }
}
</script>
