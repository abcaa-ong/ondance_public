<template>
  <q-page class="q-pa-lg">

    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Dashboard</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Desempenho dos seus cursos</p>
    </div>

    <!-- Métricas -->
    <div class="row q-gutter-sm q-mb-lg">
      <MetricCard
        class="col"
        label="Cursos publicados"
        :value="loading ? '…' : String(publicados)"
        :change="loading ? '' : publicados === 1 ? '1 publicado' : `${publicados} publicados`"
        change-type="up"
        accent-color="var(--od-accent)"
      />
      <MetricCard class="col" label="Alunos matriculados" value="—"   change="em breve"          change-type="neutral" accent-color="#1D9E75" />
      <MetricCard class="col" label="Aulas criadas"        value="—"   change="em breve"          change-type="neutral" accent-color="#7F77DD" />
      <MetricCard
        class="col"
        label="Rascunhos"
        :value="loading ? '…' : String(rascunhos)"
        :change="rascunhos > 0 ? 'aguardando revisão' : 'nenhum pendente'"
        change-type="neutral"
        accent-color="#378ADD"
      />
    </div>

    <div class="row q-gutter-md">

      <!-- Lista de cursos recentes -->
      <div class="col-12 col-md-7">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="row items-center justify-between q-mb-md">
              <div class="od-card-title od-display">Meus cursos recentes</div>
              <q-btn flat no-caps label="ver todos →" style="color: var(--od-accent); font-size: 12px;" to="/teacher/courses" />
            </div>

            <!-- Loading -->
            <div v-if="loading" class="column q-gutter-xs">
              <div v-for="n in 3" :key="n" class="row items-center q-py-sm" style="gap: 12px;">
                <q-skeleton type="rect" width="36px" height="36px" style="border-radius: 8px; flex-shrink: 0;" />
                <div class="col">
                  <q-skeleton type="text" width="55%" />
                  <q-skeleton type="text" width="30%" class="q-mt-xs" />
                </div>
                <q-skeleton type="QBadge" width="60px" />
              </div>
            </div>

            <!-- Sem cursos -->
            <div v-else-if="courses.length === 0" class="text-center q-py-md">
              <p style="font-size: 13px; color: var(--od-text-4);">Nenhum curso criado ainda.</p>
              <q-btn flat no-caps label="Criar primeiro curso" to="/teacher/courses/new" style="color: var(--od-accent); font-size: 12px;" />
            </div>

            <!-- Lista real -->
            <div
              v-else
              v-for="course in courses"
              :key="course.id"
              class="row items-center q-py-sm"
              :style="{ borderBottom: '0.5px solid var(--od-border-light)', gap: '12px' }"
            >
              <div
                class="row items-center justify-center"
                style="width: 36px; height: 36px; border-radius: 8px; flex-shrink: 0;"
                :style="{ background: thumbBg(course.id) }"
              >
                <q-icon name="play_circle_outline" size="18px" style="color: var(--od-accent);" />
              </div>
              <div style="flex: 1; min-width: 0;">
                <div class="ellipsis" style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ course.title }}</div>
                <div style="font-size: 11.5px; color: var(--od-text-3); margin-top: 2px;">{{ course.teacher }}</div>
              </div>
              <q-badge
                :label="course.is_published ? 'Publicado' : 'Rascunho'"
                :style="course.is_published
                  ? 'background:#D1FAE5;color:#065F46'
                  : 'background:#FEF3C7;color:#92400E'"
                style="font-size:10px; border-radius:6px; padding: 3px 8px;"
              />
            </div>

          </q-card-section>
        </q-card>
      </div>

      <!-- Gráfico (mock) -->
      <div class="col">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-md">Matrículas — 7 dias</div>
            <div class="row items-end" style="height: 80px; gap: 5px;">
              <div v-for="(bar, i) in weekBars" :key="i" class="col"
                style="border-radius: 3px 3px 0 0; background: var(--od-accent); transition: opacity 0.2s;"
                :style="{ height: bar + '%', opacity: i === 4 ? 1 : 0.55 }" />
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
import { ref, computed, onMounted } from 'vue'
import MetricCard from 'components/shared/MetricCard.vue'
import { courseService } from 'src/services/course'

const courses = ref([])
const loading = ref(true)
const weekBars = [20, 45, 30, 60, 85, 40, 55]

const publicados = computed(() => courses.value.filter(c => c.is_published).length)
const rascunhos  = computed(() => courses.value.filter(c => !c.is_published).length)

const BG_PALETTE = ['#FAEEDA', '#E1F5EE', '#EEEDFE', '#EFF6FF', '#FFF0F5', '#F0FFF4']
function thumbBg (id) {
  const idx = parseInt(String(id).replace(/-/g, '').slice(-4), 16) % BG_PALETTE.length
  return BG_PALETTE[idx]
}

async function load () {
  loading.value = true
  try {
    const resp = await courseService.mine()
    
    courses.value = resp.data.results ?? resp.data
  } catch {
    courses.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
