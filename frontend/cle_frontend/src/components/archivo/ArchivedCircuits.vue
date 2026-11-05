<template>
  <div class="archivo-container">

    <PageHeader title="Circuitos archivados" :subtitle="sortedArchivados.length + ' registros'" icon="bi bi-archive-fill" />

    <!-- Filtros -->
    <div class="filter-bar mb-3 d-flex flex-wrap align-items-center gap-2">
      <input
        v-model="filterEmpresa"
        type="text"
        placeholder="Buscar empresa..."
        class="form-control form-control-sm w-auto"
        style="min-width:180px"
      >
      <input
        v-model="filterNroDoc"
        type="text"
        placeholder="N° (servicio / presupuesto / legajo)..."
        class="form-control form-control-sm w-auto"
        style="min-width:200px"
        title="Buscar por N° de Servicio, Presupuesto, Legajo o Circuito"
      >
      <select v-model="filterArea" class="form-select form-select-sm w-auto">
        <option value="">Todas las áreas</option>
        <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
      </select>
      <select v-model="filterMotivo" class="form-select form-select-sm w-auto">
        <option value="">Todos los motivos</option>
        <option value="exito">Finalizado con éxito</option>
        <option value="falta_pago">Falta de pago</option>
        <option value="vencimiento_muestras">Vencimiento de muestras</option>
        <option value="desistimiento">Desistimiento</option>
        <option value="otro">Otro</option>
      </select>
      <select v-model="filterPago" class="form-select form-select-sm w-auto">
        <option value="">Estado de pago</option>
        <option value="100">100% pagado</option>
        <option value="no_arancelado">No arancelado</option>
        <option value="pago_diferido">Pago diferido</option>
        <option value="sin_pago">Sin pago</option>
      </select>
      <div class="d-flex align-items-center gap-1">
        <small class="text-muted">Archivo desde</small>
        <input type="date" v-model="filterDesde" class="form-control form-control-sm w-auto">
      </div>
      <div class="d-flex align-items-center gap-1">
        <small class="text-muted">hasta</small>
        <input type="date" v-model="filterHasta" class="form-control form-control-sm w-auto">
      </div>
      <button
        v-if="hayFiltros"
        @click="clearFilters"
        class="btn btn-sm btn-outline-secondary"
      >✕ Limpiar</button>
      <div class="col-selector-wrap ms-auto" ref="colSelectorRef">
        <button class="btn btn-sm btn-outline-secondary" @click="toggleColSelector">
          <i class="bi bi-layout-three-columns me-1"></i>Columnas
          <span v-if="colsOcultas > 0" class="badge bg-secondary ms-1">{{ colsOcultas }}</span>
        </button>
        <div v-if="mostrarColSelector" class="col-selector-panel">
          <div class="col-sel-header">
            <span>Columnas visibles</span>
            <button class="btn btn-link btn-sm py-0" @click="mostrarTodasCols">Mostrar todas</button>
          </div>
          <label v-for="col in COLS" :key="col.key" class="col-sel-item">
            <input type="checkbox" v-model="colVisible[col.key]"> {{ col.label }}
          </label>
        </div>
      </div>
      <button
        class="btn btn-sm btn-success"
        @click="exportarExcel"
        title="Exportar tabla actual a Excel (solo columnas visibles)"
      >
        <i class="bi bi-file-earmark-excel me-1"></i>Exportar Excel
      </button>
    </div>

    <!-- Tabla -->
    <div class="table-container">
      <table class="table archivo-table table-hover">
        <thead>
          <tr>
            <th v-if="colVisible.nro_dataServicio" class="sortable" @click="setSort('nro_dataServicio')">N° Servicio <span class="sort-icon">{{ sortKey === 'nro_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="colVisible.fecha_dataServicio" class="sortable" @click="setSort('fecha_dataServicio')">Fecha <span class="sort-icon">{{ sortKey === 'fecha_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="colVisible.nombre_solicitante">Empresa</th>
            <th v-if="colVisible.area_tematica">Área Temática</th>
            <th v-if="colVisible.nro_presupuesto" class="sortable" @click="setSort('nro_presupuesto')">Presupuesto <span class="sort-icon">{{ sortKey === 'nro_presupuesto' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="colVisible.nro_legajo" class="sortable" @click="setSort('nro_legajo')">Legajo <span class="sort-icon">{{ sortKey === 'nro_legajo' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="colVisible.arancel_presupuesto">Total</th>
            <th v-if="colVisible.pago">Pago</th>
            <th v-if="colVisible.motivo_archivo">Motivo</th>
            <th v-if="colVisible.fecha_archivo" class="sortable" @click="setSort('fecha_archivo')">Finalización <span class="sort-icon">{{ sortKey === 'fecha_archivo' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in sortedArchivados" :key="index" class="archivo-row">
            <td v-if="colVisible.nro_dataServicio">{{ item.nro_dataServicio }}</td>
            <td v-if="colVisible.fecha_dataServicio">{{ formatDate(item.fecha_dataServicio) }}</td>
            <td v-if="colVisible.nombre_solicitante" class="text-start empresa-cell" :title="item.nombre_solicitante">{{ item.nombre_solicitante }}</td>
            <td v-if="colVisible.area_tematica">{{ formatAreaTematica(item.area_tematica) }}</td>
            <td v-if="colVisible.nro_presupuesto">{{ item.nro_presupuesto }}</td>
            <td v-if="colVisible.nro_legajo">{{ item.nro_legajo || '—' }}</td>
            <td v-if="colVisible.arancel_presupuesto">{{ formatMonto(item.arancel_presupuesto) }}</td>
            <td v-if="colVisible.pago">
              <span :class="badgePago(item.pago)">{{ labelPago(item.pago) }}</span>
            </td>
            <td v-if="colVisible.motivo_archivo">
              <span v-if="item.motivo_archivo" :class="badgeMotivo(item.motivo_archivo)" :title="item.nota_archivo || ''">
                {{ item.motivo_archivo_display || item.motivo_archivo }}
              </span>
              <span v-else class="text-muted">—</span>
            </td>
            <td v-if="colVisible.fecha_archivo" class="text-nowrap">{{ formatDate(item.fecha_archivo) || '—' }}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary py-0" @click="abrirDetalle(item)">
                <i class="bi bi-eye"></i>
              </button>
            </td>
          </tr>
          <tr v-if="sortedArchivados.length === 0">
            <td colspan="11" class="text-center text-muted py-5" style="font-size:1.1rem">No hay registros archivados</td>
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
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">Motivo de archivo</span>
                <span v-if="detalle.motivo_archivo" :class="badgeMotivo(detalle.motivo_archivo)" class="value">
                  {{ detalle.motivo_archivo_display || detalle.motivo_archivo }}
                </span>
                <span v-else class="value text-muted">—</span>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="info-block">
                <span class="label">Fecha de finalización</span>
                <span class="value">{{ formatDate(detalle.fecha_archivo) || '—' }}</span>
              </div>
            </div>
            <div v-if="detalle.nota_archivo" class="col-12">
              <div class="info-block">
                <span class="label">Nota de archivo</span>
                <span class="value">{{ detalle.nota_archivo }}</span>
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
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import * as XLSX from 'xlsx';
import api from '@/api.js';
import { AREAS_TEMATICAS } from '@/constants/areas.js';
import PageHeader from '@/components/PageHeader.vue';

export default {
  components: { PageHeader },
  setup() {
    const archivados  = ref([]);
    const uniqueAreas = AREAS_TEMATICAS;

    // Definición de columnas
    const COLS = [
      { key: 'nro_dataServicio',   label: 'N° Servicio' },
      { key: 'fecha_dataServicio', label: 'Fecha servicio' },
      { key: 'nombre_solicitante', label: 'Empresa' },
      { key: 'area_tematica',      label: 'Área Temática' },
      { key: 'nro_presupuesto',    label: 'N° Presupuesto' },
      { key: 'nro_legajo',         label: 'N° Legajo' },
      { key: 'arancel_presupuesto',label: 'Total' },
      { key: 'pago',               label: 'Estado de pago' },
      { key: 'motivo_archivo',     label: 'Motivo de archivo' },
      { key: 'fecha_archivo',      label: 'Finalización' },
    ];

    const colVisible = reactive(Object.fromEntries(COLS.map(c => [c.key, true])));
    const colsOcultas = computed(() => COLS.filter(c => !colVisible[c.key]).length);

    const mostrarColSelector = ref(false);
    const colSelectorRef     = ref(null);
    const toggleColSelector  = () => { mostrarColSelector.value = !mostrarColSelector.value; };
    const mostrarTodasCols   = () => { COLS.forEach(c => { colVisible[c.key] = true; }); };

    const handleClickFueraColSelector = (e) => {
      if (colSelectorRef.value && !colSelectorRef.value.contains(e.target)) {
        mostrarColSelector.value = false;
      }
    };

    // Filtros
    const filterEmpresa = ref('');
    const filterArea    = ref('');
    const filterDesde   = ref('');
    const filterHasta   = ref('');
    const filterNroDoc  = ref('');
    const filterMotivo  = ref('');
    const filterPago    = ref('');

    const hayFiltros = computed(() =>
      filterEmpresa.value || filterArea.value || filterDesde.value ||
      filterHasta.value || filterNroDoc.value || filterMotivo.value || filterPago.value
    );

    const clearFilters = () => {
      filterEmpresa.value = '';
      filterArea.value    = '';
      filterDesde.value   = '';
      filterHasta.value   = '';
      filterNroDoc.value  = '';
      filterMotivo.value  = '';
      filterPago.value    = '';
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
      // Fecha filtra por fecha_archivo (finalización), con fallback a fecha_dataServicio
      const fechaRef = item.fecha_archivo || item.fecha_dataServicio || '';
      const desdeOk = !filterDesde.value || fechaRef >= filterDesde.value;
      const hastaOk = !filterHasta.value || fechaRef <= filterHasta.value;
      const nroOk = !filterNroDoc.value || [
        String(item.nro_dataServicio),
        String(item.nro_presupuesto),
        String(item.nro_legajo || ''),
        String(item.nro_circuito || ''),
      ].some(n => n.includes(filterNroDoc.value));
      const motivoOk = !filterMotivo.value || item.motivo_archivo === filterMotivo.value;
      const pagoOk = !filterPago.value || String(item.pago) === filterPago.value;
      return empresaOk && areaOk && desdeOk && hastaOk && nroOk && motivoOk && pagoOk;
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
      const p = String(pago);
      if (p === '100') return '100% pagado';
      if (p === 'no_arancelado') return 'No arancelado';
      if (p === 'pago_diferido') return 'Pago diferido';
      return 'Sin pago';
    };

    const badgePago = (pago) => {
      const p = String(pago);
      if (p === '100' || p === 'no_arancelado') return 'badge bg-success';
      if (p === 'pago_diferido') return 'badge bg-warning text-dark';
      return 'badge bg-secondary';
    };

    const badgeMotivo = (motivo) => {
      if (motivo === 'exito') return 'badge bg-success';
      if (motivo === 'falta_pago') return 'badge bg-danger';
      if (motivo === 'vencimiento_muestras') return 'badge bg-warning text-dark';
      if (motivo === 'desistimiento') return 'badge bg-secondary';
      return 'badge bg-dark';
    };

    // Mapa: key del modelo → función que devuelve el valor para Excel
    const EXCEL_COLS = [
      { key: 'nro_dataServicio',    label: 'N° Servicio',       fn: i => i.nro_dataServicio },
      { key: 'fecha_dataServicio',  label: 'Fecha servicio',    fn: i => formatDate(i.fecha_dataServicio) },
      { key: 'nombre_solicitante',  label: 'Empresa',           fn: i => i.nombre_solicitante },
      { key: 'area_tematica',       label: 'Área Temática',     fn: i => formatAreaTematica(i.area_tematica) },
      { key: 'nro_presupuesto',     label: 'N° Presupuesto',    fn: i => i.nro_presupuesto },
      { key: 'nro_legajo',          label: 'N° Legajo',         fn: i => i.nro_legajo || '' },
      { key: 'arancel_presupuesto', label: 'Total ($)',          fn: i => i.arancel_presupuesto != null ? parseFloat(i.arancel_presupuesto) : '' },
      { key: 'pago',                label: 'Estado de pago',    fn: i => labelPago(i.pago) },
      { key: 'motivo_archivo',      label: 'Motivo de archivo', fn: i => i.motivo_archivo_display || i.motivo_archivo || '' },
      { key: 'fecha_archivo',       label: 'Finalización',      fn: i => formatDate(i.fecha_archivo) },
    ];

    const exportarExcel = () => {
      const colsActivas = EXCEL_COLS.filter(c => colVisible[c.key]);
      const filas = sortedArchivados.value.map(item =>
        Object.fromEntries(colsActivas.map(c => [c.label, c.fn(item)]))
      );

      const ws = XLSX.utils.json_to_sheet(filas);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Archivo');

      // Ancho automático
      ws['!cols'] = colsActivas.map(c => ({
        wch: Math.max(c.label.length, ...filas.map(r => String(r[c.label] ?? '').length)) + 2
      }));

      // Orientación horizontal para tablas anchas
      ws['!pageSetup'] = { orientation: 'landscape', fitToPage: true, fitToWidth: 1, fitToHeight: 0 };

      const fecha = new Date().toISOString().slice(0, 10);
      XLSX.writeFile(wb, `archivo_circuitos_${fecha}.xlsx`);
    };

    onMounted(() => {
      fetchArchivados();
      document.addEventListener('click', handleClickFueraColSelector);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickFueraColSelector);
    });

    return {
      uniqueAreas,
      filterEmpresa, filterArea, filterDesde, filterHasta, filterNroDoc,
      filterMotivo, filterPago, hayFiltros, clearFilters,
      sortKey, sortDir, setSort, sortedArchivados,
      mostrarModal, detalle, abrirDetalle, cerrarModal,
      formatDate, formatAreaTematica, formatMonto, labelPago, badgePago, badgeMotivo,
      COLS, colVisible, colsOcultas, mostrarColSelector, colSelectorRef,
      toggleColSelector, mostrarTodasCols,
      exportarExcel,
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

/* Selector de columnas */
.col-selector-wrap {
  position: relative;
}

.col-selector-panel {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.13);
  z-index: 500;
  min-width: 200px;
  overflow: hidden;
}

.col-sel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  font-size: 0.8rem;
  font-weight: 600;
  color: #555;
}

.col-sel-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.12s;
  user-select: none;
}
.col-sel-item:hover { background: #f0f4f8; }
.col-sel-item input[type="checkbox"] { cursor: pointer; }
</style>
