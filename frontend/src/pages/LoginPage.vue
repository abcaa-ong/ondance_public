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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { authService } from 'src/services/auth'

const router = useRouter()
const $q = useQuasar()
const formRef = ref(null)

const form = ref({ email: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    await authService.login({
      email: form.value.email,
      password: form.value.password
    })

    $q.notify({
      type: 'positive',
      message: 'Login bem-sucedido! Redirecionando...'
    })

    router.push('/courses/initial')
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Erro ao efetuar login.'
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
  background: linear-gradient(180deg, #f5fbf9 0%, #ffffff 100%);
}

.login-card-wrapper {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: white;
  border: 1px solid rgba(77, 184, 168, 0.16);
  border-radius: 28px;
  box-shadow: 0 22px 50px rgba(42, 81, 68, 0.08);
  padding: 28px;
}

.login-card::before {
  content: '';
  display: block;
  width: 70px;
  height: 5px;
  background: #4db8a8;
  border-radius: 12px;
  margin-bottom: 22px;
}

.login-header {
  margin-bottom: 22px;
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #2d9d8f;
}

.login-subtitle {
  margin: 0;
  color: #63777d;
  font-size: 15px;
}

.login-btn {
  width: 100%;
  background: #4db8a8;
  color: #fff;
  border-radius: 16px;
  padding: 14px 0;
  font-weight: 700;
  box-shadow: 0 10px 20px rgba(77, 184, 168, 0.22);
}

.login-btn:hover {
  background: #3aa08d;
}

.signup-footer {
  margin-top: 18px;
  text-align: center;
  color: #63777d;
  font-size: 13px;
}

.signup-link {
  color: #4db8a8;
  margin-left: 6px;
  text-decoration: none;
  font-weight: 700;
}

.signup-link:hover {
  text-decoration: underline;
}

.login-input {
  --q-color: #4db8a8;
}

:deep(.login-input .q-field__control) {
  background: #f3fbf8;
  border-radius: 16px;
}

:deep(.login-input .q-field__native) {
  color: #253d38;
}

:deep(.login-input .q-field__label) {
  color: #4a7b77;
}

:deep(.login-input .q-field__border) {
  border-color: rgba(77, 184, 168, 0.3) !important;
}
</style>
