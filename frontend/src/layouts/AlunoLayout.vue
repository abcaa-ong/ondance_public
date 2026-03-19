<template>
  <q-layout view="lHh Lpr lFf">

    <!-- Topbar -->
    <q-header flat :style="{ background: 'var(--od-bg-surface)', borderBottom: '0.5px solid var(--od-border)' }">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" :style="{ color: 'var(--od-text-1)' }" class="lt-md" @click="toggleDrawer" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 4px;">
          <q-btn flat round dense icon="search"             :style="{ color: 'var(--od-text-3)' }" />
          <q-btn flat round dense icon="notifications_none" :style="{ color: 'var(--od-text-3)' }">
            <q-badge floating color="negative" style="font-size:9px;" label="3" />
          </q-btn>
          <q-btn
            flat round dense
            :icon="isDark ? 'light_mode' : 'dark_mode'"
            :style="{ color: 'var(--od-text-3)' }"
            @click="toggleDark"
          >
            <q-tooltip>{{ isDark ? 'Modo claro' : 'Modo escuro' }}</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <AppSidebar
      :nav-sections="navSections"
      settings-route="/aluno/configuracoes"
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
import AppSidebar from 'components/shared/AppSidebar.vue'
import { useDarkMode } from 'src/composables/useDarkMode'

const drawerOpen = ref(true)
function toggleDrawer () { drawerOpen.value = !drawerOpen.value }

const { isDark, toggle: toggleDark } = useDarkMode()

const navSections = [
  {
    label: null,
    items: [
      { to: '/aluno/inicio',       icon: 'home',        label: 'Início' },
      { to: '/aluno/cursos',       icon: 'play_circle', label: 'Meus Cursos',  badge: '3' },
      { to: '/aluno/explorar',     icon: 'explore',     label: 'Explorar' },
      { to: '/aluno/certificados', icon: 'workspace_premium', label: 'Certificados' }
    ]
  },
  {
    label: 'Conta',
    items: [
      { to: '/aluno/progresso',    icon: 'bar_chart',   label: 'Progresso' },
      { to: '/aluno/configuracoes',icon: 'settings',    label: 'Configurações' }
    ]
  }
]
</script>
