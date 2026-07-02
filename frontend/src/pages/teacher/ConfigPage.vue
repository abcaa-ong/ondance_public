<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Configurações</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Preferências da conta de professor</p>
    </div>

    <!-- Profile -->
    <q-card flat bordered class="od-card q-mb-md">
      <q-card-section>
        <div class="od-card-title od-display q-mb-md">Perfil</div>
        <div class="column q-gutter-sm">
          <q-input v-model="profile.name" outlined dense label="Nome" />
          <q-input v-model="profile.celular" outlined dense label="Celular" mask="(##) #####-####" />
          <q-input v-model="profile.telephone" outlined dense label="Telefone" mask="(##) ####-####" />
          <q-input v-model="profile.birthday" outlined dense label="Data de nascimento" mask="##/##/####" />
          <q-btn unelevated no-caps label="Salvar perfil" :loading="savingProfile" @click="saveProfile"
            style="background: var(--od-accent); color: #fff; border-radius: 8px; align-self: flex-start;" />
        </div>
      </q-card-section>
    </q-card>

    <!-- Password -->
    <q-card flat bordered class="od-card q-mb-md">
      <q-card-section>
        <div class="od-card-title od-display q-mb-md">Alterar senha</div>
        <div class="column q-gutter-sm">
          <q-input v-model="password.old_password" outlined dense type="password" label="Senha atual" />
          <q-input v-model="password.new_password" outlined dense type="password" label="Nova senha" />
          <q-input v-model="password.new_password2" outlined dense type="password" label="Confirmar nova senha" />
          <q-btn unelevated no-caps label="Alterar senha" :loading="savingPassword" @click="changePassword"
            style="background: var(--od-accent); color: #fff; border-radius: 8px; align-self: flex-start;" />
        </div>
      </q-card-section>
    </q-card>

    <!-- Notifications -->
    <q-card flat bordered class="od-card">
      <q-card-section>
        <div class="od-card-title od-display q-mb-md">Notificações</div>
        <div class="column q-gutter-sm">
          <q-toggle v-model="notifyEmail" label="Receber notificações por email" style="color: var(--od-text-2);" />
          <q-toggle v-model="notifyPush" label="Receber push notifications" style="color: var(--od-text-2);" />
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const profile = ref({ name: '', celular: '', telephone: '', birthday: '' })
const password = ref({ old_password: '', new_password: '', new_password2: '' })
const savingProfile = ref(false)
const savingPassword = ref(false)
const notifyEmail = ref(true)
const notifyPush = ref(true)

async function loadProfile() {
  try {
    const resp = await api.get('/profile/')
    const p = resp.data
    profile.value = {
      name: p.name || '',
      celular: p.celular || '',
      telephone: p.telephone || '',
      birthday: p.birthday || '',
    }
  } catch {
    // silently fail
  }
}

async function saveProfile() {
  savingProfile.value = true
  try {
    await api.patch('/profile/', profile.value)
    $q.notify({ type: 'positive', message: 'Perfil atualizado!' })
  } catch (e) {
    const msg = e.response?.data ? Object.values(e.response.data).flat().join(' ') : 'Erro ao salvar.'
    $q.notify({ type: 'negative', message: msg })
  } finally {
    savingProfile.value = false
  }
}

async function changePassword() {
  if (password.value.new_password !== password.value.new_password2) {
    $q.notify({ type: 'warning', message: 'As senhas não conferem.' })
    return
  }
  savingPassword.value = true
  try {
    await api.post('/password/change/', {
      old_password: password.value.old_password,
      new_password: password.value.new_password,
    })
    $q.notify({ type: 'positive', message: 'Senha alterada!' })
    password.value = { old_password: '', new_password: '', new_password2: '' }
  } catch (e) {
    const msg = e.response?.data?.message || e.response?.data?.detail || 'Erro ao alterar senha.'
    $q.notify({ type: 'negative', message: msg })
  } finally {
    savingPassword.value = false
  }
}

onMounted(loadProfile)
</script>
