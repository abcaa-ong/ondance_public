<template>
  <q-page class="q-pa-lg">
    <div class="q-mb-lg">
      <div class="od-display" style="font-size: 24px; color: var(--od-text-1);">Meus Cursos</div>
      <p style="color: var(--od-text-3); margin: 4px 0 0; font-size: 14px;">Cursos em que você está matriculado</p>
    </div>
    <q-card flat bordered class="od-card">
      <q-card-section class="text-center q-py-xl">
        <q-icon name="play_circle" size="48px" style="color: var(--od-text-5);" />
        <p style="margin-top: 12px; color: var(--od-text-3);">Suas matrículas aparecerão aqui</p>
        <q-btn unelevated no-caps label="Explorar cursos" to="/student/explorar"
          style="background: var(--od-accent); color: #fff; border-radius: 8px; margin-top: 8px;" />
      </q-card-section>
    </q-card>
  </q-page>
</template>
