<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="row items-start justify-between q-mb-lg">
      <div>
        <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Gestão de Cursos</div>
        <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Visão geral e controle dos cursos cadastrados</p>
      </div>
      <q-btn
        unelevated no-caps
        icon="add"
        label="Novo Curso"
        style="background: var(--od-accent); color: #fff; border-radius: 8px; font-weight: 500;"
        to="/curses/new"
      />
    </div>

    <!-- Metrics -->
    <div class="row q-gutter-sm q-mb-lg">
      <MetricCard
        class="col"
        label="Cursos publicados"
        value="12"
        change="↑ 2 este mês"
        change-type="up"
        accent-color="var(--od-accent)"
      />
      <MetricCard
        class="col"
        label="Alunos matriculados"
        value="348"
        change="↑ 41 esta semana"
        change-type="up"
        accent-color="#1D9E75"
      />
      <MetricCard
        class="col"
        label="Aulas cadastradas"
        value="96"
        change="↑ 8 recentes"
        change-type="up"
        accent-color="#7F77DD"
      />
      <MetricCard
        class="col"
        label="Rascunhos"
        value="3"
        change="aguardando revisão"
        change-type="neutral"
        accent-color="#378ADD"
      />
    </div>

    <!-- Main grid -->
    <div class="row q-gutter-md">

      <!-- Tabela de cursos -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="row items-center justify-between q-mb-md">
              <div class="od-card-title od-display">Cursos recentes</div>
              <q-input
                v-model="search"
                dense outlined
                placeholder="Buscar curso..."
                style="width: 200px; border-radius: 8px;"
              >
                <template #prepend>
                  <q-icon name="search" size="16px" :style="{ color: 'var(--od-text-4)' }" />
                </template>
              </q-input>
            </div>

            <div
              v-for="course in filteredCourses"
              :key="course.id"
              class="row items-center q-py-sm"
              :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px', cursor: 'pointer' }"
              @click="$router.push(`/curses/editar/${course.id}`)"
            >
              <div class="od-course-thumb" :style="{ background: course.thumbBg }">
                {{ course.emoji }}
              </div>
              <div style="flex: 1; min-width: 0;">
                <div style="font-size: 13px; font-weight: 500;" :style="{ color: 'var(--od-text-1)' }">{{ course.name }}</div>
                <div style="font-size: 11.5px; margin-top: 2px;" :style="{ color: 'var(--od-text-3)' }">
                  {{ course.teacher }} · {{ course.lessons }} aulas · {{ course.students }} alunos
                </div>
              </div>
              <q-badge
                :label="course.status === 'published' ? 'Publicado' : 'Rascunho'"
                :style="{
                  background: course.status === 'published' ? '#E3F7EE' : 'var(--od-bg-subtle)',
                  color:      course.status === 'published' ? '#1D9E75' : 'var(--od-text-3)',
                  fontSize: '11px', padding: '3px 8px', borderRadius: '20px'
                }"
              />
            </div>

            <div v-if="filteredCourses.length === 0" class="text-center q-py-xl">
              <q-icon name="search_off" size="40px" :style="{ color: 'var(--od-text-5)' }" />
              <p style="margin-top: 8px; font-size: 13px;" :style="{ color: 'var(--od-text-4)' }">Nenhum curso encontrado</p>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Coluna lateral -->
      <div class="col column q-gutter-md">

        <!-- Ação rápida: último rascunho -->
        <q-card flat class="od-card" style="background: var(--od-accent) !important; border: none !important;">
          <q-card-section>
            <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-bottom: 4px;">Rascunho pendente</div>
            <div class="od-display" style="font-size: 17px; color: #fff; margin-bottom: 8px;">Zouk Avançado</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.75);">5 aulas criadas · aguardando revisão</div>
            <q-btn
              unelevated no-caps
              label="✏  Continuar edição"
              class="full-width q-mt-md"
              style="background: rgba(255,255,255,0.2); color: #fff; border-radius: 8px; font-weight: 500;"
              to="/curses/editar/4"
            />
          </q-card-section>
        </q-card>

        <!-- Matrículas por dia -->
        <q-card flat bordered class="od-card col">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Matrículas — 7 dias</div>
            <div class="row items-end" style="height: 60px; gap: 5px;">
              <div
                v-for="(bar, i) in weekBars"
                :key="i"
                class="col"
                style="border-radius: 3px 3px 0 0; background: var(--od-accent); transition: opacity 0.2s;"
                :style="{ height: bar + '%', opacity: i === 6 ? 1 : 0.4 }"
              />
            </div>
            <div class="row justify-between q-mt-xs" :style="{ fontSize: '10px', color: 'var(--od-text-4)' }">
              <span v-for="d in ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom']" :key="d">{{ d }}</span>
            </div>
          </q-card-section>
        </q-card>

        <!-- Categorias -->
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-sm">Por categoria</div>
            <div
              v-for="cat in categories"
              :key="cat.label"
              class="row items-center justify-between q-py-xs"
              style="font-size: 13px;"
            >
              <span :style="{ color: 'var(--od-text-2)' }">{{ cat.label }}</span>
              <span style="font-weight: 600;" :style="{ color: 'var(--od-text-1)' }">{{ cat.count }}</span>
            </div>
          </q-card-section>
        </q-card>

      </div>
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import MetricCard from 'components/shared/MetricCard.vue'

const search = ref('')

const courses = [
  { id: 1, name: 'Salsa para Iniciantes',  teacher: 'Prof. Carlos Moura', lessons: 12, students: 87,  status: 'published', emoji: '💃', thumbBg: '#FAEEDA' },
  { id: 2, name: 'Forró Universitário',    teacher: 'Prof. Ana Lima',     lessons:  8, students: 64,  status: 'published', emoji: '🕺', thumbBg: '#E1F5EE' },
  { id: 3, name: 'Soltinho Moderno',       teacher: 'Prof. João Vitor',   lessons: 10, students: 112, status: 'published', emoji: '🪩', thumbBg: '#EEEDFE' },
  { id: 4, name: 'Zouk Avançado',          teacher: 'Prof. Renata Souza', lessons:  5, students:   0, status: 'draft',     emoji: '🌊', thumbBg: '#E8F0FD' },
]

const filteredCourses = computed(() =>
  courses.filter(c => c.name.toLowerCase().includes(search.value.toLowerCase()))
)

const weekBars   = [25, 60, 45, 80, 50, 70, 95]

const categories = [
  { label: 'Salsa & Merengue', count: 4 },
  { label: 'Forró',            count: 3 },
  { label: 'Zouk',             count: 2 },
  { label: 'Soltinho',         count: 2 },
  { label: 'Outros',           count: 1 },
]
</script>
