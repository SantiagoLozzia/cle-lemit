<template>
  <div class="login-background">
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
  background-image: url('@/assets/edificio.jpg');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  max-width: 400px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
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