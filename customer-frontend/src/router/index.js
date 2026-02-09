import { createRouter, createWebHistory } from 'vue-router'
import { useSession } from '@/composables/useSession'

const routes = [
  {
    path: '/',
    redirect: '/qr-scan'
  },
  {
    path: '/qr-scan',
    name: 'QRScan',
    component: () => import('@/pages/QRScanPage.vue')
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/pages/MenuListPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('@/pages/OrderPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order-status',
    name: 'OrderStatus',
    component: () => import('@/pages/OrderStatusPage.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useSession()
  
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/qr-scan')
  } else if (to.path === '/qr-scan' && isAuthenticated.value) {
    next('/menu')
  } else {
    next()
  }
})

export default router
