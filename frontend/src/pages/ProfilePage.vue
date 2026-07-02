<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Meu Perfil</div>
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Perfil do Aluno</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Gerencie suas informações pessoais</p>
    </div>

    <div class="row q-gutter-md">

      <!-- Coluna do avatar -->
      <div class="col-12 col-md-3">
        <q-card flat bordered class="od-card text-center q-pa-lg">
          <div class="avatar-wrapper" @click="triggerFileInput">
            <q-avatar size="96px" :style="{ background: 'var(--od-accent)', fontSize: '36px', color: '#fff' }">
              <img v-if="photoPreview" :src="photoPreview" style="object-fit: cover;" />
              <span v-else>{{ initials }}</span>
            </q-avatar>
            <div class="avatar-overlay">
              <q-icon name="camera_alt" size="18px" color="white" />
            </div>
          </div>
          <input ref="fileInput" type="file" accept="image/*" style="display: none;" @change="onFileChange" />

          <div style="margin-top: 12px; font-size: 12px; color: var(--od-text-4);">
            Clique para alterar
          </div>
          <div style="font-size: 14px; font-weight: 600; color: var(--od-text-1); margin-top: 8px;">
            {{ form.name || '—' }}
          </div>
          <div style="font-size: 12px; color: var(--od-text-3); margin-top: 2px;">
            {{ form.email }}
          </div>
        </q-card>
      </div>

      <!-- Coluna do formulário -->
      <div class="col">
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="form-grid">
              <q-input
                :model-value="form.email"
                label="E-mail"
                outlined dense disable
                :style="inputStyle"
              />
              <q-input
                v-model="form.name"
                label="Nome completo"
                outlined dense
                :style="inputStyle"
              />
              <q-select
                v-model="selectedState"
                :options="stateOptions"
                label="Estado"
                outlined dense
                emit-value map-options
                popup-content-style="max-height:250px;overflow-y:auto"
                :style="inputStyle"
                @update:model-value="onStateChange"
              />
              <q-input
                v-model="form.celular"
                label="Celular"
                outlined dense
                mask="(##) #####-####"
                unmasked-value
                :style="inputStyle"
              />
              <q-input
                v-model="form.telephone"
                label="Telefone"
                outlined dense
                mask="(##) ####-####"
                unmasked-value
                :style="inputStyle"
              />
              <q-input
                v-model="form.birthday"
                label="Data de nascimento"
                outlined dense
                type="date"
                stack-label
                :style="inputStyle"
              />
              <q-select
                v-model="form.city"
                :options="filteredCityOptions"
                label="Cidade"
                outlined dense
                use-input
                input-debounce="300"
                emit-value map-options
                popup-content-style="max-height:250px;overflow-y:auto"
                :disable="!selectedState || loadingCities"
                :loading="loadingCities"
                :style="inputStyle"
                @filter="filterCities"
              />
            </div>
            <div v-if="errorMsg" style="margin-top: 12px; font-size: 13px; color: #e53935;">
              {{ errorMsg }}
            </div>
          </q-card-section>
          <q-card-actions class="q-px-md q-pb-md">
            <q-space />
            <q-btn
              unelevated no-caps
              label="Salvar alterações"
              :loading="loading"
              style="background: var(--od-accent); color: #fff; border-radius: 8px; font-weight: 500;"
              @click="save"
            />
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <!-- Cursos em andamento -->
    <div class="q-mt-lg">
      <div class="od-display" style="font-size: 18px; color: var(--od-text-1); margin-bottom: 12px;">Cursos em andamento</div>

      <div v-if="loadingCourses" class="row q-gutter-md">
        <q-card v-for="n in 2" :key="n" flat bordered class="od-card" style="width: 260px;">
          <q-card-section>
            <q-skeleton type="rect" height="40px" style="border-radius: 8px;" class="q-mb-sm" />
            <q-skeleton type="text" width="50%" />
          </q-card-section>
        </q-card>
      </div>

      <q-card v-else-if="inProgressCourses.length === 0" flat bordered class="od-card">
        <q-card-section class="text-center q-py-lg">
          <q-icon name="play_circle_outline" size="36px" style="color: var(--od-text-5);" />
          <p style="margin-top: 8px; color: var(--od-text-4); font-size: 13px;">Você não tem cursos em andamento</p>
          <q-btn flat no-caps label="Explorar cursos" to="/student/explorar" style="color: var(--od-accent);" />
        </q-card-section>
      </q-card>

      <div v-else class="row q-gutter-md">
        <q-card
          v-for="enrollment in inProgressCourses"
          :key="enrollment.id"
          flat bordered
          class="od-card"
          style="width: 260px; cursor: pointer; transition: box-shadow 0.15s;"
          @click="$router.push(`/student/courses/${enrollment.course}/assistir`)"
        >
          <q-card-section style="padding: 16px;">
            <div class="row items-center q-mb-sm" style="gap: 8px;">
              <div
                v-if="enrollment.course_emoji || enrollment.course_thumb_bg"
                class="row items-center justify-center"
                :style="{ width: '32px', height: '32px', borderRadius: '8px', background: enrollment.course_thumb_bg || 'var(--od-accent)', fontSize: '16px', flexShrink: '0' }"
              >
                {{ enrollment.course_emoji || '🎓' }}
              </div>
              <div class="od-display ellipsis" style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">
                {{ enrollment.course_title }}
              </div>
            </div>
            <div v-if="enrollment.course_level" style="font-size: 12px; color: var(--od-text-4); margin-bottom: 8px;">
              {{ enrollment.course_level }}
            </div>
            <q-linear-progress
              :value="enrollment.progress_percent / 100"
              color="accent"
              size="6px"
              style="border-radius: 3px; margin-bottom: 4px;"
            />
            <span style="font-size: 12px; color: var(--od-text-4);">{{ enrollment.progress_percent }}% concluído</span>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Cursos concluídos -->
    <div class="q-mt-lg">
      <div class="od-display" style="font-size: 18px; color: var(--od-text-1); margin-bottom: 12px;">Cursos concluídos</div>

      <div v-if="loadingCourses" class="row q-gutter-md">
        <q-card v-for="n in 2" :key="n" flat bordered class="od-card" style="width: 260px;">
          <q-card-section>
            <q-skeleton type="rect" height="40px" style="border-radius: 8px;" class="q-mb-sm" />
            <q-skeleton type="text" width="50%" />
          </q-card-section>
        </q-card>
      </div>

      <q-card v-else-if="completedCourses.length === 0" flat bordered class="od-card">
        <q-card-section class="text-center q-py-lg">
          <q-icon name="check_circle_outline" size="36px" style="color: var(--od-text-5);" />
          <p style="margin-top: 8px; color: var(--od-text-4); font-size: 13px;">Você ainda não concluiu nenhum curso</p>
        </q-card-section>
      </q-card>

      <div v-else class="row q-gutter-md">
        <q-card
          v-for="enrollment in completedCourses"
          :key="enrollment.id"
          flat bordered
          class="od-card"
          style="width: 260px; cursor: pointer; transition: box-shadow 0.15s;"
          @click="$router.push(`/student/courses/${enrollment.course}/assistir`)"
        >
          <q-card-section style="padding: 16px;">
            <div class="row items-center q-mb-sm" style="gap: 8px;">
              <div
                v-if="enrollment.course_emoji || enrollment.course_thumb_bg"
                class="row items-center justify-center"
                :style="{ width: '32px', height: '32px', borderRadius: '8px', background: enrollment.course_thumb_bg || 'var(--od-accent)', fontSize: '16px', flexShrink: '0' }"
              >
                {{ enrollment.course_emoji || '🎓' }}
              </div>
              <div class="od-display ellipsis" style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">
                {{ enrollment.course_title }}
              </div>
            </div>
            <div v-if="enrollment.course_level" style="font-size: 12px; color: var(--od-text-4); margin-bottom: 8px;">
              {{ enrollment.course_level }}
            </div>
            <q-badge color="positive" label="Concluído" style="font-size: 10px;" />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Certificados -->
    <div class="q-mt-lg">
      <div class="od-display" style="font-size: 18px; color: var(--od-text-1); margin-bottom: 12px;">Certificados</div>

      <div v-if="loadingCertificates" class="row q-gutter-md">
        <q-card v-for="n in 2" :key="n" flat bordered class="od-card" style="width: 260px;">
          <q-card-section>
            <q-skeleton type="rect" height="40px" style="border-radius: 8px;" class="q-mb-sm" />
            <q-skeleton type="text" width="50%" />
          </q-card-section>
        </q-card>
      </div>

      <q-card v-else-if="certificates.length === 0" flat bordered class="od-card">
        <q-card-section class="text-center q-py-lg">
          <q-icon name="workspace_premium" size="36px" style="color: var(--od-text-5);" />
          <p style="margin-top: 8px; color: var(--od-text-4); font-size: 13px;">Você ainda não possui certificados</p>
        </q-card-section>
      </q-card>

      <div v-else class="row q-gutter-md">
        <q-card
          v-for="cert in certificates"
          :key="cert.id"
          flat bordered
          class="od-card"
          style="width: 260px; cursor: pointer; transition: box-shadow 0.15s;"
          @click="$router.push('/student/certificados')"
        >
          <q-card-section style="padding: 16px;">
            <div class="row items-center q-mb-sm" style="gap: 8px;">
              <q-icon name="workspace_premium" size="24px" style="color: var(--od-accent); flex-shrink: 0;" />
              <div class="od-display ellipsis" style="font-size: 14px; font-weight: 600; color: var(--od-text-1);">
                {{ cert.course_title }}
              </div>
            </div>
            <div style="font-size: 12px; color: var(--od-text-4); margin-bottom: 4px;">
              {{ cert.course_level }} · {{ cert.course_workload }}h
            </div>
            <div style="font-size: 11px; color: var(--od-text-5);">
              Emitido em {{ formatDate(cert.issue_date) }} · {{ cert.code }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { profileService } from 'src/services/profile'
import { stateService } from 'src/services/state'
import { cityService } from 'src/services/city'
import { courseService } from 'src/services/course'
import { certificateService } from 'src/services/certificate'
import { useAuth } from 'src/composables/useAuth'

const $q = useQuasar()
const router = useRouter()
const { user } = useAuth()

const roleHome = { admin: '/admin/overview', professor: '/teacher/dashboard', aluno: '/student/dashboard' }

const fileInput = ref(null)
const loading = ref(false)
const loadingCities = ref(false)
const errorMsg = ref('')
const photoFile = ref(null)
const photoPreview = ref(null)
const states = ref([])
const cities = ref([])
const selectedState = ref(null)

const form = ref({
  email: '',
  name: '',
  celular: '',
  telephone: '',
  birthday: '',
  city: null,
})

const enrollments = ref([])
const loadingCourses = ref(true)
const inProgressCourses = computed(() => enrollments.value.filter(e => !e.is_completed))
const completedCourses = computed(() => enrollments.value.filter(e => e.is_completed))

const certificates = ref([])
const loadingCertificates = ref(true)

const inputStyle = 'border-radius: 8px;'

const initials = computed(() => {
  const name = form.value.name || form.value.email || ''
  return name.charAt(0).toUpperCase()
})

const stateOptions = computed(() =>
  states.value.map(s => ({ label: `${s.name} (${s.abbreviation})`, value: s.abbreviation }))
)

const cityOptions = computed(() =>
  cities.value.map(c => ({ label: c.name, value: c.id }))
)

const filteredCityOptions = ref([])

watch(cityOptions, (opts) => { filteredCityOptions.value = opts }, { immediate: true })

async function filterCities(val, update, abort) {
  if (!val || val.length < 2) {
    update(() => { filteredCityOptions.value = cityOptions.value })
    return
  }
  try {
    const { data } = await cityService.list({ state: selectedState.value, search: val, page_size: 50 })
    const results = data.results ?? data
    update(() => {
      filteredCityOptions.value = results.map(c => ({ label: c.name, value: c.id }))
    })
  } catch {
    abort()
  }
}


onMounted(async () => {
  await Promise.all([loadProfile(), loadStates(), loadEnrollments(), loadCertificates()])
})

async function loadEnrollments() {
  loadingCourses.value = true
  try {
    const resp = await courseService.enrollments()
    enrollments.value = resp.data.results ?? resp.data
  } catch {
    enrollments.value = []
  } finally {
    loadingCourses.value = false
  }
}

async function loadCertificates() {
  loadingCertificates.value = true
  try {
    const resp = await certificateService.list()
    certificates.value = resp.data.results ?? resp.data
  } catch {
    certificates.value = []
  } finally {
    loadingCertificates.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR')
}

async function loadProfile() {
  try {
    const { data } = await profileService.get()
    form.value.email     = data.email     || ''
    form.value.name      = data.name      || ''
    form.value.celular   = data.celular   || ''
    form.value.telephone = data.telephone || ''
    form.value.birthday  = data.birthday  || ''
    form.value.city      = data.city      || null
    photoPreview.value   = data.photo     || null

    if (data.city_detail?.state) {
      selectedState.value = data.city_detail.state
      await loadCities(data.city_detail.state)
      // garante que a cidade salva está na lista mesmo que fora da primeira página
      if (data.city && !cities.value.find(c => c.id === data.city)) {
        cities.value.push({ id: data.city, name: data.city_detail.name })
      }
    }
  } catch {
    // silencia
  }
}

async function loadStates() {
  try {
    const { data } = await stateService.list()
    states.value = data.results ?? data
  } catch {
    // silencia
  }
}

async function onStateChange(abbr) {
  form.value.city = null
  cities.value = []
  if (abbr) await loadCities(abbr)
}

async function loadCities(abbr) {
  loadingCities.value = true
  try {
    const { data } = await cityService.list({ state: abbr })
    cities.value = data.results ?? data
  } finally {
    loadingCities.value = false
  }
}

function triggerFileInput() {
  fileInput.value.click()
}

function onFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  photoFile.value = file
  photoPreview.value = URL.createObjectURL(file)
}

async function save() {
  loading.value = true
  errorMsg.value = ''

  try {
    const fd = new FormData()
    fd.append('name', form.value.name)
    if (form.value.celular)   fd.append('celular', form.value.celular)
    if (form.value.telephone) fd.append('telephone', form.value.telephone)
    if (form.value.birthday)  fd.append('birthday', form.value.birthday)
    if (form.value.city)      fd.append('city', form.value.city)
    if (photoFile.value)      fd.append('photo', photoFile.value)

    const { data } = await profileService.update(fd)
    localStorage.setItem('profile_complete', data.profile_complete ? 'true' : 'false')
    photoFile.value = null
    $q.notify({ type: 'positive', message: 'Perfil atualizado com sucesso!', position: 'top', timeout: 2000 })
    router.push(roleHome[user.value?.role] ?? '/student/dashboard')
  } catch {
    errorMsg.value = 'Erro ao salvar. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}
</style>
