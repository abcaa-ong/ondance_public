<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '0.5px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" aria-label="Abrir menu" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
          <q-btn v-if="user?.role !== 'admin'" flat round dense icon="notifications_none" :style="{ color: 'var(--od-text-3)' }" aria-label="Notificações">
            <q-badge v-if="unreadCount > 0" floating color="negative" :label="unreadCount" style="font-size:9px;" aria-live="polite" />
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]" class="od-notification-menu" style="width: 360px; max-height: 480px;">
              <div class="q-pa-md">
                <div class="row items-center justify-between q-mb-md">
                  <span style="font-size: 16px; font-weight: 600; color: var(--od-text-1);">Notificações</span>
                </div>
                <div v-if="notifications.length === 0" class="text-center q-py-xl">
                  <q-icon name="notifications_off" size="48px" style="color: var(--od-text-5);" />
                  <p style="margin-top: 12px; color: var(--od-text-4); font-size: 13px;">Nenhuma notificação</p>
                </div>
                <div v-else class="column q-gutter-xs" style="overflow-y: auto; max-height: 380px;">
                  <div
                    v-for="n in notifications"
                    :key="n.id"
                    class="od-notification-item"
                    :class="{ 'od-notification-item--unread': !n.is_read }"
                  >
                    <q-icon name="info" size="18px" style="color: var(--od-text-4); flex-shrink: 0; margin-top: 2px;" />
                    <div style="flex: 1; min-width: 0;">
                      <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ n.title }}</div>
                      <div v-if="n.message" style="font-size: 12px; color: var(--od-text-3); margin-top: 2px;">{{ n.message }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </q-menu>
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
.od-notification-menu {
  background: var(--od-bg-surface);
  border: 1px solid var(--od-border);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.od-notification-item {
  display: flex;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
}
.od-notification-item:hover {
  background: var(--od-bg-hover);
}
.od-notification-item--unread {
  background: var(--od-bg-subtle);
}
</style>
