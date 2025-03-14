<template>
  <div>
    <NewCircuit :data="circuitData" />
    <ProgressTable :data="progressData"/>
  </div>
</template>

<script>
import NewCircuit from '../components/encurso/NewCircuit';
import ProgressTable from '../components/encurso/ProgressTable';

export default {
  data() {
    return {
      circuitData: [],
      progressData: []
    };
  },
  components: {
    NewCircuit,
    ProgressTable
  }
};
</script>

<style scoped>
.body {
  background-color: red;
}
</style>
