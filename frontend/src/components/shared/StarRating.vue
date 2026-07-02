<template>
  <div class="star-rating" :class="{ 'star-rating--readonly': readonly, 'star-rating--sm': size === 'sm', 'star-rating--lg': size === 'lg' }">
    <button
      v-for="n in 5"
      :key="n"
      type="button"
      class="star-rating__star"
      :class="{
        'star-rating__star--filled': n <= (hoverValue || modelValue),
        'star-rating__star--hover': !readonly && hoverValue >= n,
      }"
      :disabled="readonly"
      @mouseenter="onHover(n)"
      @mouseleave="onLeave"
      @click="onSelect(n)"
      :aria-label="`${n} estrela${n > 1 ? 's' : ''}`"
    >
      <q-icon name="star" />
    </button>
    <span v-if="showLabel && modelValue" class="star-rating__label">
      {{ modelValue }} de 5
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 0 },
  readonly: { type: Boolean, default: false },
  size: { type: String, default: 'md' },
  showLabel: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

const hoverValue = ref(0)

function onHover(n) {
  if (!props.readonly) hoverValue.value = n
}

function onLeave() {
  hoverValue.value = 0
}

function onSelect(n) {
  if (!props.readonly) emit('update:modelValue', n)
}
</script>

<style scoped>
.star-rating {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}
.star-rating__star {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: var(--od-text-5);
  transition: color 0.15s, transform 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.star-rating__star--filled {
  color: #f59e0b;
}
.star-rating__star--hover {
  transform: scale(1.15);
}
.star-rating__star:disabled {
  cursor: default;
}
.star-rating__star:disabled.star-rating__star--hover {
  transform: none;
}
.star-rating--sm .star-rating__star q-icon {
  font-size: 14px;
}
.star-rating--md .star-rating__star q-icon {
  font-size: 22px;
}
.star-rating--lg .star-rating__star q-icon {
  font-size: 32px;
}
.star-rating__label {
  margin-left: 8px;
  font-size: 13px;
  color: var(--od-text-3);
  font-weight: 500;
}
</style>
