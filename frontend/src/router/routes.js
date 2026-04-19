const studentRoutes = {
  path: '/student',
  component: () => import('layouts/StudentLayout.vue'),
  meta: { role: 'aluno' },
  children: [
    { path: '',             redirect: '/student/dashboard' },
    { path: 'dashboard',       name: 'student-dashboard',       component: () => import('pages/student/DashboardPage.vue') },
    { path: 'my-courses',  name: 'student-my-courses',  component: () => import('pages/student/MyCoursesPage.vue') },
    { path: 'courses/:id/assistir', name: 'student-assistir', component: () => import('pages/student/AssistirPage.vue') },
    { path: 'progresso',    name: 'student-progresso',    component: () => import('pages/student/ProgressoPage.vue') },
    { path: 'certificados', name: 'student-certificados', component: () => import('pages/student/CertificadosPage.vue') },
    { path: 'explorar',     name: 'student-explorar',     component: () => import('pages/student/ExplorarPage.vue') },
    { path: 'configuracoes',name: 'student-config',       component: () => import('pages/student/ConfigPage.vue') },
  ]
}

const teacherRoutes = {
  path: '/teacher',
  component: () => import('layouts/TeacherLayout.vue'),
  meta: { role: 'professor' },
  children: [
    { path: '',                    redirect: '/teacher/dashboard' },
    { path: 'dashboard',           name: 'teacher-dashboard', component: () => import('pages/teacher/DashboardPage.vue') },
    { path: 'courses',              name: 'teacher-courses',    component: () => import('pages/teacher/CoursesPage.vue') },
    { path: 'courses/new',         name: 'teacher-new',      component: () => import('pages/courses/CourseAdd.vue') },
    { path: 'courses/:id/editar',   name: 'teacher-editar',    component: () => import('pages/teacher/EditarCursoPage.vue') },
    { path: 'courses/:id/aulas',    name: 'teacher-aulas',     component: () => import('pages/teacher/AulasPage.vue') },
    { path: 'students',            name: 'teacher-students',  component: () => import('pages/teacher/StudentsPage.vue') },
    { path: 'ganhos',              name: 'teacher-ganhos',    component: () => import('pages/teacher/GanhosPage.vue') },
    { path: 'config',              name: 'teacher-config',    component: () => import('pages/teacher/ConfigPage.vue') },
  ]
}

const adminRoutes = {
  path: '/admin',
  component: () => import('layouts/AdminLayout.vue'),
  meta: { role: 'admin' },
  children: [
    { path: '',            redirect: '/admin/overview' },
    { path: 'overview',   name: 'admin-overview',   component: () => import('pages/admin/OverviewPage.vue') },
    { path: 'courses',    name: 'admin-courses',    component: () => import('pages/admin/CoursesPage.vue') },
    { path: 'usuarios',   name: 'admin-usuarios',   component: () => import('pages/admin/UsuariosPage.vue') },
    { path: 'analytics',  name: 'admin-analytics',  component: () => import('pages/admin/AnalyticsPage.vue') },
    { path: 'categorias', name: 'admin-categorias', component: () => import('pages/admin/CategoriasPage.vue') },
    { path: 'campanhas',  name: 'admin-campanhas',  component: () => import('pages/admin/CampanhasPage.vue') },
    { path: 'config',     name: 'admin-config',     component: () => import('pages/admin/ConfigPage.vue') },
  ]
}

const profileRoute = {
  path: '/perfil',
  component: () => import('layouts/CoursesLayout.vue'),
  children: [
    { path: '', name: 'profile', component: () => import('pages/ProfilePage.vue') }
  ]
}

const publicRoutes = {
  path: '/',
  component: () => import('layouts/MainLayout.vue'),
  meta: { guest: true },
  children: [
    { path: '',         name: 'home',     component: () => import('pages/IndexPage.vue') },
    { path: 'login',    name: 'login',    component: () => import('pages/LoginPage.vue') },
    { path: 'register', name: 'register', component: () => import('pages/RegisterPage.vue') },
  ]
}

const routes = [
  studentRoutes,
  teacherRoutes,
  adminRoutes,
  publicRoutes,
  profileRoute,
  { path: '/:catchAll(.*)*', name: '404', component: () => import('pages/ErrorNotFound.vue') }
]

export default routes
