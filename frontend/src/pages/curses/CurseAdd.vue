<template>
  <q-page class="q-pa-lg">

    <!-- Header -->
    <div class="row items-center q-mb-lg" style="gap: 12px;">
      <q-btn flat round dense icon="arrow_back" :style="{ color: 'var(--od-text-2)' }" @click="$router.push('/curses/initial')" />
      <div>
        <div class="od-display" style="font-size: 22px; color: var(--od-text-1);">Novo Curso</div>
        <p style="color: var(--od-text-3); margin: 2px 0 0; font-size: 13px;">Preencha as informações e monte a estrutura do curso</p>
      </div>
    </div>

    <div class="row q-gutter-md">

      <!-- Coluna principal -->
      <div class="col-12 col-md-8">
        <q-form @submit.prevent="handleSubmit">

          <!-- Informações do curso -->
          <q-card flat bordered class="od-card q-mb-md">
            <q-card-section>
              <div class="od-card-title od-display q-mb-md">Informações do curso</div>
              <div class="column q-gutter-sm">
                <q-input
                  v-model="form.title"
                  outlined dense
                  label="Título *"
                  :rules="[val => !!val || 'Campo obrigatório']"
                />
                <q-input
                  v-model="form.teacher"
                  outlined dense
                  label="Professor *"
                  :rules="[val => !!val || 'Campo obrigatório']"
                />
                <q-input
                  v-model="form.description"
                  outlined dense
                  type="textarea"
                  label="Descrição"
                  rows="3"
                />
                <div class="row q-gutter-sm">
                  <q-input
                    v-model="form.duration"
                    outlined dense
                    label="Duração (ex: 4 semanas)"
                    class="col"
                  />
                  <q-select
                    v-model="form.level"
                    outlined dense
                    :options="levelOptions"
                    label="Nível *"
                    class="col"
                    :rules="[val => !!val || 'Campo obrigatório']"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Módulos e Aulas -->
          <q-card flat bordered class="od-card q-mb-md">
            <q-card-section>
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="od-card-title od-display">Módulos e Aulas</div>
                  <div style="font-size: 12px; margin-top: 2px; color: var(--od-text-4);">
                    {{ totalLessons }} aula{{ totalLessons !== 1 ? 's' : '' }} em {{ modules.length }} módulo{{ modules.length !== 1 ? 's' : '' }}
                  </div>
                </div>
                <q-btn
                  unelevated no-caps dense
                  icon="add"
                  label="Módulo"
                  :style="{ background: 'var(--od-bg-subtle)', color: 'var(--od-text-2)', borderRadius: '8px', fontSize: '12px' }"
                  @click="addModule"
                />
              </div>

              <!-- Lista de módulos -->
              <div v-if="modules.length === 0" class="text-center q-py-lg">
                <q-icon name="view_module" size="36px" :style="{ color: 'var(--od-text-5)' }" />
                <p style="font-size: 13px; margin: 8px 0 0; color: var(--od-text-5);">Nenhum módulo adicionado ainda</p>
              </div>

              <div v-for="(mod, mIdx) in modules" :key="mod.id" class="q-mb-sm">
                <div
                  class="row items-center q-px-sm q-py-xs"
                  :style="{ background: 'var(--od-bg-page)', borderRadius: '8px 8px 0 0', border: '0.5px solid var(--od-border)' }"
                >
                  <!-- Número do módulo -->
                  <div style="font-size: 11px; min-width: 24px; font-weight: 600; color: var(--od-text-4);">
                    {{ mIdx + 1 }}
                  </div>

                  <!-- Input do título do módulo -->
                  <q-input
                    v-model="mod.title"
                    borderless dense
                    placeholder="Nome do módulo"
                    class="col"
                    style="font-size: 13px; font-weight: 500;"
                    :input-style="{ color: 'var(--od-text-1)', padding: '0' }"
                  />

                  <!-- Ações do módulo -->
                  <q-btn flat round dense icon="add" size="xs" :style="{ color: 'var(--od-text-4)' }" @click="addLesson(mod)">
                    <q-tooltip>Adicionar aula</q-tooltip>
                  </q-btn>
                  <q-btn flat round dense icon="delete_outline" size="xs" :style="{ color: 'var(--od-text-5)' }" @click="removeModule(mIdx)">
                    <q-tooltip>Remover módulo</q-tooltip>
                  </q-btn>
                </div>

                <!-- Aulas do módulo -->
                <div :style="{ border: '0.5px solid var(--od-border)', borderTop: 'none', borderRadius: '0 0 8px 8px', overflow: 'hidden' }">
                  <div
                    v-for="(lesson, lIdx) in mod.lessons"
                    :key="lesson.id"
                    class="row items-center q-px-sm q-py-xs"
                    :style="{ borderTop: '0.5px solid var(--od-border-light)', gap: '8px' }"
                  >
                    <q-icon name="play_circle_outline" size="14px" :style="{ color: 'var(--od-text-5)', marginLeft: '16px' }" />
                    <q-input
                      v-model="lesson.title"
                      borderless dense
                      :placeholder="`Aula ${lIdx + 1}`"
                      class="col"
                      style="font-size: 12.5px;"
                      :input-style="{ color: 'var(--od-text-2)', padding: '0' }"
                    />
                    <q-btn flat round dense icon="close" size="xs" :style="{ color: 'var(--od-text-5)' }" @click="removeLesson(mod, lIdx)" />
                  </div>

                  <!-- Botão inline de nova aula -->
                  <div
                    class="row items-center q-px-sm q-py-xs"
                    style="cursor: pointer; gap: 8px;"
                    @click="addLesson(mod)"
                  >
                    <q-icon name="add" size="14px" :style="{ color: 'var(--od-text-5)', marginLeft: '16px' }" />
                    <span style="font-size: 12px; color: var(--od-text-4);">Adicionar aula</span>
                  </div>
                </div>
              </div>

            </q-card-section>
          </q-card>

          <!-- Ações -->
          <div class="row q-gutter-sm justify-end">
            <q-btn
              flat no-caps
              label="Cancelar"
              style="color: var(--od-text-3);"
              @click="$router.push('/curses/initial')"
            />
            <q-btn
              unelevated no-caps
              label="Salvar rascunho"
              :style="{ background: 'var(--od-bg-subtle)', color: 'var(--od-text-2)', borderRadius: '8px' }"
              @click="saveDraft"
            />
            <q-btn
              unelevated no-caps
              type="submit"
              label="Publicar curso"
              :loading="saving"
              style="background: var(--od-accent); color: #fff; border-radius: 8px; font-weight: 500;"
            />
          </div>

        </q-form>
      </div>

      <!-- Coluna lateral -->
      <div class="col column q-gutter-md">

        <!-- Preview -->
        <q-card flat class="od-card" style="background: var(--od-accent) !important; border: none !important;">
          <q-card-section>
            <div style="font-size: 11px; color: rgba(255,255,255,0.5); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">
              Preview
            </div>
            <div class="od-display" style="font-size: 18px; color: #fff; margin-bottom: 4px;">
              {{ form.title || 'Título do curso' }}
            </div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.65); margin-bottom: 10px;">
              {{ form.teacher || 'Professor' }}
            </div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.5); line-height: 1.9;">
              <div v-if="form.level">Nível: {{ form.level }}</div>
              <div v-if="form.duration">{{ form.duration }}</div>
              <div v-if="modules.length">{{ modules.length }} módulo{{ modules.length !== 1 ? 's' : '' }} · {{ totalLessons }} aula{{ totalLessons !== 1 ? 's' : '' }}</div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Estrutura resumida -->
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-sm">Estrutura</div>

            <div v-if="modules.length === 0" style="font-size: 12px; text-align: center; padding: 12px 0; color: var(--od-text-5);">
              Nenhum módulo ainda
            </div>

            <div v-for="(mod, mIdx) in modules" :key="mod.id" class="q-mb-xs">
              <div style="font-size: 12px; font-weight: 600; margin-bottom: 2px; color: var(--od-text-2);">
                {{ mIdx + 1 }}. {{ mod.title || 'Módulo sem título' }}
              </div>
              <div style="font-size: 11.5px; padding-left: 12px; color: var(--od-text-4);">
                {{ mod.lessons.length }} aula{{ mod.lessons.length !== 1 ? 's' : '' }}
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Checklist -->
        <q-card flat bordered class="od-card">
          <q-card-section>
            <div class="od-card-title od-display q-mb-sm">Checklist</div>
            <div
              v-for="item in checklist"
              :key="item.label"
              class="row items-center q-py-xs"
              style="gap: 8px; font-size: 12.5px;"
            >
              <q-icon
                :name="item.done ? 'check_circle' : 'radio_button_unchecked'"
                size="16px"
                :style="{ color: item.done ? '#1D9E75' : 'var(--od-text-5)' }"
              />
              <span :style="{ color: item.done ? 'var(--od-text-2)' : 'var(--od-text-4)' }">{{ item.label }}</span>
            </div>
          </q-card-section>
        </q-card>

      </div>
    </div>

  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'

