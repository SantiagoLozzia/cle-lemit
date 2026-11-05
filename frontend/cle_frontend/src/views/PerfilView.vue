<template>
  <div class="perfil-page">
    <div class="perfil-header">
      <button class="btn btn-link back-btn" @click="$router.back()">
        <i class="bi bi-arrow-left"></i> Volver
      </button>
      <h4 class="mb-0">Mi Perfil</h4>
    </div>

    <div class="perfil-body">

      <!-- Datos personales -->
      <div class="perfil-card">
        <h6 class="section-title"><i class="bi bi-person-fill me-2"></i>Datos personales</h6>
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Nombre</label>
            <input v-model="perfilNombre" class="form-control" placeholder="Nombre">
          </div>
          <div class="col-md-6">
            <label class="form-label">Apellido</label>
            <input v-model="perfilApellido" class="form-control" placeholder="Apellido">
          </div>
          <div class="col-12">
            <label class="form-label">Email</label>
            <input v-model="perfilEmail" type="email" class="form-control" placeholder="tu@email.com">
          </div>
          <div class="col-12">
            <label class="form-label text-muted">Usuario</label>
            <input :value="perfilUsername" class="form-control" disabled>
            <div class="form-text">El nombre de usuario no se puede cambiar.</div>
          </div>
        </div>
        <div v-if="perfilOk" class="alert alert-success py-2 small mt-3 mb-0">Datos actualizados correctamente.</div>
        <div v-if="perfilError" class="alert alert-danger py-2 small mt-3 mb-0">{{ perfilError }}</div>
        <div class="mt-3 text-end">
          <button class="btn btn-primary" :disabled="guardandoPerfil" @click="guardarPerfil">
            <span v-if="guardandoPerfil" class="spinner-border spinner-border-sm me-1"></span>
            Guardar datos
          </button>
        </div>
      </div>

      <!-- Cambiar contraseña -->
      <div class="perfil-card">
        <h6 class="section-title"><i class="bi bi-shield-lock-fill me-2"></i>Cambiar contraseña</h6>
        <div class="row g-3">
          <div class="col-12">
            <label class="form-label">Contraseña actual</label>
            <input v-model="pwActual" type="password" class="form-control" placeholder="Contraseña actual">
          </div>
          <div class="col-md-6">
            <label class="form-label">Nueva contraseña</label>
            <input v-model="pwNueva" type="password" class="form-control" placeholder="Mínimo 8 caracteres">
          </div>
          <div class="col-md-6">
            <label class="form-label">Confirmar</label>
            <input v-model="pwConfirmar" type="password" class="form-control" placeholder="Repetir nueva contraseña">
          </div>
        </div>
        <div v-if="pwOk" class="alert alert-success py-2 small mt-3 mb-0">Contraseña actualizada.</div>
        <div v-if="pwError" class="alert alert-danger py-2 small mt-3 mb-0">{{ pwError }}</div>
        <div class="mt-3 text-end">
          <button class="btn btn-outline-primary" :disabled="guardandoPw" @click="cambiarPassword">
            <span v-if="guardandoPw" class="spinner-border spinner-border-sm me-1"></span>
            Cambiar contraseña
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api.js';

const perfilUsername = ref('');
const perfilNombre   = ref('');
const perfilApellido = ref('');
const perfilEmail    = ref('');
const guardandoPerfil = ref(false);
const perfilOk        = ref(false);
const perfilError     = ref('');

const pwActual    = ref('');
const pwNueva     = ref('');
const pwConfirmar = ref('');
const guardandoPw = ref(false);
const pwOk        = ref(false);
const pwError     = ref('');

onMounted(async () => {
  try {
    const res = await api.get('/auth/perfil/');
    perfilUsername.value = res.data.username    || '';
    perfilNombre.value   = res.data.first_name  || '';
    perfilApellido.value = res.data.last_name   || '';
    perfilEmail.value    = res.data.email        || '';
  } catch (_) {
    perfilUsername.value = sessionStorage.getItem('username')   || '';
    perfilNombre.value   = sessionStorage.getItem('first_name') || '';
    perfilApellido.value = sessionStorage.getItem('last_name')  || '';
  }
});

const guardarPerfil = async () => {
  guardandoPerfil.value = true;
  perfilOk.value        = false;
  perfilError.value     = '';
  try {
    const res = await api.put('/auth/perfil/', {
      first_name: perfilNombre.value.trim(),
      last_name:  perfilApellido.value.trim(),
      email:      perfilEmail.value.trim(),
    });
    sessionStorage.setItem('first_name', res.data.first_name);
    sessionStorage.setItem('last_name',  res.data.last_name);
    window.dispatchEvent(new CustomEvent('auth-changed'));
    perfilOk.value = true;
    setTimeout(() => { perfilOk.value = false; }, 3000);
  } catch (err) {
    perfilError.value = err.response?.data?.error || 'Error al guardar.';
  } finally {
    guardandoPerfil.value = false;
  }
};

const cambiarPassword = async () => {
  pwOk.value    = false;
  pwError.value = '';
  if (!pwActual.value || !pwNueva.value || !pwConfirmar.value) {
    pwError.value = 'Completá todos los campos.';
    return;
  }
  if (pwNueva.value !== pwConfirmar.value) {
    pwError.value = 'Las contraseñas no coinciden.';
    return;
  }
  if (pwNueva.value.length < 8) {
    pwError.value = 'La nueva contraseña debe tener al menos 8 caracteres.';
    return;
  }
  guardandoPw.value = true;
  try {
    await api.post('/auth/change_password/', {
      current_password: pwActual.value,
      new_password:     pwNueva.value,
    });
    pwOk.value        = true;
    pwActual.value    = '';
    pwNueva.value     = '';
    pwConfirmar.value = '';
    setTimeout(() => { pwOk.value = false; }, 3000);
  } catch (err) {
    pwError.value = err.response?.data?.error || 'Error al cambiar contraseña.';
  } finally {
    guardandoPw.value = false;
  }
};
</script>

<style scoped>
.perfil-page {
  padding-top: 70px;
  min-height: 100vh;
  background: #f4f6f9;
}

.perfil-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 32px 10px;
  background: #fff;
  border-bottom: 1px solid #dee2e6;
}

.perfil-header h4 { color: #026290; }

.back-btn {
  color: #026290;
  padding: 0;
  font-size: 0.95rem;
  text-decoration: none;
}
.back-btn:hover { color: #014f73; }

.perfil-body {
  max-width: 700px;
  margin: 32px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.perfil-card {
  background: #fff;
  border-radius: 10px;
  border: 1px solid #dee2e6;
  padding: 28px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.section-title {
  color: #026290;
  font-weight: 600;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9ecef;
}
</style>
