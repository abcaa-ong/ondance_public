<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Explorar Cursos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">
        {{ loading ? 'Carregando...' : `${filtered.length} curso${filtered.length !== 1 ? 's' : ''} disponível${filtered.length !== 1 ? 'is' : ''}` }}
      </p>
    </div>

    <!-- Filtros -->
    <div class="row q-gutter-md q-mb-lg" style="flex-wrap: wrap;">
      <!-- Busca -->
      <q-input
        v-model="search"
        outlined dense
        placeholder="Buscar por título ou professor..."
        aria-label="Buscar por título ou professor"
        style="min-width: 240px; flex: 1;"
        clearable
      >
        <template #prepend>
          <q-icon name="search" size="16px" :style="{ color: 'var(--od-text-4)' }" />
        </template>
      </q-input>

      <!-- Filtro por estilo de dança -->
      <q-select
        v-model="filterDanceStyle"
        :options="danceStyleOptions"
        outlined dense
        emit-value map-options
        clearable
        label="Estilo"
        style="min-width: 160px;"
      />

      <!-- Filtro por nível -->
      <q-select
        v-model="filterLevel"
        :options="levelOptions"
        outlined dense
        emit-value map-options
        clearable
        label="Nível"
        style="min-width: 140px;"
      />

      <!-- Filtro por professor -->
      <q-select
        v-model="filterTeacher"
        :options="teacherOptions"
        outlined dense
        emit-value map-options
        clearable
        label="Professor"
        style="min-width: 180px;"
      />

      <!-- Filtro por duração (carga horária) -->
      <q-select
        v-model="filterWorkload"
        :options="workloadOptions"
        outlined dense
        emit-value map-options
        clearable
        label="Duração"
        style="min-width: 140px;"
      />

      <!-- Limpar filtros -->
      <q-btn
        v-if="hasActiveFilters"
        flat no-caps
        icon="filter_alt_off"
        label="Limpar"
        style="color: var(--od-text-4); height: 36px;"
        @click="clearFilters"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 6" :key="n" flat bordered class="od-card" style="width: 280px;">
        <q-card-section>
          <q-skeleton type="rect" height="56px" style="border-radius: 12px;" class="q-mb-md" />
          <q-skeleton type="text" width="70%" />
          <q-skeleton type="text" width="40%" class="q-mt-xs" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Erro -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar os cursos.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="load" />
      </q-card-section>
    </q-card>

    <!-- Nenhum resultado -->
    <div v-else-if="filtered.length === 0" class="text-center q-py-xl">
      <q-icon name="search_off" size="48px" style="color: var(--od-text-5);" />
      <p style="margin-top: 12px; color: var(--od-text-3);">
        {{ courses.length === 0 ? 'Nenhum curso publicado ainda.' : 'Nenhum curso encontrado para essa busca.' }}
      </p>
      <q-btn v-if="hasActiveFilters" flat no-caps label="Limpar filtros" style="color: var(--od-accent);" @click="clearFilters" />
    </div>

    <!-- Grid de cursos -->
    <div v-else class="row q-gutter-md">
      <q-card
        v-for="course in filtered"
        :key="course.id"
        flat bordered
        class="od-card od-course-card"
        style="width: 280px; cursor: pointer; transition: box-shadow 0.15s;"
      >
        <q-card-section style="padding: 16px;" @click="onCourseClick(course)">

          <!-- Avatar do professor -->
          <div class="row items-center q-mb-md" style="gap: 10px;">
            <q-avatar size="40px" style="flex-shrink: 0;">
              <img v-if="course.teacher.photo" :src="course.teacher.photo" :alt="course.teacher.name" />
              <div
                v-else
                class="row items-center justify-center full-width full-height"
                style="background: var(--od-accent); color: #fff; font-size: 16px; font-weight: 600; border-radius: 50%;"
              >
                {{ initials(course.teacher.name || course.teacher.email) }}
              </div>
            </q-avatar>
            <div style="min-width: 0;">
              <div class="ellipsis" style="font-size: 13px; font-weight: 500; color: var(--od-text-2);">
                {{ course.teacher.name || course.teacher.email }}
              </div>
              <div style="font-size: 11px; color: var(--od-text-5);">Professor</div>
            </div>
          </div>

          <!-- Título -->
          <div class="od-display ellipsis-2-lines" style="font-size: 15px; font-weight: 600; color: var(--od-text-1); line-height: 1.35; margin-bottom: 10px;">
            {{ course.title }}
          </div>

          <!-- Badges -->
          <div class="row items-center q-gutter-xs" style="margin-bottom: 10px;">
            <q-badge
              v-if="course.level"
              :style="{ background: 'var(--od-accent)', color: '#fff', fontSize: '10px', borderRadius: '4px', padding: '2px 6px' }"
              :label="course.level"
            />
            <q-badge
              v-if="getDanceStyleLabel(course.dance_style)"
              :style="{ background: 'var(--od-bg-subtle)', color: 'var(--od-text-3)', fontSize: '10px', borderRadius: '4px', padding: '2px 6px' }"
              :label="getDanceStyleLabel(course.dance_style)"
            />
          </div>

          <!-- Rodapé -->
          <div class="row items-center justify-between">
            <div class="row items-center" style="gap: 4px;">
              <q-icon v-if="course.reviews_count > 0" name="star" size="14px" style="color: #f59e0b;" />
              <span v-if="course.reviews_count > 0" style="font-size: 12px; color: var(--od-text-3); font-weight: 500;">
                {{ course.reviews_avg ? course.reviews_avg.toFixed(1) : '—' }}
              </span>
              <span v-if="course.reviews_count > 0" style="font-size: 11px; color: var(--od-text-4);">
                ({{ course.reviews_count }})
              </span>
            </div>
            <div class="row items-center" style="gap: 4px;">
              <q-icon v-if="course.prerequisite_title" name="link" size="12px" style="color: var(--od-text-4);" />
              <span v-if="course.prerequisite_title" style="font-size: 10px; color: var(--od-text-4); max-width: 80px;" class="ellipsis">
                Pré: {{ course.prerequisite_title }}
              </span>
              <q-icon name="arrow_forward" size="16px" style="color: var(--od-text-5);" />
            </div>
          </div>

        </q-card-section>
      </q-card>
    </div>

    <!-- Enroll dialog -->
    <q-dialog v-model="showEnrollDialog">
      <q-card flat bordered class="od-card" style="width: 400px; max-width: 90vw;">
        <q-card-section>
          <div class="od-display" style="font-size: 18px; color: var(--od-text-1);">{{ selectedCourse?.title }}</div>
          <p style="color: var(--od-text-3); margin-top: 6px; font-size: 14px;">
            Por {{ selectedCourse?.teacher?.name || selectedCourse?.teacher?.email }}
          </p>
          <p v-if="selectedCourse?.description" style="color: var(--od-text-2); margin-top: 8px; font-size: 13px;">
            {{ selectedCourse.description }}
          </p>
          <div class="row q-mt-sm" style="gap: 12px; font-size: 12px; color: var(--od-text-4);">
            <span v-if="selectedCourse?.level">{{ selectedCourse.level }}</span>
            <span v-if="selectedCourse?.dance_style">{{ getDanceStyleLabel(selectedCourse.dance_style) }}</span>
            <span v-if="selectedCourse?.duration">{{ selectedCourse.duration }}</span>
            <span v-if="selectedCourse?.workload">{{ selectedCourse.workload }}h</span>
            <span v-if="selectedCourse?.lessons_count">{{ selectedCourse.lessons_count }} aula{{ selectedCourse.lessons_count !== 1 ? 's' : '' }}</span>
          </div>
          <div v-if="selectedCourse?.reviews_count > 0" class="row items-center q-mt-sm" style="gap: 6px;">
            <div class="row items-center" style="gap: 2px;">
              <q-icon v-for="n in 5" :key="n" name="star" size="14px"
                :style="{ color: n <= Math.round(selectedCourse.reviews_avg) ? '#f59e0b' : 'var(--od-text-5)' }" />
            </div>
            <span style="font-size: 13px; font-weight: 500; color: var(--od-text-2);">
              {{ selectedCourse.reviews_avg?.toFixed(1) }}
            </span>
            <span style="font-size: 12px; color: var(--od-text-4);">
              ({{ selectedCourse.reviews_count }} avaliação{{ selectedCourse.reviews_count !== 1 ? 'ões' : '' }})
            </span>
          </div>
          <div v-if="selectedCourse?.prerequisite_title" class="row items-center q-mt-sm" style="gap: 6px;">
            <q-icon name="link" size="14px" style="color: var(--od-accent);" />
            <span style="font-size: 12px; color: var(--od-text-3);">
              Pré-requisito: <strong style="color: var(--od-text-2);">{{ selectedCourse.prerequisite_title }}</strong>
            </span>
          </div>
        </q-card-section>
        <q-card-actions align="right" style="padding: 8px 16px 16px;">
          <q-btn flat no-caps label="Cancelar" v-close-popup style="color: var(--od-text-4);" />
          <q-btn
            unelevated no-caps label="Inscrever-se"
            :loading="enrolling"
            @click="enroll"
            style="background: var(--od-accent); color: #fff; border-radius: 8px;"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courseService } from 'src/services/course'

