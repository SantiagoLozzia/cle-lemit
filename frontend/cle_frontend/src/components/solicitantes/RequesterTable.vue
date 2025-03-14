<template>
    <div class="requester-container">
      
      <div class="title-container">  
        <h2>Tabla de solicitantes</h2>
      </div>
  
      <div class="table-container">
        <table class="table requester-table">
          <thead>
            <tr>
              <th class="add-border-right">Nro</th>
              <th class="add-border-right">Solicitante</th>
              <th class="add-border-right">Cuit</th>
              <th class="add-border-right">País</th>
              <th class="add-border-right">Provincia</th>
              <th class="add-border-right">Localidad</th>
              <th class="add-border-right">Dirección</th>
              <th class="add-border-right">Teléfono</th>
              <th class="add-border-right">CP</th>
              <th class="add-border-right">Email</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(solicitante, index) in solicitantes" :key="index">
              <td class="add-border-right">{{ solicitante.nro_solicitante }}</td>
              <td class="text-start add-border-right">{{ solicitante.nombre_solicitante }}</td>
              <td class="add-border-right">{{ solicitante.cuit }}</td>
              <td class="add-border-right">{{ solicitante.pais }}</td>
              <td class="add-border-right">{{ solicitante.provincia }}</td>
              <td class="add-border-right">{{ solicitante.localidad }}</td>
              <td class="add-border-right">{{ solicitante.direccion }}</td>
              <td class="add-border-right">{{ solicitante.telefono }}</td>
              <td class="add-border-right">{{ solicitante.codigoPostal }}</td>
              <td class="text-start add-border-right">{{ solicitante.email }}</td>
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
  
        const solicitantes = ref([]); 
  
        const fetchSolicitantes = async () => {
          try {
            const response = await axios.get(`http://localhost:8000/api/solicitantes/todos/`);
            
            solicitantes.value = response.data;
          } 
          
          catch (error) {
            console.error('Error al obtener solicitantes:', error);
          }
        };
  
        onMounted(fetchSolicitantes); // Utilizamos onMounted para llamar a fetchSolicitantes en la creación del componente
  
        return { 
            solicitantes,
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
  