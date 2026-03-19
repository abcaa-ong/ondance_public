<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat style="background: #fff; border-bottom: 0.5px solid rgba(0,0,0,0.08);">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" style="color: #333;" class="lt-md" @click="toggleDrawer" />
        <q-toolbar-title style="font-size: 0;" />
        <q-btn
          unelevated
          class="od-btn-primary"
          label="+ Novo Curso"
          no-caps
          padding="6px 16px"
          to="/professor/cursos/novo"
        />
      </q-toolbar>
    </q-header>

    <AppSidebar :nav-sections="navSections" />

    <q-page-container style="background: #F7F6F3;">
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

const drawerOpen = ref(true)
function toggleDrawer () { drawerOpen.value = !drawerOpen.value }

const navSections = [
  {
    label: null,
    items: [
      { to: '/professor/dashboard', icon: 'dashboard',    label: 'Dashboard' },
      { to: '/professor/cursos',    icon: 'video_library',label: 'Meus Cursos', badge: '5' },
      { to: '/professor/cursos/novo',icon: 'add_circle',  label: 'Criar Curso' },
      { to: '/professor/alunos',    icon: 'group',        label: 'Alunos', badge: '42' }
    ]
  },
  {
    label: 'Finanças',
    items: [
      { to: '/professor/ganhos',    icon: 'payments',     label: 'Ganhos' },
      { to: '/professor/config',    icon: 'settings',     label: 'Configurações' }
    ]
  }
]
</script>
