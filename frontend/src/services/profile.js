import { api } from 'boot/axios'

export const profileService = {
  get() {
    return api.get('/profile/')
  },

  update(data) {
    const isFormData = data instanceof FormData
    return api.patch('/profile/', data, {
      headers: isFormData ? { 'Content-Type': undefined } : {},
    })
  },
}
