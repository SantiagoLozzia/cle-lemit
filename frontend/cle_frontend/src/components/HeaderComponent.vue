<template>
  <header class="header-container">
    <div class="logo-container">
      <img alt="Logo" :src="logoPath" class="logo">
    </div>
    <div class="user-info" v-if="userLoaded">
      <span>{{ fullName }}</span>
      <i class="bi bi-box-arrow-in-right logout-icon" @click="logout"></i>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, watchEffect } from 'vue';
import api from '@/api.js';
import logo from '@/assets/tico.jpeg';

export default {
  setup() {
    const logoPath = ref(logo);
    const userLoaded = ref(false);
    const firstName = ref('');
    const lastName = ref('');

    const fullName = computed(() => {
      return firstName.value || lastName.value ? `${firstName.value} ${lastName.value}` : 'Invitado';
    });

    const fetchUserInfo = async () => {
      try {
        const token = sessionStorage.getItem('token');

        if (token && token !== 'null' && token !== 'undefined') {
          const response = await api.get('/auth/user_info/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          firstName.value = response.data.first_name;
          lastName.value = response.data.last_name;

          console.log('First Name:', firstName.value);
          console.log('Last Name:', lastName.value);
        } else {
          console.warn('Token inválido o no encontrado');
        }
      } catch (error) {
        console.error('Error fetching user info:', error.message);
      } finally {
        userLoaded.value = true;
      }
    };

    const logout = () => {
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('username');
      delete api.defaults.headers.common['Authorization'];
      window.location.href = '/login';
    };

    onMounted(() => {
      // Primer intento de carga
      fetchUserInfo();
    });

    // Observa si aparece el token más tarde (por ejemplo, después de login)
    watchEffect(() => {
      const token = sessionStorage.getItem('token');
      if (!userLoaded.value && token && token !== 'null' && token !== 'undefined') {
        fetchUserInfo();
      }
    });

    return {
      logoPath,
      fullName,
      logout,
      userLoaded
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
