<template>
  <q-page class="column items-center justify-center" style="min-height: 100vh; background: #F7F6F3;">
    <div class="text-center">
      <div style="font-size: 80px; margin-bottom: 8px;">🕺</div>
      <div class="od-display" style="font-size: 64px; font-weight: 800; color: #1a1a1a; letter-spacing: -3px; line-height: 1;">404</div>
      <div style="font-size: 18px; color: #888; margin: 12px 0 24px;">Essa página foi dançar…</div>
      <q-btn unelevated no-caps label="Voltar para o início" class="od-btn-primary" @click="goHome" />
    </div>
  </q-page>
</template>

<script setup>
// import { useRouter } from 'vue-router'
// import { useAuthStore } from 'stores/auth'

// const router = useRouter()
// const auth   = useAuthStore()

// function goHome () {
//   router.push(auth.isAuthenticated ? auth.homeRoute : '/login')
// }
</script>