const router = useRouter()
const courses = ref([])
const loading = ref(true)
const error = ref(false)
const showEnrollDialog = ref(false)
const selectedCourse = ref(null)
const enrolling = ref(false)

// Filtros
const search = ref('')
const filterDanceStyle = ref(null)
const filterLevel = ref(null)
const filterTeacher = ref(null)
const filterWorkload = ref(null)

// Opções de filtro
const danceStyleOptions = [
  { label: 'Ballet', value: 'ballet' },
  { label: 'Samba', value: 'samba' },
  { label: 'Forró', value: 'forro' },
  { label: 'Hip-Hop', value: 'hip_hop' },
  { label: 'Contemporâneo', value: 'contemporaneo' },
  { label: 'Funk', value: 'funk' },
  { label: 'Jazz', value: 'jazz' },
  { label: 'Dança de Salão', value: 'salão' },
  { label: 'Outras', value: 'outras' },
]

const levelOptions = [
  { label: 'Iniciante', value: 'Iniciante' },
  { label: 'Intermediário', value: 'Intermediário' },
  { label: 'Avançado', value: 'Avançado' },
]

const workloadOptions = [
  { label: 'Até 10h', value: { max: 10 } },
  { label: '10h - 20h', value: { min: 10, max: 20 } },
  { label: '20h - 50h', value: { min: 20, max: 50 } },
  { label: 'Mais de 50h', value: { min: 50 } },
]

