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
      <div class="user-pill" @click="goToSettings">
        <q-avatar size="34px" class="user-pill-avatar">
          {{ initials }}
        </q-avatar>
        <div class="user-pill-info">
          <div class="user-pill-name">{{ user?.name || user?.email }}</div>
          <span class="user-role-badge" :class="`role--${user?.role}`">{{ roleLabel }}</span>
        </div>
        <q-btn flat round dense icon="logout" size="xs" class="user-pill-logout" @click.stop="handleLogout" />
      </div>
    </div>
  </q-drawer>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from 'src/composables/useAuth'

const props = defineProps({
  navSections: { type: Array, required: true },
  settingsRoute: { type: String, default: null }
})

const drawerOpen = ref(true)
const router = useRouter()
const { user, logout } = useAuth()

const initials = computed(() => {
  const name = user.value?.name || user.value?.email || ''
  if (!name) return '?'
  const parts = name.split(' ').filter(Boolean)
  if (parts.length === 0) return '?'
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
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
  logout()
  router.push('/login')
}

defineExpose({ toggle: () => { drawerOpen.value = !drawerOpen.value } })
</script>

<style scoped>
.user-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.06);
  cursor: pointer;
  transition: background 0.15s;
}

.user-pill:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-pill-avatar {
  background: var(--od-accent);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-pill-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.user-pill-name {
  font-size: 12.5px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 20px;
  letter-spacing: 0.3px;
  width: fit-content;
}

.role--aluno {
  background: rgba(56, 189, 248, 0.18);
  color: #7dd3fc;
}

.role--professor {
  background: rgba(167, 139, 250, 0.2);
  color: #c4b5fd;
}

.role--admin {
  background: rgba(252, 165, 165, 0.18);
  color: #fca5a5;
}

.user-pill-logout {
  color: rgba(255, 255, 255, 0.3) !important;
  flex-shrink: 0;
}
</style>
