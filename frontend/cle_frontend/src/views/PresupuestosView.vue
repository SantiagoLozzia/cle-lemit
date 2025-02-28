<template>
  <div class="container-submenu">
    <SubMenu :user-permissions="userPermissions" />
    <router-view></router-view>
  </div>
</template>

<script>
  import SubMenu from '../components/presupuestos/SubMenu.vue';


  export default {
    data() {
      return {
          
      };
    },
    components: {
      SubMenu,
    }
  };
</script>

<style scoped>
  .container-submenu {
    display: flex;
    flex-direction: column;
    gap: 20px; /* Controla el espacio entre los elementos */
    margin-left: 120;
  }
</style>
