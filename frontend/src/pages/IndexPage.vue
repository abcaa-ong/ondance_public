<template>
  <q-page class="index-page">
    <!-- Two Column Layout -->
    <div class="row no-wrap full-height">
      
      <!-- Left Column - Welcome/Login Section -->
      <div class="left-column col">
        <div class="welcome-section">
          <h1 class="welcome-title">Bem-vindo de volta!</h1>
          <p class="welcome-subtitle">Para se manter conectado, faça login com suas informações pessoais</p>
          
          <router-link to="/login">
            <q-btn
              unelevated
              no-caps
              label="FAZER LOGIN"
              class="welcome-btn"
            />
          </router-link>
        </div>
      </div>

      <!-- Right Column - Signup Section -->
      <div class="right-column col">
        <div class="signup-section">
          <h2 class="signup-title">Criar Conta</h2>
          <p class="signup-subtitle">ou use seu email para se registrar</p>

          <!-- Social Login Icons -->
          <div class="social-icons q-my-md">
            <a href="#" class="social-icon facebook" title="Facebook">
              <q-icon name="fab fa-facebook-f" />
            </a>
            <a href="#" class="social-icon google" title="Google">
              <q-icon name="fab fa-google" />
            </a>
            <a href="#" class="social-icon linkedin" title="LinkedIn">
              <q-icon name="fab fa-linkedin-in" />
            </a>
          </div>

          <!-- Form -->
          <q-form ref="formRef" @submit.prevent="handleQuickSignup">
            <div class="form-group">
              <q-input
                v-model="quickForm.name"
                outlined
                dense
                type="text"
                placeholder="Nome"
                class="form-input"
                :rules="[val => !!val || 'Campo obrigatório']"
              >
                <template #prepend>
                  <q-icon name="person" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <q-input
                v-model="quickForm.email"
                outlined
                dense
                type="email"
                placeholder="Email"
                class="form-input"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Email inválido'
                ]"
              >
                <template #prepend>
                  <q-icon name="mail" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <q-input
                v-model="quickForm.password"
                outlined
                dense
                :type="showQuickPassword ? 'text' : 'password'"
                placeholder="Senha (mín. 8 caracteres)"
                class="form-input"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => val.length >= 8 || 'Mínimo 8 caracteres'
                ]"
              >
                <template #prepend>
                  <q-icon name="lock" />
                </template>
                <template #append>
                  <q-icon
                    :name="showQuickPassword ? 'visibility' : 'visibility_off'"
                    class="cursor-pointer"
                    @click="showQuickPassword = !showQuickPassword"
                  />
                </template>
              </q-input>
            </div>

            <q-btn
              unelevated
              no-caps
              type="submit"
              label="CADASTRAR"
              class="signup-btn"
              :loading="signingUp"
            />
          </q-form>

          <p class="form-footer">
            Prefere preencher tudo?
            <router-link to="/register" class="full-form-link">
              Formulário completo
            </router-link>
          </p>
        </div>
      </div>

    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { authService } from 'src/services/auth'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const formRef = ref(null)

const quickForm = ref({
  name: '',
  email: '',
  password: ''
})

const showQuickPassword = ref(false)
const signingUp = ref(false)

async function handleQuickSignup() {
  signingUp.value = true
  try {
    await authService.register({
      name: quickForm.value.name,
      email: quickForm.value.email,
      password: quickForm.value.password,
      role: 'student'
    })
    
    $q.notify({
      type: 'positive',
      message: 'Cadastro realizado! Verifique seu email.',
      position: 'top'
    })
    
    // Redirect to confirmation or reset form
    setTimeout(() => {
      quickForm.value = { name: '', email: '', password: '' }
    }, 1000)
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Erro ao criar conta',
      position: 'top'
    })
  } finally {
    signingUp.value = false
  }
}
</script>

<style scoped>
.index-page {
  height: 100vh;
  overflow: hidden;
}

.row {
  height: 100%;
}

/* Left Column - Login Section */
.left-column {
  background: linear-gradient(135deg, #4db8a8 0%, #2d9d8f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  min-width: 40%;
}

.welcome-section {
  text-align: center;
  color: white;
}

.welcome-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 15px;
  font-weight: 400;
  margin: 0 0 32px 0;
  opacity: 0.95;
  line-height: 1.6;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.welcome-btn {
  background: white !important;
  color: #4db8a8 !important;
  padding: 12px 32px !important;
  border-radius: 24px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.welcome-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Right Column - Signup Section */
.right-column {
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  overflow-y: auto;
}

.signup-section {
  width: 100%;
  max-width: 380px;
}

.signup-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: #4db8a8;
}

.signup-subtitle {
  font-size: 13px;
  color: #999;
  margin: 0 0 24px 0;
  font-weight: 500;
}

/* Social Icons */
.social-icons {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e8e8e8;
}

.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #d8d8d8;
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 16px;
}

.social-icon:hover {
  border-color: #4db8a8;
  color: #4db8a8;
  transform: translateY(-2px);
}

.social-icon.facebook:hover {
  background: #f0f2f5;
}

.social-icon.google:hover {
  background: #f8f9fa;
}

.social-icon.linkedin:hover {
  background: #f0f6ff;
}

/* Form */
.form-group {
  margin-bottom: 12px;
}

.form-input {
  font-size: 13px;
  background: #f8f9fa;
}

:deep(.form-input .q-field__control) {
  padding: 8px 12px !important;
}

:deep(.form-input .q-icon) {
  color: #999;
}

.signup-btn {
  width: 100% !important;
  background: #4db8a8 !important;
  color: white !important;
  padding: 12px !important;
  border-radius: 24px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.5px;
  margin-top: 16px;
  transition: all 0.3s ease;
}

.signup-btn:hover {
  background: #3da598 !important;
  transform: translateY(-2px);
}

.form-footer {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e8e8e8;
}

.full-form-link {
  color: #4db8a8;
  text-decoration: none;
  font-weight: 600;
}

.full-form-link:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .left-column,
  .right-column {
    min-width: 100%;
    padding: 30px 20px;
  }

  .row {
    flex-direction: column;
  }

  .welcome-title {
    font-size: 28px;
  }

  .signup-title {
    font-size: 24px;
  }
}

/* Form icon colors */
:deep(.form-input.q-focused .q-icon) {
  color: #4db8a8;
}
</style>

