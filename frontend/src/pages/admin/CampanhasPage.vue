<template>
  <q-page class="q-pa-lg">
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Campanhas</div>
        <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Gerenciar campanhas de marketing</p>
      </div>
      <q-btn unelevated no-caps label="Nova campanha" icon="add"
        @click="showCreateDialog = true"
        style="background: var(--od-accent); color: #fff; border-radius: 8px;" />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="row q-gutter-md">
      <q-card v-for="n in 3" :key="n" flat bordered class="od-card" style="flex: 1; min-width: 280px;">
        <q-card-section><q-skeleton type="rect" height="80px" /></q-card-section>
      </q-card>
    </div>

    <!-- Empty -->
    <q-card v-else-if="campaigns.length === 0" flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="campaign" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Nenhuma campanha criada ainda.</p>
      </q-card-section>
    </q-card>

    <!-- List -->
    <div v-else class="column q-gutter-md">
      <q-card v-for="c in campaigns" :key="c.id" flat bordered class="od-card">
        <q-card-section style="padding: 16px;">
          <div class="row items-start justify-between" style="gap: 12px;">
            <div style="flex: 1; min-width: 0;">
              <div class="row items-center" style="gap: 8px;">
                <span style="font-size: 15px; font-weight: 600; color: var(--od-text-1);">{{ c.title }}</span>
                <q-badge :label="typeLabel(c.type)" :style="{ background: typeColor(c.type), color: '#fff', fontSize: '10px' }" />
                <q-badge :label="statusLabel(c.status)" :style="{ background: statusColor(c.status), color: '#fff', fontSize: '10px' }" />
              </div>
              <div v-if="c.subject" style="font-size: 13px; color: var(--od-text-3); margin-top: 4px;">Assunto: {{ c.subject }}</div>
              <div v-if="c.course_title" style="font-size: 12px; color: var(--od-text-4); margin-top: 2px;">Curso: {{ c.course_title }}</div>
              <div style="font-size: 11px; color: var(--od-text-5); margin-top: 4px;">
                Criado por {{ c.created_by_name || '—' }} em {{ formatDate(c.created_at) }}
                <span v-if="c.sent_at"> · Enviado em {{ formatDate(c.sent_at) }}</span>
              </div>
            </div>
            <div class="row" style="gap: 4px;">
              <q-btn v-if="c.status === 'draft'" flat no-caps dense label="Enviar"
                icon="send" size="sm" style="color: var(--od-accent);"
                @click="sendCampaign(c)" />
              <q-btn flat no-caps dense icon="delete" size="sm" style="color: var(--od-text-4);"
                @click="deleteCampaign(c)" />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Create dialog -->
    <q-dialog v-model="showCreateDialog">
      <q-card flat bordered class="od-card" style="width: 500px; max-width: 90vw;">
        <q-card-section>
          <div style="font-size: 16px; font-weight: 600; color: var(--od-text-1); margin-bottom: 12px;">Nova campanha</div>
          <div class="column q-gutter-sm">
            <q-input v-model="newCampaign.title" outlined dense label="Título *" :rules="[val => !!val]" />
            <q-select v-model="newCampaign.type" outlined dense :options="typeOptions" emit-value map-options label="Tipo *" />
            <q-input v-model="newCampaign.subject" outlined dense label="Assunto do email" />
            <q-input v-model="newCampaign.body" outlined dense type="textarea" label="Corpo da mensagem" rows="3" />
            <q-select v-model="newCampaign.course" outlined dense :options="courseOptions" emit-value map-options clearable label="Curso relacionado" />
          </div>
        </q-card-section>
        <q-card-actions align="right" style="padding: 8px 16px 16px;">
          <q-btn flat no-caps label="Cancelar" v-close-popup style="color: var(--od-text-4);" />
          <q-btn unelevated no-caps label="Criar" :loading="creating" @click="createCampaign"
            style="background: var(--od-accent); color: #fff; border-radius: 8px;" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const campaigns = ref([])
const loading = ref(true)
const showCreateDialog = ref(false)
const creating = ref(false)
const courses = ref([])

const newCampaign = ref({ title: '', type: 'email', subject: '', body: '', course: null })

const typeOptions = [
  { label: 'Email Marketing', value: 'email' },
  { label: 'Promoção de Curso', value: 'promo' },
  { label: 'Novo Conteúdo', value: 'content' },
]

const typeLabel = (t) => ({ email: 'Email', promo: 'Promoção', content: 'Conteúdo' }[t] || t)
const typeColor = (t) => ({ email: '#7F77DD', promo: 'var(--od-accent)', content: '#1D9E75' }[t] || 'grey')
const statusLabel = (s) => ({ draft: 'Rascunho', scheduled: 'Agendada', sent: 'Enviada' }[s] || s)
const statusColor = (s) => ({ draft: 'grey', scheduled: '#E97B3C', sent: '#1D9E75' }[s] || 'grey')

const courseOptions = courses.value.map(c => ({ label: c.title, value: c.id }))

async function load() {
  loading.value = true
  try {
    const [campResp, courseResp] = await Promise.all([
      api.get('/admin/campaigns/'),
      api.get('/courses/'),
    ])
    campaigns.value = campResp.data.results ?? campResp.data
    courses.value = (courseResp.data.results ?? courseResp.data).map(c => ({ label: c.title, value: c.id }))
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

async function createCampaign() {
  if (!newCampaign.value.title) return
  creating.value = true
  try {
    const resp = await api.post('/admin/campaigns/', newCampaign.value)
    campaigns.value.unshift(resp.data)
    showCreateDialog.value = false
    newCampaign.value = { title: '', type: 'email', subject: '', body: '', course: null }
    $q.notify({ type: 'positive', message: 'Campanha criada!' })
  } catch (e) {
    const msg = e.response?.data ? Object.values(e.response.data).flat().join(' ') : 'Erro ao criar campanha.'
    $q.notify({ type: 'negative', message: msg })
  } finally {
    creating.value = false
  }
}

async function sendCampaign(c) {
  try {
    const resp = await api.post(`/admin/campaigns/${c.id}/send/`)
    Object.assign(c, resp.data)
    $q.notify({ type: 'positive', message: 'Campanha enviada!' })
  } catch (e) {
    $q.notify({ type: 'negative', message: e.response?.data?.message || 'Erro ao enviar.' })
  }
}

async function deleteCampaign(c) {
  try {
    await api.delete(`/admin/campaigns/${c.id}/`)
    campaigns.value = campaigns.value.filter(x => x.id !== c.id)
    $q.notify({ type: 'positive', message: 'Campanha removida.' })
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao remover.' })
  }
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(load)
</script>
