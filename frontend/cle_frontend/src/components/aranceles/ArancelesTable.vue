<template>
  <div class="aranceles-container">
    <div class="table-container">
      <table class="table aranceles-table">
        <thead>
          <tr>
            <th class="add-border-right">Nro</th>
            <th class="add-border-right">Servicio</th>
            <th class="add-border-right">Norma</th>
            <th class="add-border-right">Valor</th>
            <th class="add-border-right">Area Tematica</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in aranceles" :key="index">
            <td class="add-border-right">{{ arancel.nro_servicio }}</td>
            <td class="text-start add-border-right">{{ arancel.servicio }}</td>
            <td class="add-border-right">{{ arancel.norma }}</td>
            <td class="add-border-right">{{ arancel.arancel }}</td>
            <td class="add-border-right">{{ formatAreaTematica(arancel.area_tematica) }}</td>
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

      

      const aranceles = ref([]); 

      const fetchAranceles = async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/aranceles/todos/`);
          
          aranceles.value = response.data; // Actualizamos aranceles.value
        } 
        
        catch (error) {
          console.error('Error al obtener aranceles:', error);
        }
      };

      // Función para formatear el campo area_tematica
      const formatAreaTematica = (areaTematica) => {
        return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      };

      onMounted(fetchAranceles); // Utilizamos onMounted para llamar a fetchAranceles en la creación del componente

      return { 
        aranceles,
        formatAreaTematica,
      };
    }
  };
</script>

<style scoped>

.modulo {
  position: fixed; /* Establece la posición fija para que permanezca en la misma ubicación incluso al desplazarse */
  left: 10px; /* Lo sitúa en el extremo izquierdo de la pantalla */
  transform: translateY(120%); /* Centra verticalmente el elemento */
}

.table-container {
  width: 100%;
  overflow-x: auto;
  margin: 0;
}

.aranceles-table {
  width: 100%;
  border-collapse: collapse;
}

.add-border-right {
  border-right: 1px solid gainsboro; /* Establece el borde derecho */
}
</style>
