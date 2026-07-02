<template>
  <q-page class="q-pa-lg">

    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Avaliações Recebidas</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">O que seus alunos estão dizendo</p>
    </div>

    <!-- Metrics -->
    <div class="row q-gutter-sm q-mb-lg">
      <MetricCard
        class="col"
        label="Total de avaliações"
        :value="loading ? '…' : String(reviews.length)"
        :change="loading ? '' : `${reviews.length} avaliação${reviews.length !== 1 ? 'ões' : ''}`"
        change-type="up"
        accent-color="#f59e0b"
      />
      <MetricCard
        class="col"
        label="Média geral"
        :value="loading ? '…' : avgRating"
        :change="loading ? '' : avgRatingLabel"
        change-type="up"
        accent-color="var(--od-accent)"
      />
      <MetricCard
        class="col"
        label="Comentários"
        :value="loading ? '…' : String(reviewsWithComments)"
        :change="loading ? '' : `${reviewsWithComments} com comentário`"
        change-type="neutral"
        accent-color="#7F77DD"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="column q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card">
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <q-skeleton type="circle" size="40px" />
            <div class="col">
              <q-skeleton type="text" width="30%" />
              <q-skeleton type="text" width="60%" class="q-mt-xs" />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Error -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar as avaliações.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="load" />
      </q-card-section>
    </q-card>

    <!-- Empty state -->
    <q-card v-else-if="reviews.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="rate_review" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Nenhuma avaliação recebida ainda.</p>
        <p style="color: var(--od-text-4); font-size: 13px;">Quando seus alunos avaliarem seus cursos, elas aparecerão aqui.</p>
      </q-card-section>
    </q-card>

    <!-- Reviews list -->
    <div v-else class="column q-gutter-md">
      <q-card
        v-for="review in reviews"
        :key="review.id"
        flat bordered
        class="od-card"
      >
        <q-card-section style="padding: 16px;">
          <div class="row items-start" style="gap: 12px;">
            <!-- Avatar -->
            <q-avatar size="40px" style="flex-shrink: 0;">
              <img v-if="review.student_photo" :src="review.student_photo" />
              <div
                v-else
                class="row items-center justify-center full-width full-height"
                style="background: var(--od-accent); color: #fff; font-size: 14px; font-weight: 600; border-radius: 50%;"
              >{{ initials(review.student_name) }}</div>
            </q-avatar>

            <!-- Content -->
            <div style="flex: 1; min-width: 0;">
              <div class="row items-center" style="gap: 8px; flex-wrap: wrap;">
                <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ review.student_name }}</span>
                <span style="font-size: 12px; color: var(--od-text-4);">avaliou</span>
                <span style="font-size: 13px; font-weight: 500; color: var(--od-accent);">{{ review.course_title }}</span>
              </div>

              <!-- Stars + date -->
              <div class="row items-center q-mt-xs" style="gap: 8px;">
                <div class="row items-center" style="gap: 2px;">
                  <q-icon
                    v-for="n in 5" :key="n"
                    name="star"
                    size="16px"
                    :style="{ color: n <= review.rating ? '#f59e0b' : 'var(--od-text-5)' }"
                  />
                </div>
                <span style="font-size: 12px; color: var(--od-text-4);">{{ formatDate(review.created_at) }}</span>
              </div>

              <!-- Comment -->
              <p v-if="review.comment" style="margin: 8px 0 0; font-size: 13px; color: var(--od-text-2); line-height: 1.5;">
                {{ review.comment }}
              </p>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reviewService } from 'src/services/review'
import MetricCard from 'components/shared/MetricCard.vue'

const reviews = ref([])
const loading = ref(true)
const error = ref(false)

const avgRating = computed(() => {
  if (reviews.value.length === 0) return '—'
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return (sum / reviews.value.length).toFixed(1)
})

const avgRatingLabel = computed(() => {
  const avg = parseFloat(avgRating.value)
  if (isNaN(avg)) return ''
  if (avg >= 4.5) return 'Excelente'
  if (avg >= 3.5) return 'Muito bom'
  if (avg >= 2.5) return 'Bom'
  if (avg >= 1.5) return 'Regular'
  return 'Precisa melhorar'
})

const reviewsWithComments = computed(() => {
  return reviews.value.filter(r => r.comment && r.comment.trim()).length
})

async function load() {
  loading.value = true
  error.value = false
  try {
    const resp = await reviewService.list()
    reviews.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function initials(str) {
  if (!str) return '?'
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(load)
</script>
