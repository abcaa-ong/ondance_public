<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Meus Cursos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Cursos em que você está matriculado</p>
    </div>

    <!-- Tabs -->
    <q-tabs
      v-model="activeTab"
      dense
      no-caps
      inline-label
      class="q-mb-md"
      active-color="var(--od-accent)"
      indicator-color="var(--od-accent)"
      style="color: var(--od-text-4);"
    >
      <q-tab name="progress" icon="play_circle" label="Em andamento" />
      <q-tab name="completed" icon="check_circle" label="Concluídos" />
    </q-tabs>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card" style="width: 280px;">
        <q-card-section>
          <q-skeleton type="rect" height="40px" style="border-radius: 8px;" class="q-mb-sm" />
          <q-skeleton type="text" width="60%" />
          <q-skeleton type="text" width="30%" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Error -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar seus cursos.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="load" />
      </q-card-section>
    </q-card>

    <!-- Empty -->
    <q-card v-else-if="filteredEnrollments.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon :name="activeTab === 'progress' ? 'play_circle' : 'check_circle'" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">
          {{ activeTab === 'progress' ? 'Você não tem cursos em andamento' : 'Você ainda não concluiu nenhum curso' }}
        </p>
        <q-btn v-if="activeTab === 'progress'" unelevated no-caps label="Explorar cursos" to="/student/explorar"
          style="background: var(--od-accent); color: #fff; border-radius: 8px; margin-top: 8px;" />
      </q-card-section>
    </q-card>

    <!-- Course list -->
    <div v-else class="row q-gutter-md">
      <q-card
        v-for="enrollment in filteredEnrollments"
        :key="enrollment.id"
        flat bordered
        class="od-card od-course-card"
        style="width: 280px; cursor: pointer; transition: box-shadow 0.15s;"
        @click="goToCourse(enrollment)"
      >
        <q-card-section style="padding: 16px;">
          <div class="od-display ellipsis-2-lines" style="font-size: 15px; font-weight: 600; color: var(--od-text-1); line-height: 1.35; margin-bottom: 8px;">
            {{ enrollment.course_title }}
          </div>
          <div class="q-mb-sm" style="font-size: 13px; color: var(--od-text-3);">
            {{ formatDate(activeTab === 'progress' ? enrollment.started_at : enrollment.completed_at) }}
          </div>
          <q-linear-progress
            :value="enrollment.progress_percent / 100"
            color="accent"
            size="6px"
            style="border-radius: 3px; margin-bottom: 6px;"
          />
          <div class="row items-center justify-between">
            <span style="font-size: 12px; color: var(--od-text-4);">{{ enrollment.progress_percent }}% concluído</span>
            <q-badge
              v-if="enrollment.is_completed"
              color="positive"
              label="Concluído"
              style="font-size: 10px;"
            />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courseService } from 'src/services/course'

const router = useRouter()
const enrollments = ref([])
const loading = ref(true)
const error = ref(false)
const activeTab = ref('progress')

const filteredEnrollments = computed(() =>
  activeTab.value === 'progress'
    ? enrollments.value.filter(e => !e.is_completed)
    : enrollments.value.filter(e => e.is_completed)
)

async function load() {
  loading.value = true
  error.value = false
  try {
    const resp = await courseService.enrollments()
    enrollments.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('pt-BR')
}

function goToCourse(enrollment) {
  router.push(`/student/courses/${enrollment.course}/assistir`)
}

onMounted(load)
</script>

<style scoped>
.od-course-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>