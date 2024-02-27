<template>
    <div>
      <table class="table">
        <thead>
          <tr>
            <th colspan="6">Solicitud de Servicio</th>
            <th colspan="6">Legajo</th>
            <th colspan="3">Recepcion</th>
            <th colspan="2">Orden de Servicio</th>
            <th colspan="3">Informe de Area</th>
            <th colspan="3">Inter Area</th>
            <th colspan="1">Informe Area</th>
            <th colspan="1">Administracion</th>
            <th colspan="1">Servicios Tecnologicos</th>
            <th colspan="1">Responsable Area</th>
            <th colspan="1">Direccion</th>
          </tr>
          <tr>
            <!-- Subcolumnas de Solicitud de Servicio -->
            <th>N°</th>
            <th>Fecha</th>
            <th>Area Tematica</th>
            <th>N° Presupuesto</th>
            <th>Data Servicio</th>
            <th>Adjunto</th>
            <!-- Subcolumnas de Legajo -->
            <th>N°</th>
            <th>Fecha</th>
            <th>Legajo</th>
            <th>Factura</th>
            <th>Pago</th>
            <th>Plazo</th>
            <!-- Subcolumnas de Recepcion -->
            <th>N° Remitos</th>
            <th>Muestras</th>
            <th>Plazo</th>
            <!-- Subcolumnas de Orden de Servicio -->
            <th>OS</th>
            <th>Plazo</th>
            <!-- Subcolumnas de Informe de Area -->
            <th>Fecha</th>
            <th>Solicitante</th>
            <th>Informe Area</th>
            <!-- Subcolumnas de Inter Area -->
            <th>Solicitud</th>
            <th>Inter Area</th>
            <th>Informe</th>
            <!-- Subcolumnas de Informe Area -->
            <th>Estado</th>
            <!-- Subcolumnas de Administracion -->
            <th>Formato</th>
            <!-- Subcolumnas de Servicios Tecnologicos -->
            <th>Revision</th>
            <!-- Subcolumnas de Responsable Area -->
            <th>Firma</th>
            <!-- Subcolumnas de Direccion -->
            <th>Firma</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(fila, index) in subcolumnasSolicitud" :key="index">
            <td>{{ fila.nro_dataServicio }}</td>
            <td class="fecha-columna">{{ fila.fecha }}</td>
            <td>{{ fila.area_tematica }}</td>
            <td>{{ fila.nro_presupuesto }}</td>
            <td>{{ fila.doc_dataServicio }}</td>
            <td>
              <!-- Verificar si adjunto_solicitud está vacío -->
              <template v-if="fila.adjunto_solicitudServicio === null">
                <!-- Si no hay adjunto, mostrar el botón de cargar archivo -->
                <div class="custom-file">
                  <!-- El icono de Bootstrap ahora es clicleable y activa el input de tipo file -->
                  <label class="custom-file-label" for="fileInput" @click="triggerFileInput">
                    <i class="bi bi-paperclip"></i>
                  </label>
                  <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                  <input id="fileInput" type="file" class="custom-file-input" style="display: none; cursor: pointer;"  @change="cargarArchivo($event, fila.nro_dataServicio)">
                </div>
              </template>
              <template v-else>
                <!-- Si hay un adjunto, mostrar el icono del archivo -->
                <i class="bi bi-file-earmark-text" @click="abrirArchivo(fila.adjunto_solicitudServicio)"></i>
                {{ console.log('Debería mostrar icono para archivo') }}
                {{ console.log('Debería mostrar la ruta', fila.adjunto_solicitudServicio) }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
      <div>
        <SolicitudServicioColumna :subcolumnasSolicitud="subcolumnasSolicitud" @update-subcolumnas="actualizarSubcolumnasSolicitud"/>
        <LegajoColumna :subcolumnas="subcolumnasLegajo" />
        <!-- <RecepcionColumna :subcolumnas="subcolumnasRecepcion" />
        <InformeAreaColumna :subcolumnas="subcolumnasInformeArea" /> -->

      </div>
    </div>
</template>
  
<script>
  import { ref } from 'vue';
  import axios from 'axios';

  import SolicitudServicioColumna from './sectores/SolicitudServicioColumna.vue';
  // import LegajoColumna from './sectores/LegajoColumna.vue';
  // import RecepcionColumna from './sectores/RecepcionColumna.vue';
  // import InformeAreaColumna from './sectores/InformeAreaColumna.vue';

  export default {
    components: {
      SolicitudServicioColumna,
      // LegajoColumna,
      // RecepcionColumna,
      // InformeAreaColumna
    },
    setup() {

      const subcolumnasSolicitud = ref([
        'nro_dataServicio', 'fecha', 'area_tematica', 'nro_presupuesto', 'doc_dataServicio', 'adjunto_solicitudServicio'
      ]);

      const subcolumnasLegajo = ref([
        'nro_legajo', 'fecha', 'doc_legajo', 'adjunto_factura', 'pago_legajo', 'plazo_pago'
      ]);


      // const subcolumnasRecepcion = ref([
      //   'nros_remitos', 'muestras', 'plazo'
      // ]);

      // const subcolumnasOrdenServicio = ref([
      //   'doc_ordenServicio', 'plazo'
      // ]);

      // const subcolumnasInformeArea = ref([
      //   'fecha', 'area_tematica', 'adjunto_informe'
      // ]);

      //methods
      const actualizarSubcolumnasSolicitud = (nuevosDatos) => {
        //console.log('----------', nuevosDatos)
      subcolumnasSolicitud.value = nuevosDatos;
      };

      const triggerFileInput = () => {
      document.getElementById('fileInput').click();
      };

      const cargarArchivo = (event, nroDataServicio) => {
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          // console.log('NRO DATA SERVICIO PARA CARGAR ARCHIVO', nroDataServicio)
          // console.log('EVENTO PARA CARGAR ARCHIVO', event)
          // Crear un objeto FormData para enviar el archivo al servidor
          const formData = new FormData();
          // console.log('FORM DATA PARA CARGAR ARCHIVO', formData)
          formData.append('archivo', archivoSeleccionado);
          formData.append('nroDataServicio', nroDataServicio); // Agregar el número de servicio

          // Realizar una petición POST al servidor para guardar el archivo
          axios.post('api/encurso/guardar_adjuntosolicitudservicio/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
                  // Aquí puedes actualizar el estado de tu aplicación si es necesario
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };

      const abrirArchivo = (adjunto_solicitudServicio) => {
        const urlCompleta = 'http://localhost:8000' + adjunto_solicitudServicio;
        window.open(urlCompleta, '_blank');
      };


      return {
        subcolumnasSolicitud,
        subcolumnasLegajo,
        actualizarSubcolumnasSolicitud,
        triggerFileInput,
        cargarArchivo,
        abrirArchivo

        // subcolumnasRecepcion,
        // subcolumnasOrdenServicio,
        // subcolumnasInformeArea
      };
    },
  };
</script>
  
<style scoped>
  .fecha-columna {
        white-space: nowrap; /* Evita que el contenido de la columna se divida en múltiples líneas */
        overflow: hidden; /* Oculta el contenido excedente */
        text-overflow: ellipsis; /* Agrega puntos suspensivos (...) al final del texto que no se muestra */
    }
</style>
  