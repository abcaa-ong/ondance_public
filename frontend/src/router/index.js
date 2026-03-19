// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from 'stores/auth'

const routes = [
//   { path: '/login', name: 'login', component: () => import('pages/LoginPage.vue'), meta: { guest: true } },
  {
    path: '/alunos', component: () => import('layouts/AlunoLayout.vue'), // meta: { role: 'aluno' },
    children: [
      { path: '', redirect: '/alunos/inicio' },
      { path: 'inicio', name: 'aluno-inicio', component: () => import('pages/aluno/InicioPage.vue')},
      // { path: 'cursos', name: 'aluno-cursos', component: () => import('pages/aluno/MeusCursosPage.vue')}
    //   { path: 'explorar',       name: 'aluno-explorar',       component: () => import('pages/aluno/ExplorarPage.vue')       },
    //   { path: 'progresso',      name: 'aluno-progresso',      component: () => import('pages/aluno/ProgressoPage.vue')      },
    //   { path: 'certificados',   name: 'aluno-certificados',   component: () => import('pages/aluno/CertificadosPage.vue')   },
    //   { path: 'configuracoes',  name: 'aluno-config',         component: () => import('pages/aluno/ConfiguracoesPage.vue')  },
    //   { path: 'cursos/:id/assistir', name: 'aluno-assistir', component: () => import('pages/aluno/AssistirPage.vue')       }
    ]
  },

  {
    path: '/curses', component: () => import('layouts/CursesLayout.vue'), meta: { guest: true },
    children: [
      { path: '', redirect: '/curses/initial' },
      { path: 'initial', name: 'curse-initial', component: () => import('pages/curses/InitialPage.vue')},
      { path: 'new',    name: 'curse-new',    component: () => import('pages/curses/CurseAdd.vue')    },
      { path: 'lista',  name: 'curse-lista',  component: () => import('pages/curses/ListPage.vue')     },
    ]
  },

  //   {
//     path: '/professor', component: () => import('layouts/ProfessorLayout.vue'), meta: { role: 'professor' },
//     children: [
//       { path: '', redirect: 'dashboard' },
//       { path: 'dashboard',   name: 'prof-dashboard', component: () => import('pages/professor/DashboardPage.vue')   },
//       { path: 'cursos',      name: 'prof-cursos',    component: () => import('pages/professor/CursosPage.vue')      },
//       { path: 'cursos/novo', name: 'prof-novo',      component: () => import('pages/professor/NovoCursoPage.vue')   },
//       { path: 'cursos/:id',  name: 'prof-editar',    component: () => import('pages/professor/EditarCursoPage.vue') },
//       { path: 'alunos',      name: 'prof-alunos',    component: () => import('pages/professor/AlunosPage.vue')      },
//       { path: 'ganhos',      name: 'prof-ganhos',    component: () => import('pages/professor/GanhosPage.vue')      },
//       { path: 'config',      name: 'prof-config',    component: () => import('pages/professor/ConfigPage.vue')      }
//     ]
//   },

//   {
//     path: '/admin', component: () => import('layouts/AdminLayout.vue'), meta: { role: 'admin' },
//     children: [
//       { path: '', redirect: 'overview' },
//       { path: 'overview',  name: 'admin-overview',  component: () => import('pages/admin/OverviewPage.vue')   },
//       { path: 'cursos',    name: 'admin-cursos',    component: () => import('pages/admin/CursosPage.vue')     },
//       { path: 'usuarios',  name: 'admin-usuarios',  component: () => import('pages/admin/UsuariosPage.vue')   },
//       { path: 'analytics', name: 'admin-analytics', component: () => import('pages/admin/AnalyticsPage.vue')  },
//       { path: 'campanhas', name: 'admin-campanhas', component: () => import('pages/admin/CampanhasPage.vue')  },
//       { path: 'config',    name: 'admin-config',    component: () => import('pages/admin/ConfigPage.vue')     }
//     ]
//   },

//   { path: '/', redirect: '/login' },
  {
    path: '/', component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  { path: '/:catchAll(.*)*', name: '404', component: () => import('pages/ErrorNotFound.vue') }

]




const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ left: 0, top: 0 })
})

// router.beforeEach(async (to) => {
//   const auth = useAuthStore()
//   if (to.meta.guest) return auth.isAuthenticated ? auth.homeRoute : true
//   if (to.name === '404') return true
//   if (!auth.isAuthenticated) return '/login'
//   if (!auth.user) await auth.fetchMe()
//   if (to.meta.role && auth.user?.role !== to.meta.role) return auth.homeRoute
//   return true
// })

export default router
