<template>
  <header class="header-container">
    <div class="logo-container">
      <img alt="Logo" :src="logoPath" class="logo">
    </div>
    <div class="user-info" v-if="userLoaded">
      <span>{{ fullName }}</span>
      <i class="bi bi-pen-fill firma-icon" @click="abrirModalFirma" title="Mi firma"></i>
      <i class="bi bi-box-arrow-in-right logout-icon" @click="logout"></i>
    </div>
  </header>

  <!-- Modal Mi Firma -->
  <div class="modal" :class="{ 'show': mostrarModalFirma }" @click.self="cerrarModalFirma">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Mi Firma</h5>
          <button type="button" class="btn-close" @click="cerrarModalFirma"></button>
        </div>
        <div class="modal-body">
          <div v-if="firmaUrl" class="text-center mb-3">
            <p class="text-muted small mb-1">Firma actual:</p>
            <img :src="firmaUrl" alt="Mi firma" style="max-width:100%; max-height:120px; border:1px solid #dee2e6; border-radius:4px; background:#fafafa; padding:8px;">
          </div>
          <div v-else class="text-muted small text-center mb-3">
            No tenés ninguna firma cargada.
          </div>
          <label class="btn btn-outline-primary btn-sm w-100">
            <i class="bi bi-upload"></i> {{ firmaUrl ? 'Reemplazar firma' : 'Subir firma (PNG)' }}
            <input type="file" accept="image/png,image/jpeg" style="display:none;" @change="subirFirma">
          </label>
          <button v-if="firmaUrl" class="btn btn-outline-danger btn-sm w-100 mt-2" @click="eliminarFirma">
            <i class="bi bi-trash"></i> Eliminar firma
          </button>
        </div>
      </div>
    </div>
  </div>
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
    const mostrarModalFirma = ref(false);
    const firmaUrl = ref(null);

    const fullName = computed(() => {
      return firstName.value || lastName.value ? `${firstName.value} ${lastName.value}` : 'Invitado';
    });

    const loadUserFromSession = () => {
      firstName.value = sessionStorage.getItem('first_name') || '';
      lastName.value = sessionStorage.getItem('last_name') || '';
      userLoaded.value = true;
    };

    const cargarFirma = async () => {
      try {
        const res = await api.get('/authentication/firma_usuario/');
        firmaUrl.value = res.data.firma_url || null;
      } catch {}
    };

    const abrirModalFirma = async () => {
      await cargarFirma();
      mostrarModalFirma.value = true;
    };

    const cerrarModalFirma = () => {
      mostrarModalFirma.value = false;
    };

    const subirFirma = async (e) => {
      const archivo = e.target.files[0];
      if (!archivo) return;
      const formData = new FormData();
      formData.append('firma', archivo);
      try {
        const res = await api.post('/authentication/firma_usuario/', formData);
        firmaUrl.value = res.data.firma_url;
        // Notificar a otros componentes
        window.dispatchEvent(new CustomEvent('firma-usuario-actualizada', { detail: { firma_url: res.data.firma_url } }));
      } catch {}
      e.target.value = '';
    };

    const eliminarFirma = async () => {
      try {
        await api.delete('/authentication/firma_usuario/');
        firmaUrl.value = null;
        window.dispatchEvent(new CustomEvent('firma-usuario-actualizada', { detail: { firma_url: null } }));
      } catch {}
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
      logoPath, fullName, logout, userLoaded,
      mostrarModalFirma, firmaUrl,
      abrirModalFirma, cerrarModalFirma, subirFirma, eliminarFirma,
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

.logo { width: 40px; }

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info span { color: white; }

.firma-icon {
  color: white;
  font-size: 20px;
  cursor: pointer;
  opacity: 0.85;
  transition: opacity 0.2s;
}
.firma-icon:hover { opacity: 1; }

.logout-icon {
  color: white;
  font-size: 32px;
  cursor: pointer;
  transition: color 0.3s;
}
.logout-icon:hover { color: #ddd; }
</style>
