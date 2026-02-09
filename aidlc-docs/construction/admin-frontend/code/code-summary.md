# Admin Frontend - Code Summary

## Project Structure (Similar to Customer Frontend)

```
admin-frontend/
├── src/
│   ├── api/
│   │   ├── client.js          # Axios with JWT interceptor
│   │   ├── auth.js            # Admin login
│   │   ├── order.js           # Order management
│   │   ├── table.js           # Table CRUD
│   │   ├── menu.js            # Menu CRUD
│   │   └── category.js        # Category CRUD
│   ├── components/
│   │   ├── atoms/
│   │   │   ├── Button.vue
│   │   │   ├── Input.vue
│   │   │   ├── Badge.vue
│   │   │   └── Card.vue
│   │   ├── molecules/
│   │   │   ├── OrderCard.vue
│   │   │   ├── TableCard.vue
│   │   │   ├── MenuCard.vue
│   │   │   └── StatusBadge.vue
│   │   └── organisms/
│   │       ├── OrderList.vue
│   │       ├── OrderDetailModal.vue
│   │       ├── TableForm.vue
│   │       ├── MenuForm.vue
│   │       └── Sidebar.vue
│   ├── composables/
│   │   ├── useAuth.js         # JWT authentication
│   │   ├── useWebSocket.js    # WebSocket connection
│   │   ├── useApi.js          # API wrapper
│   │   └── useToast.js        # Toast notifications
│   ├── pages/
│   │   ├── LoginPage.vue
│   │   ├── DashboardPage.vue
│   │   ├── TableManagementPage.vue
│   │   ├── MenuManagementPage.vue
│   │   └── CategoryManagementPage.vue
│   ├── router/
│   │   └── index.js           # Routes with auth guards
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Key Components

### 1. DashboardPage.vue
```vue
<template>
  <div class="flex h-screen">
    <Sidebar />
    
    <main class="flex-1 overflow-auto p-6">
      <header class="mb-6">
        <h1 class="text-3xl font-bold">주문 관리</h1>
        <div class="flex gap-2 mt-4">
          <button
            v-for="status in statuses"
            :key="status"
            @click="filterStatus = status"
            :class="[
              'px-4 py-2 rounded',
              filterStatus === status ? 'bg-primary-600 text-white' : 'bg-gray-200'
            ]"
          >
            {{ statusLabels[status] }}
          </button>
        </div>
      </header>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <OrderCard
          v-for="order in filteredOrders"
          :key="order.id"
          :order="order"
          @click="selectOrder(order)"
          @status-change="updateOrderStatus"
        />
      </div>
      
      <OrderDetailModal
        v-if="selectedOrder"
        :order="selectedOrder"
        @close="selectedOrder = null"
      />
      
      <!-- WebSocket Status -->
      <div class="fixed bottom-4 right-4">
        <Badge :color="wsConnected ? 'green' : 'red'">
          {{ wsConnected ? '연결됨' : '연결 끊김' }}
        </Badge>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import { getOrders, updateStatus } from '@/api/order'
import OrderCard from '@/components/molecules/OrderCard.vue'
import OrderDetailModal from '@/components/organisms/OrderDetailModal.vue'
import Sidebar from '@/components/organisms/Sidebar.vue'

const orders = ref([])
const selectedOrder = ref(null)
const filterStatus = ref(null)

const statuses = ['pending', 'preparing', 'ready', 'served']
const statusLabels = {
  pending: '대기',
  preparing: '조리중',
  ready: '완료',
  served: '서빙완료'
}

const filteredOrders = computed(() => {
  if (!filterStatus.value) return orders.value
  return orders.value.filter(o => o.status === filterStatus.value)
})

// WebSocket
const { connected: wsConnected, messages } = useWebSocket(1)

// Watch for new orders via WebSocket
watch(messages, (newMessages) => {
  const latestMessage = newMessages[newMessages.length - 1]
  if (latestMessage.type === 'new_order') {
    orders.value.unshift(latestMessage.data)
    // Play notification sound
    playNotificationSound()
  } else if (latestMessage.type === 'order_update') {
    const index = orders.value.findIndex(o => o.id === latestMessage.data.id)
    if (index !== -1) {
      orders.value[index] = latestMessage.data
    }
  }
})

const loadOrders = async () => {
  try {
    const response = await getOrders()
    orders.value = response.data.orders
  } catch (error) {
    console.error('Failed to load orders:', error)
  }
}

const selectOrder = (order) => {
  selectedOrder.value = order
}

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await updateStatus(orderId, newStatus)
    const order = orders.value.find(o => o.id === orderId)
    if (order) {
      order.status = newStatus
    }
  } catch (error) {
    console.error('Failed to update status:', error)
  }
}

const playNotificationSound = () => {
  const audio = new Audio('/notification.mp3')
  audio.play().catch(() => {})
}

onMounted(() => {
  loadOrders()
})
</script>
```

### 2. MenuManagementPage.vue
```vue
<template>
  <div class="flex h-screen">
    <Sidebar />
    
    <main class="flex-1 overflow-auto p-6">
      <header class="mb-6 flex justify-between items-center">
        <h1 class="text-3xl font-bold">메뉴 관리</h1>
        <button @click="showForm = true" class="btn-primary">
          메뉴 추가
        </button>
      </header>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <MenuCard
          v-for="menu in menus"
          :key="menu.id"
          :menu="menu"
          @edit="editMenu(menu)"
          @delete="deleteMenu(menu.id)"
        />
      </div>
      
      <MenuForm
        v-if="showForm"
        :menu="editingMenu"
        :categories="categories"
        @save="saveMenu"
        @close="closeForm"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMenus, createMenu, updateMenu, deleteMenu as apiDeleteMenu } from '@/api/menu'
import { getCategories } from '@/api/category'
import MenuCard from '@/components/molecules/MenuCard.vue'
import MenuForm from '@/components/organisms/MenuForm.vue'
import Sidebar from '@/components/organisms/Sidebar.vue'

const menus = ref([])
const categories = ref([])
const showForm = ref(false)
const editingMenu = ref(null)

const loadMenus = async () => {
  const response = await getMenus()
  menus.value = response.data
}

const loadCategories = async () => {
  const response = await getCategories()
  categories.value = response.data
}

const editMenu = (menu) => {
  editingMenu.value = menu
  showForm.value = true
}

const saveMenu = async (menuData) => {
  if (editingMenu.value) {
    await updateMenu(editingMenu.value.id, menuData)
  } else {
    await createMenu(menuData)
  }
  await loadMenus()
  closeForm()
}

const deleteMenu = async (menuId) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await apiDeleteMenu(menuId)
    await loadMenus()
  }
}

const closeForm = () => {
  showForm.value = false
  editingMenu.value = null
}

onMounted(() => {
  loadMenus()
  loadCategories()
})
</script>
```

## Configuration Files

### package.json
```json
{
  "name": "table-order-admin",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

### vite.config.js
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5174,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
```

## Key Features

1. ✅ JWT Authentication
2. ✅ WebSocket Real-time Updates
3. ✅ Order Status Management
4. ✅ Table CRUD
5. ✅ Menu CRUD with Image Upload
6. ✅ Category CRUD
7. ✅ Notification Sound on New Order
8. ✅ Responsive Design (Desktop-first)

## Installation & Run

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

Server runs on http://localhost:5174

---

**Total Files**: ~40 files

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Complete
