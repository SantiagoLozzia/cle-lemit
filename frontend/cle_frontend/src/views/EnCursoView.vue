<template>
  <div class="container">
    <div class="button-container">
      <!-- Mostrar el componente NewCircuit solo si canSeeButton es verdadero -->
      <NewCircuit v-if="canSeeButton" :data="circuitData" />
    </div>
    <div class="table-container">
      <ProgressTable :data="progressData"/>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import NewCircuit from '../components/encurso/NewCircuit';
import ProgressTable from '../components/encurso/ProgressTable';

export default {
  components: {
    NewCircuit,
    ProgressTable
  },
  setup() {
    const circuitData = ref([]);
    const progressData = ref([]);
    const canSeeButton = ref(false);

    onMounted(() => {
      // Obtener el rol del usuario y establecer canSeeButton
      const userRole = sessionStorage.getItem('role');
      canSeeButton.value = userRole === 'servicios_tecnologicos';
    });

    return {
      circuitData,
      progressData,
      canSeeButton
    };
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-left: 0;
  max-width: 100%;
  padding: 0;
  /* Ocupa exactamente lo que queda del viewport tras el navbar fijo,
     sin generar scroll de página que haría que el navbar tape el botón */
  height: calc(100vh - 150px); /* 130px margin-top + 20px padding del content-wrapper */
  overflow: hidden;
}

.button-container {
  flex-shrink: 0;
}

.table-container {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
