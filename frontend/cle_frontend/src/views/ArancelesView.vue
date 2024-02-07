<template>
    <div>
      <NewService :data="servicioData" />
      <ArancelesTable :data="arancelesData" />
    </div>
</template>
  

<script>
  import NewService from '../components/aranceles/NewService.vue';
  import ArancelesTable from '../components/aranceles/ArancelesTable.vue';
  

  export default {
    data() {
      return {
        servicioData: [], 
        arancelesData: [] 
      };
    },
    components: {
      NewService,
      ArancelesTable,
    }
  };
</script>
  
<style>

</style>
  