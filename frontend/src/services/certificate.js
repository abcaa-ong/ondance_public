import { api } from 'boot/axios'

export const certificateService = {
  list() {
    return api.get('/certificates/')
  },
}
