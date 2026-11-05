<template>
  <div class="aranceles-container">
    <PageHeader
      title="Libro de Aranceles"
      :subtitle="sortedData.length + ' servicios'"
      icon="bi bi-clipboard-data"
    />
    <div class="table-container">
      <div class="filter-bar mb-2 d-flex flex-wrap align-items-center gap-2">
        <select v-model="filterArea" class="form-select form-select-sm w-auto">
          <option value="">Todas las áreas</option>
          <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
        </select>
        <input v-model="filterServicio" type="text" placeholder="Buscar servicio..." class="form-control form-control-sm w-auto" style="min-width:180px">
        <input v-model="filterNorma" type="text" placeholder="Buscar norma..." class="form-control form-control-sm w-auto" style="min-width:140px">
        <button v-if="filterArea || filterServicio || filterNorma" @click="clearFilter" class="btn btn-sm btn-outline-secondary">✕ Limpiar</button>
      </div>
      <table class="table aranceles-table">
        <colgroup>
          <col class="col-nro">
          <col class="col-categoria">
          <col class="col-subcategoria">
          <col class="col-servicio">
          <col class="col-norma">
          <col class="col-valor">
          <col class="col-area">
          <col v-if="esST" class="col-acciones">
        </colgroup>
        <thead>
          <tr>
            <th class="add-border-right sortable" @click="setSort('nro_servicio')">Nro <span class="sort-icon">{{ sortKey === 'nro_servicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="add-border-right text-start">Categoría</th>
            <th class="add-border-right text-start">Subcategoría</th>
            <th class="add-border-right text-start">Servicio</th>
            <th class="add-border-right">Norma</th>
            <th class="add-border-right sortable" @click="setSort('arancel')">Valor (M) <span class="sort-icon">{{ sortKey === 'arancel' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="add-border-right">Área Temática</th>
            <th v-if="esST"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in sortedData" :key="index">
            <td class="add-border-right">{{ arancel.nro_servicio }}</td>
            <td class="text-start add-border-right">{{ arancel.categoria }}</td>
            <td class="text-start add-border-right">{{ arancel.subcategoria }}</td>
            <td class="text-start add-border-right">{{ arancel.servicio }}</td>
            <td class="add-border-right">{{ arancel.norma }}</td>
            <td class="add-border-right">{{ arancel.arancel }}</td>
            <td class="add-border-right">{{ formatAreaTematica(arancel.area_tematica) }}</td>
            <td v-if="esST" class="text-center">
              <button class="btn btn-sm btn-outline-secondary py-0 px-1" @click="abrirEditar(arancel)" title="Editar">
                <i class="bi bi-pencil-fill"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal editar arancel -->
    <div v-if="mostrarModalEditar" class="modal show" @click.self="cerrarModalEditar">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar servicio #{{ servicioEnEdicion.nro_servicio }}</h5>
            <button type="button" class="btn-close" @click="cerrarModalEditar"></button>
          </div>
          <div class="modal-body">
            <div v-if="errorEdicion" class="alert alert-danger py-2">{{ errorEdicion }}</div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre del servicio</label>
              <input v-model="servicioEnEdicion.servicio" type="text" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Norma</label>
              <input v-model="servicioEnEdicion.norma" type="text" class="form-control" />
            </div>
            <div class="row g-3 mb-3">
              <div class="col-6">
                <label class="form-label fw-semibold">Categoría</label>
                <input v-model="servicioEnEdicion.categoria" type="text" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label fw-semibold">Subcategoría</label>
                <input v-model="servicioEnEdicion.subcategoria" type="text" class="form-control" />
              </div>
            </div>
            <div class="row g-3 mb-3">
              <div class="col-6">
                <label class="form-label fw-semibold">Valor (M)</label>
                <input v-model.number="servicioEnEdicion.arancel" type="number" min="0" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label fw-semibold">Área Temática</label>
                <select v-model="servicioEnEdicion.area_tematica" class="form-select">
                  <option v-for="opt in areaChoices" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer" style="gap:8px">
            <button class="btn btn-primary" style="flex:1" :disabled="guardandoEdicion" @click="guardarEdicion">
              {{ guardandoEdicion ? 'Guardando...' : 'Guardar' }}
            </button>
            <button class="btn btn-secondary" style="flex:1" @click="cerrarModalEditar">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, computed } from 'vue';
import api from '@/api.js';
import { AREAS_TEMATICAS } from '@/constants/areas.js';
import PageHeader from '@/components/PageHeader.vue';

const areaChoices = [
  { value: 'durabilidad',           label: 'Durabilidad' },
  { value: 'ensayos_mecanicos',     label: 'Ensayos Mecánicos' },
  { value: 'geologia',              label: 'Geología' },
  { value: 'hormigones',            label: 'Hormigones' },
  { value: 'metalurgia',            label: 'Metalurgia' },
  { value: 'patrimonio',            label: 'Patrimonio' },
  { value: 'quimica',               label: 'Química' },
  { value: 'tecnologia_vial',       label: 'Tecnología Vial' },
  { value: 'estudios_especiales',   label: 'Estudios Especiales' },
  { value: 'servicios_tecnologicos',label: 'Servicios Tecnológicos' },
  { value: 'direccion',             label: 'Dirección' },
];

export default {
  components: { PageHeader },
  props: {
    data: { type: Array, required: true }
  },
  emits: ['arancel-editado'],
  setup(props, { emit }) {
    const esST = computed(() => sessionStorage.getItem('role') === 'servicios_tecnologicos');

    // --- Sorting ---
    const sortKey = ref('');
    const sortDir = ref('asc');
    const setSort = (key) => {
      if (sortKey.value === key) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
      else { sortKey.value = key; sortDir.value = 'asc'; }
    };

    // --- Filters ---
    const filterArea     = ref('');
    const filterServicio = ref('');
    const filterNorma    = ref('');
    const uniqueAreas    = AREAS_TEMATICAS;

    const formatAreaTematica = (areaTematica) => {
      return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, txt =>
        txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
      );
    };

    const filteredData = computed(() => props.data.filter(a => {
      const areaOk     = !filterArea.value     || formatAreaTematica(a.area_tematica) === filterArea.value;
      const servicioOk = !filterServicio.value || a.servicio.toLowerCase().includes(filterServicio.value.toLowerCase());
      const normaOk    = !filterNorma.value    || (a.norma && a.norma.toLowerCase().includes(filterNorma.value.toLowerCase()));
      return areaOk && servicioOk && normaOk;
    }));

    const sortedData = computed(() => {
      if (!sortKey.value) return filteredData.value;
      return [...filteredData.value].sort((a, b) => {
        const valA = Number.isFinite(Number(a[sortKey.value])) && sortKey.value !== 'norma'
          ? Number(a[sortKey.value]) : a[sortKey.value];
        const valB = Number.isFinite(Number(b[sortKey.value])) && sortKey.value !== 'norma'
          ? Number(b[sortKey.value]) : b[sortKey.value];
        if (valA < valB) return sortDir.value === 'asc' ? -1 : 1;
        if (valA > valB) return sortDir.value === 'asc' ? 1 : -1;
        return 0;
      });
    });

    const clearFilter = () => { filterArea.value = ''; filterServicio.value = ''; filterNorma.value = ''; };

    // --- Edit ---
    const mostrarModalEditar = ref(false);
    const servicioEnEdicion  = ref({});
    const errorEdicion       = ref('');
    const guardandoEdicion   = ref(false);

    const abrirEditar = (arancel) => {
      servicioEnEdicion.value = { ...arancel };
      errorEdicion.value = '';
      mostrarModalEditar.value = true;
    };

    const cerrarModalEditar = () => {
      mostrarModalEditar.value = false;
    };

    const guardarEdicion = async () => {
      const { nro_servicio, servicio, norma, arancel, area_tematica, categoria, subcategoria } = servicioEnEdicion.value;
      if (!servicio?.trim()) { errorEdicion.value = 'El nombre del servicio es obligatorio.'; return; }
      if (arancel === null || arancel === undefined || arancel === '') { errorEdicion.value = 'El valor (M) es obligatorio.'; return; }

      guardandoEdicion.value = true;
      errorEdicion.value = '';
      try {
        await api.patch(`/aranceles/${nro_servicio}/`, { servicio, norma, arancel, area_tematica, categoria, subcategoria });
        mostrarModalEditar.value = false;
        emit('arancel-editado');
      } catch (err) {
        errorEdicion.value = err.response?.data?.detail || 'Error al guardar los cambios.';
      } finally {
        guardandoEdicion.value = false;
      }
    };

    return {
      esST, areaChoices,
      sortKey, sortDir, sortedData, setSort,
      filterArea, filterServicio, filterNorma, uniqueAreas, clearFilter,
      formatAreaTematica,
      mostrarModalEditar, servicioEnEdicion, errorEdicion, guardandoEdicion,
      abrirEditar, cerrarModalEditar, guardarEdicion,
    };
  }
};
</script>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
  margin: 0;
}

.aranceles-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}

.aranceles-table td,
.aranceles-table th {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.col-nro          { width: 55px; }
.col-categoria    { width: 18%; }
.col-subcategoria { width: 18%; }
.col-norma        { width: 140px; }
.col-valor        { width: 80px; }
.col-area         { width: 14%; }
.col-acciones     { width: 44px; }

.add-border-right {
  border-right: 1px solid gainsboro;
}

.modal {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.5);
  z-index: 1050;
}
.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
