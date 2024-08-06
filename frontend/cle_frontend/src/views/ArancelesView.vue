<template>
  <div>
    <UpdateModule :data="moduloData" />

    <NewService :data="servicioData" />
    
    <ArancelesTable :data="arancelesData" />

  </div>
</template>

<script>
  import UpdateModule from '../components/aranceles/UpdateModule.vue';
  import ArancelesTable from '../components/aranceles/ArancelesTable.vue';
  import NewService from '../components/aranceles/NewService.vue';
  
  

  export default {
    data() {
      return {
        UpdateModule,
        servicioData: [], 
        arancelesData: [],
      };
    },
    components: {
      UpdateModule,
      NewService,
      ArancelesTable,
    }
  };
</script>
  
<style scoped>

</style>
  