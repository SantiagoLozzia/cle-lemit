<template>
  <div>
    <CanceladosTable :data="canceladosData" />
  </div>
</template>

<script>
  import CanceladosTable from '../../components/presupuestos/CanceladosTable.vue';

  export default {
    data() {
      return {
        canceladosData: []
      };
    },
    components: {
      CanceladosTable
    }
  };
</script>

<style scoped>

</style>
