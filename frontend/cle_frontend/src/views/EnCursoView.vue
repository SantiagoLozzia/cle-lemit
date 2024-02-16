<template>
  <div>
    <ArancelesTable :data="arancelesData" />
  </div>
</template>

<script>
import ArancelesTable from '../components/aranceles/ArancelesTable.vue';

export default {
  data() {
    return {
      arancelesData: []
    };
  },
  components: {
    ArancelesTable
  }
};
</script>

<style scoped>
.body {
  background-color: red;
}
</style>
