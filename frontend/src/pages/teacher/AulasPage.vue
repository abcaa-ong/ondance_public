<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Gerenciar Aulas</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Adicione e ordene módulos e aulas</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="column q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card">
        <q-card-section><q-skeleton type="rect" height="80px" /></q-card-section>
      </q-card>
    </div>

    <!-- Empty -->
    <q-card v-else-if="courses.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="video_settings" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Nenhum curso encontrado. Crie um curso primeiro.</p>
        <q-btn flat no-caps label="Criar curso" icon="add" to="/teacher/cursos"
          style="color: var(--od-accent); margin-top: 8px;" />
      </q-card-section>
    </q-card>

    <!-- Course list -->
    <div v-else class="column q-gutter-md">
      <q-card v-for="c in courses" :key="c.id" flat bordered class="od-card">
        <q-card-section style="padding: 16px;">
          <div class="row items-center justify-between" style="gap: 12px;">
            <div style="flex: 1; min-width: 0;">
              <div style="font-size: 15px; font-weight: 600; color: var(--od-text-1);">{{ c.title }}</div>
              <div style="font-size: 12px; color: var(--od-text-4); margin-top: 2px;">
                {{ c.modules_count || 0 }} módulos · {{ c.lessons_count || 0 }} aulas
                <q-badge :label="c.is_published ? 'Publicado' : 'Rascunho'"
                  :style="{ background: c.is_published ? '#1D9E75' : '#E97B3C', color: '#fff', fontSize: '10px', marginLeft: '6px' }" />
              </div>
            </div>
            <q-btn flat no-caps dense icon="edit" label="Editar" size="sm"
              :to="`/teacher/cursos/${c.id}`"
              style="color: var(--od-accent);" />
          </div>

          <!-- Modules accordion -->
          <q-expansion-item v-if="c.modules?.length" header-style="padding: 0;"
            class="q-mt-sm" dense toggle-style="color: var(--od-text-4);">
            <template v-slot:header>
              <span style="font-size: 12px; color: var(--od-text-3);">Módulos e aulas</span>
            </template>
            <div class="column" style="padding-left: 16px;">
              <div v-for="m in c.modules" :key="m.id" class="q-py-xs">
                <div style="font-size: 12px; font-weight: 600; color: var(--od-text-2);">{{ m.title }}</div>
                <div v-for="l in m.lessons" :key="l.id"
                  style="font-size: 11px; color: var(--od-text-4); padding-left: 12px;">
                  {{ l.title }}
                </div>
                <div v-if="!m.lessons?.length"
                  style="font-size: 11px; color: var(--od-text-5); padding-left: 12px; font-style: italic;">
                  Nenhuma aula
                </div>
              </div>
            </div>
          </q-expansion-item>
          <div v-else style="font-size: 12px; color: var(--od-text-5); margin-top: 8px; font-style: italic;">
            Nenhum módulo adicionado
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const courses = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const resp = await api.get('/courses/mine/')
    const list = resp.data.results ?? resp.data ?? []
    // Load modules for each course
    const enriched = await Promise.all(list.map(async (c) => {
      try {
        const detail = await api.get(`/courses/${c.id}/`)
        return { ...c, modules: detail.data.modules || [] }
      } catch {
        return { ...c, modules: [] }
      }
    }))
    courses.value = enriched
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
