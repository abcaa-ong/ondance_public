<template>
  <router-view />
</template>

<script setup>
import { useQuasar } from 'quasar'
import { onMounted } from 'vue'
import { initDarkMode } from 'src/composables/useDarkMode'

const $q = useQuasar()
onMounted(() => initDarkMode($q))
</script>
