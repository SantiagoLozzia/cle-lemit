<template>
    <div class="archivo-container">
      
      <div class="title-container">  
        <h2>Archivados</h2>
      </div>
  
      <div class="table-container">
        <table class="table archivo-table">
          <thead>
            <tr>
              <th class="add-border-right">Nro Legajo</th>
              <th class="add-border-right">Operaciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(finalizado, index) in finalizados" :key="index">
              <td class="add-border-right">{{ finalizado.nro_legajo }}</td>
              <td class="text-start add-border-right">{{ finalizado.servicio }}</td>
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
  
        
  
        const finalizados = ref([]); 
  
        const fetchFinalizados = async () => {
          try {
            const response = await axios.get(`http://localhost:8000/api/archivo/finalizados/`);
            
            finalizados.value = response.data; // Actualizamos archivados.value
          } 
          
          catch (error) {
            console.error('Error al obtener circuitos finalizados:', error);
          }
        };
  
        // Función para formatear el campo area_tematica
        const formatAreaTematica = (areaTematica) => {
          return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        };
  
        onMounted(fetchFinalizados); // Utilizamos onMounted para llamar a fetchFinalizados en la creación del componente
  
        return { 
          finalizados,
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
  .title-container {
    position: relative;
    top: 50px;
  }
  .table-container {
    margin-top: 80px;
  }
  
  .add-border-right {
    border-right: 1px solid gainsboro; /* Establece el borde derecho */
  }
  </style>
  