<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '0.5px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" aria-label="Abrir menu" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
          <q-btn flat round dense icon="notifications_none" :style="{ color: 'var(--od-text-3)' }" aria-label="Notificações">
            <q-badge v-if="unreadCount > 0" floating color="negative" :label="unreadCount" style="font-size:9px;" aria-live="polite" />
          </q-btn>
          <q-btn
            flat round dense
            :icon="isDark ? 'light_mode' : 'dark_mode'"
            :style="{ color: 'var(--od-text-3)' }"
            @click="toggleDark"
          >
            <q-tooltip>{{ isDark ? 'Modo claro' : 'Modo escuro' }}</q-tooltip>
          </q-btn>
          <q-btn flat round dense style="padding: 2px;" :aria-label="`Menu do usuário ${userName}`">
            <q-avatar class="header-avatar">{{ userInitial }}</q-avatar>
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]" class="user-menu">
              <div class="user-menu-card">
                <q-avatar class="user-menu-avatar">{{ userInitial }}</q-avatar>
                <div class="user-menu-info">
                  <div class="user-menu-name">{{ userName }}</div>
                  <span class="user-menu-badge role--admin">Administrador</span>
                </div>
              </div>
              <q-separator />
              <q-list style="padding: 4px;">
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

    <AppSidebar ref="sidebarRef" :nav-sections="navSections" settings-route="/admin/config" />

    <q-page-container :style="{ background: 'var(--od-bg-page)' }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from 'components/shared/AppSidebar.vue'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'
import { api } from 'boot/axios'

const sidebarRef = ref(null)
function toggleDrawer() { sidebarRef.value?.toggle() }

const { isDark, toggle: toggleDark } = useDarkMode()
const { logout, user } = useAuth()
const router = useRouter()

const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

async function loadNotifications() {
  try {
    const resp = await api.get('/notifications/')
    notifications.value = resp.data.results ?? resp.data ?? []
  } catch {
    // silently fail
  }
}

onMounted(loadNotifications)

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
    label: 'Plataforma',
    items: [
      { to: '/admin/overview',   icon: 'dashboard',      label: 'Visão Geral' },
      { to: '/admin/courses',     icon: 'fact_check',     label: 'Aprovar Cursos' },
      { to: '/admin/usuarios',   icon: 'manage_accounts', label: 'Usuários' },
      { to: '/admin/analytics',  icon: 'bar_chart',      label: 'Analytics' },
      { to: '/admin/categorias', icon: 'category',       label: 'Categorias' },
    ]
  },
  {
    label: 'Operações',
    items: [
      { to: '/admin/campanhas', icon: 'campaign', label: 'Campanhas' },
      { to: '/admin/config',    icon: 'settings', label: 'Configurações' },
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
