import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tables',
    name: 'Tables',
    component: () => import('@/pages/TableManagementPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/menus',
    name: 'Menus',
    component: () => import('@/pages/MenuManagementPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('@/pages/CategoryManagementPage.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('admin_token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
