import { createRouter, createWebHistory } from 'vue-router';

// Importa las vistas
import ArancelesView from '@/views/ArancelesView.vue';
import PresupuestosView from '@/views/PresupuestosView.vue';
import EnCursoView from '@/views/EnCursoView.vue';
import ArchivoView from '@/views/ArchivoView.vue';
import SolicitantesView from '@/views/SolicitantesView.vue';
import LoginView from '@/views/LoginView.vue'; 

// Componentes para las subrutas de Presupuestos
import EnEsperaView from '@/views/SubmenuPresupuestos/EnEsperaView.vue';
import AceptadosView from '@/views/SubmenuPresupuestos/AceptadosView.vue';
import CanceladosView from '@/views/SubmenuPresupuestos/CanceladosView.vue';

// Función para verificar si el usuario está autenticado
function isAuthenticated() {
  // Comprueba si el token JWT está en el localStorage
  return !!localStorage.getItem('token');
}

// Define las rutas
const routes = [
  { path: '/userlogin', component: LoginView },
  { path: '/', component: EnCursoView, meta: { requiresAuth: true } },
  { path: '/encurso', component: EnCursoView, meta: { requiresAuth: true } },
  { path: '/aranceles', component: ArancelesView, meta: { requiresAuth: true } },
  { path: '/presupuestos', 
    component: PresupuestosView,
    meta: { requiresAuth: true },
    children: [
      { path: 'enespera', component: EnEsperaView, meta: { requiresAuth: true } },
      { path: 'aceptados', component: AceptadosView, meta: { requiresAuth: true } },
      { path: 'cancelados', component: CanceladosView, meta: { requiresAuth: true } }
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
    // Redirige a la página de inicio de sesión si no está autenticado
    next('/userlogin');
  } else {
    next();
  }
});

export default router;
