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
            <q-avatar
              size="32px"
              :style="{ background: 'var(--od-accent)', color: '#fff', fontSize: '13px', fontWeight: 600 }"
            >
              {{ userInitial }}
            </q-avatar>
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]">
              <q-list style="min-width: 160px;">
                <q-item clickable v-close-popup :to="'/perfil'">
                  <q-item-section avatar>
                    <q-icon name="person_outline" size="18px" />
                  </q-item-section>
                  <q-item-section>Meu perfil</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-close-popup @click="handleLogout">
                  <q-item-section avatar>
                    <q-icon name="logout" size="18px" />
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

const userInitial = computed(() => {
  const email = user.value?.email || ''
  return email.charAt(0).toUpperCase()
})

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
