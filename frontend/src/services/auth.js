import { api } from 'boot/axios'

export const authService = {
  login(credentials) {
    return api.post('/token/', credentials)
  },

  register(userData) {
    return api.post('/register/', userData)
  },

  googleLogin(credential, role = 'aluno') {
    return api.post('/auth/social/google/', { credential, role })
  },

  refresh(refreshToken) {
    return api.post('/token/refresh/', { refresh: refreshToken })
  },
}
