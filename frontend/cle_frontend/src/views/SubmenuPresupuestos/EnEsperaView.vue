<template>
  <div class="container">
    <EnEsperaTable />
  </div>
</template>

<script>
  import EnEsperaTable from '../../components/presupuestos/EnEsperaTable.vue';

  export default {
    components: { EnEsperaTable },
  };
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-left: 0;
    max-width: 100%;
    padding: 0;
  }
</style>
