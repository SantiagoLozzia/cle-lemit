<template>
    <div>
      <div>
        <div class="button-container">
          <button class="btn btn-primary float-start ms-2 mt-2" @click="mostrarFormulario">+ Nuevo</button>
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
                    <label for="fecha" class="form-label text-left">Fecha:</label>
                    <input v-model="nuevoDataServicio.fecha" type="date" readonly class="form-control" id="fecha" name="fecha" required />
                  </div>
  
                  <div class="mb-3">
                      <label for="solicitante" class="form-label text-left">N° Presupuesto:</label>
                      <input v-model="nuevoDataServicio.nro_presupuesto" type="text" class="form-control" id="nro-presupuesto" name="nro-presupuesto" required ref="nro-presupuesto" @input="buscarSugerencias">
                      <select v-if="sugerencias.length > 0" v-model="selectedPresupuesto" @change="seleccionarSugerencia(selectedPresupuesto)" class="form-select mt-1">
                          <option v-for="sugerencia in sugerencias" :key="sugerencia.nro_presupuesto" :value="sugerencia">
                              {{ sugerencia.nro_presupuesto }} - {{ sugerencia.nombre_solicitante }}
                          </option>
                      </select>
                  </div>
                  
                  <div class="mb-3">
                    <label for="solicitante" class="form-label text-left">Solicitante:</label>
                    <input v-model="nuevoDataServicio.contacto" type="text" class="form-control" id="contacto" name="contacto" required />
                  </div>

                  <div class="mb-3">
                    <label for="area_tematica" class="form-label text-left">Área Temática:</label>
                    <select v-model="nuevoDataServicio.area_tematica" class="form-select" id="area_tematica" name="area_tematica" required>
                      <option v-for="(option, key) in area_tematicaOptions" :key="key" :value="option.value">
                        {{ option.label }}
                      </option>
                    </select>
                  </div>

                  <div class="mb-3">
                    <label for="contacto" class="form-label text-left">Contacto:</label>
                    <input v-model="nuevoDataServicio.contacto" type="text" class="form-control" id="contacto" name="contacto" required />
                  </div>
                  
                  <div class="mb-3">
                    <label for="telefono" class="form-label text-left">Teléfono:</label>
                    <input v-model="nuevoDataServicio.telefono" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="telefono" name="telefono" required />
                  </div>
  
                  <div class="mb-3">
                    <label for="email" class="form-label text-left">Email:</label>
                    <input v-model="nuevoDataServicio.email" type="text" class="form-control" id="email" name="email" required />
                  </div>
  
                  <div class="mb-3">
                    <label for="obra" class="form-label text-left">Obra:</label>
                    <input v-model="nuevoDataServicio.subtotal" type="text" class="form-control" id="obra" name="obra" required />
                  </div>
  
                  <div class="mb-3">
                    <label for="cant_numLabs" class="form-label text-left">Cantidad N° Laboratorios:</label>
                    <input v-model="nuevoDataServicio.cant_numLabs" type="number" step="0.01" class="form-control" id="cant_numLabs" name="cant_numLabs" required />
                  </div>
  
                  <span class="left-align">Validez de 30 dias</span>
                  <div class="mb-3">
                    <label for="observaciones" class="form-label text-left">Observaciones:</label>
                    <input v-model="nuevoDataServicio.observaciones" type="text" class="form-control" id="observaciones" name="observaciones" required />
                  </div>
    
                  <button @click="guardarPresupuesto" type="button" class="btn btn-primary w-100">Guardar</button>
                </form>
              </div>
            </div>
          </div>
        </div>
    
        <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
          ¡Éxito! El presupuesto se ha creado correctamente.
        </div>
        <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
          ¡Error! Ha ocurrido un problema al guardar el presupuesto. Por favor, inténtalo de nuevo.
        </div>
    
      </div>
      </div>
  </template>
  
  <script>
    import axios from 'axios';
    import { ref } from 'vue';
    import { debounce } from 'lodash';
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
          fecha: null,
          nro_presupuesto: '',
          nombre_solicitante: '',
          contacto: '',
          telefono: null,
          email: '',
          area_tematica: '',
          obra: null,
          descuento: '0',
          cant_numLabs: null,
          });
          const area_tematicaOptions = ref([
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
          ]);
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
              nuevoDataServicio.value.fecha = formattedDate;
              
              nuevoDataServicio.value = {
                fecha: formattedDate,
                contacto: '',
                telefono: null,
                email: '',
                area_tematica: '',
                obra: null,
                descuento: '0',
                cant_numLabs: null,
              };
              
  
              mostrarModal.value = true;
          };
  
          const cerrarModal = () => {
            mostrarModal.value = false;
          };
  
          const guardarPresupuesto = () => {
            // Validar campos obligatorios
            if (!nuevoDataServicio.value.contacto || !nuevoDataServicio.value.email || !nuevoDataServicio.value.area_tematica || nuevoDataServicio.value.obra === null || nuevoDataServicio.value.descuento === null) {
              return;
            }
  
            nuevoDataServicio.value.estado_presupuesto = 'en_espera';
            console.log('nuevo presupuesto',nuevoDataServicio)
            //Enviar datos al backend usando Axios
            axios.post('http://localhost:8000/api/presupuestos/', nuevoDataServicio.value)
              .then(response => {
                console.log(response.data);
                cerrarModal();
  
                // Limpiar el formulario y mostrar la alerta de éxito
                nuevoDataServicio.value = {
                  fecha: null,
                  nombre_solicitante: '',
                  nro_presupuesto: '',
                  contacto: '',
                  telefono: null,
                  email: '',
                  area_tematica: '',
                  obra: null,
                  descuento: '0',
                  cant_numLabs: null,
                };
  
                showSuccessAlert.value = true;
  
                setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);
              })
              .catch(error => {
                console.error('Error al guardar el presupuesto:', error);
                cerrarModal();
                // Imprimir detalles del error
                console.error('Error details:', error.response.data);
                showErrorAlert.value = true;
  
                setTimeout(() => {
                  showErrorAlert.value = false;
                }, 5000);
  
              });
          };
  
          const buscarSugerencias = debounce(() => {
            const term = nuevoDataServicio.value.nro_presupuesto;
            if (term.trim() !== '') {
              axios.get('http://localhost:8000/api/presupuestos/buscar_solicitantes/', {
                params: {
                  q: term
                }
              })
              .then(response => {
                sugerencias.value = response.data;
                console.log(sugerencias);
              })
              .catch(error => {
                console.error('Error al buscar solicitantes:', error);
              });
            } else {
              // Si el término de búsqueda está vacío, limpiar las sugerencias
              sugerencias.value = [];
            }
          }, 1000); // Tiempo de espera en milisegundos antes de ejecutar la búsqueda
        
  
          const seleccionarSugerencia = () => {
            console.log("selectedPresupuesto:", selectedPresupuesto.value.nro_presupuesto);
            // Realizar una solicitud al backend para obtener los detalles del solicitante seleccionado
            axios.get(`http://localhost:8000/api/presupuestos/seleccionar_solicitante/${selectedPresupuesto.value.nro_presupuesto}/`)
              .then(response => {
                console.log("Respuesta del servidor:", response.data);
                // Actualizar los campos del formulario con los detalles del solicitante
                nuevoDataServicio.value.nro_presupuesto = response.data.nro_presupuesto;
                nuevoDataServicio.value.nombre_solicitante = response.data.nombre_solicitante;
                nuevoDataServicio.value.contacto = response.data.contacto;
                nuevoDataServicio.value.telefono = response.data.telefono;
                nuevoDataServicio.value.email = response.data.email;
  
              })
              .catch(error => {
                console.error('Error al obtener los detalles del solicitante:', error);
              });
          };
          
          return {
            inputProps,
            sugerencias,
            nuevoDataServicio,
            area_tematicaOptions,
            mostrarModal,
            showSuccessAlert,
            showErrorAlert,
            buscarSugerencias,
            selectedPresupuesto,
            seleccionarSugerencia,
            mostrarFormulario,
            cerrarModal,
            guardarPresupuesto,
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
    