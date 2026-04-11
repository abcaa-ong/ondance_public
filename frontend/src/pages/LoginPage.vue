<template>
  <q-page class="login-page q-pa-lg">
    <div class="login-card-wrapper">
      <q-card flat bordered class="login-card">
        <q-card-section>
          <div class="login-header">
            <div class="login-title">Login</div>
            <p class="login-subtitle">Entre com seu email e senha para continuar.</p>
          </div>

          <q-form ref="formRef" @submit.prevent="handleLogin">
            <div class="q-gutter-md">
              <q-input
                class="login-input"
                v-model="form.email"
                filled
                dense
                rounded
                label="Email"
                type="email"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Email inválido'
                ]"
              />

              <q-input
                class="login-input"
                v-model="form.password"
                filled
                dense
                rounded
                :type="showPassword ? 'text' : 'password'"
                label="Senha"
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

              <q-banner v-if="errorMessage" class="bg-negative text-white q-pa-sm">
                {{ errorMessage }}
              </q-banner>

              <q-btn
                unelevated
                no-caps
                type="submit"
                label="Entrar"
                class="login-btn"
                :loading="loading"
              />
            </div>
          </q-form>

          <div class="google-divider">
            <span>ou continue com</span>
          </div>

          <div id="google-login-btn" class="google-btn-wrapper" />

          <div class="signup-footer">
            <span>Não tem uma conta?</span>
            <router-link to="/register" class="signup-link">Cadastre-se</router-link>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuth } from 'src/composables/useAuth'
import { useGoogleAuth } from 'src/composables/useGoogleAuth'

function extractApiError(error, fallback = 'Erro inesperado. Tente novamente.') {
  const data = error.response?.data
  if (!data) return fallback
  const messages = [...new Set(Object.values(data).flat())]
  return messages.length ? messages.join(' ') : fallback
}

const router = useRouter()
const $q = useQuasar()
const { login } = useAuth()
const { initGoogleButton } = useGoogleAuth()
const formRef = ref(null)

onMounted(() => {
  initGoogleButton('google-login-btn', {
    onSuccess: () => {
      $q.notify({ type: 'positive', message: 'Login com Google realizado!' })
      router.push('/courses/initial')
    },
    onError: () => {
      $q.notify({ type: 'negative', message: 'Erro ao autenticar com Google.' })
    },
  })
})

const form = ref({ email: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    await login({
      email: form.value.email,
      password: form.value.password
    })

    $q.notify({
      type: 'positive',
      message: 'Login bem-sucedido! Redirecionando...'
    })

    router.push('/courses/initial')
  } catch (error) {
    errorMessage.value = extractApiError(error, 'Erro ao efetuar login.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--od-bg-page);
}

.login-card-wrapper {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 24px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
  padding: 26px;
}

.login-card::before {
  content: '';
  display: block;
  width: 64px;
  height: 5px;
  background: var(--od-accent);
  border-radius: 12px;
  margin-bottom: 18px;
}

.login-header {
  margin-bottom: 22px;
}

.login-title {
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--od-accent);
}

.login-subtitle {
  margin: 0;
  color: var(--od-text-3);
  font-size: 14px;
}

.login-btn {
  width: 100%;
  background: var(--od-accent);
  color: #fff;
  border-radius: 16px;
  padding: 14px 0;
  font-weight: 700;
  box-shadow: 0 10px 20px rgba(123, 94, 167, 0.22);
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

.signup-footer {
  margin-top: 18px;
  text-align: center;
  color: var(--od-text-3);
  font-size: 13px;
}

.signup-link {
  color: var(--od-accent);
  margin-left: 6px;
  text-decoration: none;
  font-weight: 700;
}

.signup-link:hover {
  text-decoration: underline;
}

.login-input {
  --q-color: var(--od-accent);
}

:deep(.login-input .q-field__control) {
  background: var(--od-bg-subtle);
  border-radius: 16px;
}

:deep(.login-input .q-field__native) {
  color: var(--od-text-1);
}

:deep(.login-input .q-field__label) {
  color: var(--od-text-3);
}

:deep(.login-input .q-field__border) {
  border-color: rgba(123, 94, 167, 0.3) !important;
}
</style>
