<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Aprovar Cursos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">
        Revise e publique cursos enviados por professores
      </p>
    </div>

    <!-- Filtros de status -->
    <div class="row q-mb-md" style="gap: 8px;">
      <q-btn
        v-for="tab in tabs"
        :key="tab.value"
        unelevated no-caps dense
        :label="tab.label"
        :style="activeTab === tab.value
          ? { background: 'var(--od-accent)', color: '#fff', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }
          : { background: 'var(--od-bg-subtle)', color: 'var(--od-text-3)', borderRadius: '8px', fontSize: '12px', padding: '4px 14px' }"
        @click="setTab(tab.value)"
      >
        <q-badge
          v-if="tab.count !== null"
          floating
          :color="tab.value === 'PENDING' ? 'negative' : 'grey-6'"
          :label="tab.count"
          style="font-size: 9px;"
        />
      </q-btn>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="column items-center justify-center" style="min-height: 240px; gap: 12px;">
      <q-spinner size="30px" :style="{ color: 'var(--od-accent)' }" />
      <span style="font-size: 13px; color: var(--od-text-4);">Carregando cursos...</span>
    </div>

    <!-- Lista vazia -->
    <div v-else-if="courses.length === 0" class="column items-center justify-center" style="min-height: 240px; gap: 10px;">
      <q-icon name="fact_check" size="40px" style="color: var(--od-text-5);" />
      <p style="font-size: 14px; color: var(--od-text-4); margin: 0;">
        Nenhum curso {{ emptyLabel }}
      </p>
    </div>

    <!-- Tabela de cursos -->
    <q-card v-else flat bordered class="od-card">
      <div
        v-for="(course, idx) in courses"
        :key="course.id"
        class="row items-center q-px-md q-py-sm"
        :style="{
          borderTop: idx > 0 ? '0.5px solid var(--od-border-light)' : 'none',
          gap: '12px',
        }"
      >
        <!-- Avatar do professor -->
        <q-avatar size="36px" :style="{ background: 'var(--od-accent)', flexShrink: 0 }">
          <span style="color: #fff; font-size: 13px; font-weight: 600;">
            {{ initials(course.teacher) }}
          </span>
        </q-avatar>

        <!-- Informações do curso -->
        <div class="col" style="min-width: 0;">
          <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {{ course.title }}
          </div>
          <div style="font-size: 12px; color: var(--od-text-4); margin-top: 1px;">
            {{ course.teacher.name || course.teacher.email }}
          </div>
        </div>

        <!-- Badge de status -->
        <q-badge
          :color="statusColor(course.status)"
          :label="statusLabel(course.status)"
          style="font-size: 10px; border-radius: 6px; padding: 3px 8px;"
        />

        <!-- Ações -->
        <div class="row" style="gap: 6px; flex-shrink: 0;">
          <q-btn
            v-if="course.status !== 'APPROVED'"
            unelevated no-caps dense
            label="Aprovar"
            :loading="actionId === course.id + ':approve'"
            style="background: #1D9E75; color: #fff; border-radius: 6px; font-size: 12px; padding: 3px 10px;"
            @click="handleApprove(course)"
          />
          <q-btn
            v-if="course.status !== 'REJECTED'"
            flat no-caps dense
            label="Rejeitar"
            :loading="actionId === course.id + ':reject'"
            style="color: var(--od-text-4); border-radius: 6px; font-size: 12px; padding: 3px 10px;"
            @click="handleReject(course)"
          />
        </div>
      </div>
    </q-card>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { courseService } from 'src/services/course'

const $q = useQuasar()

const loading = ref(true)
const courses = ref([])
const activeTab = ref('PENDING')
const actionId = ref(null)
const counts = ref({ PENDING: null, APPROVED: null, REJECTED: null })

const tabs = computed(() => [
  { label: 'Pendentes',  value: 'PENDING',  count: counts.value.PENDING },
  { label: 'Aprovados',  value: 'APPROVED', count: null },
  { label: 'Rejeitados', value: 'REJECTED', count: null },
  { label: 'Todos',      value: null,        count: null },
])

const emptyLabel = computed(() => {
  const map = { PENDING: 'pendente', APPROVED: 'aprovado', REJECTED: 'rejeitado' }
  return activeTab.value ? map[activeTab.value] : 'cadastrado'
})

async function load (statusFilter) {
  loading.value = true
  try {
    const { data } = await courseService.adminList(statusFilter)
    courses.value = data.results ?? data
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao carregar cursos.', position: 'top', timeout: 3000 })
  } finally {
    loading.value = false
  }
}

async function loadPendingCount () {
  try {
    const { data } = await courseService.adminList('PENDING')
    const results = data.results ?? data
    counts.value.PENDING = results.length
  } catch { /* silencioso */ }
}

async function setTab (value) {
  activeTab.value = value
  await load(value)
}

async function handleApprove (course) {
  actionId.value = course.id + ':approve'
  try {
    const { data } = await courseService.approve(course.id)
    updateCourse(data)
    $q.notify({ type: 'positive', message: `"${course.title}" aprovado!`, position: 'top', timeout: 2500 })
    if (activeTab.value === 'PENDING') courses.value = courses.value.filter(c => c.id !== course.id)
    counts.value.PENDING = Math.max(0, (counts.value.PENDING ?? 1) - 1)
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao aprovar curso.', position: 'top', timeout: 3000 })
  } finally {
    actionId.value = null
  }
}

async function handleReject (course) {
  actionId.value = course.id + ':reject'
  try {
    const { data } = await courseService.reject(course.id)
    updateCourse(data)
    $q.notify({ type: 'warning', message: `"${course.title}" rejeitado.`, position: 'top', timeout: 2500 })
    if (activeTab.value === 'PENDING') courses.value = courses.value.filter(c => c.id !== course.id)
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao rejeitar curso.', position: 'top', timeout: 3000 })
  } finally {
    actionId.value = null
  }
}

function updateCourse (updated) {
  const idx = courses.value.findIndex(c => c.id === updated.id)
  if (idx !== -1) courses.value[idx] = updated
}

function initials (teacher) {
  const str = teacher.name || teacher.email || ''
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?'
}

function statusLabel (s) {
  return { PENDING: 'Pendente', APPROVED: 'Aprovado', REJECTED: 'Rejeitado' }[s] ?? s
}

function statusColor (s) {
  return { PENDING: 'orange', APPROVED: 'positive', REJECTED: 'negative' }[s] ?? 'grey'
}

onMounted(async () => {
  await load('PENDING')
  loadPendingCount()
})
</script>
