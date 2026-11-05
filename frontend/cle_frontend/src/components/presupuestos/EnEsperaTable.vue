<template>
  <div>
    <PageHeader title="Presupuestos nuevos" :subtitle="sortedPresupuestos.length + ' presupuestos'" icon="bi bi-hourglass-split" />
    <div class="filter-bar mb-2 d-flex flex-wrap align-items-center gap-2">
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
      <button v-if="filterArea || filterDesde || filterHasta" @click="clearFilters" class="btn btn-sm btn-outline-secondary">✕ Limpiar</button>
    </div>
    <table class="table table-hover">
      <thead class="text-center">
        <tr>
          <th class="sortable" @click="setSort('nro_presupuesto')">Nro <span class="sort-icon">{{ sortKey === 'nro_presupuesto' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
          <th class="sortable" @click="setSort('fecha_presupuesto')">Fecha <span class="sort-icon">{{ sortKey === 'fecha_presupuesto' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
          <th>Solicitante</th>
          <th>Area Tematica</th>
          <th>ST-01 Presupuesto</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(presupuesto, index) in sortedPresupuestos" :key="index">
          <td>{{ presupuesto.nro_presupuesto }}</td>
          <td>{{ presupuesto.fecha }}</td>
          <td class="text-left">{{ presupuesto.nombre_solicitante }}</td>
          <td>{{ presupuesto.area_tematica }}</td>
          <td><i class="bi bi-file-earmark-check-fill text-success"  style="cursor: pointer;" @click="abrirPresupuesto(presupuesto.nro_presupuesto)"></i></td>
          <td>
            <button @click="abrirModalDescartar(presupuesto)" class="btn btn-sm btn-outline-danger" title="Descartar presupuesto">
              <i class="bi bi-x-circle"></i>
            </button>
          </td>
        </tr>
        <!-- Fila para mensaje cuando no hay datos -->
        <tr v-if="presupuestos.length === 0" class="no-results">
          <td colspan="6">No hay resultados para mostrar</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Modal para mostrar Presupuesto -->
  <div class="modal" :class="{ 'show': mostrarModalPresupuesto}" id="mostrarModalPresupuesto">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header" style="flex-direction: column; align-items: stretch; gap: 6px;">
            <ISOHeader :config="configFormularioPresupuesto" :versionDoc="versionPresupuesto" />
            <div class="d-flex justify-content-end gap-2 no-print">
              <button type="button" class="btn btn-sm btn-outline-secondary" @click="imprimirPresupuesto" title="Imprimir / Guardar como PDF">
                <i class="bi bi-printer"></i>
              </button>
              <button type="button" class="btn-close" @click="cerrarModalPresupuesto" aria-label="Close"></button>
            </div>
          </div>
          <!-- Modal Body -->
          <div class="modal-body">
            <form class="was-validated">
              <div class="d-flex justify-content-between align-items-center mb-3">
                  <h1 class="modal-title fs-5 fw-bold">Presupuesto N° {{ nroPresupuesto }}</h1>
                  <div class="text-right">
                      <span class="d-block"><strong>CUIT: 33-68485414-9</strong></span>
                      <span class="d-block"><strong>I.V.A.: Exento</strong></span>
                      <span class="d-block"><strong>Ingresos Brutos: Exento</strong></span>
                      <span class="d-block"><strong>Ganancias: Exento</strong></span>
                  </div>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Fecha:</label>
                <span><strong>{{ fechaPresupuesto }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Solicitante:</label>
                <span><strong>{{ solicitantePresupuesto }}</strong> (COD {{ nroSolicitantePresupuesto }})</span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Contacto:</label>
                <span><strong>{{ contactoPresupuesto }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Area Temática:</label>
                <span><strong>{{ areaPresupuesto }}</strong></span>
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
                    <tr v-for="detalle in detallesPresupuesto" :key="detalle.nro_servicio">
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
                      <span><strong>{{ subTotalPresupuesto }}</strong></span>
                  </div>

                  <div v-if="descuentoPresupuesto > 0" class="mb-3">
                      <label class="form-label">Descuento:</label>
                      <span><strong>{{ descuentoPresupuesto }}%</strong></span>
                  </div>

                  <div class="mb-3">
                      <label class="form-label">Total:</label>
                      <span><strong>{{ arancelPresupuesto }}</strong></span>
                  </div>
              </div>

              <hr> <!-- Línea horizontal para separar del contenido de arriba -->

              <div>
                  <span class="d-block fs-7"><strong>Notas:</strong></span>
                  <span class="d-block fs-7">Los presupuestos tienen una validez de 30 días</span>
                  <span class="d-block fs-7">El valor cotizado es con IVA incluido</span>
              </div>

              <hr> <!-- Línea horizontal para separar del contenido de arriba -->
              
              <div class="mb-3">
                <label for="observacionesPresupuesto" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesPresupuesto" type="text" class="form-control" id="observacionesPresupuesto" name="observacionesPresupuesto" readonly required />
              </div>
              
            </form>
          </div>
          <!-- Historial de revisiones del formulario -->
          <div v-if="configFormularioPresupuesto.revisiones && configFormularioPresupuesto.revisiones.length" class="revision-history-wrapper">
            <table class="revision-history-table">
              <thead>
                <tr>
                  <th colspan="4" class="revision-title">Historial de Revisiones</th>
                </tr>
                <tr>
                  <th>Versión</th>
                  <th>Fecha</th>
                  <th>Descripción</th>
                  <th>Aprobado por</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="rev in configFormularioPresupuesto.revisiones" :key="rev.version">
                  <td class="text-center">{{ rev.version }}</td>
                  <td class="text-center">{{ rev.fecha }}</td>
                  <td>{{ rev.descripcion }}</td>
                  <td>{{ rev.aprobado_por }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
          </div>
        </div>
      </div>
    </div>

  <!-- Modal Descartar Presupuesto -->
  <div class="modal" :class="{ 'show': mostrarModalDescartar }">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Descartar Presupuesto N° {{ presupuestoADescartar?.nro_presupuesto }}</h5>
          <button type="button" class="btn-close" @click="cerrarModalDescartar"></button>
        </div>
        <div class="modal-body">
          <label class="form-label fw-bold">Motivo</label>
          <select v-model="motivoDescarte" class="form-select">
            <option value="" disabled>— Seleccionar motivo —</option>
            <option value="nuevo_presupuesto">Se generó un nuevo presupuesto</option>
            <option value="rechazo">Rechazado por el cliente</option>
            <option value="sin_respuesta">Sin respuesta del cliente</option>
            <option value="otro">Otro</option>
          </select>
        </div>
        <div class="modal-footer">
          <button @click="cerrarModalDescartar" class="btn btn-secondary">Cancelar</button>
          <button @click="confirmarDescarte" class="btn btn-danger" :disabled="!motivoDescarte">Descartar</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/api.js';
import { AREAS_TEMATICAS } from '@/constants/areas.js';
import PageHeader from '@/components/PageHeader.vue';
import ISOHeader from '@/components/ISOHeader.vue';

export default {
  components: { PageHeader, ISOHeader },
  setup() {
      const presupuestos = ref([]);

      const sortKey = ref('');
      const sortDir = ref('asc');
      const sortedPresupuestos = computed(() => {
        if (!sortKey.value) return filteredPresupuestos.value;
        return [...filteredPresupuestos.value].sort((a, b) => {
          const valA = sortKey.value === 'nro_presupuesto' ? Number(a[sortKey.value]) : a[sortKey.value];
          const valB = sortKey.value === 'nro_presupuesto' ? Number(b[sortKey.value]) : b[sortKey.value];
          if (valA < valB) return sortDir.value === 'asc' ? -1 : 1;
          if (valA > valB) return sortDir.value === 'asc' ? 1 : -1;
          return 0;
        });
      });
      const setSort = (key) => {
        if (sortKey.value === key) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
        else { sortKey.value = key; sortDir.value = 'asc'; }
      };

      const filterArea = ref('');
      const filterDesde = ref('');
      const filterHasta = ref('');

      const uniqueAreas = AREAS_TEMATICAS;

      const filteredPresupuestos = computed(() => presupuestos.value.filter(p => {
        const areaOk = !filterArea.value || p.area_tematica === filterArea.value;
        const desdeOk = !filterDesde.value || p.fecha_presupuesto >= filterDesde.value;
        const hastaOk = !filterHasta.value || p.fecha_presupuesto <= filterHasta.value;
        return areaOk && desdeOk && hastaOk;
      }));

      const clearFilters = () => { filterArea.value = ''; filterDesde.value = ''; filterHasta.value = ''; };

      const nroPresupuesto = ref();
      const fechaPresupuesto = ref();
      const nroSolicitantePresupuesto = ref();
      const solicitantePresupuesto = ref();
      const contactoPresupuesto = ref();
      const telefonoPresupuesto = ref();
      const telefono2Presupuesto = ref();
      const emailPresupuesto = ref();
      const email2Presupuesto = ref();
      const areaPresupuesto = ref();
      const subTotalPresupuesto = ref();
      const descuentoPresupuesto = ref();
      const arancelPresupuesto = ref();
      const observacionesPresupuesto = ref();
      const detallesPresupuesto = ref();
      const versionPresupuesto = ref('01');
      const configFormularioPresupuesto = ref({ nombre: '', codigo: '', version_actual: '', fecha_version_actual: '', revisiones: [] });

      const mostrarModalPresupuesto = ref(false);

      const fetchPresupuestos = async () => {
          try {
          const response = await api.get('/presupuestos/en_espera/');
          presupuestos.value = response.data.map(presupuesto => ({
              ...presupuesto,
              fecha: formatDate(presupuesto.fecha_presupuesto),
              area_tematica: formatAreaTematica(presupuesto.area_tematica),
              estado_presupuesto: formatEstadoPresupuesto(presupuesto.estado_presupuesto),
          }));
          } catch (error) {
          console.error('Error al obtener presupuestos:', error);
          }
      };
      
      // Función para formatear el campo fecha
      const formatDate = (dateString) => {
          const [year, month, day] = dateString.split('-');
          return `${day}/${month}/${year}`;
      };

      // Función para formatear el campo area_tematica
      const formatAreaTematica = (areaTematica) => {
          return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      };

      // Función para formatear el campo estado_presupuesto
      const formatEstadoPresupuesto = (estadoPresupuesto) => {
          return estadoPresupuesto.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      };

      const abrirPresupuesto = async (nro_presupuesto) => {
        try {
            const [resPresupuesto, resConfig] = await Promise.all([
              api.get(`/presupuestos/obtener_presupuesto/${nro_presupuesto}/`),
              api.get('/encurso/config_formulario/presupuesto/'),
            ]);

            const { nro_presupuesto: nro, fecha_presupuesto, contacto, telefono, telefono2, email, email2, area_tematica, subtotal, descuento, arancel_presupuesto, observaciones, nro_solicitante, nombre_solicitante, detalles_presupuesto, version_formulario } = resPresupuesto.data;

            nroPresupuesto.value = nro;
            fechaPresupuesto.value = formatDate(fecha_presupuesto);
            nroSolicitantePresupuesto.value = nro_solicitante;
            solicitantePresupuesto.value = nombre_solicitante;
            contactoPresupuesto.value = contacto;
            telefonoPresupuesto.value = telefono;
            telefono2Presupuesto.value = telefono2;
            emailPresupuesto.value = email;
            email2Presupuesto.value = email2;
            areaPresupuesto.value = formatAreaTematica(area_tematica);
            subTotalPresupuesto.value = formatArancel(subtotal);
            descuentoPresupuesto.value = descuento;
            arancelPresupuesto.value = formatArancel(arancel_presupuesto);
            observacionesPresupuesto.value = observaciones;
            detallesPresupuesto.value = detalles_presupuesto;
            versionPresupuesto.value = version_formulario || '01';
            configFormularioPresupuesto.value = resConfig.data;

            mostrarModalPresupuesto.value = true;
        } catch (error) {
            console.error('Error al obtener los datos del presupuesto:', error);
        }
      };

      const cerrarModalPresupuesto = () => {
        mostrarModalPresupuesto.value = false;
      };

      const imprimirPresupuesto = () => { window.print(); };

      const formatArancel = (arancel) => {
          // Verificar si arancel es numérico
          if (!isNaN(arancel)) {
              // Convertir a número entero y formatear con signo $ y separación de miles
              return '$ ' + parseFloat(arancel).toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
          } else {
              // Si no es numérico, devolver el valor sin formato
              return arancel;
          }
      };

      const mostrarModalDescartar = ref(false);
      const presupuestoADescartar = ref(null);
      const motivoDescarte = ref('');

      const abrirModalDescartar = (presupuesto) => {
          presupuestoADescartar.value = presupuesto;
          motivoDescarte.value = '';
          mostrarModalDescartar.value = true;
      };

      const cerrarModalDescartar = () => {
          mostrarModalDescartar.value = false;
          presupuestoADescartar.value = null;
          motivoDescarte.value = '';
      };

      const confirmarDescarte = async () => {
          if (!motivoDescarte.value || !presupuestoADescartar.value) return;
          try {
              const response = await api.put(`/presupuestos/actualizar_estado/${presupuestoADescartar.value.nro_presupuesto}/`, {
                  estado_presupuesto: 'descartado',
                  motivo_descarte: motivoDescarte.value,
              });
              if (response.status === 200) {
                  cerrarModalDescartar();
                  fetchPresupuestos();
              }
          } catch (error) {
              console.error('Error al descartar el presupuesto:', error);
          }
      };

      onMounted(fetchPresupuestos); // Utilizamos onMounted para llamar a fetchPresupuestos en la creación del componente
  
      return {
        presupuestos,
        sortKey, sortDir, sortedPresupuestos, setSort,
        filterArea, filterDesde, filterHasta, uniqueAreas, clearFilters,
        nroPresupuesto,
        fechaPresupuesto,
        contactoPresupuesto,
        telefonoPresupuesto,
        telefono2Presupuesto,
        emailPresupuesto,
        email2Presupuesto,
        areaPresupuesto,
        subTotalPresupuesto,
        descuentoPresupuesto,
        arancelPresupuesto,
        nroSolicitantePresupuesto,
        solicitantePresupuesto,
        observacionesPresupuesto,
        detallesPresupuesto,
        versionPresupuesto,
        configFormularioPresupuesto,
        formatDate,
        formatAreaTematica,
        formatArancel,
        mostrarModalPresupuesto,
        cerrarModalPresupuesto,
        imprimirPresupuesto,
        abrirPresupuesto,
        mostrarModalDescartar,
        presupuestoADescartar,
        motivoDescarte,
        abrirModalDescartar,
        cerrarModalDescartar,
        confirmarDescarte,
      };
  }
};
</script>

<style scoped>

.menu {
  position: absolute;
  z-index: 1;
  background-color: #fff;
  border: 1px solid #ced4da;
  padding: 5px;
  margin-top: -50px;
  border-radius: 5px;
}
.menu select {
  width: auto;
  padding: 6px 25px;
  font-size: 14px;
}
.acciones {
  position: relative;
}

.table tbody tr.no-results td {
  text-align: center; /* Centrar el texto en la celda */
  color: #6c757d; /* Color gris para el texto */
  border-bottom: none; /* Eliminar la línea inferior */
  padding: 50px; /* Ajustar el padding según sea necesario */
  font-size: 2rem; /* Tamaño de la letra, ajustar según sea necesario */
}

.info-separado {
  margin-bottom: 1rem; /* Espacio entre los bloques */
}

.info-contenedor {
  display: flex;
  flex-wrap: wrap; /* Para permitir que los elementos se envuelvan si no caben en una línea */
}

.info-contenedor span {
  margin-right: 1rem;
}

.revision-history-wrapper {
  padding: 0 1rem 0.5rem;
}

.revision-history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.72rem;
  margin-top: 12px;
}

.revision-history-table th,
.revision-history-table td {
  border: 1px solid #aaa;
  padding: 3px 6px;
  text-align: left;
  vertical-align: middle;
}

.revision-history-table th {
  background-color: #e8f0f7 !important;
  color: #333 !important;
  font-weight: 600;
}

.revision-title {
  text-align: center !important;
  font-weight: 700;
  background-color: #cfe0f0 !important;
  color: #1a3a5c !important;
  padding: 4px !important;
  font-size: 0.75rem;
}
</style>
