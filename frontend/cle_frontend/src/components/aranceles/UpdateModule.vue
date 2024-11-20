<template>
    <div>
      <div class="button-container">
        <div class="d-flex align-items-center">
          <span class="badge bg-success fs-4 p-3 custom-shadow-btn">${{ valorModuloActual }}</span>
          <button class="btn btn-secondary ms-2" @click="abrirActualizarModulo">
            <i class="bi bi-pencil-square"></i>
          </button>
        </div>
      </div>

  
      <div class="modal" :class="{ 'show': mostrarModalActualizarModulo }" id="modalService">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5 fw-bold">Actualizar Módulo</h1>
              <button type="button" class="btn-close" @click="cerrarModalActualizarModulo" aria-label="Close"></button>
            </div>
  
            <div class="modal-body">
              <form class="was-validated">
                <div class="mb-3">
                  <input v-model.number="nuevoModulo" type="number" class="form-control" id="nuevoModulo" name="nuevoModulo" required />
                </div>
  
                <button @click="actualizarModulo" type="button" class="btn btn-primary w-100">Guardar</button>
              </form>
            </div>
            
          </div>
        </div>
      </div>
  
      <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
        ¡Éxito! El módulo se ha actualizado correctamente.
      </div>
      <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
        ¡Error! Ha ocurrido un problema al actualizar el módulo. Por favor, inténtalo de nuevo.
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted} from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
      const nuevoModulo = ref();
      const mostrarModalActualizarModulo = ref(false);
      const showSuccessAlert = ref(false);
      const showErrorAlert = ref(false);

      const valorModuloActual = ref();
      
      const obtenerModulo = async () => {
          try {
              const response = await axios.get('http://localhost:8000/api/aranceles/obtener_modulo/');
              valorModuloActual.value = response.data.valor;
          } catch (error) {
              console.error('Error al obtener el valor del módulo:', error);
          }
      };

      const abrirActualizarModulo = () => {
        mostrarModalActualizarModulo.value = true;
      };
  
      const cerrarModalActualizarModulo = () => {
        mostrarModalActualizarModulo.value = false;
      };
  
      const actualizarModulo = async () => {
        try {
            await axios.post('/api/aranceles/actualizar_modulo/', { nuevo_valor: nuevoModulo.value });
            showSuccessAlert.value = true;
            cerrarModalActualizarModulo();
            setTimeout(() => {
            showSuccessAlert.value = false;
            }, 3000);
        } catch (error) {
            cerrarModalActualizarModulo();
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
            }, 3000);
            
            console.error('Error al actualizar el valor del módulo:', error);
        }
      };

      onMounted(() => {
                obtenerModulo();
      });
  
      return {
        onMounted,
        nuevoModulo,
        valorModuloActual,
        obtenerModulo,
        mostrarModalActualizarModulo,
        showSuccessAlert,
        showErrorAlert,
        abrirActualizarModulo,
        cerrarModalActualizarModulo,
        actualizarModulo,
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
  
  #modalService .modal-dialog {
    max-width: 600px;
  }
  
  .form-select {
    font-size: 16px;
    padding: 6px;
    border: 1px solid #ced4da;
    border-radius: 5px;
    width: 100%;
    appearance: none;
    padding-right: 2.25rem;
  }
  
  .form-select:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25);
  }

  .button-container {
    display: flex;
    flex-direction: column; /* Alinea los elementos verticalmente en una columna */
    align-items: flex-start; /* Alinea horizontalmente a la izquierda */
    padding-top: 20px; 
  }

  .valor-modulo-actual {
    margin-bottom: 10px; /* Espacio entre el valor y el botón */
  }


  </style>
  