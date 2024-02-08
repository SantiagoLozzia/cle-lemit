<template>
    <div>
    <vue-autosuggest
      :suggestions="suggestions"
      :input-props="inputProps"
      @input="onInputChange"
      @selected="onSuggestionSelected"
    ></vue-autosuggest>
    </div>

    <div>
      <div class="button-container">
        <button class="btn btn-primary float-start ms-2 mt-2" @click="mostrarFormulario">Nuevo +</button>
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
                  <label for="nro_solicitante" class="form-label text-left">Nro Solicitante:</label>
                  <input v-model="nuevoPresupuesto.nro_solicitante" type="text" class="form-control" id="nro_solicitante" name="nro_solicitante" required ref="nro_solicitante" />
                </div>

                <div class="mb-3">
                  <label for="solicitante" class="form-label text-left">Solicitante:</label>
                  <input v-model="nuevoPresupuesto.solicitante" type="text" class="form-control" id="solicitante" name="solicitante" required ref="solicitante" />
                </div>

                <div class="mb-3">
                  <label for="contacto" class="form-label text-left">Contacto:</label>
                  <input v-model="nuevoPresupuesto.contacto" type="text" class="form-control" id="contacto" name="contacto" required />
                </div>
                
                <div class="mb-3">
                  <label for="telefono" class="form-label text-left">Teléfono:</label>
                  <input v-model="nuevoPresupuesto.telefono" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="telefono" name="telefono" required />
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label text-left">Email:</label>
                  <input v-model="nuevoPresupuesto.email" type="text" class="form-control" id="email" name="email" required />
                </div>
  
                <div class="mb-3">
                  <label for="area_tematica" class="form-label text-left">Área Temática:</label>
                  <select v-model="nuevoPresupuesto.area_tematica" class="form-select" id="area_tematica" name="area_tematica" required>
                    <option v-for="(option, key) in area_tematicaOptions" :key="key" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="subtotal" class="form-label text-left">SubTotal:</label>
                  <input v-model="nuevoPresupuesto.subtotal" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="subtotal" name="subtotal" required />
                </div>

                <div class="mb-3">
                  <label for="descuento" class="form-label text-left">Descuento:</label>
                  <select v-model="nuevoPresupuesto.descuento" class="form-select" id="descuento" name="descuento" required>
                    <option v-for="(option, key) in descuentoOptions" :key="key" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
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
  </template>
  
  <script>
  import axios from 'axios';
  import VueAutosuggest from 'vue-autosuggest';
  
  export default {
    
    components: {
    VueAutosuggest,
    },

    data() {
      return {
        inputProps: {
        placeholder: 'Buscar solicitante',
        },
        suggestions: [], 

        nuevoPresupuesto: {
          nro_solicitante: '',
          solicitante: '',
          contacto: '',
          telefono: null,
          email: '',
          area_tematica: '',
          subtotal: null,
          descuento: '0',
        },
        area_tematicaOptions: [
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
        ],
        descuentoOptions: [
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
        ],
        mostrarModal: false,
        showSuccessAlert: false,
        showErrorAlert: false,
      };
    },
    methods: {

      onInputChange(value) {
        console.log('Valor de entrada:', value);
        // Verificar si el usuario está escribiendo en los campos nro_solicitante o solicitante
        if (value && (this.$refs.nro_solicitante === document.activeElement || this.$refs.solicitante === document.activeElement)) {
          console.log('Término de búsqueda:', value);  
          // Realizar la solicitud HTTP para buscar sugerencias de acuerdo al valor proporcionado
            axios.get(`http://localhost:8000/api/presupuestos/buscar_solicitantes/?term=${value}`)
                .then(response => {
                    this.suggestions = response.data; // Actualizar la lista de sugerencias con los resultados de la búsqueda
                })
                .catch(error => {
                    console.error('Error al buscar solicitantes:', error);
                });
        } else {
              // Limpiar las sugerencias si el usuario no está escribiendo en los campos nro_solicitante o solicitante
              this.suggestions = [];
        }
      },
      onSuggestionSelected(suggestion) {
        // La lógica cuando el usuario selecciona una sugerencia
        // Se puede actualizar otros campos del formulario con los detalles del solicitante seleccionado
        this.nuevoPresupuesto.nro_solicitante = suggestion.nro_solicitante;
        this.nuevoPresupuesto.solicitante = suggestion.nombre_solicitante;
        this.nuevoPresupuesto.contacto = suggestion.telefono;
        this.nuevoPresupuesto.email = suggestion.email;
      },

      mostrarFormulario() {
        this.nuevoPresupuesto = {
          nro_solicitante: '', 
          solicitante: '',
          contacto: '',
          telefono: null,
          email: '',
          area_tematica: '',
          subtotal: null,
          descuento: '0',
        };
        this.mostrarModal = true;
      },
      cerrarModal() {
        this.mostrarModal = false;
      },
      guardarPresupuesto() {
        // Validar campos obligatorios
        if (!this.nuevoPresupuesto.contacto || !this.nuevoPresupuesto.email || !this.nuevoPresupuesto.area_tematica || this.nuevoPresupuesto.subtotal === null || this.nuevoPresupuesto.descuento === null ) {
          // Mostrar mensaje de error y no continuar con la acción
          //alert('Por favor, complete todos los campos obligatorios.');
          return;
        }
  
        // Enviar datos al backend usando Axios
        axios.post('/api/presupuestos/', this.nuevoPresupuesto)
          .then(response => {
            console.log(response.data);
            this.cerrarModal();
  
            // Limpiar el formulario y mostrar la alerta de éxito
            this.nuevoPresupuesto = {
              nro_solicitante: '', // Cambié solicitante por nro_solicitante, asumiendo que es el campo donde se ingresa el número del solicitante
              solicitante: '', // Este campo se llenará automáticamente cuando el usuario seleccione una sugerencia
              contacto: '',
              telefono: null,
              email: '',
              area_tematica: '',
              subtotal: null,
              descuento: '0',
            };
  
            this.showSuccessAlert = true;
  
            setTimeout(() => {
              this.showSuccessAlert = false;
            }, 3000);
  
            //console.log('Evento emitido desde NewService.vue');
            //this.$root.$emit('nuevo-servicio-agregado');
            
          })
          .catch(error => {
            console.error('Error al guardar el presupuesto:', error);
            this.cerrarModal();
            this.showErrorAlert = true;
  
            setTimeout(() => {
              this.showErrorAlert = false;
            }, 5000);
          });
      },
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
  