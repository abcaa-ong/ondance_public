<template>
  <q-page class="q-pa-lg">
    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <div style="flex: 1;">
        <q-skeleton type="rect" height="300px" style="border-radius: 12px;" />
      </div>
      <div style="width: 320px;">
        <q-skeleton type="rect" height="60px" class="q-mb-sm" style="border-radius: 8px;" />
        <q-skeleton type="rect" height="60px" style="border-radius: 8px;" />
      </div>
    </div>

    <!-- Error -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">{{ errorMessage }}</p>
        <q-btn flat no-caps label="Voltar para meus cursos" to="/student/my-courses" style="color: var(--od-accent);" />
      </q-card-section>
    </q-card>

    <!-- Course content -->
    <div v-else class="od-study-layout">
      <!-- Main area -->
      <div class="od-study-main">
        <!-- Video player -->
        <VideoPlayer
          :src="currentLesson?.video_url || ''"
          :start-position="currentLesson?.progress?.video_position || 0"
          @timeupdate="onTimeUpdate"
          @ended="onVideoEnded"
          @complete="onVideoComplete"
        />

        <!-- Lesson info -->
        <div class="q-mt-md" v-if="currentLesson">
          <div class="od-display" style="font-size: 20px; color: var(--od-text-1);">{{ currentLesson.title }}</div>
          <div class="row items-center q-mt-sm" style="gap: 8px;">
            <q-badge :color="currentLesson.progress?.is_completed ? 'positive' : 'grey'" :label="currentLesson.progress?.is_completed ? 'Concluída' : 'Em andamento'" />
            <span style="color: var(--od-text-3); font-size: 13px;">
              Módulo {{ currentModuleIndex + 1 }} · Aula {{ currentLessonIndex + 1 }}
            </span>
          </div>
        </div>

        <!-- Content area -->
        <div v-if="currentLesson?.content" class="q-mt-lg">
          <div class="od-display" style="font-size: 16px; color: var(--od-text-1); margin-bottom: 8px;">Conteúdo da aula</div>
          <div class="od-card q-pa-md" style="white-space: pre-wrap; color: var(--od-text-2);">{{ currentLesson.content }}</div>
        </div>

        <!-- Exercises -->
        <div v-if="currentLesson?.exercises" class="q-mt-md">
          <div class="od-display" style="font-size: 16px; color: var(--od-text-1); margin-bottom: 8px;">Exercícios / Atividades</div>
          <div class="od-card q-pa-md" style="white-space: pre-wrap; color: var(--od-text-2);">{{ currentLesson.exercises }}</div>
        </div>

        <!-- Materials -->
        <div v-if="currentLesson?.materials_url" class="q-mt-md">
          <q-btn
            flat no-caps icon="download" label="Material de apoio"
            :href="currentLesson.materials_url" target="_blank"
            style="color: var(--od-accent);"
          />
        </div>

        <!-- Comments section -->
        <div v-if="currentLesson" class="q-mt-lg">
          <div class="row items-center q-mb-md" style="gap: 8px;">
            <q-icon name="forum" size="20px" style="color: var(--od-text-3);" />
            <span style="font-size: 15px; font-weight: 600; color: var(--od-text-1);">
              Comentários
            </span>
            <span v-if="comments.length" style="font-size: 12px; color: var(--od-text-4);">({{ comments.length }})</span>
          </div>

          <!-- Comment input -->
          <div class="od-comment-input q-mb-md">
            <q-input
              v-model="newComment"
              outlined dense
              type="textarea"
              placeholder="Deixe um comentário sobre esta aula..."
              aria-label="Comentário sobre esta aula"
              rows="2"
              style="font-size: 13px;"
            />
            <div class="row justify-end q-mt-xs">
              <q-btn
                unelevated no-caps
                label="Comentar"
                icon="send"
                :disable="!newComment.trim()"
                :loading="submittingComment"
                @click="submitComment"
                size="sm"
                style="background: var(--od-accent); color: #fff; border-radius: 6px;"
              />
            </div>
          </div>

          <!-- Comments list -->
          <div v-if="commentsLoading" class="q-py-md">
            <q-skeleton v-for="n in 3" :key="n" type="rect" height="60px" class="q-mb-sm" style="border-radius: 8px;" />
          </div>

          <div v-else-if="comments.length === 0" class="text-center q-py-md">
            <p style="font-size: 13px; color: var(--od-text-4);">Nenhum comentário ainda. Seja o primeiro!</p>
          </div>

          <div v-else class="od-comments-list">
            <div v-for="comment in comments" :key="comment.id" class="od-comment-item">
              <div class="row items-start" style="gap: 10px;">
                <q-avatar size="32px" style="flex-shrink: 0;">
                  <img v-if="comment.student_photo" :src="comment.student_photo" />
                  <div
                    v-else
                    class="row items-center justify-center full-width full-height"
                    style="background: var(--od-accent); color: #fff; font-size: 12px; font-weight: 600; border-radius: 50%;"
                  >{{ initials(comment.student_name) }}</div>
                </q-avatar>
                <div style="flex: 1; min-width: 0;">
                  <div class="row items-center" style="gap: 6px;">
                    <span style="font-size: 13px; font-weight: 600; color: var(--od-text-1);">{{ comment.student_name }}</span>
                    <span style="font-size: 11px; color: var(--od-text-5);">{{ formatTime(comment.created_at) }}</span>
                  </div>
                  <p style="margin: 4px 0 0; font-size: 13px; color: var(--od-text-2); white-space: pre-wrap;">{{ comment.content }}</p>

                  <!-- Replies -->
                  <div v-if="comment.replies?.length" class="od-replies q-mt-sm">
                    <div v-for="reply in comment.replies" :key="reply.id" class="od-comment-item od-comment-item--reply">
                      <div class="row items-start" style="gap: 8px;">
                        <q-avatar size="24px" style="flex-shrink: 0;">
                          <img v-if="reply.student_photo" :src="reply.student_photo" />
                          <div
                            v-else
                            class="row items-center justify-center full-width full-height"
                            style="background: var(--od-accent); color: #fff; font-size: 9px; font-weight: 600; border-radius: 50%;"
                          >{{ initials(reply.student_name) }}</div>
                        </q-avatar>
                        <div style="flex: 1; min-width: 0;">
                          <div class="row items-center" style="gap: 6px;">
                            <span style="font-size: 12px; font-weight: 600; color: var(--od-text-1);">{{ reply.student_name }}</span>
                            <span style="font-size: 11px; color: var(--od-text-5);">{{ formatTime(reply.created_at) }}</span>
                          </div>
                          <p style="margin: 2px 0 0; font-size: 12px; color: var(--od-text-2); white-space: pre-wrap;">{{ reply.content }}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Reply button -->
                  <q-btn
                    v-if="!comment.replying"
                    flat no-caps dense
                    label="Responder"
                    size="xs"
                    style="color: var(--od-text-4); margin-top: 4px;"
                    @click="comment.replying = true"
                  />

                  <!-- Reply input -->
                  <div v-if="comment.replying" class="q-mt-sm">
                    <q-input
                      v-model="comment.replyText"
                      outlined dense
                      placeholder="Sua resposta..."
                      rows="1"
                      style="font-size: 12px;"
                    />
                    <div class="row q-mt-xs" style="gap: 4px;">
                      <q-btn
                        unelevated no-caps label="Enviar" size="xs"
                        :disable="!comment.replyText?.trim()"
                        :loading="comment.submittingReply"
                        @click="submitReply(comment)"
                        style="background: var(--od-accent); color: #fff; border-radius: 4px;"
                      />
                      <q-btn
                        flat no-caps label="Cancelar" size="xs"
                        style="color: var(--od-text-4);"
                        @click="comment.replying = false; comment.replyText = ''"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Mark complete button -->
        <div class="q-mt-md" v-if="currentLesson && !currentLesson.progress?.is_completed">
          <q-btn
            unelevated no-caps
            label="Marcar como concluída"
            icon="check_circle"
            :loading="markingComplete"
            @click="markComplete"
            style="background: var(--od-accent); color: #fff; border-radius: 8px;"
          />
        </div>

        <!-- Navigation -->
        <div class="row q-mt-lg" style="gap: 8px;">
          <q-btn
            v-if="prevLesson" flat no-caps icon="arrow_back" label="Aula anterior"
            @click="goToLesson(prevLesson)"
            style="color: var(--od-accent);"
          />
          <q-space />
          <q-btn
            v-if="nextLesson" unelevated no-caps icon-right="arrow_forward" label="Próxima aula"
            @click="goToLesson(nextLesson)"
            style="background: var(--od-accent); color: #fff; border-radius: 8px;"
          />
        </div>

        <!-- Review section (only when course completed) -->
        <div v-if="course.progress_percent === 100" class="od-review-section q-mt-lg">
          <div class="od-review-divider" />

          <div v-if="reviewLoading" class="q-py-md">
            <q-skeleton type="rect" height="80px" style="border-radius: 8px;" />
          </div>

          <!-- Already reviewed -->
          <div v-else-if="existingReview" class="od-review-card">
            <div class="row items-center q-mb-sm" style="gap: 8px;">
              <q-icon name="rate_review" size="20px" style="color: var(--od-accent);" />
              <span style="font-size: 15px; font-weight: 600; color: var(--od-text-1);">Sua avaliação</span>
            </div>
            <StarRating :model-value="existingReview.rating" readonly size="md" :show-label="true" />
            <p v-if="existingReview.comment" style="margin-top: 8px; font-size: 13px; color: var(--od-text-2);">{{ existingReview.comment }}</p>
          </div>

          <!-- Review form -->
          <div v-else-if="showReviewForm" class="od-review-card">
            <div class="row items-center q-mb-sm" style="gap: 8px;">
              <q-icon name="rate_review" size="20px" style="color: var(--od-accent);" />
              <span style="font-size: 15px; font-weight: 600; color: var(--od-text-1);">Avalie este curso</span>
            </div>
            <p style="font-size: 13px; color: var(--od-text-3); margin-bottom: 10px;">
              Como foi sua experiência? Sua avaliação ajuda outros alunos.
            </p>
            <StarRating v-model="reviewRating" size="lg" />
            <q-input
              v-model="reviewComment"
              outlined dense
              type="textarea"
              placeholder="Deixe um comentário (opcional)"
              aria-label="Comentário opcional sobre o curso"
              rows="3"
              class="q-mt-md"
              style="font-size: 13px;"
            />
            <div class="row q-mt-md" style="gap: 8px;">
              <q-btn
                unelevated no-caps
                label="Enviar avaliação"
                icon="send"
                :disable="reviewRating === 0"
                :loading="submittingReview"
                @click="submitReview"
                style="background: var(--od-accent); color: #fff; border-radius: 8px;"
              />
              <q-btn
                flat no-caps
                label="Agora não"
                @click="showReviewForm = false"
                style="color: var(--od-text-4);"
              />
            </div>
          </div>

          <!-- Prompt to review -->
          <div v-else class="od-review-prompt" @click="showReviewForm = true">
            <q-icon name="star_outline" size="24px" style="color: var(--od-accent);" />
            <div>
              <div style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">Avalie este curso</div>
              <div style="font-size: 12px; color: var(--od-text-4);">Compartilhe sua experiência com outros alunos</div>
            </div>
            <q-icon name="chevron_right" size="20px" style="color: var(--od-text-5); margin-left: auto;" />
          </div>
        </div>

        <!-- Next course recommendation -->
        <div v-if="course.progress_percent === 100 && nextCourse" class="od-next-course q-mt-lg">
          <div class="od-review-divider" />
          <div class="od-next-course-card">
            <q-icon name="trending_up" size="24px" style="color: var(--od-accent);" />
            <div style="flex: 1;">
              <div style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">Próximo curso recomendado</div>
              <div style="font-size: 13px; color: var(--od-text-2); margin-top: 2px;">{{ nextCourse.title }}</div>
              <div v-if="nextCourse.level" style="font-size: 11px; color: var(--od-text-4); margin-top: 2px;">{{ nextCourse.level }} · {{ nextCourse.dance_style || 'Dança' }}</div>
            </div>
            <q-btn
              unelevated no-caps
              label="Ver curso"
              icon="arrow_forward"
              :to="`/student/explorar`"
              size="sm"
              style="background: var(--od-accent); color: #fff; border-radius: 6px;"
            />
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="od-study-sidebar">
        <div class="od-display" style="font-size: 16px; color: var(--od-text-1); margin-bottom: 12px;">{{ course.title }}</div>
        <div class="q-mb-sm" style="font-size: 13px; color: var(--od-text-3);">Progresso: {{ course.progress_percent }}%</div>
        <q-linear-progress :value="course.progress_percent / 100" color="accent" size="6px" class="q-mb-md" style="border-radius: 3px;" />

        <div v-for="(mod, mi) in course.modules" :key="mod.id" class="q-mb-md">
          <div style="font-size: 12px; font-weight: 600; color: var(--od-text-3); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
            Módulo {{ mi + 1 }}
          </div>
          <div style="font-size: 14px; font-weight: 500; color: var(--od-text-2); margin-bottom: 6px;">{{ mod.title }}</div>
          <div
            v-for="les in mod.lessons" :key="les.id"
            class="od-sidebar-lesson"
            :class="{ 'od-sidebar-lesson--active': les.id === currentLessonId, 'od-sidebar-lesson--done': les.progress?.is_completed }"
            @click="goToLesson(les)"
          >
            <q-icon
              :name="les.progress?.is_completed ? 'check_circle' : 'play_circle_outline'"
              size="16px"
              :style="{ color: les.progress?.is_completed ? 'var(--od-accent)' : 'var(--od-text-5)' }"
              style="margin-right: 8px;"
            />
            <span class="ellipsis">{{ les.title }}</span>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { courseService } from 'src/services/course'
