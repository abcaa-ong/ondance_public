<template>
  <q-card flat bordered class="od-metric-card od-card">
    <div class="od-metric-accent" :style="{ background: accentColor }" />
    <div class="od-metric-label">{{ label }}</div>
    <div class="od-metric-value od-display">{{ value }}</div>
    <div class="od-metric-change" :class="changeClass">
      {{ change }}
    </div>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label:       { type: String, required: true },
  value:       { type: [String, Number], required: true },
  change:      { type: String, default: '' },
  changeType:  { type: String, default: 'neutral' }, // 'up' | 'down' | 'neutral'
  accentColor: { type: String, default: 'var(--od-accent)' }
})

const changeClass = computed(() => ({
  'text-positive': props.changeType === 'up',
  'text-negative': props.changeType === 'down'
}))
</script>
