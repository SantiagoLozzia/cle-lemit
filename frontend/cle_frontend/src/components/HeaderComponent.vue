<template>
  <header class="header-container">
    <div class="logo-container">
      <img alt="Logo" :src="logoPath" class="logo">
    </div>
    <div class="user-info">
      <span>{{ fullName }}</span>
      <i class="bi bi-box-arrow-in-right logout-icon" @click="logout"></i>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import logo from '@/assets/logo_L.png';

export default {
  setup() {
    const logoPath = ref(logo);
    const firstName = ref('');
    const lastName = ref('');

    const fullName = computed(() => {
      return firstName.value || lastName.value ? `${firstName.value} ${lastName.value}` : 'Invitado';
    });

    const fetchUserInfo = async () => {
      try {
        const token = sessionStorage.getItem('token');
         // Verificar que estamos obteniendo el token correctamente
        console.log('Token from sessionStorage:', token);

        if (token) {
          const response = await axios.get('http://localhost:8000/api/authentication/user_info/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          
          // Verificar la respuesta del backend
          console.log('User Info Response:', response.data);

          firstName.value = response.data.first_name;
          lastName.value = response.data.last_name;

          // Verificar que firstName y lastName se están configurando correctamente
          console.log('First Name:', firstName.value);
          console.log('Last Name:', lastName.value);
        }
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    };

    const logout = () => {
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('username');
      axios.defaults.headers.common['Authorization'] = '';
      window.location.href = '/login'; // Redirige a la página de login
    };

    onMounted(() => {
      fetchUserInfo();
    });

    return {
      logoPath,
      fullName,
      logout
    };
  }
};
</script>

<style scoped>
.header-container {
  position: fixed;
  background-color: #026290;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 70px;
  z-index: 1000;
}

.logo {
  width: 40px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  color: white;
  margin-right: 10px;
}

.logout-icon {
  color: white;
  font-size: 32px;
  cursor: pointer;
  transition: color 0.3s;
}

.logout-icon:hover {
  color: #ddd;
}
</style>
