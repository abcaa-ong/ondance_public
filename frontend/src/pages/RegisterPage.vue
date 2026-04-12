<template>
  <q-page class="register-page">

    <!-- Form State -->
    <div v-if="!showConfirmation" class="register-container">
      <div class="register-header">
        <div class="brand-title">OnDance</div>
        <p class="brand-subtitle">Crie sua conta para começar</p>
      </div>

      <div class="register-benefits">
        <div class="benefit-item">
          <span class="benefit-icon">🎬</span>
          <span>Acesso a mais de 30 cursos em vídeo</span>
        </div>
        <div class="benefit-item">
          <span class="benefit-icon">🎓</span>
          <span>Aprenda com os melhores professores do Brasil</span>
        </div>
        <div class="benefit-item">
          <span class="benefit-icon">⚡</span>
          <span>No seu ritmo, de qualquer lugar</span>
        </div>
      </div>

      <q-form @submit.prevent="handleSubmit">

        <q-card flat bordered class="register-card">
          <q-card-section>
            <div class="column q-gutter-md">

              <!-- Role Selector -->
              <div class="role-selector">
                <button
                  type="button"
                  class="role-card"
                  :class="{ 'role-card--active': form.role === 'aluno' }"
                  @click="form.role = 'aluno'"
                >
                  <span class="role-card-icon">🎓</span>
                  <span class="role-card-title">Sou Aluno</span>
                  <span class="role-card-sub">Quero aprender</span>
                </button>
                <button
                  type="button"
                  class="role-card"
                  :class="{ 'role-card--active': form.role === 'professor' }"
                  @click="form.role = 'professor'"
                >
                  <span class="role-card-icon">🎤</span>
                  <span class="role-card-title">Sou Professor</span>
                  <span class="role-card-sub">Quero ensinar</span>
                </button>
              </div>

              <!-- Email Field -->
              <q-input
                class="register-input"
                v-model="form.email"
                filled
                dense
                rounded
                type="email"
                label="Email *"
                placeholder="seu.email@exemplo.com"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Email inválido'
                ]"
              />

              <!-- Password Field -->
              <q-input
                class="register-input"
                v-model="form.password"
                filled
                dense
                rounded
                :type="showPassword ? 'text' : 'password'"
                label="Senha *"
                placeholder="Mínimo 8 caracteres"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => val.length >= 8 || 'Mínimo 8 caracteres'
                ]"
              >
                <template #append>
                  <q-icon
                    :name="showPassword ? 'visibility' : 'visibility_off'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>

            </div>

            <!-- Error Message -->
            <q-banner
              v-if="errorMessage"
              class="bg-negative text-white register-error"
            >
              {{ errorMessage }}
            </q-banner>

            <q-btn
              unelevated
              no-caps
              type="submit"
              label="Criar Conta"
              :loading="loading"
              class="register-btn q-mt-sm"
            />

            <div class="google-divider">
              <span>ou continue com</span>
            </div>

            <div id="google-register-btn" class="google-btn-wrapper" />

            <div class="text-center register-login-text">
              Já tem uma conta?
              <router-link to="/login" class="register-login-link">Faça login</router-link>
            </div>

          </q-card-section>
        </q-card>

      </q-form>
    </div>

    <!-- Confirmation State -->
    <div v-else style="max-width: 480px; margin: 0 auto; text-align: center;">
      <q-card flat bordered class="od-card" style="background: var(--od-bg-surface); border-color: var(--od-border);">
        <q-card-section class="q-pa-lg">
          <!-- Icon -->
          <div style="font-size: 64px; margin-bottom: 16px;">
            ✉️
          </div>

          <!-- Title -->
          <div class="od-display" style="font-size: 24px; color: var(--od-text-1); margin-bottom: 8px;">
            Verifique seu email
          </div>

          <!-- Description -->
          <p style="color: var(--od-text-2); margin: 0 0 16px 0; font-size: 14px; line-height: 1.5;">
            Enviamos um link de confirmação para:
          </p>

          <!-- Email Display -->
          <div
            style="
              background: var(--od-bg-subtle);
              padding: 12px;
              border-radius: 8px;
              margin-bottom: 24px;
              color: var(--od-text-1);
              font-weight: 500;
            "
          >
            {{ form.email }}
          </div>

          <!-- Instructions -->
          <div style="text-align: left; background: var(--od-bg-subtle); padding: 16px; border-radius: 8px; margin-bottom: 24px;">
            <p style="color: var(--od-text-2); font-size: 13px; margin: 0 0 8px 0;">
              <strong>Próximos passos:</strong>
            </p>
            <ol style="color: var(--od-text-2); font-size: 13px; margin: 0; padding-left: 20px;">
              <li>Abra seu email</li>
              <li>Clique no link de confirmação</li>
              <li>Você será redirecionado para completar seu cadastro</li>
            </ol>
          </div>

          <!-- Back to Login -->
          <router-link
            to="/login"
            class="register-login-link"
          >
            Voltar para login
          </router-link>

        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { authService } from 'src/services/auth'
