<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Categorias</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Distribuição de cursos por estilo de dança</p>
    </div>

    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 6" :key="n" flat bordered class="od-card" style="flex: 1; min-width: 200px;">
        <q-card-section><q-skeleton type="rect" height="60px" /></q-card-section>
      </q-card>
    </div>

    <template v-else>
      <div class="row q-gutter-sm q-mb-lg">
        <q-card v-for="s in styles" :key="s.value" flat bordered class="od-card"
          style="flex: 1; min-width: 180px;">
          <q-card-section style="padding: 16px;">
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">{{ s.label }}</span>
              <span style="font-size: 20px; font-weight: 700; color: var(--od-text-1);">{{ s.count }}</span>
            </div>
            <q-linear-progress :value="total > 0 ? s.count / total : 0" rounded size="6px"
              color="var(--od-accent)" class="q-mt-sm" />
          </q-card-section>
        </q-card>
      </div>

      <q-card flat bordered class="od-card">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Resumo</div>
          <div class="row items-center justify-between">
            <span style="font-size: 13px; color: var(--od-text-3);">Total de cursos publicados</span>
            <span style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">{{ total }}</span>
          </div>
        </q-card-section>
      </q-card>
    </template>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const styles = ref([])
const total = ref(0)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const resp = await api.get('/admin/dance-styles/')
    styles.value = resp.data.styles
    total.value = resp.data.total
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
