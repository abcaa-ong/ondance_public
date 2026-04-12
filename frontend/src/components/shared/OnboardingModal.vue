<template>
  <q-dialog v-model="show" persistent>
    <q-card style="width: 460px; max-width: 92vw; border-radius: 16px; padding: 8px; background: var(--od-bg-surface);">

      <q-card-section>
        <div style="font-size: 18px; font-weight: 600; color: var(--od-text-1); margin-bottom: 4px;">
          Complete seu perfil
        </div>
        <div style="font-size: 13px; color: var(--od-text-3);">
          Adicione seu celular para personalizarmos sua experiência.
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none q-gutter-sm">
        <!-- Role selector -->
        <div class="ob-role-row">
          <button
            type="button"
            class="ob-role-btn"
            :class="{ 'ob-role-btn--active': form.role === 'aluno' }"
            @click="form.role = 'aluno'"
          >
            🎓 Sou Aluno
          </button>
          <button
            type="button"
            class="ob-role-btn"
            :class="{ 'ob-role-btn--active': form.role === 'professor' }"
            @click="form.role = 'professor'"
          >
            🎤 Sou Professor
          </button>
        </div>

        <q-input
          v-model="form.name"
          label="Nome completo"
          outlined dense
          :style="inputStyle"
        />
        <q-input
          v-model="form.celular"
          label="Celular"
          outlined dense
          mask="(##) #####-####"
          unmasked-value
          :style="inputStyle"
        />
      </q-card-section>

      <div v-if="errorMsg" style="padding: 0 16px 8px; font-size: 12px; color: #e53935;">
        {{ errorMsg }}
      </div>

      <q-card-actions align="right" class="q-px-md q-pb-md">
        <q-btn
          flat no-caps
          label="Preencher depois"
          style="color: var(--od-text-3); font-size: 13px;"
          @click="dismiss"
        />
        <q-btn
          unelevated no-caps
          label="Salvar"
          :loading="loading"
          style="background: var(--od-accent); color: #fff; border-radius: 8px; font-size: 13px;"
          @click="save"
        />
      </q-card-actions>

    </q-card>
  </q-dialog>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { profileService } from 'src/services/profile'

const emit = defineEmits(['close', 'saved'])

const show = ref(true)
const loading = ref(false)
const errorMsg = ref('')
const form = ref({ role: 'aluno', name: '', celular: '' })

const inputStyle = 'border-radius: 8px;'

onMounted(async () => {
  try {
    const { data } = await profileService.get()
    form.value.name = data.name || ''
    form.value.celular = data.celular || ''
  } catch {
    // silencia — campos ficam vazios
  }
})

async function save() {
  if (!form.value.celular) {
    errorMsg.value = 'Informe o celular para continuar.'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await profileService.update({
      name: form.value.name,
      celular: form.value.celular,
      role: form.value.role,
    })
    localStorage.setItem('profile_complete', 'true')
    show.value = false
    emit('saved')
  } catch {
    errorMsg.value = 'Erro ao salvar. Tente novamente.'
  } finally {
    loading.value = false
  }
}

function dismiss() {
  localStorage.setItem('onboarding_dismissed', 'true')
  show.value = false
  emit('close')
}
</script>

<style scoped>
.ob-role-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 4px;
}

.ob-role-btn {
  padding: 10px 8px;
  border-radius: 10px;
  border: 2px solid var(--od-border);
  background: var(--od-bg-subtle);
  color: var(--od-text-1);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}

.ob-role-btn:hover {
  border-color: var(--od-accent);
}

.ob-role-btn--active {
  border-color: var(--od-accent) !important;
  background: var(--od-bg-page) !important;
}
</style>
