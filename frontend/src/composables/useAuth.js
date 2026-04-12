import { computed, ref } from 'vue'
import { authService } from 'src/services/auth'

const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const PROFILE_COMPLETE_KEY = 'profile_complete'

const accessToken = ref(localStorage.getItem(ACCESS_TOKEN_KEY) || '')
const refreshToken = ref(localStorage.getItem(REFRESH_TOKEN_KEY) || '')
const profileComplete = ref(localStorage.getItem(PROFILE_COMPLETE_KEY) === 'true')

function parseJwt(token) {
  if (!token) return null
  const payload = token.split('.')[1]
  if (!payload) return null

  try {
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
    return JSON.parse(decodeURIComponent(
      decoded
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    ))
  } catch {
    return null
  }
}

const user = computed(() => parseJwt(accessToken.value))
const isAuthenticated = computed(() => !!accessToken.value)

function saveTokens(data = {}) {
  const access = data.access ?? data.access_token ?? ''
  const refresh = data.refresh ?? data.refresh_token ?? ''

  if (access) {
    accessToken.value = access
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
  }

  if (refresh) {
    refreshToken.value = refresh
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  }

  if (data.profile_complete !== undefined) {
    profileComplete.value = !!data.profile_complete
    localStorage.setItem(PROFILE_COMPLETE_KEY, data.profile_complete ? 'true' : 'false')
  }
}

function clearTokens() {
  accessToken.value = ''
  refreshToken.value = ''
  profileComplete.value = false
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(PROFILE_COMPLETE_KEY)
}

async function login(credentials) {
  const response = await authService.login(credentials)
  saveTokens(response.data)
  return response
}

async function googleLogin(credential, role = 'aluno') {
  const response = await authService.googleLogin(credential, role)
  saveTokens(response.data)
  return response
}

async function logout() {
  clearTokens()
}

async function refresh() {
  const token = refreshToken.value || localStorage.getItem(REFRESH_TOKEN_KEY)
  if (!token) {
    clearTokens()
    return null
  }

  const response = await authService.refresh(token)
  saveTokens(response.data)
  return response
}

export function useAuth() {
  return {
    isAuthenticated,
    user,
    accessToken,
    refreshToken,
    profileComplete,
    login,
    googleLogin,
    logout,
    refresh,
    clearTokens,
    saveTokens,
  }
}
