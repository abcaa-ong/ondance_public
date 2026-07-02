<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Ganhos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Receita gerada pelos seus cursos</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card" style="flex: 1; min-width: 200px;">
        <q-card-section><q-skeleton type="rect" height="80px" /></q-card-section>
      </q-card>
    </div>

    <template v-else>
      <!-- KPIs -->
      <div class="row q-gutter-sm q-mb-lg">
        <q-card flat bordered class="od-card" style="flex: 1; min-width: 180px;">
          <q-card-section style="padding: 16px;">
            <div style="font-size: 12px; color: var(--od-text-3);">Total de matrículas</div>
            <div style="font-size: 22px; font-weight: 700; color: var(--od-text-1); margin-top: 4px;">{{ stats.total_enrollments }}</div>
          </q-card-section>
        </q-card>
        <q-card flat bordered class="od-card" style="flex: 1; min-width: 180px;">
          <q-card-section style="padding: 16px;">
            <div style="font-size: 12px; color: var(--od-text-3);">Cursos publicados</div>
            <div style="font-size: 22px; font-weight: 700; color: var(--od-text-1); margin-top: 4px;">{{ stats.published_courses }}</div>
          </q-card-section>
        </q-card>
        <q-card flat bordered class="od-card" style="flex: 1; min-width: 180px;">
          <q-card-section style="padding: 16px;">
            <div style="font-size: 12px; color: var(--od-text-3);">Média de avaliação</div>
            <div class="row items-center" style="gap: 4px; margin-top: 4px;">
              <q-icon name="star" size="16px" style="color: #f59e0b;" />
              <span style="font-size: 22px; font-weight: 700; color: var(--od-text-1);">{{ stats.avg_rating }}</span>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Per-course breakdown -->
      <q-card flat bordered class="od-card">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Receita por curso</div>
          <div v-if="stats.courses?.length === 0" class="text-center q-py-md">
            <p style="color: var(--od-text-4); font-size: 13px;">Nenhum dado disponível ainda.</p>
          </div>
          <div v-else>
            <div v-for="c in stats.courses" :key="c.title" class="row items-center q-py-sm"
              :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px' }">
              <div style="flex: 1; min-width: 0;">
                <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ c.title }}</div>
                <div style="font-size: 11px; color: var(--od-text-4);">{{ c.enrollments_count }} matrículas</div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 14px; font-weight: 600; color: #1D9E75;">R$ {{ formatCurrency(c.enrollments_count * 49.90) }}</div>
                <div style="font-size: 10px; color: var(--od-text-5);">estimativa</div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <div style="font-size: 11px; color: var(--od-text-5); margin-top: 12px; text-align: center;">
        * Valores estimados com base em R$ 49,90 por matrícula. Sistema financeiro completo em desenvolvimento.
      </div>
    </template>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const stats = ref({ total_enrollments: 0, published_courses: 0, avg_rating: 0, courses: [] })
const loading = ref(true)

function formatCurrency(value) {
  return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

async function load() {
  loading.value = true
  try {
    const [coursesResp, analyticsResp] = await Promise.all([
      api.get('/courses/mine/'),
      api.get('/admin/analytics/').catch(() => ({ data: {} })),
    ])
    const courses = coursesResp.data.results ?? coursesResp.data ?? []
    const published = courses.filter(c => c.is_published)

    // Get enrollment counts per course
    const coursesWithEnrollments = await Promise.all(published.map(async (c) => {
      try {
        const detail = await api.get(`/courses/${c.id}/`)
        return {
          title: c.title,
          enrollments_count: detail.data.enrollments_count || 0,
        }
      } catch {
        return { title: c.title, enrollments_count: 0 }
      }
    }))

    const totalEnrollments = coursesWithEnrollments.reduce((sum, c) => sum + c.enrollments_count, 0)

    stats.value = {
      total_enrollments: totalEnrollments,
      published_courses: published.length,
      avg_rating: analyticsResp.data?.avg_rating || 0,
      courses: coursesWithEnrollments.sort((a, b) => b.enrollments_count - a.enrollments_count),
    }
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
