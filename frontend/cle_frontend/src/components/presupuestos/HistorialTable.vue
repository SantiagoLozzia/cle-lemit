<template>
  <div>
    <PageHeader title="Historial de Presupuestos" :subtitle="buscado && resultados.length > 0 ? resultados.length + ' resultados' : ''" icon="bi bi-clock-history" />

    <!-- Barra de filtros -->
    <div class="filter-bar mb-3 d-flex flex-wrap align-items-end gap-2">
      <div class="d-flex flex-column">
        <small class="text-muted">Nro</small>
        <input v-model="filtros.nro" type="number" placeholder="Ej: 42" class="form-control form-control-sm" style="width:90px">
      </div>
      <div class="d-flex flex-column">
        <small class="text-muted">Solicitante</small>
        <input v-model="filtros.solicitante" type="text" placeholder="Nombre empresa..." class="form-control form-control-sm" style="min-width:180px">
      </div>
      <div class="d-flex flex-column">
        <small class="text-muted">Desde</small>
        <input v-model="filtros.desde" type="date" class="form-control form-control-sm w-auto">
      </div>
      <div class="d-flex flex-column">
        <small class="text-muted">Hasta</small>
        <input v-model="filtros.hasta" type="date" class="form-control form-control-sm w-auto">
      </div>
      <div class="d-flex flex-column">
        <small class="text-muted">Área</small>
        <select v-model="filtros.area" class="form-select form-select-sm w-auto">
          <option value="">Todas</option>
          <option v-for="area in AREAS_TEMATICAS" :key="area.value" :value="area.value">{{ area.label }}</option>
        </select>
      </div>
      <div class="d-flex flex-column">
        <small class="text-muted">Estado</small>
        <select v-model="filtros.estado" class="form-select form-select-sm w-auto">
          <option value="">Todos</option>
          <option value="en_espera">Nuevo</option>
          <option value="aceptado">Aceptado</option>
          <option value="descartado">Descartado</option>
        </select>
      </div>
      <div class="d-flex gap-2 align-self-end">
        <button @click="buscar" class="btn btn-primary btn-sm" :disabled="cargando">
          <span v-if="cargando" class="spinner-border spinner-border-sm me-1"></span>
          Buscar
        </button>
        <button v-if="buscado" @click="limpiar" class="btn btn-outline-secondary btn-sm">✕ Limpiar</button>
      </div>
    </div>

    <!-- Sin búsqueda todavía -->
    <div v-if="!buscado" class="text-center text-muted py-5">
      <i class="bi bi-search" style="font-size:2.5rem; opacity:0.3"></i>
      <p class="mt-2">Aplicá al menos un filtro y presioná Buscar</p>
    </div>

    <!-- Sin resultados -->
    <div v-else-if="resultados.length === 0" class="text-center text-muted py-5">
      <i class="bi bi-inbox" style="font-size:2.5rem; opacity:0.3"></i>
      <p class="mt-2">No hay presupuestos que coincidan con los filtros</p>
    </div>

    <!-- Tabla de resultados -->
    <table v-else class="table table-hover">
      <thead>
        <tr>
          <th>Nro</th>
          <th>Fecha</th>
          <th>Solicitante</th>
          <th>Área</th>
          <th>Estado</th>
          <th>Motivo</th>
          <th>DS</th>
          <th>Legajo</th>
          <th>ST-01</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in resultados" :key="p.nro_presupuesto">
          <td>{{ p.nro_presupuesto }}</td>
          <td>{{ formatDate(p.fecha_presupuesto) }}</td>
          <td class="text-left">{{ p.nombre_solicitante }}</td>
          <td>{{ formatArea(p.area_tematica) }}</td>
          <td>
            <span :class="estadoBadge(p.estado_presupuesto)" class="badge">
              {{ estadoLabel(p.estado_presupuesto) }}
            </span>
          </td>
          <td class="text-left motivo-cell" :title="p.motivo_descarte_label">{{ p.motivo_descarte_label || '—' }}</td>
          <td>{{ p.nro_dataServicio || '—' }}</td>
          <td>{{ p.nro_legajo || '—' }}</td>
          <td>
            <i class="bi bi-file-earmark-check-fill text-success" style="cursor:pointer" @click="abrirPresupuesto(p.nro_presupuesto)"></i>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Modal Presupuesto -->
  <div class="modal" :class="{ 'show': mostrarModal }" id="mostrarModalPresupuesto">
    <div class="modal-dialog-a4">
      <div class="modal-content">
        <div class="modal-header" style="flex-direction: column; align-items: stretch; gap: 6px;">
          <ISOHeader :config="configFormulario" :versionDoc="versionPresupuesto" />
          <div class="d-flex justify-content-end gap-2 no-print">
            <button type="button" class="btn btn-sm btn-outline-secondary" @click="() => window.print()" title="Imprimir">
              <i class="bi bi-printer"></i>
            </button>
            <button type="button" class="btn-close" @click="mostrarModal = false"></button>
          </div>
        </div>
        <div class="modal-body">
          <form class="was-validated">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h1 class="modal-title fs-5 fw-bold">Presupuesto N° {{ datosPres.nro }}</h1>
              <div class="text-right">
                <span class="d-block"><strong>CUIT: 33-68485414-9</strong></span>
                <span class="d-block"><strong>I.V.A.: Exento</strong></span>
                <span class="d-block"><strong>Ingresos Brutos: Exento</strong></span>
                <span class="d-block"><strong>Ganancias: Exento</strong></span>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Fecha:</label>
              <span><strong>{{ datosPres.fecha }}</strong></span>
            </div>
            <div class="mb-3">
              <label class="form-label">Solicitante:</label>
              <span><strong>{{ datosPres.solicitante }}</strong> (COD {{ datosPres.nroSolicitante }})</span>
            </div>
            <div class="mb-3">
              <label class="form-label">Contacto:</label>
              <span><strong>{{ datosPres.contacto }}</strong></span>
            </div>
            <div class="mb-3">
              <label class="form-label">Area Temática:</label>
              <span><strong>{{ datosPres.area }}</strong></span>
            </div>
            <div class="mb-3">
              <table class="table">
                <thead>
                  <tr>
                    <th class="text-center">Cod.</th>
                    <th class="text-center">Nombre Servicio</th>
                    <th class="text-center">Norma</th>
                    <th class="text-center">Cantidad</th>
                    <th class="text-center">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="detalle in datosPres.detalles" :key="detalle.nro_servicio">
                    <td class="text-center">{{ detalle.nro_servicio }}</td>
                    <td class="text-left">{{ detalle.nombre_servicio }}</td>
                    <td class="text-center">{{ detalle.norma }}</td>
                    <td class="text-center">{{ detalle.cant }}</td>
                    <td class="text-right">{{ formatArancel(detalle.subtotal) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="d-flex flex-column align-items-end mb-3">
              <div class="mb-3">
                <label class="form-label">SubTotal:</label>
                <span><strong>{{ datosPres.subtotal }}</strong></span>
              </div>
              <div v-if="datosPres.descuento > 0" class="mb-3">
                <label class="form-label">Descuento:</label>
                <span><strong>{{ datosPres.descuento }}%</strong></span>
              </div>
              <div class="mb-3">
                <label class="form-label">Total:</label>
                <span><strong>{{ datosPres.arancel }}</strong></span>
              </div>
            </div>
            <hr>
            <div>
              <span class="d-block fs-7"><strong>Notas:</strong></span>
              <span class="d-block fs-7">Los presupuestos tienen una validez de 30 días</span>
              <span class="d-block fs-7">El valor cotizado es con IVA incluido</span>
            </div>
            <hr>
            <div class="mb-3">
              <label class="form-label">Observaciones:</label>
              <input v-model="datosPres.observaciones" type="text" class="form-control" readonly />
            </div>
          </form>
        </div>
        <div v-if="configFormulario.revisiones && configFormulario.revisiones.length" class="revision-history-wrapper">
          <table class="revision-history-table">
            <thead>
              <tr><th colspan="4" class="revision-title">Historial de Revisiones</th></tr>
              <tr><th>Versión</th><th>Fecha</th><th>Descripción</th><th>Aprobado por</th></tr>
            </thead>
            <tbody>
              <tr v-for="rev in configFormulario.revisiones" :key="rev.version">
                <td class="text-center">{{ rev.version }}</td>
                <td class="text-center">{{ rev.fecha }}</td>
                <td>{{ rev.descripcion }}</td>
                <td>{{ rev.aprobado_por }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer-a4">
          <div class="footer-image"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import api from '@/api.js';
import PageHeader from '@/components/PageHeader.vue';
import ISOHeader from '@/components/ISOHeader.vue';

const AREAS_TEMATICAS = [
  { value: 'durabilidad', label: 'Durabilidad' },
  { value: 'ensayos_mecanicos', label: 'Ensayos Mecánicos' },
  { value: 'geologia', label: 'Geología' },
  { value: 'hormigones', label: 'Hormigones' },
  { value: 'metalurgia', label: 'Metalurgia' },
  { value: 'patrimonio', label: 'Patrimonio' },
  { value: 'quimica', label: 'Química' },
  { value: 'tecnologia_vial', label: 'Tecnología Vial' },
  { value: 'estudios_especiales', label: 'Estudios Especiales' },
  { value: 'servicios_tecnologicos', label: 'Servicios Tecnológicos' },
  { value: 'direccion', label: 'Dirección' },
];

const ESTADO_LABELS = {
  en_espera: 'Nuevo',
  aceptado: 'Aceptado',
  descartado: 'Descartado',
  rechazado: 'Descartado',
  modificado: 'Descartado',
  actualizado: 'Descartado',
};

const ESTADO_BADGES = {
  en_espera: 'bg-primary',
  aceptado: 'bg-success',
  descartado: 'bg-danger',
  rechazado: 'bg-danger',
  modificado: 'bg-danger',
  actualizado: 'bg-danger',
};

export default {
  components: { PageHeader, ISOHeader },
  setup() {
    const filtros = reactive({ nro: '', solicitante: '', desde: '', hasta: '', area: '', estado: '' });
    const resultados = ref([]);
    const buscado = ref(false);
    const cargando = ref(false);

    const mostrarModal = ref(false);
    const versionPresupuesto = ref('01');
    const configFormulario = ref({ nombre: '', codigo: '', version_actual: '', fecha_version_actual: '', revisiones: [] });
    const datosPres = reactive({
      nro: null, fecha: '', solicitante: '', nroSolicitante: null, contacto: '',
      area: '', subtotal: '', descuento: 0, arancel: '', observaciones: '', detalles: [],
    });

    const buscar = async () => {
      if (!filtros.nro && !filtros.solicitante && !filtros.desde && !filtros.hasta && !filtros.area && !filtros.estado) {
        alert('Ingresá al menos un filtro para buscar.');
        return;
      }
      cargando.value = true;
      try {
        const params = {};
        if (filtros.nro) params.nro = filtros.nro;
        if (filtros.solicitante) params.solicitante = filtros.solicitante;
        if (filtros.desde) params.desde = filtros.desde;
        if (filtros.hasta) params.hasta = filtros.hasta;
        if (filtros.area) params.area = filtros.area;
        if (filtros.estado) params.estado = filtros.estado;
        const res = await api.get('/presupuestos/historial/', { params });
        resultados.value = res.data;
        buscado.value = true;
      } catch (error) {
        console.error('Error al buscar historial:', error);
      } finally {
        cargando.value = false;
      }
    };

    const limpiar = () => {
      filtros.nro = ''; filtros.solicitante = ''; filtros.desde = '';
      filtros.hasta = ''; filtros.area = ''; filtros.estado = '';
      resultados.value = [];
      buscado.value = false;
    };

    const formatDate = (d) => {
      if (!d) return '';
      const [y, m, day] = d.split('-');
      return `${day}/${m}/${y}`;
    };

    const formatArea = (a) => a ? a.replace(/_/g, ' ').replace(/\w\S*/g, t => t.charAt(0).toUpperCase() + t.substr(1).toLowerCase()) : '';

    const formatArancel = (v) => isNaN(v) ? v : '$ ' + parseFloat(v).toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

    const estadoLabel = (e) => ESTADO_LABELS[e] || e;
    const estadoBadge = (e) => ESTADO_BADGES[e] || 'bg-secondary';

    const abrirPresupuesto = async (nro) => {
      try {
        const [resP, resC] = await Promise.all([
          api.get(`/presupuestos/obtener_presupuesto/${nro}/`),
          api.get('/encurso/config_formulario/presupuesto/'),
        ]);
        const d = resP.data;
        datosPres.nro = d.nro_presupuesto;
        datosPres.fecha = formatDate(d.fecha_presupuesto);
        datosPres.nroSolicitante = d.nro_solicitante;
        datosPres.solicitante = d.nombre_solicitante;
        datosPres.contacto = d.contacto;
        datosPres.area = formatArea(d.area_tematica);
        datosPres.subtotal = formatArancel(d.subtotal);
        datosPres.descuento = d.descuento;
        datosPres.arancel = formatArancel(d.arancel_presupuesto);
        datosPres.observaciones = d.observaciones;
        datosPres.detalles = d.detalles_presupuesto;
        versionPresupuesto.value = d.version_formulario || '01';
        configFormulario.value = resC.data;
        mostrarModal.value = true;
      } catch (e) {
        console.error('Error al abrir presupuesto:', e);
      }
    };

    return {
      AREAS_TEMATICAS, filtros, resultados, buscado, cargando,
      mostrarModal, versionPresupuesto, configFormulario, datosPres,
      buscar, limpiar, formatDate, formatArea, formatArancel,
      estadoLabel, estadoBadge, abrirPresupuesto,
    };
  },
};
</script>

<style scoped>
.motivo-cell {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.revision-history-wrapper {
  padding: 0 1.25rem 0.5rem;
}

.revision-history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.72rem;
}

.revision-history-table th,
.revision-history-table td {
  border: 1px solid #ccc;
  padding: 3px 8px;
}

.revision-title {
  text-align: center;
  font-weight: 700;
  background-color: #f0f0f0;
}
</style>