import { reviewService, commentService } from 'src/services/review'
import VideoPlayer from 'components/shared/VideoPlayer.vue'
import StarRating from 'components/shared/StarRating.vue'

const route = useRoute()
const courseId = computed(() => route.params.id)

const course = ref({ modules: [] })
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
const currentLessonId = ref(null)
const markingComplete = ref(false)
let pendingSave = null

// Review
const existingReview = ref(null)
const reviewLoading = ref(false)
const showReviewForm = ref(false)
const reviewRating = ref(0)
const reviewComment = ref('')
const submittingReview = ref(false)

// Comments
const comments = ref([])
const commentsLoading = ref(false)
const newComment = ref('')
const submittingComment = ref(false)

// Next course recommendation
const nextCourse = ref(null)

const allLessons = computed(() => {
  const lessons = []
  for (const mod of course.value.modules || []) {
    for (const les of mod.lessons || []) {
      lessons.push({ ...les, moduleId: mod.id })
    }
  }
  return lessons
})

const currentLesson = computed(() => {
  if (!currentLessonId.value) return null
  return allLessons.value.find(l => l.id === currentLessonId.value) || null
})
const currentModuleIndex = computed(() => {
  if (!currentLesson.value) return 0
  return (course.value.modules || []).findIndex(m => m.lessons?.some(l => l.id === currentLessonId.value))
})
const currentLessonIndex = computed(() => {
  if (!currentLesson.value) return 0
  const mod = (course.value.modules || [])[currentModuleIndex.value]
  return (mod?.lessons || []).findIndex(l => l.id === currentLessonId.value)
})

