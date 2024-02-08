// router/index.js
import { createRouter } from 'vue-router';
import { createWebHistory } from 'vue-router';
import ArancelesView from '@/views/ArancelesView.vue';
import PresupuestosView from '@/views/PresupuestosView.vue';
import EnCursoView from '@/views/EnCursoView.vue';
import ArchivoView from '@/views/ArchivoView.vue';
import SolicitantesView from '@/views/SolicitantesView.vue';

// Componentes para las subrutas de Presupuestos
import EnEsperaView from '@/views/SubmenuPresupuestos/EnEsperaView.vue';
import AceptadosView from '@/views/SubmenuPresupuestos/AceptadosView.vue';
import CanceladosView from '@/views/SubmenuPresupuestos/CanceladosView.vue';

const routes = [
  { path: '/', component: EnCursoView },
  { path: '/encurso', component: EnCursoView },
  { path: '/aranceles', component: ArancelesView },
  { 
    path: '/presupuestos', 
    component: PresupuestosView,
    children: [
      { path: '/presupuestos/enespera', component: EnEsperaView },
      { path: '/presupuestos/aceptados', component: AceptadosView },
      { path: '/presupuestos/cancelados', component: CanceladosView }
    ]
  },
  { path: '/archivo', component: ArchivoView },
  { path: '/solicitantes', component: SolicitantesView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
