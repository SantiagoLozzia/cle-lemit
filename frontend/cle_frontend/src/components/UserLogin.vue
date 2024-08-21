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
          <button type="submit" class="btn btn-primary w-100">Acceder</button>
          <p v-if="errorMessage" class="text-danger text-center mt-3">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const username = ref('');
const password = ref('');
const errorMessage = ref('');

async function login() {
  try {
    const response = await axios.post('http://localhost:8000/api/authentication/', {
      username: username.value,
      password: password.value
    });

    // Verificar que recibimos el token correctamente
    console.log('Login Response:', response.data);

    // Guardar el token y el nombre de usuario en el localStorage
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('username', username.value);

    // Verificar que el token se guardó correctamente
    console.log('Token stored in localStorage:', localStorage.getItem('token'));

    // Configurar Axios para incluir el token en futuras solicitudes
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

    // Redirigir al usuario a la página principal o a la página que estaba intentando acceder
    window.location.href = '/';
  } catch (error) {
    console.error('Login error:', error);
    errorMessage.value = 'Invalid username or password';
  }
}

</script>

<style scoped>
/* Contenedor de fondo con imagen */
.login-background {
  background-image: url('@/assets/fabian.jpg');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Contenedor del login */
.login-container {
  max-width: 400px;
  background-color: rgba(255, 255, 255, 0.9); /* Fondo semi-transparente */
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
