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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import api from '@/api.js';
import logo from '@/assets/logo_L.png';

export default {
  setup() {
    const logoPath = ref(logo);
    const userLoaded = ref(false);
    const firstName = ref('');
    const lastName = ref('');

    const fullName = computed(() => {
      return firstName.value || lastName.value ? `${firstName.value} ${lastName.value}` : 'Invitado';
    });

    const loadUserFromSession = () => {
      firstName.value = sessionStorage.getItem('first_name') || '';
      lastName.value = sessionStorage.getItem('last_name') || '';
      userLoaded.value = true;
    };

    const logout = () => {
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('username');
      sessionStorage.removeItem('first_name');
      sessionStorage.removeItem('last_name');
      delete api.defaults.headers.common['Authorization'];
      window.location.href = '/login';
    };

    onMounted(() => {
      loadUserFromSession();
      window.addEventListener('auth-changed', loadUserFromSession);
    });

    onUnmounted(() => {
      window.removeEventListener('auth-changed', loadUserFromSession);
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
