<template>
  <div>
    <HeaderComponent />
    <HorizontalMenu :user-permissions="userPermissions" />
    <router-view></router-view>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import HeaderComponent from './components/HeaderComponent.vue';
import HorizontalMenu from './components/HorizontalMenu.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    HorizontalMenu,
  },
  setup() {
    // Estado reactivo
    const userPermissions = ref({
      option1: true,
      option2: false,
      // ... y así sucesivamente
    });

    // Efecto secundario al montar el componente
    onMounted(() => {
      document.title = "Circuito Legajo Electronico";
    });

    // Devolver el estado y los efectos secundarios
    return {
      userPermissions,
    };
  },
};
</script>

<style>
@import "~bootstrap-icons/font/bootstrap-icons.css";

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
