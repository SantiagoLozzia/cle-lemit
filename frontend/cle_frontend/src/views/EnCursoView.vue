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
  gap: 20px; /* Controla el espacio entre los elementos */
  margin-left: 0;
}
</style>
