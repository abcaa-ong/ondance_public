<template>
  <q-layout view="lHh Lpr lFf">

    <q-header flat style="background: #fff; border-bottom: 0.5px solid rgba(0,0,0,0.08);">
      <q-toolbar style="height: 56px; padding: 0 24px;">
        <q-btn flat round dense icon="menu" style="color: #333;" class="lt-md" />
        <q-toolbar-title style="font-size: 0;" />

        <div class="row items-center" style="gap: 8px;">
          <q-chip
            icon="circle"
            label="Plataforma Online"
            dense
            style="background: #D1FAE5; color: #065F46; font-size: 12px; font-weight: 500;"
          />
          <q-btn flat round dense icon="notifications_none" style="color: #888;">
            <q-badge floating color="negative" label="7" style="font-size:9px;" />
          </q-btn>
        </div>
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
import AppSidebar from 'components/shared/AppSidebar.vue'

const navSections = [
  {
    label: 'Plataforma',
    items: [
      { to: '/admin/overview',   icon: 'dashboard',     label: 'Visão Geral' },
      { to: '/admin/cursos',     icon: 'video_library', label: 'Aprovar Cursos', badge: '7' },
      { to: '/admin/usuarios',   icon: 'manage_accounts',label: 'Usuários' },
      { to: '/admin/analytics',  icon: 'bar_chart',     label: 'Analytics' }
    ]
  },
  {
    label: 'Operações',
    items: [
      { to: '/admin/campanhas',  icon: 'campaign',      label: 'Campanhas' },
      { to: '/admin/config',     icon: 'settings',      label: 'Configurações' }
    ]
  }
]
</script>