const currentIndex = computed(() => allLessons.value.findIndex(l => l.id === currentLessonId.value))
const prevLesson = computed(() => currentIndex.value > 0 ? allLessons.value[currentIndex.value - 1] : null)
const nextLesson = computed(() => currentIndex.value < allLessons.value.length - 1 ? allLessons.value[currentIndex.value + 1] : null)

async function loadCourse() {
  loading.value = true
  error.value = false
  try {
    const resp = await courseService.study(courseId.value)
    course.value = resp.data
    if (!course.value.modules) course.value.modules = []
    const firstIncomplete = allLessons.value.find(l => !l.progress?.is_completed)
    currentLessonId.value = (firstIncomplete || allLessons.value[0] || {}).id || null
    if (course.value.progress_percent === 100) loadReview()
  } catch (e) {
    error.value = true
    const status = e.response?.status
    if (status === 403) {
      errorMessage.value = 'Você não está matriculado neste curso. Volte ao catálogo e inscreva-se.'
    } else if (status === 404) {
      errorMessage.value = 'Curso não encontrado ou não disponível.'
    } else {
      errorMessage.value = `Não foi possível carregar o curso. (erro ${status || 'desconhecido'})`
    }
  } finally {
    loading.value = false
  }
}

function goToLesson(lesson) {
  if (lesson && lesson.id !== currentLessonId.value) {
    flushSave()
    currentLessonId.value = lesson.id
  }
}

