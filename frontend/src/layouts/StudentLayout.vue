<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '1px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px; font-family: 'Poppins', sans-serif;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
          <q-btn flat round dense icon="notifications_none" :style="{ color: 'var(--od-text-3)' }" @click="showNotifications = true">
            <q-badge v-if="unreadCount > 0" floating color="negative" :label="unreadCount" style="font-size:9px;" />
          </q-btn>
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
                  <span class="user-menu-badge role--aluno">Aluno</span>
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

    <AppSidebar ref="sidebarRef" :nav-sections="navSections" settings-route="/student/configuracoes" />

    <q-page-container :style="{ background: 'var(--od-bg-page)' }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>

    <!-- Notification panel -->
    <q-drawer v-model="showNotifications" side="right" :width="360" class="od-notification-drawer">
      <div class="q-pa-md">
        <div class="row items-center justify-between q-mb-md">
          <span style="font-size: 16px; font-weight: 600; color: var(--od-text-1);">Notificações</span>
          <q-btn v-if="unreadCount > 0" flat no-caps label="Marcar todas como lidas" size="sm" style="color: var(--od-accent);" @click="markAllRead" />
        </div>
        <div v-if="notifications.length === 0" class="text-center q-py-xl">
          <q-icon name="notifications_off" size="48px" style="color: var(--od-text-5);" />
          <p style="margin-top: 12px; color: var(--od-text-4); font-size: 13px;">Nenhuma notificação</p>
        </div>
        <div v-else class="column q-gutter-xs">
          <div
            v-for="n in notifications"
            :key="n.id"
            class="od-notification-item"
            :class="{ 'od-notification-item--unread': !n.is_read }"
            @click="onNotificationClick(n)"
          >
            <q-icon :name="notifIcon(n.type)" size="18px" :style="{ color: notifColor(n.type) }" style="flex-shrink: 0; margin-top: 2px;" />
            <div style="flex: 1; min-width: 0;">
              <div style="font-size: 13px; font-weight: 500; color: var(--od-text-1);">{{ n.title }}</div>
              <div v-if="n.message" style="font-size: 12px; color: var(--od-text-3); margin-top: 2px;">{{ n.message }}</div>
              <div style="font-size: 11px; color: var(--od-text-5); margin-top: 4px;">{{ formatNotifTime(n.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>
    </q-drawer>

    <WelcomeModal />

    <!-- "Continue seu curso" popup -->
    <q-dialog v-model="showContinuePopup" persistent>
      <q-card flat bordered class="od-card" style="width: 380px; max-width: 90vw;">
        <q-card-section class="text-center q-py-lg">
          <q-icon name="play_circle" size="48px" style="color: var(--od-accent);" />
          <div class="od-display" style="font-size: 18px; color: var(--od-text-1); margin-top: 12px;">Volte e continue!</div>
          <p style="font-size: 13px; color: var(--od-text-3); margin-top: 6px;">
            Você tem cursos em andamento. Continue de onde parou!
          </p>
          <div class="row q-mt-md justify-center" style="gap: 8px;">
            <q-btn unelevated no-caps label="Continuar agora" icon="play_arrow"
              :to="continueLink"
              @click="showContinuePopup = false"
              style="background: var(--od-accent); color: #fff; border-radius: 8px;" />
            <q-btn flat no-caps label="Agora não" @click="showContinuePopup = false"
              style="color: var(--od-text-4);" />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- "Novo curso disponível" popup -->
    <q-dialog v-model="showNewCoursePopup" persistent>
      <q-card flat bordered class="od-card" style="width: 380px; max-width: 90vw;">
        <q-card-section class="text-center q-py-lg">
          <q-icon name="school" size="48px" style="color: var(--od-accent);" />
          <div class="od-display" style="font-size: 18px; color: var(--od-text-1); margin-top: 12px;">Novo curso disponível!</div>
          <p style="font-size: 13px; color: var(--od-text-3); margin-top: 6px;">
            {{ newCourseMessage }}
          </p>
          <div class="row q-mt-md justify-center" style="gap: 8px;">
            <q-btn unelevated no-caps label="Explorar cursos" icon="explore"
              to="/student/explorar"
              @click="showNewCoursePopup = false"
              style="background: var(--od-accent); color: #fff; border-radius: 8px;" />
            <q-btn flat no-caps label="Agora não" @click="showNewCoursePopup = false"
              style="color: var(--od-text-4);" />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from 'components/shared/AppSidebar.vue'
import WelcomeModal from 'components/shared/WelcomeModal.vue'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'
import { api } from 'boot/axios'

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

// Notifications
const showNotifications = ref(false)
const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

async function loadNotifications() {
  try {
    const resp = await api.get('/notifications/')
    notifications.value = resp.data.results ?? resp.data
  } catch {
    // silently fail
  }
}

async function markAllRead() {
  try {
    await api.post('/notifications/mark-read/', {})
    notifications.value.forEach(n => n.is_read = true)
  } catch {
    // silently fail
  }
}

function onNotificationClick(n) {
  if (!n.is_read) {
    n.is_read = true
    api.post('/notifications/mark-read/', { ids: [n.id] }).catch(() => {})
  }
  if (n.link) {
    showNotifications.value = false
    router.push(n.link)
  }
}

function notifIcon(type) {
  const icons = { new_lesson: 'play_circle', new_course: 'school', almost_done: 'trending_up', review: 'star', comment: 'comment', system: 'info' }
  return icons[type] || 'notifications'
}

function notifColor(type) {
  const colors = { new_lesson: '#1D9E75', new_course: 'var(--od-accent)', almost_done: '#f59e0b', review: '#f59e0b', comment: '#7F77DD', system: 'var(--od-text-4)' }
  return colors[type] || 'var(--od-text-4)'
}

function formatNotifTime(dateStr) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return 'agora'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}min atrás`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h atrás`
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })
}

