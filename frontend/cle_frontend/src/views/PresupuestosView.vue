<template>
  <div>
    <NewBudget :data="budgetData" />
  </div>
</template>


<script>
import NewBudget from '../components/presupuestos/NewBudget.vue';


export default {
  data() {
    return {
      budgetData: [], 
    };
  },
  components: {
    NewBudget,
  }
};
</script>

<style>

</style>
