// ── Público ───────────────────────────────
// { path: '/login', name: 'login', component: () => import('pages/LoginPage.vue'), meta: { guest: true } },

const studentRoutes = {
  path: '/students',
  component: () => import('layouts/StudentLayout.vue'),
  // meta: { role: 'student' },
  children: [
    { path: '', redirect: '/students/initial' },
    { path: 'initial', name: 'student-initial', component: () => import('pages/students/InitialPage.vue') },
    // { path: 'cursos',      name: 'student-cursos',    component: () => import('pages/student/MeusCursosPage.vue')    },
    // { path: 'explorar',    name: 'student-explorar',  component: () => import('pages/student/ExplorarPage.vue')      },
    // { path: 'progresso',   name: 'student-progresso', component: () => import('pages/student/ProgressoPage.vue')     },
    // { path: 'certificados',name: 'student-certs',     component: () => import('pages/student/CertificadosPage.vue')  },
    // { path: 'cursos/:id/assistir', name: 'student-assistir', component: () => import('pages/student/AssistirPage.vue') }
  ]
}

const coursesRoutes = {
  path: '/courses',
  component: () => import('layouts/CoursesLayout.vue'),
  meta: { guest: true },
  children: [
    { path: '', redirect: '/courses/initial' },
    { path: 'initial', name: 'course-initial', component: () => import('pages/courses/InitialPage.vue') },
    { path: 'new',     name: 'course-new',     component: () => import('pages/courses/CourseAdd.vue')    },
    { path: 'lista',   name: 'course-lista',   component: () => import('pages/courses/ListPage.vue')    },
  ]
}

const loginRoutes = {
  path: '/login',
  component: () => import('layouts/MainLayout.vue'),
  meta: { guest: true },
  children: [
    { path: '', name: 'login', component: () => import('pages/LoginPage.vue') }
  ]
}

const registerRoutes = {
  path: '/register',
  component: () => import('layouts/MainLayout.vue'),
  meta: { guest: true },
  children: [
    { path: '', name: 'register', component: () => import('pages/RegisterPage.vue') }
  ]
}

const citiesRoutes = {
  path: '/cities',
  component: () => import('layouts/CoursesLayout.vue'),
  meta: { guest: true },
  children: [
    { path: '', redirect: '/cities/initial' },
    { path: 'initial', name: 'cities-initial', component: () => import('pages/cities/ListPage.vue') },
    { path: 'new',     name: 'cities-new',     component: () => import('pages/cities/AddPage.vue')  },
  ]
}

// const professorRoutes = {
//   path: '/professor',
//   component: () => import('layouts/ProfessorLayout.vue'),
//   meta: { role: 'professor' },
//   children: [
//     { path: '', redirect: 'dashboard' },
//     { path: 'dashboard',   name: 'prof-dashboard', component: () => import('pages/professor/DashboardPage.vue')   },
//     { path: 'cursos',      name: 'prof-cursos',    component: () => import('pages/professor/CursosPage.vue')      },
//     { path: 'cursos/novo', name: 'prof-novo',      component: () => import('pages/professor/NovoCursoPage.vue')   },
//     { path: 'cursos/:id',  name: 'prof-editar',    component: () => import('pages/professor/EditarCursoPage.vue') },
//     { path: 'students',      name: 'prof-students',    component: () => import('pages/professor/StudentsPage.vue')      },
//     { path: 'ganhos',      name: 'prof-ganhos',    component: () => import('pages/professor/GanhosPage.vue')      },
//     { path: 'config',      name: 'prof-config',    component: () => import('pages/professor/ConfigPage.vue')      }
//   ]
// }

// const adminRoutes = {
//   path: '/admin',
//   component: () => import('layouts/AdminLayout.vue'),
//   meta: { role: 'admin' },
//   children: [
//     { path: '', redirect: 'overview' },
//     { path: 'overview',  name: 'admin-overview',  component: () => import('pages/admin/OverviewPage.vue')  },
//     { path: 'cursos',    name: 'admin-cursos',    component: () => import('pages/admin/CursosPage.vue')    },
//     { path: 'usuarios',  name: 'admin-usuarios',  component: () => import('pages/admin/UsuariosPage.vue')  },
//     { path: 'analytics', name: 'admin-analytics', component: () => import('pages/admin/AnalyticsPage.vue') },
//     { path: 'campanhas', name: 'admin-campanhas', component: () => import('pages/admin/CampanhasPage.vue') },
//     { path: 'config',    name: 'admin-config',    component: () => import('pages/admin/ConfigPage.vue')    }
//   ]
// }

const mainRoutes = {
  path: '/',
  component: () => import('layouts/MainLayout.vue'),
  children: [
    { path: '',        name: 'home',        component: () => import('pages/IndexPage.vue')         },
    { path: 'cidades', name: 'cities-list', component: () => import('pages/cities/ListPage.vue')   },
  ]
}

const routes = [
  studentRoutes,
  coursesRoutes,
  citiesRoutes,
  loginRoutes,
  registerRoutes,
  // professorRoutes,
  // adminRoutes,
  mainRoutes,
  { path: '/:catchAll(.*)*', name: '404', component: () => import('pages/ErrorNotFound.vue') }
]

export default routes
