import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ left: 0, top: 0 })
})

function parseRole(token) {
  if (!token) return null
  try {
    const b64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    const payload = decodeURIComponent(
      atob(b64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')
    )
    return JSON.parse(payload).role
  } catch {
    return null
  }
}

const roleHome = {
  admin:     '/admin/overview',
  professor: '/teacher/dashboard',
  aluno:     '/student/dashboard',
}

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')

  if (!to.meta.guest && !token) return '/login'

  const role = parseRole(token)

  if (token && to.meta.guest) {
    return roleHome[role] ?? '/student/dashboard'
  }

  if (to.meta.role) {
    const allowed = Array.isArray(to.meta.role) ? to.meta.role : [to.meta.role]
    // admin acessa tudo
    if (role !== 'admin' && !allowed.includes(role)) {
      return roleHome[role] ?? '/student/dashboard'
    }
  }

  return true
})

export default router
