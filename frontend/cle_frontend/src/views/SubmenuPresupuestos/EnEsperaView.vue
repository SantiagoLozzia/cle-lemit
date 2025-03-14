<template>
  <div>
    <NewBudget :data="budgetData" />
    <EnEsperaTable :data="enesperaData" />
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

</style>
