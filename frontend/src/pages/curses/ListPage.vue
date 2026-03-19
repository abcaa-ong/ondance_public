<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <div class="od-display" style="font-size: 22px; color: var(--od-text-1);">Cursos</div>
        <p style="color: var(--od-text-3); margin: 2px 0 0; font-size: 13px;">{{ filteredCourses.length }} curso{{ filteredCourses.length !== 1 ? 's' : '' }} encontrado{{ filteredCourses.length !== 1 ? 's' : '' }}</p>
      </div>
      <q-btn
        unelevated no-caps
        icon="add"
        label="Novo Curso"
        style="background: var(--od-accent); color: #fff; border-radius: 8px; font-weight: 500;"
        to="/curses/new"
      />
    </div>

    <!-- Filtros -->
    <div class="row items-center q-gutter-sm q-mb-lg">
      <q-input
        v-model="search"
        outlined dense
        placeholder="Buscar por título ou professor..."
        style="width: 280px;"
      >
        <template #prepend>
          <q-icon name="search" size="16px" :style="{ color: 'var(--od-text-4)' }" />
        </template>
        <template v-if="search" #append>
          <q-icon name="close" size="14px" :style="{ color: 'var(--od-text-4)', cursor: 'pointer' }" @click="search = ''" />
        </template>
      </q-input>

      <q-select
        v-model="filterLevel"
        outlined dense
        :options="['Todos', 'Iniciante', 'Intermediário', 'Avançado']"
        style="width: 150px;"
        label="Nível"
      />

      <q-select
        v-model="filterStatus"
        outlined dense
        :options="statusOptions"
        option-label="label"
        option-value="value"
        emit-value
        map-options
        style="width: 150px;"
        label="Status"
      />

      <q-btn
        v-if="hasActiveFilters"
        flat no-caps dense
        label="Limpar filtros"
        style="font-size: 12px; color: var(--od-text-3);"
        @click="clearFilters"
      />
    </div>

    <!-- Lista de cursos -->
    <div v-if="filteredCourses.length === 0" class="text-center q-py-xl">
      <q-icon name="search_off" size="48px" :style="{ color: 'var(--od-text-5)' }" />
      <p style="font-size: 14px; margin-top: 12px;" :style="{ color: 'var(--od-text-4)' }">Nenhum curso encontrado</p>
    </div>

    <div v-else class="column q-gutter-sm">
      <q-card
        v-for="course in filteredCourses"
        :key="course.id"
        flat bordered
        class="od-card"
        style="cursor: pointer;"
        @click="$router.push(`/curses/editar/${course.id}`)"
      >
        <q-card-section class="row items-center" style="gap: 16px; padding: 14px 16px;">

          <!-- Thumb -->
          <div
            class="od-course-thumb"
            :style="{ background: course.thumbBg, fontSize: '22px', width: '48px', height: '48px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }"
          >
            {{ course.emoji }}
          </div>

          <!-- Info principal -->
          <div style="flex: 1; min-width: 0;">
            <div class="row items-center" style="gap: 8px; margin-bottom: 2px;">
              <span style="font-size: 14px; font-weight: 500;" :style="{ color: 'var(--od-text-1)' }">{{ course.title }}</span>
              <q-badge
                :label="course.status === 'published' ? 'Publicado' : 'Rascunho'"
                :style="{
                  background: course.status === 'published' ? '#E3F7EE' : 'var(--od-bg-subtle)',
                  color:      course.status === 'published' ? '#1D9E75' : 'var(--od-text-3)',
                  fontSize: '10.5px', padding: '2px 7px', borderRadius: '20px'
                }"
              />
            </div>
            <div style="font-size: 12px; color: var(--od-text-3);">
              {{ course.teacher }}
              <span style="margin: 0 4px; color: var(--od-border);">·</span>
              {{ course.level }}
            </div>
          </div>

          <!-- Módulos e aulas -->
          <div class="column items-center" style="min-width: 60px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: var(--od-text-1);">{{ course.modules }}</div>
            <div style="font-size: 11px; color: var(--od-text-4);">módulo{{ course.modules !== 1 ? 's' : '' }}</div>
          </div>

          <div :style="{ width: '1px', height: '32px', background: 'var(--od-border)' }" />

          <div class="column items-center" style="min-width: 60px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: var(--od-text-1);">{{ course.lessons }}</div>
            <div style="font-size: 11px; color: var(--od-text-4);">aula{{ course.lessons !== 1 ? 's' : '' }}</div>
          </div>

          <div :style="{ width: '1px', height: '32px', background: 'var(--od-border)' }" />

          <!-- Alunos -->
          <div class="column items-center" style="min-width: 60px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: var(--od-text-1);">{{ course.students }}</div>
            <div style="font-size: 11px; color: var(--od-text-4);">aluno{{ course.students !== 1 ? 's' : '' }}</div>
          </div>

          <!-- Ações -->
          <q-btn flat round dense icon="more_vert" :style="{ color: 'var(--od-text-4)' }" @click.stop>
            <q-menu anchor="bottom right" self="top right">
              <q-list style="min-width: 160px; font-size: 13px;">
                <q-item clickable v-close-popup @click="$router.push(`/curses/editar/${course.id}`)">
                  <q-item-section avatar><q-icon name="edit" size="16px" /></q-item-section>
                  <q-item-section>Editar</q-item-section>
                </q-item>
                <q-item clickable v-close-popup @click="toggleStatus(course)">
                  <q-item-section avatar>
                    <q-icon :name="course.status === 'published' ? 'unpublished' : 'publish'" size="16px" />
                  </q-item-section>
                  <q-item-section>{{ course.status === 'published' ? 'Despublicar' : 'Publicar' }}</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-close-popup class="text-negative" @click="confirmDelete(course)">
                  <q-item-section avatar><q-icon name="delete_outline" size="16px" color="negative" /></q-item-section>
                  <q-item-section>Excluir</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

        </q-card-section>
      </q-card>
    </div>

    <!-- Dialog de confirmação de exclusão -->
    <q-dialog v-model="deleteDialog.open">
      <q-card style="min-width: 320px; border-radius: 12px; background: var(--od-bg-surface);">
        <q-card-section>
          <div class="od-display" style="font-size: 16px; color: var(--od-text-1); margin-bottom: 6px;">Excluir curso?</div>
          <p style="font-size: 13px; margin: 0; color: var(--od-text-3);">
            O curso <strong>{{ deleteDialog.course?.title }}</strong> será excluído permanentemente.
          </p>
        </q-card-section>
        <q-card-actions align="right" style="padding: 8px 16px 16px;">
          <q-btn flat no-caps label="Cancelar" style="color: var(--od-text-3);" v-close-popup />
          <q-btn unelevated no-caps label="Excluir" color="negative" style="border-radius: 8px;" @click="deleteCourse" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'

