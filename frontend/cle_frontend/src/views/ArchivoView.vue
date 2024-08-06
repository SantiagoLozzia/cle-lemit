<template>
  <div>
    <ArchivedCircuits :data="moduloData" />
  </div>
</template>

<script>
  import ArchivedCircuits from '../components/archivo/ArchivedCircuits.vue';
  

  export default {
    data() {
      return {
        ArchivedCircuits,
      };
    },
    components: {
      ArchivedCircuits,
    }
  };
</script>
  
<style scoped>

</style>
  