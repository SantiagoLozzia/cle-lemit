<template>
  <div>
    <button class="btn btn-primary custom-shadow-btn" @click="abrirModal">Actualizar Módulo</button>

    <div class="modal" :class="{ 'show': mostrarModal }" id="modalActualizarModulo">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Actualizar Módulo</h5>
            <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>
            <div class="mb-3">
              <label for="nuevoModulo" class="form-label">Nuevo valor del módulo</label>
              <input v-model.number="nuevoModulo" id="nuevoModulo" type="number" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="actualizarModulo">Actualizar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/api.js';

export default {
  setup() {
    const nuevoModulo = ref(null);
    const mostrarModal = ref(false);
    const error = ref('');
    const success = ref('');

    const abrirModal = () => {
      nuevoModulo.value = null;
      error.value = '';
      success.value = '';
      mostrarModal.value = true;
    };

    const cerrarModal = () => {
      mostrarModal.value = false;
    };

    const actualizarModulo = async () => {
      try {
        const response = await api.post('/aranceles/actualizar_modulo/', {
          nuevo_valor: nuevoModulo.value,
        });
        if (response.data.success) {
          success.value = 'El módulo se actualizó correctamente.';
          error.value = '';
        } else {
          error.value = 'Hubo un error al actualizar el módulo.';
          success.value = '';
        }
        setTimeout(() => {
          success.value = '';
          error.value = '';
          cerrarModal();
        }, 2000);
      } catch (err) {
        error.value = 'Hubo un error al contactar al servidor.';
        success.value = '';
        setTimeout(() => { error.value = ''; }, 3000);
      }
    };

    return { nuevoModulo, mostrarModal, error, success, abrirModal, cerrarModal, actualizarModulo };
  },
};
</script>
