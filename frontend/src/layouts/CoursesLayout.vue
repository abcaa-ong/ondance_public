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
          <q-btn
            flat round dense
            icon="logout"
            :style="{ color: 'var(--od-text-3)' }"
            @click="handleLogout"
          >
            <q-tooltip>Sair</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <AppSidebar
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

  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from 'components/shared/AppSidebar.vue'
import { useDarkMode } from 'src/composables/useDarkMode'
import { useAuth } from 'src/composables/useAuth'

const drawerOpen = ref(true)
function toggleDrawer () { drawerOpen.value = !drawerOpen.value }

const { isDark, toggle: toggleDark } = useDarkMode()
const { logout } = useAuth()
const router = useRouter()

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
