<template>
  <div>
    <ArancelesTable :data="arancelesData" />
    <!-- Otros componentes específicos de esta vista -->
  </div>
</template>

<script>
import ArancelesTable from '../components/servicios/ServiciosTable.vue';

export default {
  data() {
    return {
      arancelesData: [] // Puedes cargar datos específicos de esta vista aquí
    };
  },
  components: {
    ArancelesTable
    // Otros componentes específicos de esta vista
  }
};
</script>

<style>
.body {
  background-color: red;
}
</style>
