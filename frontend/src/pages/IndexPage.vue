<template>
  <q-page class="landing-page">

    <!-- ── Seção 1: Hero ─────────────────────────────── -->
    <section class="hero-section">
      <div class="section-container hero-container">

        <!-- Texto -->
        <div class="hero-text">
          <p class="hero-eyebrow">Plataforma oficial ABCAA</p>
          <h1 class="hero-headline">
            Aprenda dança com os melhores professores do Brasil
          </h1>
          <p class="hero-sub">
            Cursos em vídeo para todos os níveis — do iniciante ao avançado.
            No seu ritmo, onde quiser.
          </p>
          <div class="hero-actions">
            <q-btn
              unelevated
              no-caps
              label="Começar gratuitamente"
              class="hero-btn-primary"
              @click="scrollToSignup"
            />
            <router-link to="/courses/lista" class="hero-btn-ghost">
              Ver cursos
            </router-link>
          </div>
        </div>

        <!-- Formulário de cadastro -->
        <div id="signup-form" class="signup-card">

          <!-- Estado: confirmação após cadastro -->
          <div v-if="signupDone" class="signup-confirmation">
            <div class="signup-confirm-icon">✉️</div>
            <h2 class="signup-title">Verifique seu email</h2>
            <p class="signup-sub">Enviamos um link de confirmação para:</p>
            <div class="signup-confirm-email">{{ confirmedEmail }}</div>
            <ol class="signup-confirm-steps">
              <li>Abra seu email</li>
              <li>Clique no link de confirmação</li>
              <li>Você será redirecionado para completar o cadastro</li>
            </ol>
            <router-link to="/login" class="footer-link">Ir para o login →</router-link>
          </div>

          <!-- Estado: formulário -->
          <template v-else>
            <h2 class="signup-title">Crie sua conta grátis</h2>
            <p class="signup-sub">Comece a aprender hoje mesmo</p>

            <q-form @submit.prevent="handleQuickSignup" class="signup-form">
              <q-input
                v-model="quickForm.email"
                outlined
                type="email"
                label="E-mail"
                class="form-input"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'E-mail inválido'
                ]"
              >
                <template #prepend>
                  <q-icon name="mail_outline" size="18px" />
                </template>
              </q-input>

              <q-input
                v-model="quickForm.password"
                outlined
                :type="showPassword ? 'text' : 'password'"
                label="Senha"
                hint="Mínimo 8 caracteres"
                class="form-input"
                :rules="[
                  val => !!val || 'Campo obrigatório',
                  val => val.length >= 8 || 'Mínimo 8 caracteres'
                ]"
              >
                <template #prepend>
                  <q-icon name="lock_outline" size="18px" />
                </template>
                <template #append>
                  <q-icon
                    :name="showPassword ? 'visibility' : 'visibility_off'"
                    size="18px"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>

              <q-btn
                unelevated
                no-caps
                type="submit"
                label="Cadastrar"
                class="signup-btn"
                :loading="signingUp"
              />
            </q-form>

            <div class="divider">
              <span>ou continue com</span>
            </div>

            <div id="google-signup-btn" class="google-btn-wrapper" />

            <p class="form-footer">
              Já tem conta?
              <router-link to="/login" class="footer-link">Entrar</router-link>
            </p>
          </template>
        </div>

      </div>
    </section>

    <!-- ── Seção 2: Stats ─────────────────────────────── -->
    <section class="stats-section">
      <div class="section-container stats-container">
        <div v-for="stat in stats" :key="stat.label" class="stat-item">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </section>

    <!-- ── Seção 3: Cursos em destaque ──────────────────────────────────── -->
    <section class="courses-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Cursos em destaque</h2>
          <p class="section-desc">Comece hoje com um dos nossos cursos mais populares</p>
        </div>

        <!-- Loading -->
        <div v-if="loadingCourses" class="courses-loading">
          <q-spinner-dots color="var(--od-accent)" size="40px" />
        </div>

        <!-- Empty state -->
        <div v-else-if="featuredCourses.length === 0" class="courses-empty">
          <q-icon name="school" size="48px" style="color: var(--od-text-5);" />
          <p>Em breve novos cursos por aqui</p>
        </div>

        <!-- Grid de cursos -->
        <div v-else class="courses-grid">
          <div
            v-for="course in featuredCourses"
            :key="course.id"
            class="course-card od-card"
            @click="$router.push('/courses/lista')"
          >
            <div class="course-thumb">
              <q-icon name="music_note" size="28px" style="color: var(--od-accent);" />
            </div>
            <div class="course-info">
              <span class="course-title od-card-title">{{ course.title }}</span>
              <span class="course-teacher">{{ course.teacher }}</span>
            </div>
            <q-icon name="arrow_forward" size="18px" class="course-arrow" />
          </div>
        </div>

        <div v-if="featuredCourses.length > 0" class="courses-footer">
          <router-link to="/courses/lista" class="courses-all-link">
            Ver todos os cursos →
          </router-link>
        </div>
      </div>
    </section>

    <!-- ── Seção 4: Categorias ────────────────────────── -->
    <section class="categories-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Explore os estilos</h2>
          <p class="section-desc">Encontre o ritmo que combina com você</p>
        </div>

        <div class="categories-grid">
          <div
            v-for="cat in categories"
            :key="cat.name"
            class="category-card od-card"
            @click="$router.push('/courses/lista')"
          >
            <span class="category-emoji">{{ cat.emoji }}</span>
            <span class="category-name od-card-title">{{ cat.name }}</span>
            <span class="category-link">Ver cursos →</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Seção 4: Como funciona ─────────────────────── -->
    <section class="how-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Como funciona</h2>
          <p class="section-desc">Em 3 passos simples você já está dançando</p>
        </div>

        <div class="steps-grid">
          <div v-for="step in steps" :key="step.title" class="step-item">
            <div class="step-icon-wrap">
              <q-icon :name="step.icon" size="28px" class="step-icon" />
              <span class="step-number">{{ step.number }}</span>
            </div>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Seção 5: CTA Final + Footer ───────────────── -->
    <section class="cta-section">
      <div class="section-container cta-container">
        <h2 class="cta-title">Pronto para começar?</h2>
        <p class="cta-sub">Junte-se a centenas de alunos que já estão aprendendo</p>
        <q-btn
          unelevated
          no-caps
          label="Criar conta gratuita"
          class="cta-btn"
          @click="scrollToSignup"
        />
      </div>
    </section>

    <footer class="landing-footer">
      <div class="section-container footer-container">
        <div class="od-logo footer-logo">
          <span class="od-logo-dot" />
          <span>OnDance</span>
        </div>
        <p class="footer-copy">
          © {{ currentYear }} OnDance · ABCAA — Associação Beneficente e Cultural Amor em Ação
        </p>
        <nav class="footer-nav">
          <a href="#" class="footer-link-item">Sobre</a>
          <a href="#" class="footer-link-item">Contato</a>
        </nav>
      </div>
    </footer>

  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from 'src/services/auth'
