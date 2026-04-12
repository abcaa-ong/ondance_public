<template>
  <q-layout view="hHh Lpr lFf">
    <q-header class="main-header">
      <q-toolbar class="main-toolbar">
        <!-- Logo -->
        <router-link to="/" class="od-logo navbar-logo">
          <span class="od-logo-dot" />
          <span>OnDance</span>
        </router-link>

        <div style="flex: 1;" />

        <!-- Desktop nav -->
        <nav class="desktop-nav">
          <router-link to="/courses/lista" class="nav-link">Cursos</router-link>

          <template v-if="isAuthenticated">
            <router-link to="/courses/initial" class="nav-link">Minha Área</router-link>
            <q-btn
              unelevated
              no-caps
              label="Sair"
              class="nav-btn-ghost"
              @click="handleLogout"
            />
          </template>

          <template v-else>
            <router-link to="/login" class="nav-link">Entrar</router-link>
            <q-btn
              unelevated
              no-caps
              label="Começar grátis"
              class="nav-btn-primary"
              @click="scrollToSignup"
            />
          </template>

          <q-btn
            flat
            round
            dense
            :icon="isDark ? 'light_mode' : 'dark_mode'"
            class="nav-dark-btn"
            @click="toggleDark"
          />
        </nav>

        <!-- Mobile hamburger -->
        <button
          class="mobile-menu-btn"
          @click="openDrawer"
          aria-label="Abrir menu"
        >
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M3 6h16M3 11h16M3 16h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>

  <!-- Mobile drawer — fora do q-layout para evitar stacking context -->
  <Teleport to="body">
    <div
      v-if="mobileDrawer"
      class="od-overlay"
      @click.self="mobileDrawer = false"
    >
      <nav class="od-panel">
        <div class="od-panel-header">
          <span class="od-panel-logo">OnDance</span>
          <button class="od-panel-close" @click="mobileDrawer = false" aria-label="Fechar menu">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 4L16 16M16 4L4 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="od-panel-nav">
          <router-link to="/courses/lista" class="od-panel-link" @click="mobileDrawer = false">
            Cursos
          </router-link>

          <template v-if="isAuthenticated">
            <router-link to="/courses/initial" class="od-panel-link" @click="mobileDrawer = false">
              Minha Área
            </router-link>
            <router-link to="/perfil" class="od-panel-link" @click="mobileDrawer = false">
              Perfil
            </router-link>
            <button class="od-panel-link od-panel-logout" @click="handleLogout">
              Sair
            </button>
          </template>

          <template v-else>
            <router-link to="/login" class="od-panel-link" @click="mobileDrawer = false">
              Entrar
            </router-link>
            <button class="od-panel-link od-panel-cta" @click="scrollToSignup(); mobileDrawer = false">
              Começar grátis
            </button>
          </template>
        </div>
      </nav>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'

const { isDark, toggle: toggleDark } = useDarkMode()
const { isAuthenticated, logout } = useAuth()
const router = useRouter()

const mobileDrawer = ref(false)

function openDrawer() {
  mobileDrawer.value = true
}

function handleLogout() {
  logout()
  mobileDrawer.value = false
  router.push('/login')
}

function scrollToSignup() {
  const el = document.getElementById('signup-form')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.main-header {
  background: var(--od-bg-surface) !important;
  border-bottom: 1px solid var(--od-border);
  box-shadow: none !important;
}

.main-toolbar {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px;
  min-height: 64px;
}

.navbar-logo {
  font-size: 18px;
  color: var(--od-text-1) !important;
  text-decoration: none;
  letter-spacing: -0.5px;
}

.navbar-logo :deep(.od-logo-dot) {
  background: var(--od-accent);
}

/* Desktop nav */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--od-text-2);
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 8px;
  transition: background 0.15s, color 0.15s;
}

.nav-link:hover {
  background: var(--od-bg-subtle);
  color: var(--od-text-1);
}

.nav-btn-ghost {
  font-size: 14px !important;
  font-weight: 500 !important;
  color: var(--od-text-2) !important;
  border: 1px solid var(--od-border) !important;
  border-radius: 8px !important;
  padding: 0 16px !important;
  height: 36px !important;
  margin-left: 4px;
  transition: border-color 0.15s, color 0.15s;
}

.nav-btn-ghost:hover {
  border-color: var(--od-accent) !important;
  color: var(--od-accent) !important;
}

.nav-btn-primary {
  font-size: 14px !important;
  font-weight: 600 !important;
  background: var(--od-accent) !important;
  color: #fff !important;
  border-radius: 8px !important;
  padding: 0 18px !important;
  height: 36px !important;
  margin-left: 4px;
}

.nav-dark-btn {
  color: var(--od-text-3) !important;
  margin-left: 8px;
}

/* Mobile */
.mobile-menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: var(--od-text-2);
  cursor: pointer;
  border-radius: 8px;
  padding: 0;
}

.mobile-menu-btn:hover {
  background: var(--od-bg-subtle);
}

@media (max-width: 767px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }
}
</style>

<!-- Estilos globais do drawer mobile (Teleport sai do escopo do componente) -->
<style>
.od-overlay {
  position: fixed;
  inset: 0;
  z-index: 9000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: flex-end;
}

.od-panel {
  width: 280px;
  height: 100%;
  background: var(--od-bg-surface);
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  animation: od-slide-in 0.18s ease;
}

@keyframes od-slide-in {
  from { transform: translateX(100%); }
  to   { transform: translateX(0); }
}

.od-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 12px;
  border-bottom: 1px solid var(--od-border);
}

.od-panel-logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--od-accent);
  letter-spacing: -0.5px;
}

.od-panel-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--od-text-2);
  cursor: pointer;
  transition: background 0.12s;
}

.od-panel-close:hover {
  background: var(--od-bg-subtle);
}

.od-panel-nav {
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  gap: 4px;
}

.od-panel-link {
  display: block;
  font-size: 15px;
  font-weight: 500;
  color: var(--od-text-1);
  text-decoration: none;
  padding: 12px 16px;
  border-radius: 10px;
  transition: background 0.12s;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  width: 100%;
}

.od-panel-link:hover {
  background: var(--od-bg-subtle);
}

.od-panel-cta {
  background: var(--od-accent) !important;
  color: #fff !important;
  margin-top: 8px;
  text-align: center !important;
}

.od-panel-logout {
  color: #e53935 !important;
}
</style>
