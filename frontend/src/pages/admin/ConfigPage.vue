<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Configurações</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Configurações globais da plataforma</p>
    </div>

    <div v-if="loading" class="column q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card">
        <q-card-section><q-skeleton type="rect" height="60px" /></q-card-section>
      </q-card>
    </div>

    <template v-else>
      <!-- Geral -->
      <q-card flat bordered class="od-card q-mb-md">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Geral</div>
          <div class="column q-gutter-sm">
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Nome da plataforma</span>
              <span style="font-size: 14px; font-weight: 500; color: var(--od-text-1);">{{ config.platform_name }}</span>
            </div>
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Descrição</span>
              <span style="font-size: 14px; font-weight: 500; color: var(--od-text-1);">{{ config.platform_description }}</span>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Paginação -->
      <q-card flat bordered class="od-card q-mb-md">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Paginação</div>
          <div class="column q-gutter-sm">
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Itens por página (padrão)</span>
              <span style="font-size: 14px; font-weight: 500; color: var(--od-text-1);">{{ config.default_page_size }}</span>
            </div>
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Máximo por página</span>
              <span style="font-size: 14px; font-weight: 500; color: var(--od-text-1);">{{ config.max_page_size }}</span>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Segurança -->
      <q-card flat bordered class="od-card">
        <q-card-section>
          <div class="od-card-title od-display q-mb-md">Segurança</div>
          <div class="column q-gutter-sm">
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Modo debug</span>
              <q-badge :label="config.debug ? 'Ativado' : 'Desativado'"
                :style="{ background: config.debug ? '#E97B3C' : '#1D9E75', color: '#fff', fontSize: '10px' }" />
            </div>
            <div class="row items-center justify-between">
              <span style="font-size: 13px; color: var(--od-text-3);">Hosts permitidos</span>
              <span style="font-size: 14px; font-weight: 500; color: var(--od-text-1);">{{ config.allowed_hosts?.join(', ') }}</span>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </template>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const config = ref({})
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const resp = await api.get('/admin/config/')
    config.value = resp.data
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
