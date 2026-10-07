<template>
  <div class="aranceles-container">
    <div class="table-container">
      <table class="table aranceles-table">
        <colgroup>
          <col class="col-nro">
          <col class="col-servicio">
          <col class="col-norma">
          <col class="col-valor">
          <col class="col-area">
        </colgroup>
        <thead>
          <tr>
            <th class="add-border-right">Nro</th>
            <th class="add-border-right text-start">Servicio</th>
            <th class="add-border-right">Norma</th>
            <th class="add-border-right">Valor</th>
            <th class="add-border-right">Area Tematica</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in data" :key="index">
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
export default {
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  setup() {
    const formatAreaTematica = (areaTematica) => {
      return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    };

    return {
      formatAreaTematica
    };
  }
};
</script>

<style scoped>
.modulo {
  position: fixed;
  left: 10px;
  transform: translateY(120%);
}

.table-container {
  width: 100%;
  overflow-x: auto;
  margin: 0;
}

.aranceles-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}

.aranceles-table td,
.aranceles-table th {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.col-nro     { width: 70px; }
.col-norma   { width: 160px; }
.col-valor   { width: 90px; }
.col-area    { width: 22%; }
/* col-servicio toma el espacio restante */

.add-border-right {
  border-right: 1px solid gainsboro;
}
</style>
