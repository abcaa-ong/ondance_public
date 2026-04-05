<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>
          On Dance
        </q-toolbar-title>
        
        <!-- Spacer to push link to the right -->
        <div style="flex: 1;" />
        
        <!-- Cadastro Link -->
        <router-link
          to="/register"
          style="
            color: var(--od-text-1, #333);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 4px;
            transition: all 0.3s ease;
          "
          @mouseenter="e => e.target.style.backgroundColor = 'var(--od-bg-subtle, #f5f5f5)'"
          @mouseleave="e => e.target.style.backgroundColor = 'transparent'"
        >
          Cadastro
        </router-link>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>
          Menu
        </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Aluno',
    icon: 'person',
    to: '/students'
  },
  {
    title: 'Professor',
    icon: 'school',
    to: '/professores'
  },
  {
    title: 'Cursos',
    icon: 'book',
    to: '/courses'
  },
  {
    title: 'Cidades',
    icon: 'city',
    to: '/cities'
  },
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
