<template>
  <div>
    <div class="button-container">
      <button class="btn btn-primary float-start ms-2 mt-2" @click="mostrarFormulario">Nuevo +</button>
    </div>

    <div class="modal" :class="{ 'show': mostrarModal }" id="modalSolicitante">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Nuevo Solicitante</h1>
            <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                <label for="nombre_solicitante" class="form-label text-left">Nombre:</label>
                <input v-model="nuevoSolicitante.nombre_solicitante" type="text" class="form-control" id="nombre_solicitante" name="nombre_solicitante" required />
              </div>

              <div class="mb-3">
                <label for="cuit" class="form-label text-left">Cuit:</label>
                <input v-model="nuevoSolicitante.cuit" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="cuit" name="cuit" required />
              </div>

              <div class="mb-3">
                <label for="pais" class="form-label text-left">País:</label>
                <input v-model="nuevoSolicitante.pais" type="text" class="form-control" id="pais" name="pais" required />
              </div>

              <div class="mb-3">
                <label for="provincia" class="form-label text-left">Provincia:</label>
                <input v-model="nuevoSolicitante.provincia" type="text" class="form-control" id="provincia" name="provincia" required />
              </div>

              <div class="mb-3">
                <label for="localidad" class="form-label text-left">Localidad:</label>
                <input v-model="nuevoSolicitante.localidad" type="text" class="form-control" id="localidad" name="localidad" required />
              </div>

              <div class="mb-3">
                <label for="direccion" class="form-label text-left">Dirección:</label>
                <input v-model="nuevoSolicitante.direccion" type="text" class="form-control" id="direccion" name="direccion" required />
              </div>

              <div class="mb-3">
                <label for="telefono" class="form-label text-left">Teléfono:</label>
                <input v-model="nuevoSolicitante.telefono" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="telefono" name="telefono" required />
              </div>

              <div class="mb-3">
                <label for="email" class="form-label text-left">Email:</label>
                <input v-model="nuevoSolicitante.email" type="text" class="form-control" id="email" name="email" required />
              </div>

              <div class="mb-3">
                <label for="codigoPostal" class="form-label text-left">Código Postal:</label>
                <input v-model="nuevoSolicitante.codigoPostal" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="codigoPostal" name="codigoPostal" required />
              </div>

              <button @click="guardarSolicitante" type="button" class="btn btn-primary w-100">Guardar</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! El solicitante se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar el solicitante Por favor, inténtalo de nuevo.
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      nuevoSolicitante: {
        nombre_solicitante: '',
        cuit: null,
        pais: '',
        provincia: '',
        localidad: '',
        direccion: '',
        telefono: '',
        email: '',
        codigoPostal: null,
      },
      
      mostrarModal: false,
      showSuccessAlert: false,
      showErrorAlert: false,
    };
  },
  methods: {
    mostrarFormulario() {
      this.nuevoSolicitante = {
        nombre_solicitante: '',
        cuit: null,
        pais: '',
        provincia: '',
        localidad: '',
        direccion: '',
        telefono: '',
        email: '',
        codigoPostal: null,
      };
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
    },
    guardarSolicitante() {
      // Validar campos obligatorios
      if (!this.nuevoSolicitante.nombre_solicitante || !this.nuevoSolicitante.cuit  === null || !this.nuevoSolicitante.pais || !this.nuevoSolicitante.provincia || !this.nuevoSolicitante.localidad || !this.nuevoSolicitante.direccion || !this.nuevoSolicitante.telefono || !this.nuevoSolicitante.email || !this.nuevoSolicitante.codigoPostal) {
        // Mostrar mensaje de error y no continuar con la acción
        //alert('Por favor, complete todos los campos obligatorios.');
        return;
      }

      // Enviar datos al backend usando Axios
      axios.post('api/solicitantes/', this.nuevoSolicitante)
        .then(response => {
          console.log(response.data);
          this.cerrarModal();

          // Limpiar el formulario y mostrar la alerta de éxito
          this.nuevoSolicitante = {
            nombre_solicitante: '',
            cuit: null,
            pais: '',
            provincia: '',
            localidad: '',
            direccion: '',
            telefono: '',
            email: '',
            codigoPostal: null,
          };

          this.showSuccessAlert = true;

          setTimeout(() => {
            this.showSuccessAlert = false;
          }, 3000);

          //console.log('Evento emitido desde NewSolicitante.vue');
          //this.$root.$emit('nuevo-nombre_solicitante-agregado');
          
        })
        .catch(error => {
          console.error('Error al guardar el solicitante:', error);
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
/* Estilos personalizados para el modal */
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

#modalSolicitante {
  max-width: 100% !important;
  margin: 0 auto; /* Centra el modal horizontalmente */
  margin-top: 0px; /* Agrega un margen superior para evitar que el modal se pegue en la parte superior */
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
  right: 10px; /* Ajusta la posición según sea necesario */
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none; /* Asegura que el ícono no interfiera con los eventos del ratón */
}

.form-select:focus {
  border-color: #007bff; /* Color de resaltado cuando el desplegable está enfocado */
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25); /* Efecto de resaltado cuando está enfocado */
}

form div.label-container label {
  text-align: left !important;
}
</style>
