import { api } from 'boot/axios'

export const reviewService = {
  list(params = {}) {
    return api.get('/reviews/', { params })
  },

  get(id) {
    return api.get(`/reviews/${id}/`)
  },

  create(data) {
    return api.post('/reviews/', data)
  },

  update(id, data) {
    return api.patch(`/reviews/${id}/`, data)
  },

  remove(id) {
    return api.delete(`/reviews/${id}/`)
  },

  byCourse(courseId) {
    return api.get(`/courses/${courseId}/reviews/`)
  },

  myReviews() {
    return api.get('/reviews/', { params: { mine: true } })
  },
}

export const commentService = {
  listByLesson(lessonId) {
    return api.get(`/lessons/${lessonId}/comments/`)
  },

  create(lessonId, data) {
    return api.post(`/lessons/${lessonId}/comments/`, data)
  },

  update(id, data) {
    return api.patch(`/comments/${id}/`, data)
  },

  remove(id) {
    return api.delete(`/comments/${id}/`)
  },
}
