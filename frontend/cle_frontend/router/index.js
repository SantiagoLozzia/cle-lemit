import { createRouter, createWebHistory } from 'vue-router';

// Importa las vistas
import ArancelesView from '@/views/ArancelesView.vue';
import PresupuestosView from '@/views/PresupuestosView.vue';
import EnCursoView from '@/views/EnCursoView.vue';
import ArchivoView from '@/views/ArchivoView.vue';
import SolicitantesView from '@/views/SolicitantesView.vue';
import LoginView from '@/views/LoginView.vue';
import ResetPasswordView from '@/views/ResetPasswordView.vue';

// Componentes para las subrutas de Presupuestos
import EnEsperaView from '@/views/SubmenuPresupuestos/EnEsperaView.vue';
import AceptadosView from '@/views/SubmenuPresupuestos/AceptadosView.vue';
import CanceladosView from '@/views/SubmenuPresupuestos/CanceladosView.vue';
import HistorialView from '@/views/SubmenuPresupuestos/HistorialView.vue';

// Función para verificar si el usuario está autenticado
function isAuthenticated() {
  // Comprueba si el token JWT está en el sessionStorage
  return !!sessionStorage.getItem('token');
}

// Define las rutas
const routes = [
  { path: '/userlogin', component: LoginView },
  { path: '/reset-password', component: ResetPasswordView },
  { path: '/', component: EnCursoView, meta: { requiresAuth: true } },
  { path: '/encurso', component: EnCursoView, meta: { requiresAuth: true } },
  { path: '/aranceles', component: ArancelesView, meta: { requiresAuth: true } },
  { path: '/presupuestos',
    component: PresupuestosView,
    meta: { requiresAuth: true },
    redirect: '/presupuestos/nuevos',
    children: [
      { path: 'nuevos', component: EnEsperaView, meta: { requiresAuth: true } },
      { path: 'enespera', redirect: '/presupuestos/nuevos' },
      { path: 'aceptados', component: AceptadosView, meta: { requiresAuth: true } },
      { path: 'descartados', component: CanceladosView, meta: { requiresAuth: true } },
      { path: 'cancelados', redirect: '/presupuestos/descartados' },
      { path: 'historial', component: HistorialView, meta: { requiresAuth: true } }
    ]
  },
  { path: '/archivo', component: ArchivoView, meta: { requiresAuth: true } },
  { path: '/solicitantes', component: SolicitantesView, meta: { requiresAuth: true } },
  { path: '/:catchAll(.*)', redirect: '/' }  // Redirigir cualquier ruta no encontrada a la página de inicio
];

// Crea el enrutador
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Agrega una guardia global para proteger las rutas
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next('/userlogin');
  } else if (to.path.startsWith('/presupuestos') && sessionStorage.getItem('role') === 'administracion') {
    next('/encurso');
  } else {
    next();
  }
});

export default router;
