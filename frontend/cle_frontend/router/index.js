// router/index.js
import { createRouter } from 'vue-router';
import { createWebHistory } from 'vue-router';
import ArancelesView from '@/views/ArancelesView.vue';
import PresupuestosView from '@/views/PresupuestosView.vue';
import ServiciosView from '@/views/ServiciosView.vue';
import ArchivoView from '@/views/ArchivoView.vue';

const routes = [
  { path: '/', component: ServiciosView },
  { path: '/aranceles', component: ArancelesView },
  { path: '/presupuestos', component: PresupuestosView },
  { path: '/servicios', component: ServiciosView },
  { path: '/archivo', component: ArchivoView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
