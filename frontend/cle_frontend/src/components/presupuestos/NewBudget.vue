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
              <h1 class="modal-title fs-5 fw-bold">Nuevo Presupuesto</h1>
              <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form class="was-validated">

                <div class="mb-3">
                  <label for="fecha_presupuesto" class="form-label text-left">Fecha:</label>
                  <input v-model="nuevoPresupuesto.fecha_presupuesto" type="date" readonly class="form-control" id="fecha_presupuesto" name="fecha_presupuesto" required />
                </div>

                <div class="mb-3">
                  <label for="nro_solicitante" class="form-label text-left">Nro Solicitante:</label>
                  <input v-model="nuevoPresupuesto.nro_solicitante" readonly type="text" class="form-control" id="nro_solicitante" name="nro_solicitante" required ref="nro_solicitante" />
                </div>

                <div class="mb-3">
                    <label for="solicitante" class="form-label text-left">Solicitante:</label>
                    <input v-model="nuevoPresupuesto.nombre_solicitante" type="text" class="form-control" id="solicitante" name="solicitante" required ref="solicitante" @input="buscarSugerencias">
                    <select v-if="sugerencias.length > 0" v-model="selectedSolicitante" @change="seleccionarSugerencia(selectedSolicitante)" class="form-select mt-1">
                        <option v-for="sugerencia in sugerencias" :key="sugerencia.nro_solicitante" :value="sugerencia">
                            {{ sugerencia.nro_solicitante }} - {{ sugerencia.nombre_solicitante }}
                        </option>
                    </select>
                </div>

                <!-- <div class="mb-3">
                    <label for="solicitante" class="form-label text-left">Solicitante:</label>
                    <v-select v-model="nuevoPresupuesto.solicitante" :options="sugerencias" label="nombre_solicitante" />
                </div> -->

                <div class="mb-3">
                  <label for="contacto" class="form-label text-left">Contacto:</label>
                  <input v-model="nuevoPresupuesto.contacto" type="text" class="form-control" id="contacto" name="contacto" required />
                </div>
                
                <div class="mb-3">
                  <label for="telefono" class="form-label text-left">Teléfono:</label>
                  <input v-model="nuevoPresupuesto.telefono" type="text" inputmode="numeric" pattern="[0-9]*" readonly class="form-control" id="telefono" name="telefono" required />
                </div>

                <div class="mb-3">
                  <label for="telefono2" class="form-label text-left">Teléfono 2:</label>
                  <input v-model="nuevoPresupuesto.telefono2" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="telefono" name="telefono"/>
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label text-left">Email:</label>
                  <input v-model="nuevoPresupuesto.email" type="text" readonly class="form-control" id="email" name="email" required />
                </div>

                <div class="mb-3">
                  <label for="email2" class="form-label text-left">Email 2:</label>
                  <input v-model="nuevoPresupuesto.email2" type="text" class="form-control" id="email2" name="email2"/>
                </div>
  
                <div class="mb-3">
                  <label for="area_tematica" class="form-label text-left">Área Temática:</label>
                  <select v-model="nuevoPresupuesto.area_tematica" class="form-select" id="area_tematica" name="area_tematica" required>
                    <option v-for="(option, key) in area_tematicaOptions" :key="key" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <DetallePresupuesto @actualizar-subtotal="actualizarSubTotal" @detalle-Presupuesto="agregarDetallePresupuesto"></DetallePresupuesto>

                <div class="mb-3">
                  <label for="subtotal" class="form-label text-left">SubTotal:</label>
                  <input v-model="nuevoPresupuesto.subtotal" type="text" inputmode="numeric" pattern="[0-9]*" readonly class="form-control" id="subtotal" name="subtotal" required />
                </div>

                <div class="mb-3">
                  <label for="descuento" class="form-label text-left">Descuento:</label>
                  <select v-model="nuevoPresupuesto.descuento" class="form-select" id="descuento" name="descuento" required>
                    <option v-for="(option, key) in descuentoOptions" :key="key" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="arancel_presupuesto" class="form-label text-left">Total:</label>
                  <input v-model="nuevoPresupuesto.arancel_presupuesto" type="number" step="0.01" class="form-control" id="arancel_presupuesto" name="arancel_presupuesto" required />
                </div>

                <span class="left-align">Validez de 30 dias</span>
                <div class="mb-3">
                  <label for="observaciones" class="form-label text-left">Observaciones:</label>
                  <input v-model="nuevoPresupuesto.observaciones" type="text" class="form-control" id="observaciones" name="observaciones" />
                </div>
  
                <button @click="guardarPresupuesto()" type="button" class="btn btn-primary w-100">Guardar</button>
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
  import { ref, watch } from 'vue';
  import { debounce } from 'lodash';
  import DetallePresupuesto from './DetallePresupuesto.vue';
  // eslint-disable-next-line no-unused-vars
  // import vSelect from 'vue-select';
  // import 'vue-select/dist/vue-select.css';

  export default {
    components: {
      DetallePresupuesto,
    },

    setup() {
      const inputProps = ref({ placeholder: 'Buscar solicitante' });
      const sugerencias = ref([]);
      const selectedSolicitante = ref(null);
      let solicitanteSeleccionado = ref(false);
      
      const nuevoPresupuesto = ref({
        fecha_presupuesto: null,
        nro_solicitante: '',
        nombre_solicitante: '',
        contacto: '',
        telefono2: null,
        email2: '',
        area_tematica: '',
        subtotal: null,
        descuento: '0',
        arancel_presupuesto: null,
        detalles_presupuesto: [
          {
            nro_servicio: '',
            cant: 0,
            subtotal: null
          }
        ]
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
      const descuentoOptions = ref([
          { value: '0', label: '0%' },
          { value: '5', label: '5%' },
          { value: '10', label: '10%' },
          { value: '15', label: '15%' },
          { value: '20', label: '20%' },
          { value: '25', label: '25%' },
          { value: '30', label: '30%' },
          { value: '40', label: '40%' },
          { value: '50', label: '50%' },
          { value: '60', label: '60%' },
          { value: '70', label: '70%' },
          { value: '80', label: '80%' },
          { value: '90', label: '90%' },
          { value: '100', label: '100%' },
      ]);
      const mostrarModal = ref(false);
      const showSuccessAlert = ref(false);
      const showErrorAlert = ref(false);

      // const detallesPresupuesto = ref([]);

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
        nuevoPresupuesto.value.fecha_presupuesto = formattedDate;
            
        nuevoPresupuesto.value = {
          fecha_presupuesto: formattedDate,
          nro_solicitante: '',
          nombre_solicitante: '',
          contacto: '',
          telefono2: null,
          email2: '',
          area_tematica: '',
          subtotal: null,
          descuento: '0',
          arancel_presupuesto: null,
          detalles_presupuesto: [
          {
            nro_servicio: '',
            cant: 0,
            subtotal: null
          }
        ]
        };
            

        mostrarModal.value = true;
          solicitanteSeleccionado.value = false;
        };

        const cerrarModal = () => {
          mostrarModal.value = false;
        };

        const guardarPresupuesto = () => {
          // Validar campos obligatorios
          if (!nuevoPresupuesto.value.contacto || !nuevoPresupuesto.value.email || !nuevoPresupuesto.value.area_tematica || nuevoPresupuesto.value.subtotal === null || nuevoPresupuesto.value.descuento === null) {
            return;
          }

          nuevoPresupuesto.value.estado_presupuesto = 'en_espera';
          console.log('nuevo presupuesto enviando al backend',nuevoPresupuesto)
          // return
          //Enviar datos al backend usando Axios
          axios.post('http://localhost:8000/api/presupuestos/', nuevoPresupuesto.value)
            .then(response => {
              console.log(response.data);
              cerrarModal();

              // Limpiar el formulario y mostrar la alerta de éxito
              nuevoPresupuesto.value = {
                fecha_presupuesto: null,
                nro_solicitante: '',
                nombre_solicitante: '',
                contacto: '',
                telefono2: null,
                email2: '',
                area_tematica: '',
                subtotal: null,
                descuento: '0',
                arancel_presupuesto: null,
                detalles_presupuesto: [
                  {
                    nro_servicio: '',
                    cant: 0,
                    subtotal: null
                  }
                ]
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

              solicitanteSeleccionado.value = false;
            });
        };

        const buscarSugerencias = debounce(() => {
          const term = nuevoPresupuesto.value.nombre_solicitante;
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
          console.log("selectedSolicitante:", selectedSolicitante.value.nro_solicitante);
          // Realizar una solicitud al backend para obtener los detalles del solicitante seleccionado
          axios.get(`http://localhost:8000/api/presupuestos/seleccionar_solicitante/${selectedSolicitante.value.nro_solicitante}/`)
            .then(response => {
              console.log("Respuesta del servidor:", response.data);
              // Actualizar los campos del formulario con los detalles del solicitante
              nuevoPresupuesto.value.nro_solicitante = response.data.nro_solicitante;
              nuevoPresupuesto.value.nombre_solicitante = response.data.nombre_solicitante;
              nuevoPresupuesto.value.telefono = response.data.telefono;
              nuevoPresupuesto.value.email = response.data.email;

              // Para que no se pueda modificar nro_solicitante una vez seleccionado un solicitante
              console.log(solicitanteSeleccionado.value);
              solicitanteSeleccionado.value = true;
              console.log(solicitanteSeleccionado.value);
            })
            .catch(error => {
              console.error('Error al obtener los detalles del solicitante:', error);
            });
        };
        
        // Evento recibido del componente hijo, DetallePresupuesto
        const actualizarSubTotal = (nuevoSubTotal) => {
          console.log('Evento recibido en el componente padre. Subtotal:', nuevoSubTotal);
          nuevoPresupuesto.value.subtotal = nuevoSubTotal;
        }

        watch([() => nuevoPresupuesto.value.subtotal, () => nuevoPresupuesto.value.descuento], ([subtotal, descuento]) => {
            const descuentoDecimal = descuento / 100; // Convertir el descuento de porcentaje a decimal
            nuevoPresupuesto.value.arancel_presupuesto = subtotal * (1 - descuentoDecimal); // Calcular el total con descuento
        });

        // const agregarDetallePresupuesto = (detallePresupuesto) => {
        //     console.log('Evento detalle presupuesto en el componente padre', detallePresupuesto);
            // const detalle = detallePresupuesto.value;
            // // Agregar el detalle recibido al array detallesPresupuesto
            // nuevoPresupuesto.detallesPresupuesto.value.push(detalle);
            // console.log('Array detallesPresupuesto:', nuevoPresupuesto.detallesPresupuesto.value)
            // console.log('numero primer servicio', nuevoPresupuesto.detallesPresupuesto.value[0].nro_servicio)
            // console.log('cantidad primer setvicio', nuevoPresupuesto.detallesPresupuesto.value[0].cantidad)
            // console.log('total primer servicio', nuevoPresupuesto.detallesPresupuesto.value[0].total)
        // };s

        const agregarDetallePresupuesto = (detallePresupuesto) => {
            console.log('Evento detalle presupuesto en el componente padre', detallePresupuesto);
            // Asegúrate de que detallePresupuesto es un ref y tiene un valor
            if (detallePresupuesto && detallePresupuesto.value) {
                // detallePresupuesto.value es el array que contiene tus objetos de detalles
                console.log('Reemplazando detalles:', detallePresupuesto.value);

                // Asignamos el nuevo array de detalles directamente
                nuevoPresupuesto.value.detalles_presupuesto = detallePresupuesto.value;
            }
            console.log('Array dentro de nuevoPresupuesto', nuevoPresupuesto.value.detalles_presupuesto);
        };
        
        return {
          inputProps,
          sugerencias,
          nuevoPresupuesto,
          area_tematicaOptions,
          descuentoOptions,
          mostrarModal,
          showSuccessAlert,
          showErrorAlert,
          buscarSugerencias,
          selectedSolicitante,
          seleccionarSugerencia,
          mostrarFormulario,
          cerrarModal,
          guardarPresupuesto,
          actualizarSubTotal,
          agregarDetallePresupuesto,
          // detallesPresupuesto
        };
    }
  };
</script>

  
  
<style scoped>
  /* .modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
  } */
  
  /* .modal.show {
    display: flex;
    align-items: center;
    justify-content: center;
  } */
  
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
  