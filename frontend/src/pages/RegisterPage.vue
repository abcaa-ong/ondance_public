<template>
  <q-page class="register-page">

    <!-- Form State -->
    <div v-if="!showConfirmation" class="register-container">
      <div class="register-header">
        <div class="brand-title">On Dance</div>
        <p class="brand-subtitle">Crie sua conta para começar</p>
      </div>

      <q-form ref="formRef" @submit.prevent="handleSubmit">

        <q-card flat bordered class="register-card">
          <q-card-section>
            <div class="column q-gutter-md">

              <!-- Name Field -->
              <q-input
                v-model="form.name"
                outlined
                dense
                label="Nome Completo *"
                placeholder="Digite seu nome"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => val.length >= 3 || 'Mínimo 3 caracteres'
                ]"
              />

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

              <!-- Role Select -->
              <q-select
                class="register-input"
                v-model="form.role"
                filled
                dense
                rounded
                label="Tipo de Usuário *"
                :options="roleOptions"
                option-value="value"
                option-label="label"
                emit-value
                map-options
                :rules="[val => !!val || 'Campo obrigatório']"
                popup-content-class="register-select-popup"
              />

            </div>
          </q-card-section>
        </q-card>

        <!-- Error Message -->
        <q-banner
          v-if="errorMessage"
          class="bg-negative text-white q-mb-md register-error"
        >
          {{ errorMessage }}
        </q-banner>

        <!-- Action Buttons -->
        <div class="column q-gutter-sm">
          <q-btn
            unelevated
            no-caps
            type="submit"
            label="Criar Conta"
            :loading="loading"
            class="register-btn"
          />
          <div class="text-center register-login-text">
            <p>
              Já tem uma conta?
              <router-link
                to="/login"
                class="register-login-link"
              >
                Faça login
              </router-link>
            </p>
          </div>
        </div>

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
import { ref } from 'vue'
import { authService } from 'src/services/auth'

const formRef = ref(null)

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'student'
})

const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const showConfirmation = ref(false)

const roleOptions = [
  { label: 'Estudante', value: 'student' },
  { label: 'Professor', value: 'teacher' }
]

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''

  try {
    await authService.register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role
    })

    // Show confirmation screen
    showConfirmation.value = true
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Erro ao criar conta. Tente novamente.'
    console.error('Registration error:', error)
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
  background: linear-gradient(180deg, #f5fbf9 0%, #ffffff 100%);
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
  color: #2d9d8f;
  margin-bottom: 8px;
}

.brand-subtitle {
  color: #63777d;
  font-size: 15px;
  margin: 0;
}

.register-card {
  background: white;
  border: 1px solid rgba(77, 184, 168, 0.16);
  border-radius: 28px;
  box-shadow: 0 24px 52px rgba(42, 81, 68, 0.06);
}

.register-btn {
  background: #4db8a8;
  color: white;
  border-radius: 14px;
  padding: 14px 0;
  font-weight: 700;
}

.register-btn:hover {
  background: #3aa08d;
}

.register-login-text {
  color: #63777d;
  font-size: 13px;
}

.register-login-link {
  color: #4db8a8;
  font-weight: 700;
  text-decoration: none;
}

.register-login-link:hover {
  text-decoration: underline;
}

.register-input {
  --q-color: #4db8a8;
}

:deep(.register-input .q-field__control) {
  background: #f3fbf8;
  border-radius: 16px;
}

:deep(.register-input .q-field__label) {
  color: #4a7b77;
}

:deep(.register-input .q-field__native) {
  color: #253d38;
}

.register-select-popup {
  background: #ffffff !important;
  border: 1px solid rgba(77, 184, 168, 0.18) !important;
  box-shadow: 0 20px 40px rgba(42, 81, 68, 0.08) !important;
  border-radius: 18px !important;
}

.register-select-popup :deep(.q-item) {
  color: #253d38;
}

.register-select-popup :deep(.q-item:hover) {
  background: rgba(77, 184, 168, 0.12) !important;
}

.register-error {
  border-radius: 12px;
}
</style>
