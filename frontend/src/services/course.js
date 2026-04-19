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

  published() {
    return api.get('/courses/published/')
  },

  adminList(status = null) {
    const params = status ? { status } : {}
    return api.get('/admin/courses/', { params })
  },

  approve(id) {
    return api.post(`/admin/courses/${id}/approve/`)
  },

  reject(id) {
    return api.post(`/admin/courses/${id}/reject/`)
  },

  students({ courseId = null } = {}) {
    const params = courseId ? { course_id: courseId } : {}
    return api.get('/teacher/students/', { params })
  },
}