async function onTimeUpdate(data) {
  if (!currentLessonId.value) return
  pendingSave = { ...data, lessonId: currentLessonId.value }
}

async function onVideoEnded() {
  if (currentLesson.value && !currentLesson.value.progress?.is_completed) {
    await markComplete()
  }
}

async function onVideoComplete() {
  await markComplete()
}

async function markComplete() {
  if (!currentLessonId.value || markingComplete.value) return
  markingComplete.value = true
  try {
    await courseService.saveProgress(courseId.value, currentLessonId.value, {
      video_position: 0,
      is_completed: true,
    })
    if (currentLesson.value) {
      if (!currentLesson.value.progress) currentLesson.value.progress = {}
      currentLesson.value.progress.is_completed = true
    }
    // Check if course is now completed
    const totalLessons = allLessons.value.length
    const completedLessons = allLessons.value.filter(l => l.progress?.is_completed).length
    if (totalLessons > 0 && completedLessons === totalLessons) {
      course.value.progress_percent = 100
      loadReview()
    }
  } catch {
    // silently fail
  } finally {
    markingComplete.value = false
  }
}

async function flushSave() {
  if (!pendingSave) return
  const data = { ...pendingSave }
  pendingSave = null
  try {
    await courseService.saveProgress(courseId.value, data.lessonId, {
      video_position: data.video_position,
      is_completed: data.is_completed || false,
    })
  } catch {
    // silently fail
  }
}

