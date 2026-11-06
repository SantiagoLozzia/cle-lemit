<template>
  <header class="header-container">
    <div class="logo-container">
      <img alt="Logo" :src="logoPath" class="logo">
    </div>
    <div class="user-info" v-if="userLoaded" ref="userMenuRef">
      <div class="user-btn" @click="toggleMenu">
        <span>{{ fullName }}</span>
        <i class="bi bi-chevron-down chev" :class="{ rotated: menuAbierto }"></i>
      </div>
      <div class="dropdown-menu-custom" v-if="menuAbierto">
        <button class="dd-item" @click="irAlPerfil">
          <i class="bi bi-person-fill"></i> Mi Perfil
        </button>
        <button class="dd-item" @click="abrirModalFirma">
          <i class="bi bi-pen-fill"></i> Mi Firma
        </button>
        <div class="dd-divider"></div>
        <button class="dd-item dd-logout" @click="logout">
          <i class="bi bi-box-arrow-right"></i> Cerrar Sesión
        </button>
      </div>
    </div>
  </header>

  <!-- Modal Mi Firma -->
  <div class="modal" :class="{ 'show': mostrarModalFirma }" @click.self="cerrarModalFirma">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Mi Firma y Leyenda</h5>
          <button type="button" class="btn-close" @click="cerrarModalFirma"></button>
        </div>
        <div class="modal-body">
          <p class="fw-semibold mb-1" style="font-size:0.85rem">Imagen de firma</p>
          <div v-if="firmaUrl" class="text-center mb-2">
            <img :src="firmaUrl" alt="Mi firma" style="max-width:100%; max-height:120px; border:1px solid #dee2e6; border-radius:4px; background:#fafafa; padding:8px;">
          </div>
          <div v-else class="text-muted small text-center mb-2">
            No tenés ninguna firma cargada.
          </div>
          <label class="btn btn-outline-primary btn-sm w-100 mb-1">
            <i class="bi bi-upload"></i> {{ firmaUrl ? 'Reemplazar firma' : 'Subir firma (PNG/JPG)' }}
            <input type="file" accept="image/png,image/jpeg" style="display:none;" @change="subirFirma">
          </label>
          <button v-if="firmaUrl" class="btn btn-outline-danger btn-sm w-100 mb-3" @click="eliminarFirma">
            <i class="bi bi-trash"></i> Eliminar firma
          </button>

          <hr class="my-2">

          <p class="fw-semibold mb-1" style="font-size:0.85rem">Leyenda bajo la firma</p>
          <p class="text-muted small mb-2">Texto que aparece debajo de tu firma en los informes firmados.</p>
          <textarea
            v-model="leyendaTexto"
            class="form-control form-control-sm mb-2"
            rows="2"
            placeholder="Ej: Ing. Gustavo Veloso"
            maxlength="200"
          ></textarea>
          <div v-if="leyendaGuardada" class="alert alert-success py-1 small mb-2">Leyenda guardada.</div>
          <div v-if="errorLeyenda" class="alert alert-danger py-1 small mb-2">{{ errorLeyenda }}</div>
          <button class="btn btn-primary btn-sm w-100" :disabled="guardandoLeyenda" @click="guardarLeyenda">
            {{ guardandoLeyenda ? 'Guardando...' : 'Guardar leyenda' }}
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api.js';
import logo from '@/assets/logo_L.png';

