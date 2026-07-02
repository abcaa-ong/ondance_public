<template>
  <q-page class="q-pa-lg">

    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Visão Geral</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">KPIs globais da plataforma</p>
    </div>

    <div class="row q-gutter-sm q-mb-lg">
      <MetricCard class="col" label="Usuários ativos"
        :value="loading ? '…' : String(analytics.total_users || 0)"
        :change="loading ? '' : `${analytics.total_students || 0} alunos · ${analytics.total_teachers || 0} professores`"
        change-type="up" accent-color="var(--od-accent)" />
      <MetricCard class="col" label="Cursos publicados"
        :value="loading ? '…' : String(analytics.published_courses || 0)"
        :change="loading ? '' : `${analytics.total_courses || 0} total`"
        change-type="up" accent-color="#1D9E75" />
      <MetricCard class="col" label="Matrículas totais"
        :value="loading ? '…' : String(analytics.total_enrollments || 0)"
        :change="loading ? '' : `${analytics.completion_rate || 0}% conclusão`"
        change-type="up" accent-color="#7F77DD" />
      <MetricCard class="col" label="Leads captados"
        :value="loading ? '…' : String(analytics.total_leads || 0)"
        change="cadastros na landing"
        change-type="neutral" accent-color="#E97B3C" />
    </div>

    <div class="row q-gutter-md">
      <div class="col-12 col-md-6">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Cursos mais populares</div>
            <div v-if="loading" class="column q-gutter-xs">
              <q-skeleton v-for="n in 3" :key="n" type="text" height="30px" />
            </div>
            <div v-else-if="analytics.top_courses?.length === 0" class="text-center q-py-md">
              <p style="color: var(--od-text-4); font-size: 13px;">Nenhum dado disponível ainda.</p>
            </div>
            <div v-else>
              <div v-for="(c, i) in analytics.top_courses" :key="i" class="row items-center q-py-sm"
                :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px' }">
                <div style="width: 24px; text-align: center; font-size: 13px; font-weight: 600; color: var(--od-text-4);">{{ i + 1 }}</div>
                <div style="flex:1; min-width:0;">
                  <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ c.title }}</div>
                </div>
                <q-badge :label="`${c.enrollments_count} matrículas`"
                  style="background: var(--od-bg-subtle); color: var(--od-text-3); font-size: 10px;" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Métricas gerais</div>
            <div class="column q-gutter-md">
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Média de carga horária</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ analytics.avg_workload_hours || 0 }}h</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Média de avaliação</span>
                <div class="row items-center" style="gap: 4px;">
                  <q-icon name="star" size="14px" style="color: #f59e0b;" />
                  <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ analytics.avg_rating || 0 }}</span>
                </div>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Total de avaliações</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ analytics.total_reviews || 0 }}</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Total de aulas</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ analytics.total_lessons || 0 }}</span>
              </div>
              <div class="row items-center justify-between">
                <span style="font-size: 13px; color: var(--od-text-3);">Cursos concluídos</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ analytics.completed_enrollments || 0 }}</span>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import MetricCard from 'components/shared/MetricCard.vue'

const analytics = ref({})
const loading = ref(true)

async function loadAnalytics() {
  loading.value = true
  try {
    const resp = await api.get('/admin/analytics/')
    analytics.value = resp.data
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(loadAnalytics)
</script>