import { courseService } from 'src/services/course'
import { useQuasar } from 'quasar'
import { useGoogleAuth } from 'src/composables/useGoogleAuth'

const $q = useQuasar()
const router = useRouter()
const { initGoogleButton } = useGoogleAuth()

const currentYear = new Date().getFullYear()

const loadingCourses = ref(false)
const featuredCourses = ref([])

async function fetchFeaturedCourses() {
  loadingCourses.value = true
  try {
    const res = await courseService.list()
    const courses = res.data?.results ?? res.data ?? []
    featuredCourses.value = courses.slice(0, 6)
  } catch {
    featuredCourses.value = []
  } finally {
    loadingCourses.value = false
  }
}

onMounted(() => {
  fetchFeaturedCourses()
  initGoogleButton('google-signup-btn', {
    onSuccess: () => {
      $q.notify({ type: 'positive', message: 'Login realizado com sucesso!' })
      router.push('/courses/initial')
    },
    onError: () => {
      $q.notify({ type: 'negative', message: 'Erro ao autenticar com Google.' })
    },
  })
})

const quickForm = ref({ email: '', password: '' })
const showPassword = ref(false)
const signingUp = ref(false)
const signupDone = ref(false)
const confirmedEmail = ref('')

function scrollToSignup() {
  const el = document.getElementById('signup-form')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

function extractApiError(error, fallback = 'Erro inesperado. Tente novamente.') {
  const data = error.response?.data
  if (!data) return fallback
  const messages = [...new Set(Object.values(data).flat())]
  return messages.length ? messages.join(' ') : fallback
}

async function handleQuickSignup() {
  signingUp.value = true
  try {
    confirmedEmail.value = quickForm.value.email
    await authService.register({
      email: quickForm.value.email,
      password: quickForm.value.password,
    })
    signupDone.value = true
    quickForm.value = { email: '', password: '' }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: extractApiError(error, 'Erro ao criar conta. Tente novamente.'),
      position: 'top'
    })
  } finally {
    signingUp.value = false
  }
}

