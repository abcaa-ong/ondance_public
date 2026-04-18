<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Explorar Cursos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">
        {{ loading ? 'Carregando...' : `${filtered.length} curso${filtered.length !== 1 ? 's' : ''} disponível${filtered.length !== 1 ? 'is' : ''}` }}
      </p>
    </div>

    <!-- Busca -->
    <div class="q-mb-lg">
      <q-input
        v-model="search"
        outlined dense
        placeholder="Buscar por título ou professor..."
        style="max-width: 360px;"
        clearable
      >
        <template #prepend>
          <q-icon name="search" size="16px" :style="{ color: 'var(--od-text-4)' }" />
        </template>
      </q-input>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 6" :key="n" flat bordered class="od-card" style="width: 280px;">
        <q-card-section>
          <q-skeleton type="rect" height="56px" style="border-radius: 12px;" class="q-mb-md" />
          <q-skeleton type="text" width="70%" />
          <q-skeleton type="text" width="40%" class="q-mt-xs" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Erro -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar os cursos.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="load" />
      </q-card-section>
    </q-card>

    <!-- Nenhum resultado -->
    <div v-else-if="filtered.length === 0" class="text-center q-py-xl">
      <q-icon name="search_off" size="48px" style="color: var(--od-text-5);" />
      <p style="margin-top: 12px; color: var(--od-text-3);">
        {{ courses.length === 0 ? 'Nenhum curso publicado ainda.' : 'Nenhum curso encontrado para essa busca.' }}
      </p>
      <q-btn v-if="search" flat no-caps label="Limpar busca" style="color: var(--od-accent);" @click="search = ''" />
    </div>

    <!-- Grid de cursos -->
    <div v-else class="row q-gutter-md">
      <q-card
        v-for="course in filtered"
        :key="course.id"
        flat bordered
        class="od-card od-course-card"
        style="width: 280px; cursor: pointer; transition: box-shadow 0.15s;"
      >
        <q-card-section style="padding: 16px;">

          <!-- Avatar do professor -->
          <div class="row items-center q-mb-md" style="gap: 10px;">
            <q-avatar size="40px" style="flex-shrink: 0;">
              <img v-if="course.teacher.photo" :src="course.teacher.photo" :alt="course.teacher.name" />
              <div
                v-else
                class="row items-center justify-center full-width full-height"
                style="background: var(--od-accent); color: #fff; font-size: 16px; font-weight: 600; border-radius: 50%;"
              >
                {{ initials(course.teacher.name || course.teacher.email) }}
              </div>
            </q-avatar>
            <div style="min-width: 0;">
              <div class="ellipsis" style="font-size: 13px; font-weight: 500; color: var(--od-text-2);">
                {{ course.teacher.name || course.teacher.email }}
              </div>
              <div style="font-size: 11px; color: var(--od-text-5);">Professor</div>
            </div>
          </div>

          <!-- Título -->
          <div class="od-display ellipsis-2-lines" style="font-size: 15px; font-weight: 600; color: var(--od-text-1); line-height: 1.35; margin-bottom: 10px;">
            {{ course.title }}
          </div>

          <!-- Rodapé -->
          <div class="row items-center justify-between">
            <q-badge
              color="positive"
              label="Publicado"
              style="font-size: 10.5px; border-radius: 4px;"
            />
            <q-icon name="arrow_forward" size="16px" style="color: var(--od-text-5);" />
          </div>

        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { courseService } from 'src/services/course'

const courses = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref('')

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return courses.value
  return courses.value.filter(c =>
    c.title.toLowerCase().includes(q) ||
    (c.teacher.name || '').toLowerCase().includes(q) ||
    c.teacher.email.toLowerCase().includes(q)
  )
})

async function load () {
  loading.value = true
  error.value = false
  try {
    const resp = await courseService.published()
    courses.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function initials (str) {
  if (!str) return '?'
  return str.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

onMounted(load)
</script>

<style scoped>
.od-course-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
