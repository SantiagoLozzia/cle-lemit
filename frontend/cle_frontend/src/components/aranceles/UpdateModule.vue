<template>
  <div>
    <!-- Modal -->
    <div class="modal fade" id="actualizarModulo" tabindex="-1" aria-labelledby="actualizarModuloLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="actualizarModuloLabel">Actualizar Módulo</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
              {{ error }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            <div v-if="success" class="alert alert-success alert-dismissible fade show" role="alert">
              {{ success }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>

            <div class="form-group">
              <label for="nuevoModulo" class="form-label">Valor Actual</label>
              <input v-model.number="nuevoModulo" id="nuevoModulo" type="number" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="actualizarModulo">Actualizar</button>
          </div>
        </div>
      </div>
    </div>

    <button class="btn btn-primary" @click="abrirActualizarModulo">Actualizar Módulo</button>
  </div>
</template>

<script>
import { ref } from "vue";
import api from '@/api.js'; 

export default {
  setup() {
    const nuevoModulo = ref(null); // Variable para el valor del módulo
    const mostrarModalActualizarModulo = ref(false); // Para mostrar/ocultar el modal
    const error = ref(""); // Mensaje de error
    const success = ref(""); // Mensaje de éxito

    // Función para abrir el modal
    const abrirActualizarModulo = () => {
      mostrarModalActualizarModulo.value = true;
    };

    // Función para actualizar el módulo
    const actualizarModulo = async () => {
      try {
        const response = await api.post('/aranceles/actualizar_modulo/', {
          nuevo_valor: nuevoModulo.value,
        });
        if (response.data.success) {
          success.value = "El módulo se actualizó correctamente.";
          error.value = "";
        } else {
          success.value = "";
          error.value = "Hubo un error al actualizar el módulo.";
        }
        setTimeout(() => {
          success.value = "";
          error.value = "";
        }, 3000);
      } catch (err) {
        error.value = "Hubo un error al contactar al servidor.";
        success.value = "";
        setTimeout(() => {
          error.value = "";
        }, 3000);
      }
    };

    return {
      nuevoModulo,
      mostrarModalActualizarModulo,
      error,
      success,
      abrirActualizarModulo,
      actualizarModulo,
    };
  },
};
</script>

<style scoped>
/* Puedes añadir estilos aquí si es necesario */
</style>
