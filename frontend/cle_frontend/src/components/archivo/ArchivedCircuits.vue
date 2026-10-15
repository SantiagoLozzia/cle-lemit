<template>
  <div class="archivo-container">

    <!-- Filtros -->
    <div class="filter-bar mb-3 d-flex flex-wrap align-items-center gap-2">
      <input
        v-model="filterEmpresa"
        type="text"
        placeholder="Buscar empresa..."
        class="form-control form-control-sm w-auto"
        style="min-width:180px"
      >
      <select v-model="filterArea" class="form-select form-select-sm w-auto">
        <option value="">Todas las áreas</option>
        <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
      </select>
      <div class="d-flex align-items-center gap-1">
        <small class="text-muted">Desde</small>
        <input type="date" v-model="filterDesde" class="form-control form-control-sm w-auto">
      </div>
      <div class="d-flex align-items-center gap-1">
        <small class="text-muted">Hasta</small>
        <input type="date" v-model="filterHasta" class="form-control form-control-sm w-auto">
      </div>
      <input
        v-model="filterNroDoc"
        type="text"
        placeholder="N° documento..."
        class="form-control form-control-sm w-auto"
        style="min-width:130px"
        title="Buscar por N° de Servicio, Presupuesto, Legajo o Circuito"
      >
      <button
        v-if="filterEmpresa || filterArea || filterDesde || filterHasta || filterNroDoc"
        @click="clearFilters"
        class="btn btn-sm btn-outline-secondary"
      >✕ Limpiar</button>
      <span class="ms-auto text-muted small">{{ sortedArchivados.length }} registros</span>
    </div>

    <!-- Tabla -->
    <div class="table-container">
      <table class="table archivo-table table-hover">
        <thead>
          <tr>
            <th class="sortable" @click="setSort('nro_dataServicio')">N° Servicio <span class="sort-icon">{{ sortKey === 'nro_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="sortable" @click="setSort('fecha_dataServicio')">Fecha <span class="sort-icon">{{ sortKey === 'fecha_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th>Empresa</th>
            <th>Área Temática</th>
            <th class="sortable" @click="setSort('nro_presupuesto')">Presupuesto <span class="sort-icon">{{ sortKey === 'nro_presupuesto' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="sortable" @click="setSort('nro_legajo')">Legajo <span class="sort-icon">{{ sortKey === 'nro_legajo' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th>Total</th>
            <th>Pago</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in sortedArchivados" :key="index" class="archivo-row">
            <td>{{ item.nro_dataServicio }}</td>
            <td>{{ formatDate(item.fecha_dataServicio) }}</td>
            <td class="text-start empresa-cell" :title="item.nombre_solicitante">{{ item.nombre_solicitante }}</td>
            <td>{{ formatAreaTematica(item.area_tematica) }}</td>
            <td>{{ item.nro_presupuesto }}</td>
            <td>{{ item.nro_legajo || '—' }}</td>
            <td>{{ formatMonto(item.arancel_presupuesto) }}</td>
            <td>
              <span :class="badgePago(item.pago)">{{ labelPago(item.pago) }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-outline-primary py-0" @click="abrirDetalle(item)">
                <i class="bi bi-eye"></i>
              </button>
            </td>
          </tr>
          <tr v-if="sortedArchivados.length === 0">
            <td colspan="9" class="text-center text-muted py-5" style="font-size:1.1rem">No hay registros archivados</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal detalle -->
    <div v-if="mostrarModal" class="modal-backdrop-custom" @click.self="cerrarModal">
      <div class="modal-detalle">
        <div class="modal-detalle-header">
          <span class="fw-bold fs-6">Detalle — N° Servicio {{ detalle.nro_dataServicio }}</span>
          <button class="btn-close" @click="cerrarModal"></button>
        </div>
        <div class="modal-detalle-body">

          <!-- Info principal -->
          <div class="row g-2 mb-3">
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">N° Circuito</span>
                <span class="value">{{ detalle.nro_circuito }}</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">Fecha</span>
                <span class="value">{{ formatDate(detalle.fecha_dataServicio) }}</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">N° Presupuesto</span>
                <span class="value">{{ detalle.nro_presupuesto }}</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">N° Legajo</span>
                <span class="value">{{ detalle.nro_legajo || '—' }}</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">Área Temática</span>
                <span class="value">{{ formatAreaTematica(detalle.area_tematica) }}</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">Estado de pago</span>
                <span :class="badgePago(detalle.pago)" class="value">{{ labelPago(detalle.pago) }}</span>
              </div>
            </div>
            <div class="col-12 col-md-6">
              <div class="info-block">
                <span class="label">Empresa</span>
                <span class="value">{{ detalle.nombre_solicitante }}</span>
              </div>
            </div>
            <div class="col-12 col-md-6">
              <div class="info-block">
                <span class="label">CUIT</span>
                <span class="value">{{ detalle.cuit_solicitante }}</span>
              </div>
            </div>
            <div v-if="detalle.obra" class="col-12">
              <div class="info-block">
                <span class="label">Obra</span>
                <span class="value">{{ detalle.obra }}</span>
              </div>
            </div>
            <div v-if="detalle.observaciones_servicio" class="col-12">
              <div class="info-block">
                <span class="label">Observaciones</span>
                <span class="value">{{ detalle.observaciones_servicio }}</span>
              </div>
            </div>
          </div>

          <!-- Servicios -->
          <div class="mb-2 fw-semibold">Servicios</div>
          <table class="table table-sm mb-3">
            <thead>
              <tr>
                <th>Cod.</th>
                <th class="text-start">Servicio</th>
                <th>Norma</th>
                <th>Cant.</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in detalle.servicios" :key="s.nro_servicio">
                <td>{{ s.nro_servicio }}</td>
                <td class="text-start">{{ s.servicio }}</td>
                <td>{{ s.norma }}</td>
                <td>{{ s.cant }}</td>
                <td>{{ formatMonto(s.subtotal) }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Totales -->
          <div class="d-flex flex-column align-items-end gap-1">
            <div v-if="detalle.descuento > 0">
              <span class="text-muted me-2">Descuento:</span>
              <strong>{{ detalle.descuento }}%</strong>
            </div>
            <div>
              <span class="text-muted me-2">Total:</span>
              <strong>{{ formatMonto(detalle.arancel_presupuesto) }}</strong>
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/api.js';
import { AREAS_TEMATICAS } from '@/constants/areas.js';

export default {
  setup() {
    const archivados = ref([]);
    const uniqueAreas = AREAS_TEMATICAS;

    // Filtros
    const filterEmpresa = ref('');
    const filterArea = ref('');
    const filterDesde = ref('');
    const filterHasta = ref('');
    const filterNroDoc = ref('');

    const clearFilters = () => {
      filterEmpresa.value = '';
      filterArea.value = '';
      filterDesde.value = '';
      filterHasta.value = '';
      filterNroDoc.value = '';
    };

    // Ordenamiento
    const sortKey = ref('nro_dataServicio');
    const sortDir = ref('desc');
    const setSort = (key) => {
      if (sortKey.value === key) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
      else { sortKey.value = key; sortDir.value = 'desc'; }
    };

    const filteredArchivados = computed(() => archivados.value.filter(item => {
      const empresaOk = !filterEmpresa.value ||
        item.nombre_solicitante.toLowerCase().includes(filterEmpresa.value.toLowerCase());
      const areaOk = !filterArea.value ||
        formatAreaTematica(item.area_tematica) === filterArea.value;
      const desdeOk = !filterDesde.value || item.fecha_dataServicio >= filterDesde.value;
      const hastaOk = !filterHasta.value || item.fecha_dataServicio <= filterHasta.value;
      const nroOk = !filterNroDoc.value || [
        String(item.nro_dataServicio),
        String(item.nro_presupuesto),
        String(item.nro_legajo || ''),
        String(item.nro_circuito || ''),
      ].some(n => n.includes(filterNroDoc.value));
      return empresaOk && areaOk && desdeOk && hastaOk && nroOk;
    }));

    const NUMERIC_KEYS = ['nro_dataServicio', 'nro_presupuesto', 'nro_legajo'];

    const sortedArchivados = computed(() => {
      return [...filteredArchivados.value].sort((a, b) => {
        const valA = NUMERIC_KEYS.includes(sortKey.value) ? Number(a[sortKey.value]) : a[sortKey.value];
        const valB = NUMERIC_KEYS.includes(sortKey.value) ? Number(b[sortKey.value]) : b[sortKey.value];
        if (valA < valB) return sortDir.value === 'asc' ? -1 : 1;
        if (valA > valB) return sortDir.value === 'asc' ? 1 : -1;
        return 0;
      });
    });

    // Modal detalle
    const mostrarModal = ref(false);
    const detalle = ref({});

    const abrirDetalle = (item) => {
      detalle.value = item;
      mostrarModal.value = true;
    };
    const cerrarModal = () => { mostrarModal.value = false; };

    // Carga de datos
    const fetchArchivados = async () => {
      try {
        const response = await api.get('/encurso/archivados/');
        archivados.value = response.data;
      } catch (error) {
        console.error('Error al obtener archivados:', error);
      }
    };

    // Helpers de formato
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const [y, m, d] = dateStr.split('-');
      return `${d}/${m}/${y}`;
    };

    const formatAreaTematica = (v) => v
      ? v.replace(/_/g, ' ').replace(/\w\S*/g, t => t.charAt(0).toUpperCase() + t.substr(1).toLowerCase())
      : '';

    const formatMonto = (v) => {
      if (v === null || v === undefined || v === '') return '—';
      const n = parseFloat(v);
      return isNaN(n) ? v : '$ ' + n.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    };

    const labelPago = (pago) => {
      if (pago === 100) return '100% pagado';
      if (pago === 50) return '50% pagado';
      return 'Sin pago';
    };

    const badgePago = (pago) => {
      if (pago === 100) return 'badge bg-success';
      if (pago === 50) return 'badge bg-warning text-dark';
      return 'badge bg-secondary';
    };

    onMounted(fetchArchivados);

    return {
      uniqueAreas,
      filterEmpresa, filterArea, filterDesde, filterHasta, filterNroDoc, clearFilters,
      sortKey, sortDir, setSort, sortedArchivados,
      mostrarModal, detalle, abrirDetalle, cerrarModal,
      formatDate, formatAreaTematica, formatMonto, labelPago, badgePago,
    };
  }
};
</script>

<style scoped>
.archivo-container {
  padding: 0 4px;
}

.table-container {
  overflow-x: auto;
}

.archivo-table {
  width: 100%;
  table-layout: auto;
}

.empresa-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Modal */
.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-detalle {
  background: #fff;
  border-radius: 8px;
  width: 100%;
  max-width: 680px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

.modal-detalle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  border-bottom: 1px solid #dee2e6;
}

.modal-detalle-body {
  overflow-y: auto;
  padding: 18px;
}

.info-block {
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  border-radius: 4px;
  padding: 6px 10px;
}

.info-block .label {
  font-size: 0.72em;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.info-block .value {
  font-weight: 500;
  font-size: 0.9em;
}
</style>
