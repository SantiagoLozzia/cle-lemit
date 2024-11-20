<template>
  <div>
    <table class="table table-hover">
      <thead class="text-center">
        <tr>
          <th>Nro</th>
          <th>Fecha</th>
          <th>Solicitante</th>
          <th>Area Tematica</th>
          <th>ST-01 Presupuesto</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(presupuesto, index) in presupuestos" :key="index">
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
                  <option value="rechazado">Rechazado</option>
                  <option value="modificado">Modificado</option>
                  <option value="actualizado">Actualizado</option>
                </select>
                <button @click="cambiarEstado(presupuesto)" class="btn btn-primary">Guardar</button>
                <button @click="cerrarMenu(index)" class="btn btn-danger">✖</button> <!-- Botón de cerrar -->
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
            <button type="button" class="btn-close" @click="cerrarModalPresupuesto" aria-label="Close"></button>
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
                      <th class="text-center">Cantidad</th>
                      <th class="text-center">Subtotal</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="detalle in detallesPresupuesto" :key="detalle.nro_servicio">
                      <td class="text-center">{{ detalle.nro_servicio }}</td>
                      <td class="text-left">{{ detalle.nombre_servicio }}</td>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
      const presupuestos = ref([]);

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
          const response = await axios.get('http://localhost:8000/api/presupuestos/en_espera/');
          // Formatear los datos antes de asignarlos a presupuestos.value
          presupuestos.value = response.data.map(presupuesto => ({
              ...presupuesto,
              fecha: formatDate(presupuesto.fecha_presupuesto),
              area_tematica: formatAreaTematica(presupuesto.area_tematica),
              estado_presupuesto: formatEstadoPresupuesto(presupuesto.estado_presupuesto),
              mostrarMenu: false, // Agregar propiedad para controlar la visibilidad del menú
              nuevoEstado: '' // Nuevo estado seleccionado
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
        axios.get(`http://localhost:8000/api/presupuestos/obtener_presupuesto/${nro_presupuesto}/`)
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
          // Restablecer el nuevo estado seleccionado
          presupuestos.value[index].nuevoEstado = '';
      };

      const cambiarEstado = async (presupuesto) => {
          try {
              // Realizar la petición para actualizar el estado del presupuesto en la base de datos
              const response = await axios.put(`http://localhost:8000/api/presupuestos/actualizar_estado/${presupuesto.nro_presupuesto}/`, {
              estado_presupuesto: presupuesto.nuevoEstado
              });
      
              // Verificar si la actualización fue exitosa
              if (response.status === 200) {
              console.log('Estado del presupuesto actualizado correctamente:', presupuesto.nuevoEstado);
              // Recargar la página para reflejar los cambios actualizados
              location.reload();
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
