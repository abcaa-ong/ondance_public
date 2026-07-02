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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { courseService } from 'src/services/course'
import VideoPlayer from 'components/shared/VideoPlayer.vue'

const route = useRoute()
const courseId = computed(() => route.params.id)

const course = ref({ modules: [] })
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
const currentLessonId = ref(null)
const markingComplete = ref(false)
let pendingSave = null

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

onMounted(loadCourse)
onBeforeUnmount(flushSave)
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