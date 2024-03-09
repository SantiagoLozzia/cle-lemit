<template>
     <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! Se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar. Por favor, inténtalo de nuevo.
    </div>

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
            <th colspan="1">Archivo</th>
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
            <!-- Subcolumnas de Archivo -->
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(fila, index) in filas" :key="index">
            <td>{{ fila.nro_dataServicio }}</td>
            <td class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <td>{{ fila.area_tematica }}</td>
            <td>{{ fila.nro_presupuesto }}</td>
            <td><i class="bi bi-file-check"  style="cursor: pointer;" @click="abrirDataServicio(fila.nro_dataServicio)"></i></td>
            <td>
              <!-- Verificar si adjunto_solicitud está vacío -->
              <template v-if="fila.adjunto_solicitudServicio === null">
                <!-- Si no hay adjunto, mostrar el botón de cargar archivo -->
                <div class="custom-file">
                  <!-- El icono de Bootstrap ahora es clicleable y activa el input de tipo file -->
                  <label class="custom-file-label"  style="cursor: pointer;" for="fileInput">
                    <i class="bi bi-paperclip"></i>
                  </label>
                  <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                  <input id="fileInput" type="file" class="custom-file-input" style="display: none; cursor: pointer;"  @change="cargarArchivo($event, fila.nro_dataServicio)">
                </div>
              </template>
              <template v-else>
                <!-- Si hay un adjunto, mostrar el icono del archivo -->
                <i class="bi bi-file-earmark-text" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_solicitudServicio)"></i>
                <!-- {{ console.log('Debería mostrar icono para archivo') }}
                {{ console.log('Debería mostrar la ruta', fila.adjunto_solicitudServicio) }} -->
              </template>
            </td>
            <td>{{ fila.nro_legajo }}</td>
            <td class="fecha-columna">{{ fila.fecha_legajo }}</td>
            <td>
              <template v-if="fila.dataServicio_completo && !fila.nro_legajo">
                  <i class="bi bi-plus-square text-success"  style="cursor: pointer;" @click="crearLegajo(fila.nro_circuito)"></i>
              </template>
              <template v-else-if="fila.dataServicio_completo && fila.nro_legajo">
                  <i class="bi bi-file-check"  style="cursor: pointer;" @click="abrirLegajo(fila.nro_circuito)"></i>
              </template>
              <template v-else>
                  <!-- Deja el td vacío si dataServicio_completo es false -->
              </template>
            </td>
            <td>
                <template v-if="fila.nro_legajo && !fila.adjunto_factura">
                    <!-- Si nro_legajo está completo y adjunto_factura está vacío, mostrar el botón de cargar archivo -->
                    <div class="custom-file">
                        <!-- El icono de Bootstrap es clicleable y activa el input de tipo file -->
                        <label class="custom-file-label" style="cursor: pointer;" for="fileInput">
                            <i class="bi bi-paperclip"></i>
                        </label>
                        <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                        <input id="fileInput" type="file" class="custom-file-input" style="display: none;"  @change="cargarAdjuntoSolicitudServicio($event, fila.nro_dataServicio)">
                    </div>
                </template>
                <template v-else-if="fila.nro_legajo && fila.adjunto_factura">
                    <!-- Si nro_legajo está completo y adjunto_factura está completo, mostrar el icono del archivo -->
                    <i class="bi bi-file-earmark-text"  style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_factura)"></i>
                </template>
                <template v-else>
                    <!-- Si nro_legajo está vacío, entonces adjunto_factura también debe estar vacío -->
                </template>
            </td>
            <td>
                <div v-if="fila.pago !== undefined && fila.pago !== null">
                    <!-- Mostrar el valor de fila.pago -->
                    <span v-if="fila.pago === 0">0%</span>
                    <span v-else-if="fila.pago === 50">50%</span>
                    <span v-else-if="fila.pago === 100">100%</span>
                    <br><br>
                    <!-- Mostrar botón de edición -->
                    <i class="bi bi-pencil-square" style="cursor: pointer;" @click="mostrarModalPagoLegajo(fila.pago)"></i>
                </div>
            </td>
            <td>{{ fila.plazo_pago }}
                <br><br>
                <i class="bi bi-pencil-square" style="cursor: pointer;" @click="mostrarModalPlazoLegajo(fila.plazo_pago)"></i>
            </td>
            <td>{{ fila.nros_remitos }}</td>
            <td>
              <div v-if="fila.estado_recepcion !== undefined && fila.estado_recepcion !== null">
                <!-- Mostrar el valor de fila.estado_recepcion -->
                <span v-if="fila.estado_recepcion === 'sin_llegar'">Sin Llegar</span>
                <span v-else-if="fila.estado_recepcion === 'parcial'">Parcial</span>
                <span v-else-if="fila.estado_recepcion === 'total'">Total</span>
              </div>

              <div class="acciones">
                <button @click="abrirEstadoMuestras" class="btn btn-link"><i class="bi bi-pencil-square"></i></button>
                <select v-if="mostrarSelect" v-model="estadoMuestrasNuevo">
                  <option value="parcial">Parcial</option>
                  <option value="total">Total</option>
                </select>
                <button @click="guardarEstado(fila)" class="btn btn-primary">Guardar</button>
                <button @click="cerrarEstadoMuestras(fila)" class="btn btn-danger">X</button>
              </div>

            </td>

            <td>{{ fila.plazo_muestras }}</td>
            <td>{{ fila.fecha_ordenServicio}}</td>
            <td>
              <template v-if="(fila.pago == 50 ||fila.pago == 100) && (fila.estado_recepcion == 'parcial' || fila.estado_recepcion == 'total')">
                <i class="bi bi-file-check"  style="cursor: pointer;" @click="abrirOrdenServicio(fila.nro_circuito)"></i>
              </template>
              <template v-else>
                
              </template>
            </td>
            <td>{{ fila.estado_recepcion }}</td>
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
            <td>
              <button @click="enviarArchivar" class="btn btn-link"><i class="bi bi-arrow-right-square"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalDataServicio }" id="modalAbrirDataServicio">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Servicio N° {{ nroDataServicio }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalDataServicio" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fechaDataServicio" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaDataServicio" type="date" readonly class="form-control" id="fechaDataServicio" name="fechaDataServicio" required />
              </div>

              <div class="mb-3">
                <label for="obraDataServicio" class="form-label text-left">Obra:</label>
                <input v-model="obraDataServicio" type="text" class="form-control" id="obraDataServicio" name="obraDataServicio" readonly required />
              </div>
              
              <div class="mb-3">
                <label for="cantNumLabsDataServicio" class="form-label text-left">Cantidad Num Laboratorios:</label>
                <input v-model="cantNumLabsDataServicio" type="text" class="form-control" id="cantNumLabsDataServicio" name="cantNumLabsDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="plazoEstimadoDataServicio" class="form-label text-left">Plazo Estimado:</label>
                <input v-model="plazoEstimadoDataServicio" type="text" class="form-control" id="plazoEstimadoDataServicio" name="plazoEstimadoDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="muestrasDataServicio" class="form-label text-left">Muestras:</label>
                <input v-model="muestrasDataServicio" type="text" class="form-control" id="muestrasDataServicio" name="muestrasDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="nroPresupuestoDataServicio" class="form-label text-left">N° Presupuesto:</label>
                <input v-model="nroPresupuestoDataServicio" type="text" class="form-control" id="nroPresupuestoDataServicio" name="nroPresupuestoDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="areaDataServicio" class="form-label text-left">Area Tematica:</label>
                <input v-model="areaDataServicio" type="text" class="form-control" id="areaDataServicio" name="areaDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="solicitanteDataServicio" class="form-label text-left">Solicitante:</label>
                <input v-model="solicitanteDataServicio" type="text" class="form-control" id="solicitanteDataServicio" name="solicitanteDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="arancelDataServicio" class="form-label text-left">Arancel:</label>
                <input v-model="arancelDataServicio" type="text" class="form-control" id="arancelDataServicio" name="arancelDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="observacionesDataServicio" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesDataServicio" type="text" class="form-control" id="observacionesDataServicio" name="observacionesDataServicio" readonly required />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModal }" id="modalCrearLegajo">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Nuevo Legajo</h1>
            <button type="button" class="btn-close" @click="cerrarModalLegajo" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fecha_nuevoLegajo" class="form-label text-left">Fecha:</label>
                  <input v-model="nuevoLegajo.fecha_legajo" type="date" readonly class="form-control" id="fecha_nuevoLegajo" name="fecha_nuevoLegajo" required />
              </div>

              <div class="mb-3">
                <label for="rango_nums" class="form-label text-left">Rango Numeros de Laboratorios:</label>
                <input v-model="nuevoLegajo.rangos_laboratorios" type="text" class="form-control" id="rango_nums" name="rango_nums" readonly required />
              </div>
              <button @click="guardarLegajo" type="button" class="btn btn-primary w-100">Guardar</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalLegajo }" id="modalAbrirLegajo">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Legajo N°{{ nroLegajo }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalLegajo" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fechaLegajo" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaLegajo" type="date" readonly class="form-control" id="fechaLegajo" name="fechaLegajo" required />
              </div>

              <div class="mb-3">
                <label for="rangosLaboratorios" class="form-label text-left">Rango Numeros de Laboratorios:</label>
                <input v-model="rangosLaboratorios" type="text" class="form-control" id="rangosLaboratorios" name="rangosLaboratorios" readonly required />
              </div>

              <div class="mb-3">
                <label for="nombreSolicitante" class="form-label text-left">Solicitante:</label>
                <input v-model="nombreSolicitante" type="text" class="form-control" id="nombreSolicitante" name="nombreSolicitante" readonly required />
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
    
    <div class="modal" :class="{ 'show': mostrarModalOrdenServicio }" id="mostrarModalOrdenServicio">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Orden de Servicio N°{{ nroOS }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalOrdenServicio" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fechaOS" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaOS" type="date" readonly class="form-control" id="fechaOS" name="fechaOS" required />
              </div>

              <div class="mb-3">
                <label for="areaOS" class="form-label text-left">Area Tematica</label>
                <input v-model="areaOS" type="text" class="form-control" id="areaOS" name="areaOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="legajoOS" class="form-label text-left">N° Legajo:</label>
                <input v-model="legajoOS" type="text" class="form-control" id="legajoOS" name="legajoOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="rangosOS" class="form-label text-left">Rangos Laboratorios:</label>
                <input v-model="rangosOS" type="text" class="form-control" id="rangosOS" name="rangosOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="plazoOS" class="form-label text-left">Plazo Estimado:</label>
                <input v-model="plazoOS" type="text" class="form-control" id="plazoOS" name="plazoOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="solicitanteOS" class="form-label text-left">Solicitante:</label>
                <input v-model="solicitanteOS" type="text" class="form-control" id="solicitanteOS" name="solicitanteOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="muestrasOS" class="form-label text-left">Muestras:</label>
                <input v-model="muestrasOS" type="text" class="form-control" id="muestrasOS" name="muestrasOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="observacionesOS" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesOS" type="text" class="form-control" id="observacionesOS" name="observacionesOS" readonly required />
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>


   
    
</template>
  
<script>
  import { onMounted, ref, watch} from 'vue';
  import axios from 'axios';

  export default {
    components: {
    },
    setup() {
      
      const filas = ref([]);
      
      const nuevoLegajo = ref({
        fecha_legajo: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
        rangos_laboratorios: '',
        pago: 0,
        plazo_pago: 30,
        nuevo_ultimo_numero: '',
        nro_circuito: null,
      });
      console.log('PRIMER NUEVO LEGAJO', nuevoLegajo)

      const nuevoRecepcion = ref ({
        nros_remitos: '',
        estado_recepcion: '',
        plazo_muestras: 30,
      })

      const nroLegajo = ref();
      const fechaLegajo = ref();
      const rangosLaboratorios = ref();
      const nombreSolicitante = ref();

      const nroDataServicio = ref(); 
      const fechaDataServicio = ref();
      const obraDataServicio = ref();
      const cantNumLabsDataServicio = ref();
      const plazoEstimadoDataServicio = ref();
      const muestrasDataServicio = ref();
      const nroPresupuestoDataServicio = ref();
      const areaDataServicio = ref();
      const solicitanteDataServicio = ref();
      const arancelDataServicio = ref();
      const observacionesDataServicio = ref();
       
      const mostrarModal = ref(false);
      const mostrarModalDataServicio = ref(false);
      const mostrarModalLegajo = ref(false);
      const showSuccessAlert = ref(false);
      const showErrorAlert = ref(false);

      const mostrarSelect = ref(false);
      // const estadoMuestrasNuevo = ref('');
      const mostrarModalOrdenServicio = ref(false);

      const nroOS = ref();
      const fechaOS = ref();
      const areaOS = ref();
      const legajoOS = ref();
      const rangosOS = ref();
      const plazoOS = ref();
      const solicitanteOS = ref();
      const muestrasOS = ref();
      const observacionesOS = ref();

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
              const recepcionCorrespondiente = data.recepciones.find(recepciones => recepciones.nro_circuito === solicitud.nro_circuito);
              const ordenCorrespondiente = data.ordenes_servicio.find(ordenes_servicio => ordenes_servicio === solicitud.nro_circuito);
              // Construir la fila de la tabla combinando datos de solicitudes, legajos, recepciones, etc.
              const fila = {
                nro_dataServicio: solicitud.nro_dataServicio,
                fecha_dataServicio: solicitud.fecha_dataServicio,
                area_tematica: solicitud.area_tematica,
                nro_presupuesto: solicitud.nro_presupuesto,
                adjunto_solicitudServicio: solicitud.adjunto_solicitudServicio,
                nro_circuito: solicitud.nro_circuito,
                dataServicio_completo: solicitud.completo,
                nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo : '',
                fecha_legajo: legajoCorrespondiente ? legajoCorrespondiente.fecha_legajo : '',
                adjunto_factura: legajoCorrespondiente ? legajoCorrespondiente.adjunto_factura : '',
                pago: legajoCorrespondiente ? legajoCorrespondiente.pago : '',
                plazo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago : '',
                nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.nros_remitos: '',
                estado_recepcion: recepcionCorrespondiente ? recepcionCorrespondiente.estado_recepcion: '',
                plazo_muestras: recepcionCorrespondiente ? recepcionCorrespondiente.plazo_muestras: '',
                fecha_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.fecha_ordenServicio: '',
                plazo_estimado: solicitud.plazo_estimado,
              };
                console.log('fechaaaaaaaa:', fila.fecha_ordenServicio)


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
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };



      const abrirArchivo = (adjunto) => {
        const urlCompleta = 'http://localhost:8000' + adjunto;
        window.open(urlCompleta, '_blank');
      };

      const crearLegajo = (nro_circuito) => {
        // Realizar la llamada a la API para obtener el rango de laboratorios
        axios.get(`/api/encurso/obtener_rangoLab/${nro_circuito}/`)
            .then(response => {
                // Si la llamada es exitosa, obtén el rango de laboratorios del cuerpo de la respuesta
                const rangoLab = response.data.rangoLab;
                const nuevo_ultimo_numero = response.data.ultimo_numero;
                console.log('Rango:', rangoLab);
                console.log('Ultimo Numero =',nuevo_ultimo_numero); 
                // Crea el nuevo legajo con el rango de laboratorios obtenido
                nuevoLegajo.value = {
                    fecha_legajo: new Date().toISOString().substring(0, 10), 
                    rangos_laboratorios: rangoLab, // Asignar el rango de laboratorios obtenido
                    pago: 0,
                    plazo_pago: 30,
                    nuevo_ultimo_numero: nuevo_ultimo_numero,
                    nro_circuito: nro_circuito,
                };

                // Muestra el modal una vez que se ha creado el legajo
                mostrarModal.value = true;
            })
            .catch(error => {
                console.error('Error al obtener el rango de laboratorios:', error);
                // Manejar el error de la llamada a la API
            });
      };

      const guardarLegajo = () => {
        axios.post('api/encurso/guardar_legajo/', nuevoLegajo.value)
        .then(response => {
          console.log(response)
          cerrarModal();

          nuevoLegajo.value = {
            fecha_legajo: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
            rangos_laboratorios: '',
            pago: 0,
            plazo_pago: 30,
            nuevo_ultimo_numero: '',
            nro_circuito: null,
          };

          showSuccessAlert.value = true;

          setTimeout(() => {
            showSuccessAlert.value = false;
          }, 3000);
        })
        .catch(error => {
          console.error('Error al guardar el arancel:', error);
          cerrarModal();
          showErrorAlert.value = true;

          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        });
      };

      const cerrarModal = () => {
        mostrarModal.value = false;
      };

      const formatAreaTematica = (area) => {
          return area.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
      };

      const formatArancel = (arancel) => {
          // Verificar si arancel es numérico
          if (!isNaN(arancel)) {
              // Si es numérico, formatearlo con el signo $ y separación de miles
              return '$ ' + arancel.toLocaleString(); // Utilizamos toLocaleString() para la separación de miles
          } else {
              // Si no es numérico, devolver el valor sin formato
              return arancel;
          }
      };

      const abrirDataServicio = (nro_dataServicio) => {
          axios.get(`api/encurso/obtener_dataservicio/${nro_dataServicio}/`)
              .then(response => {
                  // Obtener los datos del data servicio de la respuesta
                  const { nro_dataServicio, fecha_dataServicio, obra, cant_numLabs, plazo_estimado, muestras, nro_presupuesto, area_tematica, nombre_solicitante, arancel_presupuesto, observaciones } = response.data;

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroDataServicio.value = nro_dataServicio;
                  fechaDataServicio.value = fecha_dataServicio;
                  obraDataServicio.value = obra;
                  cantNumLabsDataServicio.value = cant_numLabs;
                  plazoEstimadoDataServicio.value = plazo_estimado;
                  muestrasDataServicio.value = muestras;
                  nroPresupuestoDataServicio.value = nro_presupuesto;
                  areaDataServicio.value = formatAreaTematica(area_tematica);
                  solicitanteDataServicio.value = nombre_solicitante ;
                  arancelDataServicio.value = formatArancel(arancel_presupuesto);
                  observacionesDataServicio.value = observaciones ;

                  // Mostrar el modal para mostrar los detalles del legajo
                  mostrarModalDataServicio.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos del legajo:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };
      
      const cerrarModalDataServicio = () => {
        console.log('CERRAR MODAL')
        mostrarModalDataServicio.value = false;
      };

      const abrirLegajo = (nro_circuito) => {
          axios.get(`api/encurso/obtener_legajo/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos del legajo de la respuesta
                  const { nro_legajo, fecha_legajo, rangos_laboratorios, nombre_solicitante } = response.data;

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroLegajo.value = nro_legajo;
                  fechaLegajo.value = fecha_legajo;
                  rangosLaboratorios.value = rangos_laboratorios;
                  nombreSolicitante.value = nombre_solicitante;

                  // Mostrar el modal para mostrar los detalles del legajo
                  mostrarModalLegajo.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos del legajo:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };


      const cerrarModalLegajo = () => {
        console.log('CERRAR MODAL') 
        mostrarModalLegajo.value = false;
      };

      const abrirEstadoMuestras = () => {
        mostrarSelect.value = true;
      };


      const cerrarEstadoMuestras = () => {
        mostrarSelect.value = false;
      };
      

      const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];  
      console.log('VARIABLE CRSTOKEN=', csrfToken)

      // Función watch para monitorear cambios en fila.pago y fila.estado_recepcion
      watch(filas, (nuevasFilas) => {
        nuevasFilas.forEach((fila) => {
          if ((fila.pago === 50 || fila.pago === 100) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total') && (fila.fecha_ordenServicio === 'null')) {
            
            // Enviar la solicitud por Axios
            axios.post(`http://localhost:8000/api/encurso/crear_ordenservicio/${fila.nro_circuito}/`,
            {},
            {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
              console.log('Respuesta Orden Servicio:', response)
              showSuccessAlert.value = true;

              setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);
            })
            .catch(error => {
              console.log(error)
              showErrorAlert.value = true;

              setTimeout(() => {
                  showErrorAlert.value = false;
                }, 5000);
            });
          }
        });
      }, { deep: true }); // Usamos { deep: true } para observar cambios profundos en las propiedades del objeto

      const abrirOrdenServicio = (nro_circuito) => {
          axios.get(`api/encurso/obtener_orden_servicio/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos del legajo de la respuesta
                  const { nro_ordenServicio, fecha_ordenServicio, area_tematica, nro_legajo, rangos_laboratorios, plazo_estimado, nombre_solicitante, muestras, observaciones } = response.data;

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroOS.value = nro_ordenServicio;
                  fechaOS.value = fecha_ordenServicio;
                  areaOS.value = area_tematica;
                  legajoOS.value = nro_legajo;
                  rangosOS.value= rangos_laboratorios;
                  plazoOS.value= plazo_estimado;
                  solicitanteOS.value= nombre_solicitante;
                  muestrasOS.value= muestras;
                  observacionesOS.value= observaciones;


                  // Mostrar el modal para mostrar los detalles del legajo
                  mostrarModalOrdenServicio.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos de la orden de servicio:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };

      const cerrarModalOrdenServicio = () => {
        console.log('CERRAR MODAL') 
        mostrarModalOrdenServicio.value = false;
      };

      // const cambiarEstado = async (nro_circuito, estadoMuestrasNuevo) => {
      //   try {
      //     // Realizar la petición para actualizar el estado de la recepción de muestras en la base de datos
      //     const response = await axios.put(`http://localhost:8000/api/estado_recepcion/actualizar_estado/${nro_circuito,estadoMuestrasNuevo}/`, {
      //       estado_recepcion: estadoMuestrasNuevo
      //     });

      //     // Verificar si la actualización fue exitosa
      //     if (response.status === 200) {
      //       console.log('Estado de recepción de muestras actualizado correctamente:', recepcionMuestras.nuevoEstado);
      //       // Recargar la página para reflejar los cambios actualizados
      //       location.reload();
      //     } else {
      //       console.error('Error al actualizar el estado de la recepción de muestras:', response.statusText);
      //     }
      //   } catch (error) {
      //     console.error('Error al cambiar el estado de la recepción de muestras:', error);
      //   }
      // };


      return {
        filas,
        nuevoLegajo,
        nuevoRecepcion,
        triggerFileInput,
        abrirDataServicio,
        nroDataServicio,
        fechaDataServicio,
        obraDataServicio,
        cantNumLabsDataServicio,
        plazoEstimadoDataServicio,
        muestrasDataServicio,
        nroPresupuestoDataServicio,
        areaDataServicio,
        solicitanteDataServicio,
        arancelDataServicio,
        observacionesDataServicio,
        cargarArchivo,
        abrirArchivo,
        crearLegajo,
        abrirLegajo,
        nroLegajo,
        fechaLegajo,
        rangosLaboratorios,
        nombreSolicitante,
        mostrarModal,
        mostrarModalDataServicio,
        mostrarModalLegajo,
        cerrarModal,
        cerrarModalDataServicio,
        cerrarModalLegajo,
        guardarLegajo,
        showSuccessAlert,
        showErrorAlert,
        formatAreaTematica,
        formatArancel,
        abrirEstadoMuestras,
        cerrarEstadoMuestras,
        abrirOrdenServicio,
        mostrarModalOrdenServicio,
        cerrarModalOrdenServicio,
        nroOS,
        fechaOS,
        areaOS,
        legajoOS,
        rangosOS,
        plazoOS,
        solicitanteOS,
        muestrasOS,
        observacionesOS,
        // cambiarEstado,
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

  .radio-options input[type="radio"] {
    display: inline-block;
    margin-right: 5px;
  }

  .radio-options label {
    font-size: 10px;
  }

  .modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .modal.show {
    display: flex;
    align-items: center;
    justify-content: center;
  }

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

  .btn-group {
    display: inline-block; /* Para mostrar los botones en línea */
  }
</style>
  