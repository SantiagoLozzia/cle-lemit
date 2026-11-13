<template>
  <div class="login-page">

    <div class="login-panel">

      <!-- Panel izquierdo: branding -->
      <div class="brand-panel">
        <div class="brand-content">
          <img src="@/assets/logo_lemit.png" alt="LEMIT" class="brand-logo" />
          <h1 class="brand-title">CLE</h1>
          <p class="brand-subtitle">Circuito Legajo Electrónico</p>
          <div class="brand-divider"></div>
          <p class="brand-institution">Laboratorio de Entrenamiento Multidisciplinario para la Investigación Tecnológica</p>
        </div>
      </div>

      <!-- Panel derecho: formulario -->
      <div class="form-panel">
        <div class="form-inner">
          <h2 class="form-title">Iniciar sesión</h2>
          <p class="form-subtitle">Ingresá tus credenciales para acceder</p>

          <form @submit.prevent="login">
            <div class="field-group">
              <label class="field-label" for="username">Usuario</label>
              <div class="input-wrap">
                <i class="bi bi-person input-icon"></i>
                <input
                  v-model="username"
                  type="text"
                  id="username"
                  class="form-control field-input"
                  placeholder="Nombre de usuario"
                  autocomplete="username"
                  required
                />
              </div>
            </div>

            <div class="field-group">
              <label class="field-label" for="password">Contraseña</label>
              <div class="input-wrap">
                <i class="bi bi-lock input-icon"></i>
                <input
                  v-model="password"
                  :type="mostrarPassword ? 'text' : 'password'"
                  id="password"
                  class="form-control field-input"
                  placeholder="Contraseña"
                  autocomplete="current-password"
                  required
                />
                <button type="button" class="toggle-pw" @click="mostrarPassword = !mostrarPassword" tabindex="-1">
                  <i :class="mostrarPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2 small mb-3">
              <i class="bi bi-exclamation-circle me-1"></i>{{ errorMessage }}
            </div>

            <button type="submit" class="btn-acceder" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              <span v-else><i class="bi bi-box-arrow-in-right me-2"></i></span>
              Acceder
            </button>

            <p class="text-center mt-3 mb-0">
              <a href="#" class="forgot-link" @click.prevent="abrirModalOlvide">¿Olvidaste tu contraseña?</a>
            </p>
          </form>
        </div>
      </div>

    </div>

  </div>

  <!-- Modal Olvidé mi contraseña -->
  <div class="modal-overlay" v-if="mostrarModalOlvide" @click.self="cerrarModalOlvide">
    <div class="modal-box">
      <div class="modal-header-custom">
        <h5>Recuperar contraseña</h5>
        <button class="btn-close" @click="cerrarModalOlvide"></button>
      </div>
      <div class="modal-body-custom">
        <p class="small text-muted mb-3">Ingresá tu email y te enviaremos un enlace para restablecer tu contraseña.</p>
        <input
          v-model="emailOlvide"
          type="email"
          class="form-control form-control-sm mb-2"
          placeholder="tu@email.com"
          :disabled="enviandoOlvide || olvideMsgOk"
        >
        <div v-if="olvideMsgOk" class="alert alert-success py-1 small mb-2">
          Si ese email existe en el sistema, te llegará un correo con el enlace.
        </div>
        <div v-if="olvideMsgError" class="alert alert-danger py-1 small mb-2">{{ olvideMsgError }}</div>
        <button
          class="btn btn-primary btn-sm w-100"
          :disabled="enviandoOlvide || olvideMsgOk || !emailOlvide.trim()"
          @click="enviarOlvide"
        >
          {{ enviandoOlvide ? 'Enviando...' : 'Enviar enlace' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api.js';

const router = useRouter();

const username        = ref('');
const password        = ref('');
const mostrarPassword = ref(false);
const errorMessage    = ref('');
const isLoading       = ref(false);

const mostrarModalOlvide = ref(false);
const emailOlvide        = ref('');
const enviandoOlvide     = ref(false);
const olvideMsgOk        = ref(false);
const olvideMsgError     = ref('');

const abrirModalOlvide = () => {
  emailOlvide.value    = '';
  olvideMsgOk.value    = false;
  olvideMsgError.value = '';
  mostrarModalOlvide.value = true;
};

const cerrarModalOlvide = () => { mostrarModalOlvide.value = false; };

const enviarOlvide = async () => {
  olvideMsgError.value = '';
  enviandoOlvide.value = true;
  try {
    await api.post('/auth/forgot_password/', { email: emailOlvide.value.trim() });
    olvideMsgOk.value = true;
  } catch (_) {
    olvideMsgError.value = 'No se pudo enviar el correo. Intentá de nuevo.';
  } finally {
    enviandoOlvide.value = false;
  }
};

async function login() {
  isLoading.value    = true;
  errorMessage.value = '';
  try {
    const response = await api.post('/auth/', {
      username: username.value,
      password: password.value
    });

    if (response.data && response.data.access) {
      sessionStorage.setItem('token',        response.data.access);
      sessionStorage.setItem('username',     username.value);
      sessionStorage.setItem('role',         response.data.role);
      sessionStorage.setItem('area_tematica', response.data.area_tematica);
      sessionStorage.setItem('first_name',   response.data.first_name);
      sessionStorage.setItem('last_name',    response.data.last_name);

      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      window.dispatchEvent(new CustomEvent('auth-changed'));
      router.push('/');
    } else {
      errorMessage.value = 'No se recibió el token';
    }
  } catch (error) {
    if (error.response?.data) {
      errorMessage.value = error.response.data.detail || 'Usuario o contraseña incorrectos';
    } else {
      errorMessage.value = 'No se pudo conectar con el servidor';
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-image: url('@/assets/edificioviejo.jpg');
  background-size: cover;
  background-position: center 55%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
}

.login-page::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.28);
}

.login-panel {
  position: relative;
  z-index: 1;
  display: flex;
  width: 100%;
  max-width: 860px;
  min-height: 520px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

/* Panel izquierdo */
.brand-panel {
  flex: 1;
  background: linear-gradient(160deg, #014f73 0%, #026290 60%, #0282be 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 36px;
}

.brand-content {
  text-align: center;
  color: white;
}

.brand-logo-upcn {
  display: block;
  height: 70px;
  object-fit: contain;
  margin: 0 auto 20px;
}

.brand-logo {
  display: block;
  height: 70px;
  object-fit: contain;
  margin: 0 auto 24px;
  filter: brightness(0) invert(1);
  opacity: 0.9;
}

.brand-title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: 4px;
  margin: 0;
  line-height: 1;
}

.brand-subtitle {
  font-size: 0.9rem;
  opacity: 0.85;
  margin: 6px 0 20px;
  letter-spacing: 0.5px;
}

.brand-divider {
  width: 40px;
  height: 2px;
  background: rgba(255, 255, 255, 0.4);
  margin: 0 auto 20px;
  border-radius: 2px;
}

.brand-institution {
  font-size: 0.75rem;
  opacity: 0.65;
  line-height: 1.5;
  max-width: 220px;
  margin: 0 auto;
}

/* Panel derecho */
.form-panel {
  flex: 1;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
}

.form-inner {
  width: 100%;
  max-width: 320px;
}

.form-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.form-subtitle {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 28px;
}

.field-group {
  margin-bottom: 18px;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
  display: block;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: #aaa;
  font-size: 1rem;
  pointer-events: none;
}

.field-input {
  padding-left: 36px;
  padding-right: 36px;
  border-radius: 8px;
  border: 1.5px solid #e0e0e0;
  font-size: 0.9rem;
  height: 42px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.field-input:focus {
  border-color: #026290;
  box-shadow: 0 0 0 3px rgba(2, 98, 144, 0.12);
  outline: none;
}

.toggle-pw {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  padding: 4px;
  font-size: 1rem;
  line-height: 1;
}
.toggle-pw:hover { color: #555; }

.btn-acceder {
  width: 100%;
  height: 44px;
  background: #026290;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.1s;
  margin-top: 4px;
}
.btn-acceder:hover:not(:disabled) { background: #014f73; }
.btn-acceder:active:not(:disabled) { transform: scale(0.98); }
.btn-acceder:disabled { opacity: 0.65; cursor: not-allowed; }

.forgot-link {
  font-size: 0.82rem;
  color: #026290;
  text-decoration: none;
}
.forgot-link:hover { text-decoration: underline; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-box {
  background: #fff;
  border-radius: 10px;
  width: 100%;
  max-width: 380px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header-custom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid #dee2e6;
}
.modal-header-custom h5 { margin: 0; font-size: 1rem; }

.modal-body-custom { padding: 20px; }

/* Responsive: en móvil apilar verticalmente */
@media (max-width: 600px) {
  .login-panel { flex-direction: column; min-height: unset; }
  .brand-panel { padding: 32px 24px; }
  .brand-title { font-size: 2rem; }
  .form-panel { padding: 32px 24px; }
}
</style>
