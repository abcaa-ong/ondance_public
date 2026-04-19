<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Meus Cursos</div>
        <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Gerencie os cursos que você criou</p>
      </div>
      <q-btn unelevated no-caps icon="add" label="Novo Curso" to="/teacher/courses/new"
        style="background: var(--od-accent); color: #fff; border-radius: 8px;" />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="column q-gutter-sm">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card">
        <q-card-section class="row items-center q-gutter-md">
          <div class="col">
            <q-skeleton type="text" width="40%" />
            <q-skeleton type="text" width="20%" class="q-mt-xs" />
          </div>
          <q-skeleton type="QBtn" width="80px" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Erro -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar os cursos.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="fetch" />
      </q-card-section>
    </q-card>

    <!-- Vazio -->
    <q-card v-else-if="courses.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="video_library" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Você ainda não criou nenhum curso.</p>
        <q-btn unelevated no-caps label="Criar primeiro curso" to="/teacher/courses/new"
          style="background: var(--od-accent); color: #fff; border-radius: 8px; margin-top: 8px;" />
      </q-card-section>
    </q-card>

    <!-- Lista de cursos -->
    <div v-else class="column q-gutter-sm">
      <q-card
        v-for="course in courses"
        :key="course.id"
        flat bordered
        class="od-card"
      >
        <q-card-section class="row items-center no-wrap" style="gap: 12px;">

          <!-- Ícone -->
          <div
            class="row items-center justify-center"
            style="width: 40px; height: 40px; border-radius: 10px; background: var(--od-bg-subtle); flex-shrink: 0;"
          >
            <q-icon name="play_circle_outline" size="20px" style="color: var(--od-accent);" />
          </div>

          <!-- Título e status -->
          <div class="col" style="min-width: 0;">
            <div
              class="od-display ellipsis"
              style="font-size: 14px; color: var(--od-text-1); font-weight: 600;"
            >
              {{ course.title }}
            </div>
            <div class="row items-center q-mt-xs" style="gap: 6px;">
              <q-badge
                :color="statusColor(course)"
                :label="statusLabel(course)"
                style="font-size: 11px; border-radius: 4px;"
              />
              <span style="font-size: 11px; color: var(--od-text-5);">{{ course.teacher }}</span>
            </div>
          </div>

          <!-- Ações -->
          <q-btn
            flat round dense
            icon="edit"
            size="sm"
            style="color: var(--od-text-4);"
            :to="`/teacher/courses/${course.id}/editar`"
          >
            <q-tooltip>Editar</q-tooltip>
          </q-btn>

        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { courseService } from 'src/services/course'

const courses = ref([])
const loading = ref(true)
const error = ref(false)

async function fetch () {
  loading.value = true
  error.value = false
  try {
    const resp = await courseService.mine()
    courses.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function statusColor (course) {
  if (course.is_published) return 'positive'
  if (course.status === 'REJECTED') return 'negative'
  return 'grey-6'
}

function statusLabel (course) {
  if (course.is_published) return 'Publicado'
  if (course.status === 'REJECTED') return 'Rejeitado'
  return 'Rascunho'
}

onMounted(fetch)
</script>