export default {
  inheritAttrs: false,
  setup() {
    const router      = useRouter();
    const logoPath    = ref(logo);
    const userLoaded  = ref(false);
    const firstName   = ref('');
    const lastName    = ref('');
    const menuAbierto = ref(false);
    const userMenuRef = ref(null);

    // Firma & leyenda
    const mostrarModalFirma = ref(false);
    const firmaUrl          = ref(null);
    const leyendaTexto      = ref('');
    const guardandoLeyenda  = ref(false);
    const leyendaGuardada   = ref(false);
    const errorLeyenda      = ref('');

    const fullName = computed(() =>
      firstName.value || lastName.value
        ? `${firstName.value} ${lastName.value}`.trim()
        : 'Invitado'
    );

    const loadUserFromSession = () => {
      firstName.value  = sessionStorage.getItem('first_name') || '';
      lastName.value   = sessionStorage.getItem('last_name')  || '';
      userLoaded.value = true;
    };

    // --- Menú desplegable ---
    const toggleMenu = () => { menuAbierto.value = !menuAbierto.value; };

    const handleClickOutside = (e) => {
      if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
        menuAbierto.value = false;
      }
    };

    // --- Firma ---
    const cargarFirma = async () => {
      try {
        const res = await api.get('/auth/firma_usuario/');
        firmaUrl.value = res.data.firma_url || null;
      } catch (_) { /* sin acción */ }
    };

    const cargarLeyenda = async () => {
      try {
        const res = await api.get('/auth/leyenda_usuario/');
        leyendaTexto.value = res.data.leyenda || '';
      } catch (_) { /* sin acción */ }
    };

    const abrirModalFirma = async () => {
      menuAbierto.value = false;
      await Promise.all([cargarFirma(), cargarLeyenda()]);
      leyendaGuardada.value = false;
      errorLeyenda.value    = '';
      mostrarModalFirma.value = true;
    };

    const cerrarModalFirma = () => { mostrarModalFirma.value = false; };

    const subirFirma = async (e) => {
      const archivo = e.target.files[0];
      if (!archivo) return;
      const formData = new FormData();
      formData.append('firma', archivo);
      try {
        const res = await api.post('/auth/firma_usuario/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        firmaUrl.value = res.data.firma_url;
        window.dispatchEvent(new CustomEvent('firma-usuario-actualizada', { detail: { firma_url: res.data.firma_url } }));
      } catch (err) {
        alert('Error al subir la firma: ' + (err.response?.data?.error || err.message));
      }
      e.target.value = '';
    };

    const eliminarFirma = async () => {
      try {
        await api.delete('/auth/firma_usuario/');
        firmaUrl.value = null;
        window.dispatchEvent(new CustomEvent('firma-usuario-actualizada', { detail: { firma_url: null } }));
      } catch (_) { /* sin acción */ }
    };

    const guardarLeyenda = async () => {
      guardandoLeyenda.value = true;
      errorLeyenda.value     = '';
      try {
        await api.post('/auth/leyenda_usuario/', { leyenda: leyendaTexto.value });
        leyendaGuardada.value = true;
        setTimeout(() => { leyendaGuardada.value = false; }, 2500);
      } catch (_) {
        errorLeyenda.value = 'Error al guardar la leyenda.';
      } finally {
        guardandoLeyenda.value = false;
      }
    };

    // --- Perfil ---
    const irAlPerfil = () => {
      menuAbierto.value = false;
      router.push('/perfil');
    };

    const logout = () => {
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('username');
      sessionStorage.removeItem('first_name');
      sessionStorage.removeItem('last_name');
      delete api.defaults.headers.common['Authorization'];
      window.location.href = '/userlogin';
    };

    onMounted(() => {
      loadUserFromSession();
      window.addEventListener('auth-changed', loadUserFromSession);
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      window.removeEventListener('auth-changed', loadUserFromSession);
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      logoPath, fullName, userLoaded,
      menuAbierto, userMenuRef, toggleMenu,
      mostrarModalFirma, firmaUrl,
      abrirModalFirma, cerrarModalFirma, subirFirma, eliminarFirma,
      leyendaTexto, guardandoLeyenda, leyendaGuardada, errorLeyenda, guardarLeyenda,
      irAlPerfil,
      logout,
    };
  }
};
</script>

<style scoped>
.header-container {
  position: fixed;
  top: 0; left: 0;
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
  position: relative;
  display: flex;
  align-items: center;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
  user-select: none;
}
.user-btn:hover { background: rgba(255,255,255,0.15); }

.chev {
  font-size: 12px;
  transition: transform 0.2s;
}
.chev.rotated { transform: rotate(180deg); }

.dropdown-menu-custom {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 170px;
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  z-index: 2000;
  overflow: hidden;
}

.dd-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 16px;
  background: none;
  border: none;
  text-align: left;
  font-size: 0.9rem;
  color: #333;
  cursor: pointer;
  transition: background 0.15s;
}
.dd-item:hover { background: #f0f4f8; }
.dd-divider { height: 1px; background: #dee2e6; margin: 2px 0; }
.dd-logout { color: #dc3545; }
.dd-logout:hover { background: #fff5f5; }

.modal {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.5);
  z-index: 1100;
}
.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
