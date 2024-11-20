<template>
  <div>
    <div class="button-container">
      <button class="btn btn-primary float-start ms-2 mt-2 custom-shadow-btn" @click="mostrarFormulario">+ Servicio</button>
    </div>

    <div class="modal" :class="{ 'show': mostrarModal }" id="modalService">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Nuevo Servicio</h1>
            <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                <label for="servicio" class="form-label text-left">Servicio:</label>
                <input v-model="nuevoServicio.servicio" type="text" class="form-control" id="servicio" name="servicio" required />
              </div>

              <div class="mb-3">
                <label for="norma" class="form-label text-left">Norma:</label>
                <input v-model="nuevoServicio.norma" type="text" class="form-control" id="norma" name="norma" required />
              </div>

              <div class="mb-3">
                <label for="arancel" class="form-label text-left">Valor:</label>
                <input v-model="nuevoServicio.arancel" type="text" inputmode="numeric" pattern="[0-9]*" class="form-control" id="arancel" name="arancel" required />
              </div>

              <div class="mb-3">
                <label for="area_tematica" class="form-label text-left">Área Temática:</label>
                <select v-model="nuevoServicio.area_tematica" class="form-select" id="area_tematica" name="area_tematica" required>
                  <option v-for="(option, key) in area_tematicaOptions" :key="key" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
              </div>

              <button @click="guardarArancel" type="button" class="btn btn-primary w-100">Guardar</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! El arancel se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar el arancel. Por favor, inténtalo de nuevo.
    </div>

  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const nuevoServicio = ref({
      servicio: '',
      norma: '',
      arancel: null,
      area_tematica: '',
    });

    const area_tematicaOptions = [
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
    ];

    const mostrarModal = ref(false);
    const showSuccessAlert = ref(false);
    const showErrorAlert = ref(false);

    const mostrarFormulario = () => {
      nuevoServicio.value = {
        servicio: '',
        norma: '',
        arancel: null,
        area_tematica: '',
      };
      mostrarModal.value = true;
    };

    const cerrarModal = () => {
      mostrarModal.value = false;
    };

    const guardarArancel = () => {
      if (!nuevoServicio.value.servicio || !nuevoServicio.value.norma || nuevoServicio.value.arancel === null || !nuevoServicio.value.area_tematica) {
        return;
      }

      axios.post(`http://localhost:8000/api/aranceles/`, nuevoServicio.value)
        .then(response => {
          console.log(response.data);
          cerrarModal();

          nuevoServicio.value = {
            servicio: '',
            norma: '',
            arancel: null,
            area_tematica: '',
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

    return {
      nuevoServicio,
      area_tematicaOptions,
      mostrarModal,
      showSuccessAlert,
      showErrorAlert,
      mostrarFormulario,
      cerrarModal,
      guardarArancel
    };
  }
};
</script>

<style scoped>

.button-container {
  margin-left: 0;
}

form div.label-container label {
  text-align: left !important;
}
</style>
