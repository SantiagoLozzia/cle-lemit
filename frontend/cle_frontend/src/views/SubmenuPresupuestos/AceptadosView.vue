<template>
  <div>
    <AceptadosTable :data="aceptadosData" />
  </div>
</template>

<script>
  import AceptadosTable from '../../components/presupuestos/AceptadosTable.vue';

  export default {
    data() {
      return {
        aceptadosData: []
      };
    },
    components: {
      AceptadosTable
    }
  };
</script>

<style scoped>

</style>
