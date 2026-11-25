<template>
  <div class="aranceles-view">

    <!-- Submenú estilo Presupuestos -->
    <nav class="aranceles-submenu">
      <div class="submenu-item" :class="{ active: tabActivo === 'libro' }" @click="tabActivo = 'libro'">
        Libro de Aranceles
      </div>
      <div class="submenu-item" :class="{ active: tabActivo === 'conceptos' }" @click="tabActivo = 'conceptos'">
        Concepto de Facturación
      </div>
    </nav>

    <!-- Tab: Libro de Aranceles -->
    <template v-if="tabActivo === 'libro'">
      <PageHeader title="Libro de Aranceles" :subtitle="arancelesData.length + ' servicios'" icon="bi bi-clipboard-data" />
      <div class="actions-bar">
        <UpdateModule v-if="!isAdmin" />
        <NewService v-if="!isAdmin" @arancel-creado="fetchAranceles" />
      </div>
      <ArancelesTable :data="arancelesData" @arancel-editado="fetchAranceles" />
    </template>

    <!-- Tab: Concepto de Facturación -->
    <template v-else>
      <PageHeader title="Concepto de Facturación" :subtitle="catalogoConceptos.length + ' conceptos'" icon="bi bi-tags" />
      <div class="actions-bar" v-if="isST">
        <button class="btn btn-primary custom-shadow-btn" @click="abrirModalNuevoConcepto">
          <i class="bi bi-plus-circle me-1" style="font-size:1rem"></i> Nuevo Concepto
        </button>
      </div>

      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Nombre</th>
            <th v-if="isST" style="width:120px">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="catalogoConceptos.length === 0">
            <td :colspan="isST ? 2 : 1" class="text-center text-muted">Sin conceptos registrados.</td>
          </tr>
          <tr v-for="c in catalogoConceptos" :key="c.id">
            <td class="text-start">{{ c.nombre }}</td>
            <td v-if="isST">
              <button class="btn btn-sm btn-outline-secondary me-1" @click="abrirModalEditarConcepto(c)">
                <i class="bi bi-pencil" style="font-size:0.9rem"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="eliminarConcepto(c)">
                <i class="bi bi-trash" style="font-size:0.9rem"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <!-- Modal Nuevo / Editar Concepto -->
    <div class="modal" :class="{ show: modalConceptoAbierto }" tabindex="-1" @click.self="modalConceptoAbierto = false">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editandoConcepto ? 'Editar' : 'Nuevo' }} Concepto de Facturación</h5>
            <button type="button" class="btn-close" @click="modalConceptoAbierto = false"></button>
          </div>
          <div class="modal-body">
            <label class="form-label fw-semibold">Nombre</label>
            <input v-model="formConcepto.nombre" type="text" class="form-control" placeholder="Ej: Informe técnico" maxlength="200" />
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="modalConceptoAbierto = false">Cancelar</button>
            <button class="btn btn-primary" :disabled="!formConcepto.nombre.trim()" @click="guardarConcepto">
              {{ editandoConcepto ? 'Guardar cambios' : 'Crear' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api.js';
import UpdateModule     from '../components/aranceles/UpdateModule.vue';
import ArancelesTable   from '../components/aranceles/ArancelesTable.vue';
import NewService       from '../components/aranceles/NewService.vue';
import PageHeader       from '../components/PageHeader.vue';

export default {
  components: { UpdateModule, NewService, ArancelesTable, PageHeader },

  setup() {
    const moduloData    = ref([]);
    const servicioData  = ref([]);
    const arancelesData = ref([]);

    const tabActivo = ref('libro');
    const userRole = sessionStorage.getItem('role') || '';
    const isST = ref(userRole === 'servicios_tecnologicos');
    const isAdmin = ref(userRole === 'administracion');

    const catalogoConceptos = ref([]);
    const modalConceptoAbierto = ref(false);
    const editandoConcepto = ref(null);
    const formConcepto = ref({ nombre: '' });

    const fetchAranceles = async () => {
      try {
        const response = await api.get('/aranceles/todos/');
        arancelesData.value = response.data;
      } catch (err) {
        console.error('Fetch error:', err.message);
      }
    };

    const fetchConceptos = async () => {
      try {
        const response = await api.get('/aranceles/conceptos/');
        catalogoConceptos.value = response.data;
      } catch (err) {
        console.error('Error cargando conceptos:', err.message);
      }
    };

    const abrirModalNuevoConcepto = () => {
      editandoConcepto.value = null;
      formConcepto.value = { nombre: '' };
      modalConceptoAbierto.value = true;
    };

    const abrirModalEditarConcepto = (c) => {
      editandoConcepto.value = c;
      formConcepto.value = { nombre: c.nombre };
      modalConceptoAbierto.value = true;
    };

    const guardarConcepto = async () => {
      const nombre = formConcepto.value.nombre.trim();
      if (!nombre) return;
      try {
        if (editandoConcepto.value) {
          await api.patch(`/aranceles/conceptos/${editandoConcepto.value.id}/`, { nombre });
        } else {
          await api.post('/aranceles/conceptos/', { nombre });
        }
        await fetchConceptos();
        modalConceptoAbierto.value = false;
      } catch (err) {
        console.error('Error guardando concepto:', err.message);
      }
    };

    const eliminarConcepto = async (c) => {
      if (!confirm(`¿Eliminar concepto "${c.nombre}"?`)) return;
      try {
        await api.delete(`/aranceles/conceptos/${c.id}/`);
        await fetchConceptos();
      } catch (err) {
        console.error('Error eliminando concepto:', err.message);
      }
    };

    const initSocket = () => {
      const token = sessionStorage.getItem('token');
      if (!token) return;
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const socket = new WebSocket(`${protocol}//${window.location.host}/ws/mi_canal/`, ['jwt', token]);
      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.aranceles_action === 'add' && data.servicio) {
            arancelesData.value.push(data.servicio);
          }
        } catch (err) {
          console.error('Error parseando mensaje WebSocket:', err);
        }
      };
      socket.onclose = () => setTimeout(initSocket, 5000);
    };

    onMounted(() => {
      fetchAranceles();
      fetchConceptos();
      initSocket();
    });

    return {
      moduloData, servicioData, arancelesData, fetchAranceles,
      tabActivo, isST, isAdmin,
      catalogoConceptos, modalConceptoAbierto, editandoConcepto, formConcepto,
      abrirModalNuevoConcepto, abrirModalEditarConcepto, guardarConcepto, eliminarConcepto,
    };
  }
};
</script>

<style scoped>
.aranceles-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.aranceles-submenu {
  background-color: #fff;
  border-bottom: 1px solid #ccc;
  display: flex;
  position: sticky;
  top: 0;
  z-index: 10;
}

.submenu-item {
  color: #026290;
  padding: 10px 20px;
  cursor: pointer;
}

.submenu-item:hover {
  color: #fff;
  background-color: #026290;
}

.submenu-item.active {
  color: #fff;
  background-color: #026290;
}

.actions-bar {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding: 4px 0;
}

.actions-bar :deep(.btn) {
  min-width: 160px;
}
</style>
