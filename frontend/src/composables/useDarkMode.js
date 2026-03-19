import { useQuasar } from 'quasar'
import { computed } from 'vue'

const STORAGE_KEY = 'od-dark'

export function useDarkMode () {
  const $q = useQuasar()

  const isDark = computed(() => $q.dark.isActive)

  function toggle () {
    $q.dark.toggle()
    localStorage.setItem(STORAGE_KEY, $q.dark.isActive ? '1' : '0')
  }

  return { isDark, toggle }
}

export function initDarkMode ($q) {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved === '1') $q.dark.set(true)
  else if (saved === '0') $q.dark.set(false)
}