const stats = [
  { value: '500+', label: 'Alunos matriculados' },
  { value: '30+',  label: 'Cursos disponíveis' },
  { value: '200h', label: 'De conteúdo em vídeo' },
]

const categories = [
  { emoji: '🩰', name: 'Ballet' },
  { emoji: '🥁', name: 'Samba' },
  { emoji: '🪗', name: 'Forró' },
  { emoji: '🎤', name: 'Hip-Hop' },
  { emoji: '💫', name: 'Contemporâneo' },
  { emoji: '🎵', name: 'Funk' },
]

const steps = [
  { number: '01', icon: 'person_add',   title: 'Crie sua conta',       desc: 'Cadastro gratuito em menos de 1 minuto. Sem cartão de crédito.' },
  { number: '02', icon: 'school',        title: 'Escolha um curso',      desc: 'Filtre por estilo, nível e professor. Encontre o ideal para você.' },
  { number: '03', icon: 'play_circle',   title: 'Aprenda no seu ritmo',  desc: 'Assista quando e onde quiser. Pause, repita, domine cada movimento.' },
]
</script>

<style scoped>
.landing-page {
  background: var(--od-bg-page);
}

/* ── Utilitários ── */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--od-text-1);
  margin: 0 0 10px;
  letter-spacing: -0.5px;
}

.section-desc {
  font-size: 16px;
  color: var(--od-text-3);
  margin: 0;
}

/* ── Hero ── */
.hero-section {
  padding: 80px 0 64px;
  background: linear-gradient(135deg, rgba(123, 94, 167, 0.06) 0%, transparent 60%);
}

.hero-container {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 64px;
  align-items: center;
}

.hero-eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--od-accent);
  margin: 0 0 16px;
}

.hero-headline {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -1px;
  color: var(--od-text-1);
  margin: 0 0 20px;
}

.hero-sub {
  font-size: 17px;
  line-height: 1.7;
  color: var(--od-text-2);
  margin: 0 0 36px;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-btn-primary {
  background: var(--od-accent) !important;
  color: #fff !important;
  height: 48px !important;
  padding: 0 28px !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: 15px !important;
}

.hero-btn-ghost {
  font-size: 15px;
  font-weight: 600;
  color: var(--od-text-2);
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 10px;
  border: 1px solid var(--od-border);
  transition: border-color 0.15s, color 0.15s;
}

.hero-btn-ghost:hover {
  border-color: var(--od-accent);
  color: var(--od-accent);
}

/* Signup card */
.signup-card {
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 24px;
  padding: 36px 32px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.07);
}

.signup-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--od-text-1);
  margin: 0 0 4px;
}

.signup-sub {
  font-size: 13px;
  color: var(--od-text-3);
  margin: 0 0 24px;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

:deep(.form-input .q-field__control) {
  background: var(--od-bg-subtle);
  border-radius: 10px;
  min-height: 50px;
}

:deep(.form-input .q-field__control::before) {
  border-color: var(--od-border);
  border-radius: 10px;
}

:deep(.form-input .q-field__control::after) {
  border-radius: 10px;
  border-color: var(--od-accent);
}

:deep(.form-input .q-field__label) {
  color: var(--od-text-3);
  font-size: 13px;
}

:deep(.form-input .q-field__native) {
  color: var(--od-text-1);
  font-size: 14px;
}

:deep(.form-input .q-icon) {
  color: var(--od-text-3);
}

:deep(.form-input.q-field--focused .q-icon) {
  color: var(--od-accent);
}

.signup-btn {
  width: 100% !important;
  background: var(--od-accent) !important;
  color: white !important;
  height: 46px !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  margin-top: 8px;
}

.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
  color: var(--od-text-4);
  font-size: 12px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--od-border);
}

.google-btn-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.form-footer {
  text-align: center;
  font-size: 13px;
  color: var(--od-text-3);
  margin: 0;
}

.footer-link {
  color: var(--od-accent);
  text-decoration: none;
  font-weight: 700;
}

.footer-link:hover {
  text-decoration: underline;
}

/* ── Confirmação de cadastro ── */
.signup-confirmation {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.signup-confirm-icon {
  font-size: 48px;
  line-height: 1;
}

.signup-confirm-email {
  background: var(--od-bg-subtle);
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  color: var(--od-text-1);
  width: 100%;
}

.signup-confirm-steps {
  text-align: left;
  background: var(--od-bg-subtle);
  padding: 14px 14px 14px 30px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--od-text-2);
  line-height: 1.8;
  margin: 0;
  width: 100%;
}

