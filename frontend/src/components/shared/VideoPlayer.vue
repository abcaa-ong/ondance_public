<template>
  <div class="od-video-player">
    <div v-if="videoType === 'youtube'" class="od-video-youtube">
      <iframe
        :src="embedUrl"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        style="width: 100%; aspect-ratio: 16/9; border-radius: 12px;"
      />
    </div>
    <div v-else-if="videoType === 'vimeo'" class="od-video-vimeo">
      <iframe
        :src="embedUrl"
        frameborder="0"
        allow="autoplay; fullscreen; picture-in-picture"
        allowfullscreen
        style="width: 100%; aspect-ratio: 16/9; border-radius: 12px;"
      />
    </div>
    <div v-else-if="videoType === 'native'" class="od-video-native">
      <video
        ref="videoEl"
        :src="src"
        controls
        preload="metadata"
        style="width: 100%; aspect-ratio: 16/9; border-radius: 12px; background: #000;"
        @play="onPlay"
        @pause="onPause"
        @ended="onEnded"
        @loadedmetadata="onLoadedMetadata"
      />
    </div>
    <div v-else class="od-video-empty">
      <q-icon name="smart_display" size="64px" style="color: var(--od-text-5);" />
      <p style="color: var(--od-text-3); margin-top: 8px;">Nenhum vídeo disponível para esta aula.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  startPosition: { type: Number, default: 0 },
})

const emit = defineEmits(['timeupdate', 'ended', 'pause', 'complete'])

const videoEl = ref(null)
let saveInterval = null

const YOUTUBE_PATTERNS = [
  /(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/watch\?.*v=([\w-]{11})/,
  /(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/embed\/([\w-]{11})/,
  /(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/shorts\/([\w-]{11})/,
  /(?:https?:\/\/)?youtu\.be\/([\w-]{11})/,
]

const VIMEO_PATTERNS = [
  /(?:https?:\/\/)?(?:www\.)?vimeo\.com\/(\d+)/,
  /(?:https?:\/\/)?player\.vimeo\.com\/video\/(\d+)/,
]

function extractYouTubeId(url) {
  for (const pattern of YOUTUBE_PATTERNS) {
    const match = url.match(pattern)
    if (match) return match[1]
  }
  return null
}

function extractVimeoId(url) {
  for (const pattern of VIMEO_PATTERNS) {
    const match = url.match(pattern)
    if (match) return match[1]
  }
  return null
}

const videoType = computed(() => {
  if (!props.src) return 'empty'
  if (extractYouTubeId(props.src)) return 'youtube'
  if (extractVimeoId(props.src)) return 'vimeo'
  if (/\.(mp4|webm|ogg|mov)(\?.*)?$/i.test(props.src)) return 'native'
  if (props.src.startsWith('http')) return 'native'
  return 'empty'
})

const embedUrl = computed(() => {
  if (videoType.value === 'youtube') {
    const id = extractYouTubeId(props.src)
    return id ? `https://www.youtube.com/embed/${id}?rel=0&modestbranding=1` : ''
  }
  if (videoType.value === 'vimeo') {
    const id = extractVimeoId(props.src)
    return id ? `https://player.vimeo.com/video/${id}` : ''
  }
  return ''
})

function onPlay() {
  startSaveInterval()
}

function onPause() {
  stopSaveInterval()
  emitSave()
}

function onEnded() {
  stopSaveInterval()
  emit('complete')
  emit('ended')
}

function onLoadedMetadata() {
  if (props.startPosition > 0 && videoEl.value) {
    videoEl.value.currentTime = props.startPosition
  }
}

function emitSave() {
  if (!videoEl.value) return
  emit('timeupdate', {
    video_position: Math.floor(videoEl.value.currentTime),
    is_completed: false,
  })
}

function startSaveInterval() {
  stopSaveInterval()
  saveInterval = setInterval(emitSave, 10000)
}

function stopSaveInterval() {
  if (saveInterval) {
    clearInterval(saveInterval)
    saveInterval = null
  }
}

watch(() => props.src, () => {
  stopSaveInterval()
})

onBeforeUnmount(() => {
  stopSaveInterval()
  emitSave()
})
</script>

<style scoped>
.od-video-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  aspect-ratio: 16/9;
  background: var(--od-bg-surface, #1a1a2e);
  border-radius: 12px;
}
</style>