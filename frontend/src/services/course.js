import { api } from 'boot/axios'

export const courseService = {
  list() {
    return api.get('/courses/')
  },

  get(id) {
    return api.get(`/courses/${id}/`)
  },

  create(data) {
    return api.post('/courses/', data)
  },

  update(id, data) {
    return api.put(`/courses/${id}/`, data)
  },

  remove(id) {
    return api.delete(`/courses/${id}/`)
  },

  mine() {
    return api.get('/courses/mine/')
  },
}
