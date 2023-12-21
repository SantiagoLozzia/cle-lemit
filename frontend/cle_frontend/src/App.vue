<template>
  <div>
    <HeaderComponent />
    <HorizontalMenu :user-permissions="userPermissions" />
    <router-view></router-view>
  </div>
</template>

<script>
import HeaderComponent from './components/HeaderComponent.vue';
import HorizontalMenu from './components/HorizontalMenu.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    HorizontalMenu,
  },
  data() {
    return {
      userPermissions: {
        option1: true,
        option2: false,
        // ... y así sucesivamente
      },
    };
  },
  created() {
    // Cambiar el título de la página
    document.title = "Circuito Legajo Electronico";
  },
};
</script>

<style>
body {
  background-color: #ccc;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
