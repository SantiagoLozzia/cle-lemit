<template>
  <div class="container">
    <div class="button-container">
      <NewBudget :data="budgetData" />
    </div>
    <div class="table-container">
    <EnEsperaTable :data="enesperaData" />
    </div>
  </div>
</template>

<script>
  import NewBudget from '../../components/presupuestos/NewBudget.vue';
  import EnEsperaTable from '../../components/presupuestos/EnEsperaTable.vue';

  export default {
    data() {
      return {
        budgetData: [],
        enesperaData: []
      };
    },
    components: {
      NewBudget,
      EnEsperaTable,
    }
  };
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    gap: 20px; /* Controla el espacio entre los elementos */
    margin-left: 0;
  }
</style>
