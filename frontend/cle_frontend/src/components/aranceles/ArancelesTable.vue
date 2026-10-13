<template>
  <div class="aranceles-container">
    <div class="table-container">
      <div class="filter-bar mb-2 d-flex align-items-center gap-2">
        <select v-model="filterArea" class="form-select form-select-sm w-auto">
          <option value="">Todas las áreas</option>
          <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
        </select>
        <button v-if="filterArea" @click="clearFilter" class="btn btn-sm btn-outline-secondary">✕ Limpiar</button>
      </div>
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
            <th class="add-border-right sortable" @click="setSort('nro_servicio')">Nro <span class="sort-icon">{{ sortKey === 'nro_servicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="add-border-right text-start">Servicio</th>
            <th class="add-border-right">Norma</th>
            <th class="add-border-right sortable" @click="setSort('arancel')">Valor <span class="sort-icon">{{ sortKey === 'arancel' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th class="add-border-right">Area Tematica</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in sortedData" :key="index">
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
import { ref, computed } from 'vue';
import { AREAS_TEMATICAS } from '@/constants/areas.js';

export default {
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const sortKey = ref('');
    const sortDir = ref('asc');
    const sortedData = computed(() => {
      if (!sortKey.value) return filteredData.value;
      return [...filteredData.value].sort((a, b) => {
        const valA = Number.isFinite(Number(a[sortKey.value])) && sortKey.value !== 'norma'
          ? Number(a[sortKey.value]) : a[sortKey.value];
        const valB = Number.isFinite(Number(b[sortKey.value])) && sortKey.value !== 'norma'
          ? Number(b[sortKey.value]) : b[sortKey.value];
        if (valA < valB) return sortDir.value === 'asc' ? -1 : 1;
        if (valA > valB) return sortDir.value === 'asc' ? 1 : -1;
        return 0;
      });
    });
    const setSort = (key) => {
      if (sortKey.value === key) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
      else { sortKey.value = key; sortDir.value = 'asc'; }
    };

    const filterArea = ref('');
    const uniqueAreas = AREAS_TEMATICAS;
    const filteredData = computed(() =>
      !filterArea.value ? props.data : props.data.filter(a => formatAreaTematica(a.area_tematica) === filterArea.value)
    );
    const clearFilter = () => { filterArea.value = ''; };

    const formatAreaTematica = (areaTematica) => {
      return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    };

    return {
      sortKey, sortDir, sortedData, setSort,
      filterArea, uniqueAreas, clearFilter,
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
