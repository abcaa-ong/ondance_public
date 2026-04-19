<template>
  <q-page class="q-pa-lg">

    <div class="row items-start justify-between q-mb-lg">
      <div>
        <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Olá, {{ firstName }} 👋</div>
        <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Continue de onde parou</p>
      </div>
    </div>

    <div class="row q-gutter-sm q-mb-lg">
      <MetricCard class="col" label="Cursos ativos"    value="3"   change="↑ 1 este mês"     change-type="up"      accent-color="var(--od-accent)" />
      <MetricCard class="col" label="Horas assistidas" value="12h" change="↑ 3h esta semana"  change-type="up"      accent-color="#1D9E75" />
      <MetricCard class="col" label="Progresso geral"  value="61%" change="em andamento"       change-type="neutral" accent-color="#7F77DD" />
      <MetricCard class="col" label="Certificados"     value="1"   change="↑ ganho recente"   change-type="up"      accent-color="#378ADD" />
    </div>

    <div class="row q-gutter-md">
      <div class="col-12 col-md-7">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="row items-center justify-between q-mb-md">
              <div class="od-card-title od-display">Meus cursos</div>
              <q-btn flat no-caps label="ver todos →" style="color: var(--od-accent); font-size: 12px;" to="/student/my-courses" />
            </div>
            <div
              v-for="course in activeCourses" :key="course.id"
              class="row items-center q-py-sm"
              :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px', cursor: 'pointer' }"
              @click="$router.push(`/student/courses/${course.id}/assistir`)"
            >
              <div class="od-course-thumb" :style="{ background: course.thumbBg }">{{ course.emoji }}</div>
              <div style="flex: 1; min-width: 0;">
                <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ course.name }}</div>
                <div style="font-size: 11.5px; color: var(--od-text-3); margin-top: 2px;">{{ course.teacher }} · {{ course.lessons }} aulas</div>
              </div>
              <div style="width: 80px;">
                <div class="od-progress-wrap">
                  <div class="od-progress-fill" :style="{ width: course.progress + '%', background: course.color }" />
                </div>
                <div style="font-size: 11px; color: var(--od-text-3); text-align: right; margin-top: 3px;">{{ course.progress }}%</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col column q-gutter-md">
        <q-card flat class="od-card" style="background: var(--od-accent) !important; border: none !important;">
          <q-card-section>
            <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-bottom: 4px;">Salsa para Iniciantes</div>
            <div class="od-display" style="font-size: 17px; color: #fff; margin-bottom: 8px;">Aula 9 — Giro Básico</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.75);">32 min · Vídeo + Exercício</div>
            <q-btn unelevated no-caps label="▶  Continuar" class="full-width q-mt-md"
              style="background: rgba(255,255,255,0.2); color: #fff; border-radius: 8px; font-weight: 500;"
              to="/student/courses/1/assistir" />
          </q-card-section>
        </q-card>

        <q-card flat bordered class="od-card col">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Minha semana</div>
            <div class="row items-end" style="height: 60px; gap: 5px;">
              <div v-for="(bar, i) in weekBars" :key="i" class="col"
                style="border-radius: 3px 3px 0 0; background: var(--od-accent); transition: opacity 0.2s;"
                :style="{ height: bar + '%', opacity: i === 4 ? 1 : 0.4 }" />
            </div>
            <div class="row justify-between q-mt-xs" :style="{ fontSize: '10px', color: 'var(--od-text-4)' }">
              <span v-for="d in ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom']" :key="d">{{ d }}</span>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

  </q-page>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from 'src/composables/useAuth'
import MetricCard from 'components/shared/MetricCard.vue'

const { user } = useAuth()
const firstName = computed(() => user.value?.name?.split(' ')[0] ?? 'Você')
const weekBars = [30, 50, 40, 70, 90, 60, 80]
const activeCourses = [
  { id: 1, name: 'Salsa para Iniciantes', teacher: 'Prof. Carlos Moura', lessons: 12, progress: 75, emoji: '💃', thumbBg: '#FAEEDA', color: 'var(--od-accent)' },
  { id: 2, name: 'Forró Universitário',   teacher: 'Prof. Ana Lima',     lessons:  8, progress: 40, emoji: '🕺', thumbBg: '#E1F5EE', color: '#1D9E75' },
  { id: 3, name: 'Soltinho Moderno',      teacher: 'Prof. João Vitor',   lessons: 10, progress: 20, emoji: '🪩', thumbBg: '#EEEDFE', color: '#7F77DD' },
]
</script>