const saving = ref(false)
let nextId = 1

const form = ref({
  title:       '',
  teacher:     '',
  description: '',
  duration:    '',
  level:       null,
})

const modules = ref([])

const levelOptions = ['Iniciante', 'Intermediário', 'Avançado']

const totalLessons = computed(() =>
  modules.value.reduce((sum, mod) => sum + mod.lessons.length, 0)
)

const checklist = computed(() => [
  { label: 'Título preenchido',     done: !!form.value.title },
  { label: 'Professor definido',    done: !!form.value.teacher },
  { label: 'Descrição adicionada',  done: !!form.value.description },
  { label: 'Nível selecionado',     done: !!form.value.level },
  { label: 'Ao menos 1 módulo',     done: modules.value.length > 0 },
  { label: 'Ao menos 1 aula',       done: totalLessons.value > 0 },
])

function addModule () {
  modules.value.push({ id: nextId++, title: '', lessons: [] })
}

function removeModule (mIdx) {
  modules.value.splice(mIdx, 1)
}

function addLesson (mod) {
  mod.lessons.push({ id: nextId++, title: '' })
}

function removeLesson (mod, lIdx) {
  mod.lessons.splice(lIdx, 1)
}

function saveDraft () {
  console.log('rascunho:', { ...form.value, modules: modules.value })
  // TODO: integrar com API
}

async function handleSubmit () {
  saving.value = true
  try {
    console.log('publicando:', { ...form.value, modules: modules.value })
    // TODO: integrar com API
  } finally {
    saving.value = false
  }
}
</script>
