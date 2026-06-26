<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '1px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px; font-family: 'Poppins', sans-serif;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
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
            <q-avatar class="header-avatar">{{ userInitial }}</q-avatar>
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]" class="user-menu">
              <div class="user-menu-card">
                <q-avatar class="user-menu-avatar">{{ userInitial }}</q-avatar>
                <div class="user-menu-info">
                  <div class="user-menu-name">{{ userName }}</div>
                  <span class="user-menu-badge role--professor">Professor</span>
                </div>
              </div>
              <q-separator />
              <q-list style="padding: 4px;">
                <!-- <q-item clickable v-close-popup to="/perfil" class="user-menu-item">
                  <q-item-section avatar style="min-width: 32px;"><q-icon name="person_outline" size="16px" /></q-item-section>
                  <q-item-section>Meu perfil</q-item-section>
                </q-item> -->
                <q-item clickable v-close-popup @click="handleLogout" class="user-menu-item user-menu-logout">
                  <q-item-section avatar style="min-width: 32px;"><q-icon name="logout" size="16px" /></q-item-section>
                  <q-item-section>Sair</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <AppSidebar ref="sidebarRef" :nav-sections="navSections" settings-route="/teacher/config" />

    <q-page-container :style="{ background: 'var(--od-bg-page)' }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>

    <WelcomeModal />

  </q-layout>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from 'components/shared/AppSidebar.vue'
import WelcomeModal from 'components/shared/WelcomeModal.vue'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'

const sidebarRef = ref(null)
function toggleDrawer() { sidebarRef.value?.toggle() }

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

function handleLogout() {
  logout()
  router.push('/login')
}

const navSections = [
  {
    label: null,
    items: [
      { to: '/teacher/dashboard', icon: 'dashboard', label: 'Dashboard'   },
      { to: '/teacher/courses', icon: 'video_library', label: 'Meus Cursos' },      
      { to: '/teacher/students', icon: 'group', label: 'Meus Alunos' },
      { to: '/teacher/config', icon: 'settings', label: 'Avaliações' },
      { to: '/teacher/config', icon: 'settings', label: 'Progresso dos alunos' },
      { to: '/teacher/perfil', icon: 'profile', label: 'Perfil' },      
    ]
  },
  {
    label: 'Finanças',
    items: [
      { to: '/teacher/ganhos', icon: 'payments', label: 'Ganhos' },      
    ]
  }
]
</script>

<style scoped>
.header-avatar {
  width: 32px; height: 32px;
  background: var(--od-accent); color: #fff;
  font-size: 13px; font-weight: 700;
}
</style>
