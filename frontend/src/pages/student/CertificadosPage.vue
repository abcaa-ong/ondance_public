<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Certificados</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Certificados emitidos ao concluir cursos</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 2" :key="n" flat bordered class="od-card" style="width: 320px;">
        <q-card-section>
          <q-skeleton type="rect" height="60px" style="border-radius: 8px;" class="q-mb-sm" />
          <q-skeleton type="text" width="60%" />
          <q-skeleton type="text" width="40%" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Error -->
    <q-card v-else-if="error" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="error_outline" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Não foi possível carregar seus certificados.</p>
        <q-btn flat no-caps label="Tentar novamente" style="color: var(--od-accent);" @click="load" />
      </q-card-section>
    </q-card>

    <!-- Empty -->
    <q-card v-else-if="certificates.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="workspace_premium" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Seus certificados aparecerão aqui após concluir um curso</p>
      </q-card-section>
    </q-card>

    <!-- Certificate list -->
    <div v-else class="row q-gutter-md">
      <q-card
        v-for="cert in certificates"
        :key="cert.id"
        flat bordered
        class="od-card od-course-card"
        style="width: 320px; transition: box-shadow 0.15s;"
      >
        <q-card-section style="padding: 20px;">
          <div class="row items-center q-mb-md" style="gap: 12px;">
            <q-icon name="workspace_premium" size="32px" style="color: var(--od-accent); flex-shrink: 0;" />
            <div>
              <div class="od-display ellipsis-2-lines" style="font-size: 15px; font-weight: 600; color: var(--od-text-1); line-height: 1.35;">
                {{ cert.course_title }}
              </div>
              <div style="font-size: 12px; color: var(--od-text-4); margin-top: 2px;">
                {{ cert.course_level }} · {{ cert.course_workload }}h
              </div>
            </div>
          </div>

          <div style="font-size: 12px; color: var(--od-text-3); margin-bottom: 4px;">
            Professor: {{ cert.teacher_name }}
          </div>
          <div style="font-size: 12px; color: var(--od-text-4); margin-bottom: 12px;">
            Emitido em {{ formatDate(cert.issue_date) }}
          </div>

          <div class="row items-center justify-between">
            <span style="font-size: 11px; color: var(--od-text-5); font-family: monospace;">{{ cert.code }}</span>
            <q-btn
              v-if="cert.file"
              flat no-caps dense
              icon="download"
              label="Baixar"
              :href="cert.file"
              target="_blank"
              style="color: var(--od-accent); font-size: 12px;"
            />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { certificateService } from 'src/services/certificate'

const certificates = ref([])
const loading = ref(true)
const error = ref(false)

async function load() {
  loading.value = true
  error.value = false
  try {
    const resp = await certificateService.list()
    certificates.value = resp.data.results ?? resp.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR')
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
