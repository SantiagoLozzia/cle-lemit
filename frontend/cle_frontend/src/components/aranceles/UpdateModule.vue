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
              <input v-model.number="nuevoModulo" id="nuevoModulo" type="number" min="1" class="form-control" />
            </div>
          </div>
          <div class="modal-footer" style="gap:8px">
            <button type="button" class="btn btn-primary" style="flex:1" :disabled="!nuevoModulo || guardando" @click="actualizarModulo">
              {{ guardando ? 'Actualizando...' : 'Actualizar' }}
            </button>
            <button type="button" class="btn btn-secondary" style="flex:1" @click="cerrarModal">Cerrar</button>
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
    const guardando = ref(false);

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
      if (!nuevoModulo.value || nuevoModulo.value <= 0) {
        error.value = 'Ingresá un valor válido mayor a 0.';
        return;
      }
      guardando.value = true;
      error.value = '';
      try {
        await api.post('/aranceles/actualizar_modulo/', { nuevo_valor: nuevoModulo.value });
        success.value = 'Módulo actualizado correctamente.';
        setTimeout(() => {
          success.value = '';
          cerrarModal();
        }, 1800);
      } catch (err) {
        error.value = err.response?.data?.error || 'Error al contactar al servidor.';
        setTimeout(() => { error.value = ''; }, 3000);
      } finally {
        guardando.value = false;
      }
    };

    return { nuevoModulo, mostrarModal, error, success, guardando, abrirModal, cerrarModal, actualizarModulo };
  },
};
</script>

<style scoped>
.modal {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.5);
}
.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