let notifInterval = null

// Popups
const showContinuePopup = ref(false)
const showNewCoursePopup = ref(false)
const continueLink = ref('/student/my-courses')
const newCourseMessage = ref('Um novo curso está esperando por você!')

async function checkPopups() {
  try {
    // Check for incomplete courses
    const enrollResp = await api.get('/enrollments/')
    const enrollments = enrollResp.data.results ?? enrollResp.data
    const incomplete = enrollments.find(e => !e.is_completed && e.progress_percent > 0 && e.progress_percent < 100)
    if (incomplete) {
      continueLink.value = `/student/courses/${incomplete.course}/assistir`
      const lastShown = localStorage.getItem('ondance_continue_popup')
      if (!lastShown || Date.now() - parseInt(lastShown) > 86400000) {
        showContinuePopup.value = true
        localStorage.setItem('ondance_continue_popup', String(Date.now()))
      }
    }

    // Check for new courses
    const courseResp = await api.get('/courses/published/')
    const courses = courseResp.data.results ?? courseResp.data
    const lastCheck = localStorage.getItem('ondance_last_course_check')
    const newCourses = lastCheck
      ? courses.filter(c => new Date(c.id) > new Date(parseInt(lastCheck)))
      : []
    if (newCourses.length > 0 && !incomplete) {
      newCourseMessage.value = `${newCourses.length} novo${newCourses.length > 1 ? 's' : ''} curso${newCourses.length > 1 ? 's' : ''} está${newCourses.length === 1 ? '' : 'ão'} disponível!`
      showNewCoursePopup.value = true
    }
    localStorage.setItem('ondance_last_course_check', String(Date.now()))
  } catch {
    // silently fail
  }
}

onMounted(() => {
  loadNotifications()
  notifInterval = setInterval(loadNotifications, 30000)
  checkPopups()
})
onUnmounted(() => { if (notifInterval) clearInterval(notifInterval) })

const navSections = [
  {
    label: null,
    items: [
      { to: '/student/dashboard', icon: 'dashboard',  label: 'Dashboard' },
      { to: '/student/my-courses', icon: 'play_circle', label: 'Meus Cursos' },
      { to: '/student/explorar', icon: 'explore', label: 'Explorar' },
      { to: '/student/certificados', icon: 'workspace_premium', label: 'Certificados' },
      { to: '/perfil', icon: 'settings',  label: 'Perfil' },
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
.od-notification-drawer {
  background: var(--od-bg-surface);
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
