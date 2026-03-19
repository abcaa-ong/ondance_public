<template>
  <q-drawer
    v-model="drawerOpen"
    show-if-above
    :width="230"
    class="od-sidebar"
    side="left"
  >
    <!-- Logo -->
    <div class="od-logo q-px-lg q-pt-lg q-pb-md">
      <span class="od-logo-dot" />
      <a href="/">On Dance</a>
    </div>

    <!-- Nav Items -->
    <q-list padding class="q-px-xs">
      <template v-for="section in navSections" :key="section.label">
        <div v-if="section.label" class="od-section-label">{{ section.label }}</div>

        <q-item
          v-for="item in section.items"
          :key="item.to"
          :to="item.to"
          exact
          clickable
          v-ripple
          active-class="active-nav"
          class="q-mb-xs"
          style="border-radius: 8px;"
        >
          <q-item-section avatar style="min-width: 36px;">
            <q-icon :name="item.icon" size="18px" />
          </q-item-section>
          <q-item-section>{{ item.label }}</q-item-section>
          <q-item-section v-if="item.badge" side>
            <q-badge
              :label="item.badge"
              style="background: var(--od-accent); font-size: 10px; padding: 2px 6px;"
            />
          </q-item-section>
        </q-item>
      </template>
    </q-list>

    <!-- User pill -->
    <div class="q-mt-auto q-pa-sm">
      <div
        class="row items-center q-pa-sm"
        style="background: rgba(255,255,255,0.06); border-radius: 10px; cursor: pointer; gap: 10px;"
        @click="goToSettings"
      >
        <q-avatar size="32px" style="background: var(--od-accent); font-size: 12px; font-weight: 600; color: #fff;">
          {{ initials }}
        </q-avatar>
        <div style="flex: 1; min-width: 0;">
          <div style="font-size: 12.5px; font-weight: 500; color: rgba(255,255,255,0.85); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {{ user?.name }}
          </div>
          <div style="font-size: 11px; color: rgba(255,255,255,0.35);">{{ roleLabel }}</div>
        </div>
        <q-btn flat round dense icon="logout" size="xs" style="color: rgba(255,255,255,0.3);" @click.stop="handleLogout" />
      </div>
    </div>
  </q-drawer>
</template>

<script setup>
import { computed, ref } from 'vue'
// import { useAuthStore } from 'stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps({
  navSections: { type: Array, required: true },
  settingsRoute: { type: String, default: null }
})

const drawerOpen = ref(true)
// const auth   = useAuthStore()
const router = useRouter()
// const user   = computed(() => auth.user)
const user   = "Luciano"

const initials = computed(() => {
  if (!user.value?.name) return '?'
  return user.value.name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
})

const roleLabel = computed(() => ({
  aluno:     'Aluno',
  professor: 'Professor',
  admin:     'Administrador'
}[user.value?.role] ?? ''))

function goToSettings () {
  if (props.settingsRoute) router.push(props.settingsRoute)
}

function handleLogout () {
  // auth.logout()
  router.push('/login')
}
</script>
