<template>
  <div>
    <NewCircuit :data="circuitData" />
    <ArancelesTable :data="arancelesData" />
  </div>
</template>

<script>
import NewCircuit from '../components/encurso/NewCircuit';
import ArancelesTable from '../components/aranceles/ArancelesTable.vue';

export default {
  data() {
    return {
      circuitData: [],
      arancelesData: []
    };
  },
  components: {
    NewCircuit,
    ArancelesTable
  }
};
</script>

<style scoped>
.body {
  background-color: red;
}
</style>
