<template>
    <div id="app">
      <nav>
        <router-link to="/presupuestos/enespera" class="router-link-item" :class="{ active: isRouteActive('/presupuestos/enespera') || isRouteActive('/') }">
          <div @click="navigateTo('EnCurso')">En Espera</div>
        </router-link>
        <router-link to="/presupuestos/aceptados" class="router-link-item" :class="{ active: isRouteActive('/presupuestos/aceptados') }">
          <div @click="navigateTo('Aceptados')">Aceptados</div>
        </router-link>
        <router-link to="/presupuestos/cancelados" class="router-link-item" :class="{ active: isRouteActive('/presupuestos/cancelados') }">
          <div @click="navigateTo('Cancelados')">Cancelados</div>
        </router-link>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      navigateTo(item) {
        // Cambiar la ruta solo si no está ya en la página correspondiente
        if (this.$route.path !== '/' + item.toLowerCase()) {
          this.$router.push('/' + item.toLowerCase());
        }
      },
      isRouteActive(route) {
        return this.$route.matched.some(record => record.path === route);
      },
    },
  };
  </script>
  
  <style scoped>
  nav {
    background-color: #fff;
    border-bottom: 1px solid #ccc;
    display: flex;
  }
  
  .router-link-item {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .router-link-item a {
    text-decoration: none; /* Quitamos el subrayado de todos los enlaces router-link */
  }
  
  .router-link-item div {
    color: #026290;
    padding: 10px;
    display: block;
    cursor: pointer;
    margin: 0 10px; /* Agregamos margen para separar las opciones */
  }
  
  .router-link-item div:hover {
    color: #fff;
    background-color: #026290;
    text-decoration: none; /* Quitamos el subrayado al pasar el mouse sobre él */
  }
  
  .active div {
    color: #fff;
    background-color: #026290;
    text-decoration: none; /* Quitamos el subrayado cuando está activo */
  }
  
  /* Sobrescribimos el estilo del enlace en específico */
  .router-link-item a.router-link-exact-active {
    text-decoration: none !important;
  }
  </style>