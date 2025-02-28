<template>
  <div id="app">
    <nav>
      <router-link to="/encurso" class="router-link-item" :class="{ active: isRouteActive('/encurso') || isRouteActive('/') }">
        <div @click="navigateTo('EnCurso')">En Curso</div>
      </router-link>
      <router-link v-if="!isRoleRestricted" to="/aranceles" class="router-link-item" :class="{ active: isRouteActive('/aranceles') }">
        <div @click="navigateTo('Aranceles')">Aranceles</div>
      </router-link>
      <router-link v-if="!isRoleRestricted" to="/presupuestos" class="router-link-item" :class="{ active: isRouteActive('/presupuestos') }">
        <div @click="navigateTo('Presupuestos')">Presupuestos</div>
      </router-link>
      <router-link v-if="!isRoleRestricted" to="/archivo" class="router-link-item" :class="{ active: isRouteActive('/archivo') }">
        <div @click="navigateTo('Archivo')">Archivo</div>
      </router-link>
      <router-link v-if="!isRoleRestricted" to="/solicitantes" class="router-link-item" :class="{ active: isRouteActive('/solicitantes') }">
        <div @click="navigateTo('Solicitantes')">Solicitantes</div>
      </router-link>
    </nav>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

export default {
  setup() {
    const $route = useRoute();
    const $router = useRouter();

    const userRole = sessionStorage.getItem('role'); // Obtener el rol del usuario desde sessionStorage

    const isRoleRestricted = computed(() => {
      return userRole === 'area_jefe' || userRole === 'area_standard';
    });

    const isRouteActive = (route) => {
      return $route.matched.some(record => record.path === route);
    };

    const navigateTo = (item) => {
      if ($route.path !== '/' + item.toLowerCase()) {
        $router.push('/' + item.toLowerCase());
      }
    };

    return {
      isRouteActive,
      navigateTo,
      isRoleRestricted
    };
  }
};
</script>

<style scoped>
nav {
  background-color: #fff;
  border-bottom: 1px solid #ccc;
  display: flex;
  width: 100%;
  position: relative;
  z-index: 999;
}

.router-link-item {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.router-link-item a {
  text-decoration: none;
}

.router-link-item div {
  color: #026290;
  padding: 10px;
  display: block;
  cursor: pointer;
  margin: 0 10px;
}

.router-link-item div:hover {
  color: #fff;
  background-color: #026290;
}

.active div {
  color: #fff;
  background-color: #026290;
}

.router-link-item a.router-link-exact-active {
  text-decoration: none !important;
}

a {
  color: transparent;
}
</style>
