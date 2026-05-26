import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/question-bank',
    name: 'QuestionBank',
    component: () => import('@/pages/QuestionBank.vue'),
    meta: { title: '题库', requiresAuth: true }
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/pages/Practice.vue'),
    meta: { title: '练习', requiresAuth: true }
  },
  {
    path: '/wrong-book',
    name: 'WrongBook',
    component: () => import('@/pages/WrongBook.vue'),
    meta: { title: '错题本', requiresAuth: true }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('@/pages/Courses.vue'),
    meta: { title: '课程', requiresAuth: true }
  },
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/pages/Community.vue'),
    meta: { title: '社区', requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/pages/Profile.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '培训平台'}`
  
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
