<template>
  <div class="aranceles-container">
    <button class="btn-nuevo-arancel">Nuevo +</button>
    <h2>Tabla de Aranceles</h2>
    <table class="aranceles-table">
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
</template>

<script>
export default {
  data() {
    return {
      aranceles: [
        { nro: 1, servicio: 'Servicio A', arancel: 'ValorA', areaTematica: 'Area 1' },
        { nro: 2, servicio: 'Servicio B', arancel: 'ValorB', areaTematica: 'Area 2' },
      ],
    };
  },
};
</script>

<style scoped>
.aranceles-container {
  background-color: white; 
  padding: 2px; 
  position: relative;
}

.btn-nuevo-arancel {
  position: absolute;
  left: 10px; 
  top: 10px; 
  background-color: #026290; 
  color: white; 
  padding: 10px 15px; 
  font-size: 16px; 
  border: none; 
  cursor: pointer; 
}

.aranceles-table {
  width: 100%; 
  border-collapse: collapse;
  margin-top: 20px; 
}

</style>
