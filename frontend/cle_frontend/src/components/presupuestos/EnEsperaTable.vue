<template>
  <div>
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
            <div class="acciones">
              <button @click="mostrarMenu(index)" class="btn btn-link"><i class="bi bi-arrow-right-square"></i></button>
              <!-- Menú desplegable para cambiar el estado -->
              <div v-if="presupuesto.mostrarMenu" class="menu">
                <select v-model="presupuesto.nuevoEstado" class="form-select">
                  <option value="" disabled>— Seleccionar —</option>
                  <option value="rechazado">Rechazado</option>
                  <option value="modificado">Modificado</option>
                  <option value="actualizado">Actualizado</option>
                </select>
                <textarea
                  v-if="['rechazado','modificado','actualizado'].includes(presupuesto.nuevoEstado)"
                  v-model="presupuesto.motivo"
                  class="form-control mt-1"
                  rows="2"
                  placeholder="Motivo (requerido)..."
                  style="min-width:200px"
                ></textarea>
                <button @click="cambiarEstado(presupuesto)" class="btn btn-primary mt-1">Guardar</button>
                <button @click="cerrarMenu(index)" class="btn btn-danger mt-1">✖</button>
              </div>
            </div>
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
          <div class="modal-header">
            <div class="modal-logo"></div>
            <div class="d-flex align-items-center gap-2 no-print">
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
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
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

      const mostrarModalPresupuesto = ref(false);

      const fetchPresupuestos = async () => {
          try {
          const response = await api.get('/presupuestos/en_espera/');
          // Formatear los datos antes de asignarlos a presupuestos.value
          presupuestos.value = response.data.map(presupuesto => ({
              ...presupuesto,
              fecha: formatDate(presupuesto.fecha_presupuesto),
              area_tematica: formatAreaTematica(presupuesto.area_tematica),
              estado_presupuesto: formatEstadoPresupuesto(presupuesto.estado_presupuesto),
              mostrarMenu: false,
              nuevoEstado: '',
              motivo: '',
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

      const abrirPresupuesto = (nro_presupuesto) => {
        api.get(`/presupuestos/obtener_presupuesto/${nro_presupuesto}/`)
            .then(response => {
                // Obtener los datos del presupuesto de la respuesta
                const { nro_presupuesto, fecha_presupuesto, contacto, telefono, telefono2, email, email2, area_tematica, subtotal, descuento, arancel_presupuesto, observaciones, nro_solicitante, nombre_solicitante, detalles_presupuesto  } = response.data;

                // Asignar los datos a variables en el contexto del componente
                nroPresupuesto.value = nro_presupuesto;
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
                observacionesPresupuesto.value = observaciones ;
                detallesPresupuesto.value = detalles_presupuesto;

                // Mostrar el modal para mostrar los detalles del presupuesto
                mostrarModalPresupuesto.value = true;
            })
            .catch(error => {
                console.error('Error al obtener los datos del legajo:', error);
                // Manejar el error, mostrar un mensaje al usuario, etc.
            });
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

      // Función para mostrar u ocultar el menú desplegable
      const mostrarMenu = (index) => {
          presupuestos.value.forEach((presupuesto, i) => {
          if (i === index) {
              presupuesto.mostrarMenu = !presupuesto.mostrarMenu;
          } else {
              presupuesto.mostrarMenu = false;
          }
          });
      };

      const cerrarMenu = (index) => {
          presupuestos.value[index].mostrarMenu = false;
          presupuestos.value[index].nuevoEstado = '';
          presupuestos.value[index].motivo = '';
      };

      const ESTADOS_CANCELADOS = ['rechazado', 'modificado', 'actualizado'];

      const cambiarEstado = async (presupuesto) => {
          if (!presupuesto.nuevoEstado) return;
          if (ESTADOS_CANCELADOS.includes(presupuesto.nuevoEstado) && !presupuesto.motivo.trim()) {
              alert('Por favor, ingresá un motivo para este cambio de estado.');
              return;
          }
          try {
              const payload = { estado_presupuesto: presupuesto.nuevoEstado };
              if (ESTADOS_CANCELADOS.includes(presupuesto.nuevoEstado)) {
                  payload.motivo_cancelacion = presupuesto.motivo.trim();
              }
              const response = await api.put(`/presupuestos/actualizar_estado/${presupuesto.nro_presupuesto}/`, payload);
      
              // Verificar si la actualización fue exitosa
              if (response.status === 200) {
              console.log('Estado del presupuesto actualizado correctamente:', presupuesto.nuevoEstado);
              fetchPresupuestos();
              } else {
              console.error('Error al actualizar el estado del presupuesto:', response.statusText);
              }
          } catch (error) {
              console.error('Error al cambiar el estado del presupuesto:', error);
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
        formatDate,
        formatAreaTematica,
        formatArancel,
        mostrarModalPresupuesto,
        cerrarModalPresupuesto,
        imprimirPresupuesto,
        mostrarMenu,
        cambiarEstado,
        cerrarMenu,
        abrirPresupuesto,
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
  margin-right: 1rem; /* Espacio entre los elementos */
  /* O usa `margin-right: 0.5rem;` para espacio más pequeño */
}
</style>