/* ── Stats ── */
.stats-section {
  padding: 48px 0;
  background: var(--od-bg-surface);
  border-top: 1px solid var(--od-border);
  border-bottom: 1px solid var(--od-border);
}

.stats-container {
  display: flex;
  justify-content: center;
  gap: 80px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 40px;
  font-weight: 700;
  color: var(--od-accent);
  letter-spacing: -1px;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--od-text-3);
  font-weight: 500;
}

/* ── Categories ── */
.categories-section {
  padding: 80px 0;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 16px;
  border-radius: 16px;
  border: 1px solid var(--od-border) !important;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  text-align: center;
}

.category-card:hover {
  border-color: var(--od-accent) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(123, 94, 167, 0.12);
}

.category-emoji {
  font-size: 32px;
  line-height: 1;
}

.category-name {
  font-size: 13px;
  font-weight: 600;
}

.category-link {
  font-size: 11px;
  color: var(--od-accent);
  font-weight: 500;
}

/* ── Como funciona ── */
.how-section {
  padding: 80px 0;
  background: var(--od-bg-surface);
  border-top: 1px solid var(--od-border);
  border-bottom: 1px solid var(--od-border);
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.step-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-icon-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-icon {
  color: var(--od-accent) !important;
}

.step-number {
  font-size: 13px;
  font-weight: 700;
  color: var(--od-text-4);
  letter-spacing: 0.5px;
}

.step-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--od-text-1);
  margin: 0;
}

.step-desc {
  font-size: 14px;
  line-height: 1.6;
  color: var(--od-text-3);
  margin: 0;
}

/* ── CTA Final ── */
.cta-section {
  padding: 80px 0;
  background: var(--od-accent);
}

.cta-container {
  text-align: center;
}

.cta-title {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 12px;
  letter-spacing: -0.5px;
}

.cta-sub {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 36px;
}

.cta-btn {
  background: #fff !important;
  color: var(--od-accent) !important;
  height: 50px !important;
  padding: 0 36px !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: 15px !important;
}

/* ── Footer ── */
.landing-footer {
  padding: 32px 0;
  background: var(--od-bg-surface);
  border-top: 1px solid var(--od-border);
}

.footer-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-logo {
  font-size: 15px;
  font-weight: 700;
  color: var(--od-text-1);
  gap: 6px;
}

.footer-copy {
  font-size: 12px;
  color: var(--od-text-4);
  margin: 0;
  text-align: center;
  flex: 1;
}

.footer-nav {
  display: flex;
  gap: 20px;
}

.footer-link-item {
  font-size: 13px;
  color: var(--od-text-3);
  text-decoration: none;
}

.footer-link-item:hover {
  color: var(--od-text-1);
}

/* ── Cursos em destaque ── */
.courses-section {
  padding: 80px 0;
  background: var(--od-bg-subtle);
  border-top: 1px solid var(--od-border);
  border-bottom: 1px solid var(--od-border);
}

.courses-loading,
.courses-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px 0;
  color: var(--od-text-3);
  font-size: 14px;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.course-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid var(--od-border) !important;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

.course-card:hover {
  border-color: var(--od-accent) !important;
  box-shadow: 0 6px 20px rgba(123, 94, 167, 0.1);
  transform: translateY(-2px);
}

.course-thumb {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(123, 94, 167, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.course-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.course-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--od-text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-teacher {
  font-size: 12px;
  color: var(--od-text-3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-arrow {
  color: var(--od-text-4);
  flex-shrink: 0;
  transition: color 0.2s;
}

.course-card:hover .course-arrow {
  color: var(--od-accent);
}

.courses-footer {
  text-align: center;
}

.courses-all-link {
  font-size: 14px;
  font-weight: 600;
  color: var(--od-accent);
  text-decoration: none;
}

.courses-all-link:hover {
  text-decoration: underline;
}

/* ── Responsividade ── */
@media (max-width: 1024px) {
  .categories-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .courses-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .hero-section {
    padding: 48px 0 40px;
  }

  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-headline {
    font-size: 32px;
  }

  .hero-sub {
    font-size: 15px;
  }

  .stats-container {
    gap: 40px;
  }

  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .courses-grid {
    grid-template-columns: 1fr;
  }

  .steps-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .section-title {
    font-size: 26px;
  }

  .cta-title {
    font-size: 28px;
  }

  .footer-container {
    flex-direction: column;
    text-align: center;
  }

  .footer-nav {
    justify-content: center;
  }
}
</style>