import { useGoogleAuth } from 'src/composables/useGoogleAuth'

const router = useRouter()
const $q = useQuasar()
const { initGoogleButton } = useGoogleAuth()

onMounted(() => {
  initGoogleButton('google-register-btn', {
    onSuccess: () => {
      $q.notify({ type: 'positive', message: 'Login com Google realizado!' })
      router.push('/courses/initial')
    },
    onError: () => {
      $q.notify({ type: 'negative', message: 'Erro ao autenticar com Google.' })
    },
  })
})

const form = ref({
  role: 'aluno',
  email: '',
  password: '',
})

const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const showConfirmation = ref(false)

function extractApiError(error, fallback = 'Erro inesperado. Tente novamente.') {
  const data = error.response?.data
  if (!data) return fallback
  const messages = [...new Set(Object.values(data).flat())]
  return messages.length ? messages.join(' ') : fallback
}

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''

  try {
    await authService.register({
      email: form.value.email,
      password: form.value.password,
      role: form.value.role,
    })

    showConfirmation.value = true
  } catch (error) {
    errorMessage.value = extractApiError(error, 'Erro ao criar conta. Tente novamente.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: var(--od-bg-page);
}

.register-container {
  width: 100%;
  max-width: 520px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.brand-title {
  font-size: 34px;
  font-weight: 700;
  color: var(--od-accent);
  margin-bottom: 8px;
}

.brand-subtitle {
  color: var(--od-text-3);
  font-size: 15px;
  margin: 0;
}

.register-benefits {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--od-text-2);
}

.benefit-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.register-card {
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 28px;
  box-shadow: 0 24px 52px rgba(42, 81, 68, 0.06);
}

.register-card::before {
  content: '';
  display: block;
  width: 64px;
  height: 5px;
  background: var(--od-accent);
  border-radius: 12px;
  margin-bottom: 18px;
}

.google-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0 14px;
  color: var(--od-text-3);
  font-size: 12px;
}

.google-divider::before,
.google-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--od-border);
}

.google-btn-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 4px;
}

.register-btn {
  background: var(--od-accent);
  color: white;
  border-radius: 14px;
  padding: 14px 0;
  font-weight: 700;
}


.register-login-text {
  color: var(--od-text-3);
  font-size: 13px;
}

.register-login-link {
  color: var(--od-accent);
  font-weight: 700;
  text-decoration: none;
}

.register-login-link:hover {
  text-decoration: underline;
}

.role-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 10px;
  border-radius: 14px;
  border: 2px solid var(--od-border);
  background: var(--od-bg-subtle);
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  text-align: center;
}

.role-card:hover {
  border-color: var(--od-accent);
  background: var(--od-bg-page);
}

.role-card--active {
  border-color: var(--od-accent) !important;
  background: var(--od-bg-page) !important;
}

.role-card-icon {
  font-size: 24px;
  line-height: 1;
}

.role-card-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--od-text-1);
}

.role-card-sub {
  font-size: 11px;
  color: var(--od-text-3);
}

.register-input {
  --q-color: var(--od-accent);
}

:deep(.register-input .q-field__control) {
  background: var(--od-bg-subtle);
  border-radius: 16px;
}

:deep(.register-input .q-field__label) {
  color: var(--od-text-3);
}

:deep(.register-input .q-field__native) {
  color: var(--od-text-1);
}

.register-select-popup {
  background: var(--od-bg-surface) !important;
  border: 1px solid var(--od-border) !important;
  box-shadow: 0 20px 40px rgba(42, 81, 68, 0.08) !important;
  border-radius: 18px !important;
}

.register-select-popup :deep(.q-item) {
  color: var(--od-text-1);
}

.register-select-popup :deep(.q-item:hover) {
  background: var(--od-bg-hover) !important;
}

.register-error {
  border-radius: 12px;
}
</style>
