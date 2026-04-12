<template>
  <q-layout view="lHh Lpr lFf">

    <!-- Topbar -->
    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '0.5px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
          <q-btn flat round dense icon="search"             :style="{ color: 'var(--od-text-3)' }" />
          <q-btn flat round dense icon="notifications_none" :style="{ color: 'var(--od-text-3)' }" />
          <q-btn
            flat round dense
            :icon="isDark ? 'light_mode' : 'dark_mode'"
            :style="{ color: 'var(--od-text-3)' }"
            @click="toggleDark"
          >
            <q-tooltip>{{ isDark ? 'Modo claro' : 'Modo escuro' }}</q-tooltip>
          </q-btn>

          <q-btn flat round dense style="padding: 2px;">
            <q-avatar class="header-avatar">
              {{ userInitial }}
            </q-avatar>
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]" class="user-menu">
              <!-- User card -->
              <div class="user-menu-card">
                <q-avatar class="user-menu-avatar">{{ userInitial }}</q-avatar>
                <div class="user-menu-info">
                  <div class="user-menu-name">{{ userName }}</div>
                  <span class="user-menu-badge" :class="`role--${user?.role}`">{{ roleLabel }}</span>
                </div>
              </div>
              <q-separator />
              <q-list style="padding: 4px;">
                <q-item clickable v-close-popup :to="'/perfil'" class="user-menu-item">
                  <q-item-section avatar style="min-width: 32px;">
                    <q-icon name="person_outline" size="16px" />
                  </q-item-section>
                  <q-item-section>Meu perfil</q-item-section>
                </q-item>
                <q-item clickable v-close-popup @click="handleLogout" class="user-menu-item user-menu-logout">
                  <q-item-section avatar style="min-width: 32px;">
                    <q-icon name="logout" size="16px" />
                  </q-item-section>
                  <q-item-section>Sair</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <AppSidebar
      ref="sidebarRef"
      :nav-sections="navSections"
      settings-route="/courses/configuracoes"
    />

    <!-- Page -->
    <q-page-container :style="{ background: 'var(--od-bg-page)' }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>

    <OnboardingModal
      v-if="showOnboarding"
      @close="showOnboarding = false"
      @saved="showOnboarding = false"
    />

  </q-layout>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from 'components/shared/AppSidebar.vue'
import OnboardingModal from 'components/shared/OnboardingModal.vue'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'

const profileComplete = localStorage.getItem('profile_complete')
const onboardingDismissed = localStorage.getItem('onboarding_dismissed')
const showOnboarding = ref(profileComplete === 'false' && !onboardingDismissed)

const sidebarRef = ref(null)
function toggleDrawer () { sidebarRef.value?.toggle() }

const { isDark, toggle: toggleDark } = useDarkMode()
const { logout, user } = useAuth()
const router = useRouter()

const userName = computed(() => user.value?.name || user.value?.email || '')

const userInitial = computed(() => {
  const name = user.value?.name || user.value?.email || ''
  const parts = name.split(' ').filter(Boolean)
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
  return name.charAt(0).toUpperCase()
})

const roleLabel = computed(() => ({
  aluno: 'Aluno',
  professor: 'Professor',
  admin: 'Administrador',
}[user.value?.role] ?? ''))

function handleLogout () {
  logout()
  router.push('/login')
}

const navSections = [
  {
    label: null,
    items: [
      { to: '/',                  icon: 'home',             label: 'Página Inicial' },
      { to: '/courses/initial',      icon: 'dashboard',        label: 'Início' },
      { to: '/courses/lista',        icon: 'list_alt',         label: 'Cursos' },
      { to: '/courses/new',         icon: 'add_circle',       label: 'Novo Curso' },
      { to: '/courses/categorias',   icon: 'category',         label: 'Categorias' },
    ]
  },
  {
    label: 'Gestão',
    items: [
      { to: '/courses/students',       icon: 'group',            label: 'Students' },
      { to: '/courses/configuracoes',icon: 'settings',         label: 'Configurações' }
    ]
  }
]
</script>

<style scoped>
.header-avatar {
  width: 32px;
  height: 32px;
  background: var(--od-accent);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}
</style>

<style>
.user-menu {
  border-radius: 14px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.14) !important;
  min-width: 220px !important;
  overflow: hidden;
  border: 1px solid var(--od-border) !important;
  background: var(--od-bg-surface) !important;
}

.user-menu-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.user-menu-avatar {
  width: 40px;
  height: 40px;
  background: var(--od-accent);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  flex-shrink: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-menu-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.user-menu-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--od-text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-menu-badge {
  display: inline-block;
  font-size: 10.5px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
  width: fit-content;
}

.role--aluno {
  background: rgba(14, 165, 233, 0.12);
  color: #0284c7;
}

.role--professor {
  background: rgba(139, 92, 246, 0.12);
  color: #7c3aed;
}

.role--admin {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
}

.body--dark .role--aluno  { background: rgba(56, 189, 248, 0.18); color: #7dd3fc; }
.body--dark .role--professor { background: rgba(167, 139, 250, 0.2); color: #c4b5fd; }
.body--dark .role--admin  { background: rgba(252, 165, 165, 0.18); color: #fca5a5; }

.user-menu-item {
  border-radius: 8px !important;
  font-size: 13.5px;
  color: var(--od-text-1) !important;
  min-height: 36px !important;
}

.user-menu-logout {
  color: #e53935 !important;
}

.user-menu-logout .q-icon {
  color: #e53935 !important;
}
</style>
