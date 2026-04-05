import { api } from 'boot/axios'

export const authService = {
  login(credentials) {
    return api.post('/token/', credentials)
  },

  register(userData) {
    return api.post('/register/', userData)
  },

  refresh(refreshToken) {
    return api.post('/token/refresh/', { refresh: refreshToken })
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
}
