<template>
    <div>
      <table class="table">
        <thead>
          <tr>
            <th colspan="6">Solicitud de Servicio</th>
            <th colspan="6">Legajo</th>
            <th colspan="3">Recepcion</th>
            <th colspan="3">Orden de Servicio</th>
            <th colspan="3">Informe de Area</th>
            <th colspan="4">Inter Area</th>
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
            <th>Fecha</th>
            <th>OS</th>
            <th>Plazo</th>
            <!-- Subcolumnas de Informe de Area -->
            <th>Fecha</th>
            <th>Solicitante</th>
            <th>Informe Area</th>
            <!-- Subcolumnas de Inter Area -->
            <th>Fecha</th>
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
          <tr v-for="(fila, index) in filas" :key="index">
            <td>{{ fila.nro_dataServicio }}</td>
            <td class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <td>{{ fila.area_tematica }}</td>
            <td>{{ fila.nro_presupuesto }}</td>
            <td><i class="bi bi-file-check"></i></td>
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
                <!-- {{ console.log('Debería mostrar icono para archivo') }}
                {{ console.log('Debería mostrar la ruta', fila.adjunto_solicitudServicio) }} -->
              </template>
            </td>
            <td>{{ fila.nro_legajo }}</td>
            <td class="fecha-columna">{{ fila.fecha_legajo }}</td>
            <td><i class="bi bi-file-check"></i></td>
            <td>
              <template v-if="fila.adjunto_factura === null">
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
                <i class="bi bi-file-earmark-text" @click="abrirArchivo(fila.adjunto_factura)"></i>
              </template>
            </td>
            <td>{{ fila.pago }}</td>
            <td>{{ fila.plazo_pago }}</td>
            <td>{{ fila.nros_remitos }}</td>
            <td>{{ fila.estado_recepcion }}</td>
            <td>{{ fila.plazo_muestras }}</td>
            <td>{{ fila.fecha_ordenServicio }}</td>
            <td><i class="bi bi-file-check"></i></td>
            <td>{{ fila.plazo_estimado }}</td>
            <td>{{ fila.fecha_informeArea }}</td>
            <td>{{ fila.nombre_solicitante }}</td>
            <td><i class="bi bi-paperclip"></i></td>
            <td>{{ fila.fecha_solicitudInterarea }}</td>
            <td><i class="bi bi-file-check"></i></td>
            <td>{{ fila.inter_areaTematica }}</td>
            <td><i class="bi bi-paperclip"></i></td>
            <td>{{ fila.estado_informeArea }}</td>
            <td><i class="bi bi-paperclip"></i></td>
            <td>{{ fila.revision }}</td>
            <td>{{ fila.firma_area }}</td>
            <td>{{ fila.firma_direccion }}</td>
            <td><i class="bi bi-file-check"></i></td>
          </tr>
        </tbody>
      </table>
    </div>
</template>
  
<script>
  import { onMounted, ref} from 'vue';
  import axios from 'axios';

  export default {
    components: {
    },
    setup() {
      
      const filas = ref([]);

      

      //methods

      const fetchData = () => {
        axios.get('api/encurso/obtener_todoencurso/')
          .then(response => {
            const data = response.data;
            console.log('DATA:', data)
            console.log('NRO DATA SERVICIO', data.solicitudes[0].nro_dataServicio)
            
            // Iterar sobre las solicitudes
            data.solicitudes.forEach(solicitud => {
              // Buscar el objeto legajo correspondiente
              const legajoCorrespondiente = data.legajos.find(legajo => legajo.nro_circuito === solicitud.nro_circuito);
              const recepcionCorrespondiente = data.legajos.find(recepcion => recepcion.nro_circuito === solicitud.nro_circuito);

              // Construir la fila de la tabla combinando datos de solicitudes, legajos, recepciones, etc.
              const fila = {
                nro_dataServicio: solicitud.nro_dataServicio,
                fecha_dataServicio: solicitud.fecha_dataServicio,
                area_tematica: solicitud.area_tematica,
                nro_presupuesto: solicitud.nro_presupuesto,
                adjunto_solicitudServicio: solicitud.adjunto_solicitudServicio,
                nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo : '',
                fecha_legajo: legajoCorrespondiente ? legajoCorrespondiente.fecha_legajo : '',
                adjunto_factura: legajoCorrespondiente ? legajoCorrespondiente.adjunto_factura : '',
                pago: legajoCorrespondiente ? legajoCorrespondiente.pago : '',
                palzo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago : '',
                nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.recepcionCorrespondiente: '',
                // etc
              };


              filas.value.push(fila);
            });
          })
          .catch(error => {
            console.error('Error al obtener datos:', error);
          });
      };

      // Llamamos a fetchData cuando el componente se monta
      onMounted(() => {
        fetchData();
      });

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

      const abrirArchivo = (adjunto) => {
        const urlCompleta = 'http://localhost:8000' + adjunto;
        window.open(urlCompleta, '_blank');
      };


      return {
        filas,
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
  