const search       = ref('')
const filterLevel  = ref('Todos')
const filterStatus = ref('all')

const statusOptions = [
  { label: 'Todos',      value: 'all'       },
  { label: 'Publicados', value: 'published' },
  { label: 'Rascunhos',  value: 'draft'     },
]

const courses = ref([
  { id: 1, title: 'Salsa para Iniciantes',  teacher: 'Prof. Carlos Moura', level: 'Iniciante',     modules: 3, lessons: 12, students: 87,  status: 'published', emoji: '💃', thumbBg: '#FAEEDA' },
  { id: 2, title: 'Forró Universitário',    teacher: 'Prof. Ana Lima',     level: 'Intermediário', modules: 4, lessons:  8, students: 64,  status: 'published', emoji: '🕺', thumbBg: '#E1F5EE' },
  { id: 3, title: 'Soltinho Moderno',       teacher: 'Prof. João Vitor',   level: 'Avançado',      modules: 5, lessons: 10, students: 112, status: 'published', emoji: '🪩', thumbBg: '#EEEDFE' },
  { id: 4, title: 'Zouk Avançado',          teacher: 'Prof. Renata Souza', level: 'Avançado',      modules: 2, lessons:  5, students:   0, status: 'draft',     emoji: '🌊', thumbBg: '#E8F0FD' },
])

const hasActiveFilters = computed(() =>
  search.value !== '' || filterLevel.value !== 'Todos' || filterStatus.value !== 'all'
)

const filteredCourses = computed(() =>
  courses.value.filter(c => {
    const matchSearch = !search.value ||
      c.title.toLowerCase().includes(search.value.toLowerCase()) ||
      c.teacher.toLowerCase().includes(search.value.toLowerCase())
    const matchLevel  = filterLevel.value === 'Todos' || c.level === filterLevel.value
    const matchStatus = filterStatus.value === 'all'  || c.status === filterStatus.value
    return matchSearch && matchLevel && matchStatus
  })
)

function clearFilters () {
  search.value       = ''
  filterLevel.value  = 'Todos'
  filterStatus.value = 'all'
}

function toggleStatus (course) {
  course.status = course.status === 'published' ? 'draft' : 'published'
}

const deleteDialog = ref({ open: false, course: null })

function confirmDelete (course) {
  deleteDialog.value = { open: true, course }
}

function deleteCourse () {
  courses.value = courses.value.filter(c => c.id !== deleteDialog.value.course?.id)
  deleteDialog.value = { open: false, course: null }
}
</script>
