<template>
  <div>
    <HeaderComponent />
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

</style>
