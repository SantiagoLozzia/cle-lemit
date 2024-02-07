// router/index.js
import { createRouter } from 'vue-router';
import { createWebHistory } from 'vue-router';
import ArancelesView from '@/views/ArancelesView.vue';
import PresupuestosView from '@/views/PresupuestosView.vue';
import EnCursoView from '@/views/EnCursoView.vue';
import ArchivoView from '@/views/ArchivoView.vue';
import SolicitantesView from '@/views/SolicitantesView.vue';

const routes = [
  { path: '/', component: EnCursoView },
  { path: '/encurso', component: EnCursoView },
  { path: '/aranceles', component: ArancelesView },
  { path: '/presupuestos', component: PresupuestosView },
  { path: '/archivo', component: ArchivoView },
  { path: '/solicitantes', component: SolicitantesView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
