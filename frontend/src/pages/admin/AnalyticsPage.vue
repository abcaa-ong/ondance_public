<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Analytics</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Dados de uso e engajamento da plataforma</p>
    </div>

    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 6" :key="n" flat bordered class="od-card" style="flex: 1; min-width: 200px;">
        <q-card-section><q-skeleton type="rect" height="60px" /></q-card-section>
      </q-card>
    </div>

    <template v-else>
      <div class="row q-gutter-sm q-mb-lg">
        <MetricCard class="col" label="Total de usuários" :value="String(a.total_users || 0)" accent-color="var(--od-accent)" />
        <MetricCard class="col" label="Alunos" :value="String(a.total_students || 0)" accent-color="#7F77DD" />
        <MetricCard class="col" label="Professores" :value="String(a.total_teachers || 0)" accent-color="#1D9E75" />
        <MetricCard class="col" label="Cursos publicados" :value="String(a.published_courses || 0)" accent-color="#E97B3C" />
      </div>

      <div class="row q-gutter-md q-mb-lg">
        <q-card flat bordered class="od-card col-12 col-md-6">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Engajamento</div>
            <div class="column q-gutter-md">
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Matrículas totais</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.total_enrollments || 0 }}</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Cursos concluídos</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.completed_enrollments || 0 }}</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Taxa de conclusão</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.completion_rate || 0 }}%</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Total de aulas</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.total_lessons || 0 }}</span>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <q-card flat bordered class="od-card col-12 col-md-6">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Avaliações</div>
            <div class="column q-gutter-md">
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Média de avaliação</span>
                <div class="row items-center" style="gap: 4px;">
                  <q-icon name="star" size="14px" style="color: #f59e0b;" />
                  <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.avg_rating || 0 }}</span>
                </div>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Total de avaliações</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.total_reviews || 0 }}</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Média carga horária</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.avg_workload_hours || 0 }}h</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Leads captados</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ a.total_leads || 0 }}</span>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Top courses -->
      <q-card v-if="a.top_courses?.length > 0" flat bordered class="od-card">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Cursos mais populares</div>
          <div v-for="(c, i) in a.top_courses" :key="i" class="row items-center q-py-sm"
            :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px' }">
            <div style="width: 24px; text-align: center; font-size: 13px; font-weight: 600; color: var(--od-text-4);">{{ i + 1 }}</div>
            <div style="flex: 1; min-width: 0; font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ c.title }}</div>
            <q-badge :label="`${c.enrollments_count} matrículas`"
              style="background: var(--od-bg-subtle); color: var(--od-text-3); font-size: 10px;" />
          </div>
        </q-card-section>
      </q-card>
    </template>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import MetricCard from 'components/shared/MetricCard.vue'

const a = ref({})
const loading = ref(true)

async function loadAnalytics() {
  loading.value = true
  try {
    const resp = await api.get('/admin/analytics/')
    a.value = resp.data
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(loadAnalytics)
</script>
