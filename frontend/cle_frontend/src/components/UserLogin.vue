<template>
  <div class="login-background">
    <div class="brand-bar">
      <img src="@/assets/logo_lemit.png" alt="LEMIT" class="brand-logo" />
      <span class="brand-text">Laboratorio de Entrenamiento Multidisciplinario para la Investigación Tecnológica</span>
    </div>
    <div class="login-wrapper">
      <div class="login-container card shadow-lg">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Circuito Legajo Electrónico</h2>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Usuario</label>
              <input v-model="username" type="text" id="username" class="form-control" placeholder="Ingrese su usuario" required />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Contraseña</label>
              <input v-model="password" type="password" id="password" class="form-control" placeholder="Ingrese su contraseña" required />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Acceder
            </button>
            <p v-if="errorMessage" class="text-danger text-center mt-3">{{ errorMessage }}</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api.js'; // Importa la instancia de Axios

const router = useRouter();

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

async function login() {
  isLoading.value = true;
  try {
    const response = await api.post('/auth/', {
      username: username.value,
      password: password.value
    });

    if (response.data && response.data.access) {
      // Guardar el token y la información del usuario en sessionStorage
      sessionStorage.setItem('token', response.data.access);
      sessionStorage.setItem('username', username.value);
      sessionStorage.setItem('role', response.data.role);
      sessionStorage.setItem('area_tematica', response.data.area_tematica);
      sessionStorage.setItem('first_name', response.data.first_name);
      sessionStorage.setItem('last_name', response.data.last_name);

      // Configurar Axios para incluir el token en futuras solicitudes
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

      // Notificar al header que el usuario cambió
      window.dispatchEvent(new CustomEvent('auth-changed'));

      console.log('Redirigiendo a la página principal');
      router.push('/')
        .then(() => console.log('Redirección exitosa'))
        .catch(err => console.error('Error al redirigir:', err));
    } else {
      errorMessage.value = 'No se recibió el token';
    }
  } catch (error) {
    console.error('Login error:', error.message);
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.detail || 'Error desconocido';
    } else {
      errorMessage.value = 'No se pudo conectar con el servidor';
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.login-background {
  background-image: url('@/assets/edificioviejo.jpg');
  background-size: cover;
  background-position: center 55%;
  min-height: calc(100vh / 0.7); /* compensate body { zoom: 0.7 } */
  display: flex;
  flex-direction: column;
  position: relative;
}

.login-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
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

.brand-logo {
  height: 44px;
  object-fit: contain;
}

.brand-text {
  color: white;
  font-size: 0.82rem;
  font-weight: 400;
  line-height: 1.3;
  max-width: 480px;
}

.login-wrapper {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.card-body {
  padding: 30px;
}

.form-control {
  border-radius: 0.25rem;
}

.btn-primary {
  border-radius: 0.25rem;
}

.text-danger {
  font-weight: bold;
}
</style>