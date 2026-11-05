<template>
  <div class="container">
    <HistorialTable />
  </div>
</template>

<script>
import HistorialTable from '../../components/presupuestos/HistorialTable.vue';

export default {
  components: { HistorialTable },
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