const teacherOptions = computed(() => {
  const teacherMap = new Map()
  courses.value.forEach(c => {
    if (c.teacher && c.teacher.id) {
      teacherMap.set(c.teacher.id, {
        label: c.teacher.name || c.teacher.email,
        value: c.teacher.id,
      })
    }
  })
  return Array.from(teacherMap.values()).sort((a, b) => a.label.localeCompare(b.label))
})

const hasActiveFilters = computed(() => {
  return search.value || filterDanceStyle.value || filterLevel.value || filterTeacher.value || filterWorkload.value
})

const filtered = computed(() => {
  let result = courses.value

  // Busca por texto
  const q = search.value.trim().toLowerCase()
  if (q) {
    result = result.filter(c =>
      c.title.toLowerCase().includes(q) ||
      (c.teacher.name || '').toLowerCase().includes(q) ||
      c.teacher.email.toLowerCase().includes(q)
    )
  }

  // Filtro por estilo de dança
  if (filterDanceStyle.value) {
    result = result.filter(c => c.dance_style === filterDanceStyle.value)
  }

  // Filtro por nível
  if (filterLevel.value) {
    result = result.filter(c => c.level === filterLevel.value)
  }

  // Filtro por professor
  if (filterTeacher.value) {
    result = result.filter(c => c.teacher.id === filterTeacher.value)
  }

  // Filtro por duração (carga horária)
  if (filterWorkload.value) {
    const { min, max } = filterWorkload.value
    result = result.filter(c => {
      const w = c.workload || 0
      if (min !== undefined && w < min) return false
      if (max !== undefined && w > max) return false
      return true
    })
  }

  return result
})

function getDanceStyleLabel(value) {
  if (!value) return ''
  const option = danceStyleOptions.find(o => o.value === value)
  return option ? option.label : value
}

function clearFilters() {
  search.value = ''
  filterDanceStyle.value = null
  filterLevel.value = null
  filterTeacher.value = null
  filterWorkload.value = null
}

async function load () {
  loading.value = true
  error.value = false
  try {
    const resp = await courseService.published()
    courses.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function initials (str) {
  if (!str) return '?'
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function onCourseClick(course) {
  selectedCourse.value = course
  showEnrollDialog.value = true
}

async function enroll() {
  if (!selectedCourse.value) return
  enrolling.value = true
  try {
    await courseService.enroll(selectedCourse.value.id)
    showEnrollDialog.value = false
    router.push(`/student/courses/${selectedCourse.value.id}/assistir`)
  } catch (e) {
    if (e.response?.status === 409) {
      showEnrollDialog.value = false
      router.push(`/student/courses/${selectedCourse.value.id}/assistir`)
    }
  } finally {
    enrolling.value = false
  }
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
