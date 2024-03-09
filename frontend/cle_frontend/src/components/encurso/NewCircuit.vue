<template>
    <div>
      <div>
        <div class="button-container">
          <button class="btn btn-primary float-start ms-2 mt-2" @click="mostrarFormulario">+ Data Servicio</button>
        </div>
    
        <div class="modal" :class="{ 'show': mostrarModal }" id="modalPresupuesto">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5 fw-bold">Nuevo Data Servicio</h1>
                <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form class="was-validated">
  
                  <div class="mb-3">
                    <label for="fecha_dataServicio" class="form-label text-left">Fecha:</label>
                    <input v-model="nuevoDataServicio.fecha_dataServicio" type="date" readonly class="form-control" id="fecha_dataServicio" name="fecha_dataServicio" required />
                  </div>
  
                  <div class="mb-3">
                      <label for="nro_presupuesto" class="form-label text-left">N° Presupuesto:</label>
                      <select v-model="selectedPresupuesto" @click="buscarSugerencias" @change="presupuestoSeleccionado(selectedPresupuesto)" class="form-select mt-1">
                          <option v-for="sugerencia in sugerencias" :key="sugerencia.nro_presupuesto" :value="sugerencia.nro_presupuesto">
                              {{ sugerencia.nro_presupuesto }} - {{ sugerencia.nombre_solicitante }}
                          </option>
                      </select>
                  </div>
                  
                  <div class="mb-3">
                    <label for="obra" class="form-label text-left">Obra:</label>
                    <input v-model="nuevoDataServicio.obra" type="text" class="form-control" id="obra" name="obra"/>
                  </div>

                  <div class="mb-3">
                      <label for="muestras" class="form-label text-left">Muestras:</label>
                      <textarea v-model="nuevoDataServicio.muestras" class="form-control" id="muestras" name="muestras" required style="resize: vertical;"></textarea>
                  </div>
                  
                  <div class="mb-3">
                    <label for="plazo_estimado" class="form-label text-left">Plazo Estimado:</label>
                    <input v-model="nuevoDataServicio.plazo_estimado" type="number" class="form-control" id="plazo_estimado" name="plazo_estimado" required />
                  </div>

                  <div class="mb-3">
                    <label for="cant_numLabs" class="form-label text-left">Cantidad N° Laboratorios:</label>
                    <input v-model="nuevoDataServicio.cant_numLabs" type="number" class="form-control" id="cant_numLabs" name="cant_numLabs" required />
                  </div>
  
                  <div class="mb-3">
                    <label for="observaciones" class="form-label text-left">Observaciones:</label>
                    <input v-model="nuevoDataServicio.observaciones" type="text" class="form-control" id="observaciones" name="observaciones" />
                  </div>
    
                  <button @click="guardarDataServicio" type="button" class="btn btn-primary w-100">Guardar</button>
                </form>
              </div>
            </div>
          </div>
        </div>
    
        <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
          ¡Éxito! El Data Servicio se ha creado correctamente.
        </div>
        <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
          ¡Error! Ha ocurrido un problema al guardar el Data Servicio. Por favor, inténtalo de nuevo.
        </div>
    
      </div>
      </div>
  </template>
  
  <script>
    import axios from 'axios';
    import { ref } from 'vue';
    // eslint-disable-next-line no-unused-vars
    // import vSelect from 'vue-select';
    // import 'vue-select/dist/vue-select.css';
  
    export default {
      components: {
      },
          
      setup() {
        const inputProps = ref({ placeholder: 'Buscar solicitante' });
        const sugerencias = ref([]);
        const selectedPresupuesto = ref(null);
        const nuevoDataServicio = ref({
            fecha_dataServicio: null,
            obra: null,
            muestras:null,
            plazo_estimado: null,
            cant_numLabs: null,
        });
        const mostrarModal = ref(false);
        const showSuccessAlert = ref(false);
        const showErrorAlert = ref(false);
  
        // Definir métodos
        const mostrarFormulario = () => {
          
          // Calcular la fecha actual
          const today = new Date();
          const year = today.getFullYear();
          let month = today.getMonth() + 1;
          let day = today.getDate();
    
          // Formatear la fecha como "YYYY-MM-DD"
          if (month < 10) {
            month = '0' + month;
          }
          if (day < 10) {
            day = '0' + day;
          }
          const formattedDate = `${year}-${month}-${day}`;
          // Asignar la fecha actual al campo de fecha del nuevo presupuesto
          nuevoDataServicio.value.fecha_dataServicio = formattedDate;
              
          nuevoDataServicio.value = {
            fecha_dataServicio: formattedDate,
            obra: null,
            muestras:null,
            plazo_estimado: null,
            cant_numLabs: null,
          };
  
          mostrarModal.value = true;
        };
  
        const cerrarModal = () => {
          mostrarModal.value = false;
        };
  
        const guardarDataServicio = () => {
          // Validar campos obligatorios
          if (!nuevoDataServicio.value.plazo_estimado || !nuevoDataServicio.value.cant_numLabs) {
            return;
          }
          console.log('nuevo presupuesto',nuevoDataServicio)
          axios.post('http://localhost:8000/api/encurso/guardar_dataServicio/', nuevoDataServicio.value)
            .then(response => {
              console.log(response.data);
              cerrarModal();
    
              // Limpiar el formulario y mostrar la alerta de éxito
              nuevoDataServicio.value = {
                fecha_dataServicio: null,
                obra: null,
                muestras:null, 
                plazo_estimado: null,
                cant_numLabs: null,
              };
    
              showSuccessAlert.value = true;
    
              setTimeout(() => {
                showSuccessAlert.value = false;
              }, 3000);
              })

              .catch(error => {
                console.error('Error al guardar el Data Servicio:', error);
                cerrarModal();
                // Imprimir detalles del error
                console.error('Error details:', error.response.data);
                showErrorAlert.value = true;
      
                setTimeout(() => {
                  showErrorAlert.value = false;
                }, 5000);
      
              });
          };
  
          const buscarSugerencias = () => {
              axios.get('http://localhost:8000/api/encurso/buscar_presupuestos/')
                .then(response => {
                  sugerencias.value = response.data;
                  console.log('sugerencias',sugerencias.value);
                })
                .catch(error => {
                  console.error('Error al buscar presupuestos:', error);
                });
          };
        
  
          const presupuestoSeleccionado = () => {
            console.log("selectedPresupuesto:", selectedPresupuesto.value);
            axios.get(`http://localhost:8000/api/encurso/presupuesto_seleccionado/${selectedPresupuesto.value}/`)
              .then(response => {
                console.log("Respuesta del servidor:", response.data);
                // Actualizar los campos del formulario con los detalles del solicitante
                nuevoDataServicio.value.nro_presupuesto = response.data.nro_presupuesto;
                console.log('Le asigno a nuevoDataServicio, el nro presup:', nuevoDataServicio.value.nro_presupuesto)
              })
              .catch(error => {
                console.error('Error al obtener los detalles del solicitante:', error);
              });
          };
          
          return {
            inputProps,
            sugerencias,
            nuevoDataServicio,
            mostrarModal,
            showSuccessAlert,
            showErrorAlert,
            buscarSugerencias,
            selectedPresupuesto,
            presupuestoSeleccionado,
            mostrarFormulario,
            cerrarModal,
            guardarDataServicio,
          };
      }
    };
  </script>
  
    
    
  <style scoped>
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
    
    #modalPresupuesto .modal-dialog {
      max-width: 1500px !important; 
    }
    
    .form-select {
      font-size: 16px;
      padding: 6px;
      border: 1px solid #ced4da;
      border-radius: 5px;
      width: 100%;
      appearance: none;
      padding-right: 2.25rem; /* Espaciado para el ícono */
    }
    
    /* Espaciado para el ícono de flecha en el desplegable */
    .form-select::after {
      content: '\25BC'; /* Código de la flecha hacia abajo */
      position: absolute;
      right: 10px; 
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none; 
    }
    
    .form-select:focus {
      border-color: #007bff; /* Color de resaltado cuando el desplegable está enfocado */
      box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25); /* Efecto de resaltado cuando está enfocado */
    }
    
    form div.label-container label {
      text-align: left !important;
    }
  </style>
    