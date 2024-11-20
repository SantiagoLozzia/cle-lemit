<template>
  <div class="container">
    <div class="button-module">
      <UpdateModule :data="moduloData" />
    </div>
    <div class="button-new-service">
      <NewService :data="servicioData" />
    </div>
    <div class="table-container">
      <ArancelesTable :data="arancelesData" />
    </div>
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

  .container {
    display: flex;
    flex-direction: column;
    gap: 20px; /* Controla el espacio entre los elementos */
    width: 100%; 
    padding: 0; 
    margin: 0;
  }

  .button-new-service {
    margin-left: 0;
  }
</style>
  