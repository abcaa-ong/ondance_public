<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Meus Alunos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">
        Alunos matriculados nos seus cursos
      </p>
    </div>

    <!-- Filtro por curso -->
    <div class="row items-center q-mb-md" style="gap: 8px; flex-wrap: wrap;">
      <q-btn
        unelevated no-caps dense
        label="Todos os cursos"
        :style="activeCourse === null
          ? { background: 'var(--od-accent)', color: '#fff', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }
          : { background: 'var(--od-bg-subtle)', color: 'var(--od-text-3)', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }"
        @click="setCourse(null)"
      />
      <q-btn
        v-for="course in courses"
        :key="course.id"
        unelevated no-caps dense
        :label="course.title"
        :style="activeCourse === course.id
          ? { background: 'var(--od-accent)', color: '#fff', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }
          : { background: 'var(--od-bg-subtle)', color: 'var(--od-text-3)', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }"
        @click="setCourse(course.id)"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="column items-center justify-center" style="min-height: 240px; gap: 12px;">
      <q-spinner size="30px" :style="{ color: 'var(--od-accent)' }" />
      <span style="font-size: 13px; color: var(--od-text-4);">Carregando alunos...</span>
    </div>

    <!-- Lista vazia -->
    <div v-else-if="enrollments.length === 0" class="column items-center justify-center" style="min-height: 240px; gap: 10px;">
      <q-icon name="group" size="40px" style="color: var(--od-text-5);" />
      <p style="font-size: 14px; color: var(--od-text-4); margin: 0;">
        Nenhum aluno matriculado{{ activeCourse ? ' neste curso' : ' ainda' }}
      </p>
    </div>

    <!-- Lista de matrículas -->
    <q-card v-else flat bordered class="od-card">
      <div
        v-for="(enrollment, idx) in enrollments"
        :key="enrollment.id"
        class="row items-center q-px-md q-py-sm"
        :style="{
          borderTop: idx > 0 ? '0.5px solid var(--od-border-light)' : 'none',
          gap: '12px',
        }"
      >
        <!-- Avatar -->
        <q-avatar size="36px" :style="{ flexShrink: 0 }">
          <img v-if="enrollment.student_photo" :src="enrollment.student_photo" style="object-fit: cover;" />
          <span
            v-else
            :style="{
              background: avatarColor(enrollment.student_email),
              color: '#fff', fontSize: '13px', fontWeight: 600,
              width: '100%', height: '100%',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }"
          >
            {{ initials(enrollment) }}
          </span>
        </q-avatar>

        <!-- Nome e e-mail -->
        <div class="col" style="min-width: 0;">
          <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {{ enrollment.student_name || '—' }}
          </div>
          <div style="font-size: 12px; color: var(--od-text-4); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {{ enrollment.student_email }}
          </div>
        </div>

        <!-- Curso (visível somente quando "Todos os cursos") -->
        <div
          v-if="activeCourse === null"
          style="font-size: 12px; color: var(--od-text-3); max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0;"
          class="gt-sm"
        >
          {{ enrollment.course_title }}
        </div>

        <!-- Data de matrícula -->
        <div style="font-size: 12px; color: var(--od-text-4); white-space: nowrap; flex-shrink: 0;" class="gt-xs">
          {{ formatDate(enrollment.started_at) }}
        </div>

        <!-- Status de conclusão -->
        <q-badge
          :color="enrollment.is_completed ? 'positive' : 'grey-5'"
          :label="enrollment.is_completed ? 'Concluído' : 'Em andamento'"
          style="font-size: 10px; border-radius: 6px; padding: 3px 8px; flex-shrink: 0;"
        />
      </div>
    </q-card>

    <!-- Total -->
    <div v-if="!loading && enrollments.length > 0" style="font-size: 12px; color: var(--od-text-4); margin-top: 10px; text-align: right;">
      {{ total }} matrícula{{ total !== 1 ? 's' : '' }}
      · {{ completedCount }} concluída{{ completedCount !== 1 ? 's' : '' }}
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { courseService } from 'src/services/course'

const $q = useQuasar()

const loading = ref(true)
const enrollments = ref([])
const courses = ref([])
const activeCourse = ref(null)

const total = computed(() => enrollments.value.length)
const completedCount = computed(() => enrollments.value.filter(e => e.is_completed).length)

async function load () {
  loading.value = true
  try {
    const { data } = await courseService.students({ courseId: activeCourse.value })
    const results = data.results ?? data
    enrollments.value = results

    if (courses.value.length === 0) {
      const seen = new Map()
      for (const e of results) {
        if (!seen.has(e.course_id)) seen.set(e.course_id, { id: e.course_id, title: e.course_title })
      }
      courses.value = [...seen.values()]
    }
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao carregar alunos.', position: 'top', timeout: 3000 })
  } finally {
    loading.value = false
  }
}

function setCourse (id) {
  activeCourse.value = id
  load()
}

function initials (enrollment) {
  const str = enrollment.student_name || enrollment.student_email || ''
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?'
}

const COLORS = ['#6366F1', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#EF4444']
function avatarColor (email) {
  let hash = 0
  for (const c of email) hash = (hash * 31 + c.charCodeAt(0)) & 0xffffffff
  return COLORS[Math.abs(hash) % COLORS.length]
}

function formatDate (iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(load)
</script>
