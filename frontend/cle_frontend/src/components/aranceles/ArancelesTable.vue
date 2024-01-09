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
              <th>Arancel</th>
              <th>Area Tematica</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(arancel, index) in aranceles" :key="index">
              <td>{{ arancel.nro }}</td>
              <td>{{ arancel.servicio }}</td>
              <td>{{ arancel.arancel }}</td>
              <td>{{ arancel.areaTematica }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        aranceles: [
          { nro: 1, servicio: 'Servicio A', arancel: 'ValorA', areaTematica: 'Area 1' },
          { nro: 2, servicio: 'Servicio B', arancel: 'ValorB', areaTematica: 'Area 2' },
        ],
        showSuccessAlert: false,
      };
    },
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