async function loadReview() {
  reviewLoading.value = true
  try {
    const resp = await reviewService.byCourse(courseId.value)
    const reviews = resp.data.results ?? resp.data
    existingReview.value = reviews.length > 0 ? reviews[0] : null
  } catch {
    // silently fail
  } finally {
    reviewLoading.value = false
  }
  // Load next course recommendation
  loadNextCourse()
}

async function loadNextCourse() {
  try {
    const resp = await courseService.published()
    const courses = resp.data.results ?? resp.data
    // Find courses that have this course as prerequisite
    const next = courses.find(c => c.prerequisite === courseId.value)
    nextCourse.value = next || null
  } catch {
    nextCourse.value = null
  }
}

async function submitReview() {
  if (!reviewRating.value) return
  submittingReview.value = true
  try {
    const resp = await reviewService.create({
      course: courseId.value,
      rating: reviewRating.value,
      comment: reviewComment.value || '',
    })
    existingReview.value = resp.data
    showReviewForm.value = false
    reviewRating.value = 0
    reviewComment.value = ''
  } catch {
    // silently fail
  } finally {
    submittingReview.value = false
  }
}

// Comments
async function loadComments() {
  if (!currentLessonId.value) return
  commentsLoading.value = true
  try {
    const resp = await commentService.listByLesson(currentLessonId.value)
    comments.value = (resp.data.results ?? resp.data).map(c => ({
      ...c,
      replying: false,
      replyText: '',
      submittingReply: false,
    }))
  } catch {
    comments.value = []
  } finally {
    commentsLoading.value = false
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  submittingComment.value = true
  try {
    const resp = await commentService.create(currentLessonId.value, {
      content: newComment.value.trim(),
    })
    comments.value.push({
      ...resp.data,
      replying: false,
      replyText: '',
      submittingReply: false,
    })
    newComment.value = ''
  } catch {
    // silently fail
  } finally {
    submittingComment.value = false
  }
}

async function submitReply(comment) {
  if (!comment.replyText?.trim()) return
  comment.submittingReply = true
  try {
    const resp = await commentService.create(currentLessonId.value, {
      content: comment.replyText.trim(),
      parent: comment.id,
    })
    if (!comment.replies) comment.replies = []
    comment.replies.push(resp.data)
    comment.replying = false
    comment.replyText = ''
  } catch {
    // silently fail
  } finally {
    comment.submittingReply = false
  }
}

function formatTime(dateStr) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return 'agora'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}min`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })
}

function initials(str) {
  if (!str) return '?'
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

onMounted(loadCourse)
onBeforeUnmount(flushSave)

watch(currentLessonId, () => {
  if (currentLessonId.value) loadComments()
})
</script>

<style scoped>
.od-study-layout {
  display: flex;
  gap: 24px;
}
.od-study-main {
  flex: 1;
  min-width: 0;
}
.od-study-sidebar {
  width: 320px;
  flex-shrink: 0;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  padding: 16px;
  background: var(--od-bg-surface, #1a1a2e);
  border-radius: 12px;
  border: 1px solid var(--od-border, #2a2a3e);
}
.od-sidebar-lesson {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--od-text-2);
  transition: background 0.15s;
}
.od-sidebar-lesson:hover {
  background: var(--od-bg-page, #0f0f1a);
}
.od-sidebar-lesson--active {
  background: var(--od-bg-page, #0f0f1a);
  color: var(--od-accent);
  font-weight: 600;
}
.od-sidebar-lesson--done {
  color: var(--od-text-4);
}

/* Review section */
.od-review-section {
  margin-top: 24px;
}
.od-review-divider {
  height: 1px;
  background: var(--od-border);
  margin-bottom: 20px;
}
.od-review-card {
  padding: 20px;
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 12px;
}
.od-review-prompt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: var(--od-bg-surface);
  border: 1px dashed var(--od-border);
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.od-review-prompt:hover {
  border-color: var(--od-accent);
  background: var(--od-bg-hover);
}

/* Comments */
.od-comment-input {
  padding: 12px;
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 8px;
}
.od-comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.od-comment-item {
  padding: 12px;
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 8px;
}
.od-comment-item--reply {
  background: transparent;
  border: none;
  padding: 8px 0 0 0;
}
.od-replies {
  padding-left: 12px;
  border-left: 2px solid var(--od-border);
}

/* Next course */
.od-next-course-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 12px;
  border-left: 3px solid var(--od-accent);
}

@media (max-width: 900px) {
  .od-study-layout {
    flex-direction: column;
  }
  .od-study-sidebar {
    width: 100%;
    max-height: none;
  }
}
</style>