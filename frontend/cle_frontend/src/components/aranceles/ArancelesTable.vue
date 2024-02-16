<template>
  <div class="aranceles-container">
    
    <div class="title-container">  
      <h2>Tabla de Aranceles</h2>
    </div>

    <div class="table-container">
      <table class="table aranceles-table">
        <thead>
          <tr>
            <th>Nro</th>
            <th>Servicio</th>
            <th>Norma</th>
            <th>Arancel</th>
            <th>Area Tematica</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in aranceles" :key="index">
            <td>{{ arancel.nro_servicio }}</td>
            <td>{{ arancel.servicio }}</td>
            <td>{{ arancel.norma }}</td>
            <td>{{ arancel.arancel }}</td>
            <td>{{ arancel.area_tematica }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>

  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
      const aranceles = ref([]); // Utilizamos ref para aranceles

      const fetchAranceles = async () => {
        try {
          const response = await axios.get('api/aranceles/todos/');
          aranceles.value = response.data; // Actualizamos aranceles.value
        } 
        
        catch (error) {
          console.error('Error al obtener aranceles:', error);
        }
      };

      onMounted(fetchAranceles); // Utilizamos onMounted para llamar a fetchAranceles en la creación del componente

      return { aranceles }; // Devolvemos aranceles para usarlo en el template
    }
  };
</script>

<style scoped>
.title-container {
  position: relative;
  top: 50px;
}
.table-container {
  margin-top: 80px;
}
</style>
