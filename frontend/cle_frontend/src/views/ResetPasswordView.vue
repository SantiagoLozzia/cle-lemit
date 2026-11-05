<template>
  <div class="reset-bg">
    <div class="brand-bar">
      <img src="@/assets/logo_lemit.png" alt="LEMIT" class="brand-logo" />
      <span class="brand-text">Laboratorio de Entrenamiento Multidisciplinario para la Investigación Tecnológica</span>
    </div>
    <div class="reset-wrapper">
      <div class="reset-box card shadow-lg">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Nueva contraseña</h2>

          <div v-if="tokenInvalido" class="alert alert-danger text-center">
            El enlace es inválido o ya expiró. Solicitá uno nuevo desde la pantalla de inicio.
          </div>

          <form v-else-if="!exito" @submit.prevent="resetear">
            <div class="mb-3">
              <label class="form-label">Nueva contraseña</label>
              <input v-model="pw1" type="password" class="form-control" placeholder="Mínimo 8 caracteres" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Confirmar contraseña</label>
              <input v-model="pw2" type="password" class="form-control" placeholder="Repetir contraseña" required>
            </div>
            <div v-if="errorMsg" class="alert alert-danger py-2 small mb-2">{{ errorMsg }}</div>
            <button type="submit" class="btn btn-primary w-100" :disabled="cargando">
              <span v-if="cargando" class="spinner-border spinner-border-sm me-1"></span>
              Cambiar contraseña
            </button>
          </form>

          <div v-else class="text-center">
            <div class="alert alert-success">
              ¡Contraseña actualizada con éxito!
            </div>
            <a href="/userlogin" class="btn btn-outline-primary btn-sm mt-2">Ir al inicio de sesión</a>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api.js';

const route        = useRoute();
const uid          = ref('');
const token        = ref('');
const pw1          = ref('');
const pw2          = ref('');
const cargando     = ref(false);
const errorMsg     = ref('');
const exito        = ref(false);
const tokenInvalido = ref(false);

onMounted(() => {
  uid.value   = route.query.uid   || '';
  token.value = route.query.token || '';
  if (!uid.value || !token.value) tokenInvalido.value = true;
});

const resetear = async () => {
  errorMsg.value = '';
  if (pw1.value.length < 8) {
    errorMsg.value = 'La contraseña debe tener al menos 8 caracteres.';
    return;
  }
  if (pw1.value !== pw2.value) {
    errorMsg.value = 'Las contraseñas no coinciden.';
    return;
  }
  cargando.value = true;
  try {
    await api.post('/auth/reset_password/', {
      uid:          uid.value,
      token:        token.value,
      new_password: pw1.value,
    });
    exito.value = true;
  } catch (err) {
    const msg = err.response?.data?.error || '';
    if (msg.includes('expiró') || msg.includes('inválido')) {
      tokenInvalido.value = true;
    } else {
      errorMsg.value = msg || 'No se pudo restablecer la contraseña.';
    }
  } finally {
    cargando.value = false;
  }
};
</script>

<style scoped>
.reset-bg {
  background-image: url('@/assets/edificioviejo.jpg');
  background-size: cover;
  background-position: center 55%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.reset-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.45);
  pointer-events: none;
}

.brand-bar {
  position: relative;
  z-index: 1;
  background-color: rgba(2, 98, 144, 0.88);
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}
.brand-logo { height: 44px; object-fit: contain; }
.brand-text {
  color: white;
  font-size: 0.82rem;
  font-weight: 400;
  line-height: 1.3;
  max-width: 480px;
}

.reset-wrapper {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.reset-box {
  width: 100%;
  max-width: 400px;
  background-color: rgba(255,255,255,0.95);
  border-radius: 10px;
}
.card-body { padding: 30px; }
</style>
