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

import axios from 'axios';

export default {
  data() {
    return {
      aranceles: [] // Inicialmente vacío
    };
  },
  created() {
    // Escuchar el evento emitido por NewService.vue
    //const actualizarArancelesUnaVez = () => {
      //console.log('Evento recibido en ArancelesTable.vue'); // Agregar este console.log
      //this.actualizarAranceles();
      //this.$root.$off('nuevo-servicio-agregado', actualizarArancelesUnaVez);
    //};

    //this.$root.$on('nuevo-servicio-agregado', actualizarArancelesUnaVez);
    this.fetchAranceles();
  },
  methods: {
    async fetchAranceles() {
      try {
        // Realizar una solicitud HTTP utilizando Axios
        const response = await axios.get('api/aranceles/todos/');
        this.aranceles = response.data; // Asignar los aranceles obtenidos a la variable aranceles
      } catch (error) {
        console.error('Error al obtener aranceles:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Ajuste de la posición vertical del título */
.title-container {
  position: relative;
  top: 50px;
}

/* Espaciado entre el título y la tabla */
.table-container {
  margin-top: 80px;
}
</style>
