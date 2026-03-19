const routes = [

  // ── Público ───────────────────────────────
  // {
  //   path: '/login',
  //   name: 'login',
  //   component: () => import('pages/LoginPage.vue'),
  //   meta: { guest: true }
  // },

    // ── Aluno ─────────────────────────────────
  {
    path: '/alunos',
    component: () => import('layouts/AlunoLayout.vue'),
    // meta: { role: 'aluno' },
    children: [
      { path: '', name: 'aluno-inicio', component: () => import('pages/aluno/InicioPage.vue') },
      { path: '/cursos',  name: 'aluno-cursos',   component: () => import('pages/aluno/MeusCursosPage.vue') },
      // { path: 'explorar',name: 'aluno-explorar', component: () => import('pages/aluno/ExplorarPage.vue') },
      // { path: 'progresso',name:'aluno-progresso',component: () => import('pages/aluno/ProgressoPage.vue') },
      // { path: 'cursos/:id/assistir', name: 'aluno-assistir', component: () => import('pages/aluno/AssistirPage.vue') },
      // { path: 'certificados', name: 'aluno-certificados', component: () => import('pages/aluno/CertificadosPage.vue') }
    ]
  },



  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
