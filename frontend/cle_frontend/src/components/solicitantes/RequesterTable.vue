<template>
  <div class="requester-container">

    <PageHeader
      title="Solicitantes"
      :subtitle="filteredSolicitantes.length + ' empresas'"
      icon="bi bi-people-fill"
    />

    <div class="filter-bar mb-2 d-flex flex-wrap align-items-center gap-2">
      <input
        v-model="filterNombre"
        type="text"
        placeholder="Buscar empresa o CUIT..."
        class="form-control form-control-sm w-auto"
        style="min-width: 200px"
      >
      <select v-model="filterPais" class="form-select form-select-sm w-auto">
        <option value="">Todos los países</option>
        <option v-for="p in uniquePaises" :key="p" :value="p">{{ p }}</option>
      </select>
      <input
        v-model="filterProvincia"
        type="text"
        placeholder="Provincia..."
        class="form-control form-control-sm w-auto"
        style="min-width: 140px"
      >
      <button
        v-if="filterNombre || filterPais || filterProvincia"
        @click="clearFilters"
        class="btn btn-sm btn-outline-secondary"
      >✕ Limpiar</button>
    </div>

    <div class="table-container">
      <table class="table requester-table">
        <thead>
          <tr>
            <th class="add-border-right">Nro</th>
            <th class="add-border-right">Solicitante</th>
            <th class="add-border-right">CUIT</th>
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
          <tr v-for="(solicitante, index) in filteredSolicitantes" :key="index">
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
          <tr v-if="filteredSolicitantes.length === 0">
            <td colspan="10" class="text-center text-muted py-4">No hay resultados para mostrar</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import api from '@/api.js';
import PageHeader from '@/components/PageHeader.vue';

export default {
  components: { PageHeader },
  setup() {
    const solicitantes = ref([]);

    const filterNombre   = ref('');
    const filterPais     = ref('');
    const filterProvincia = ref('');

    const fetchSolicitantes = async () => {
      try {
        const response = await api.get('/solicitantes/todos/');
        solicitantes.value = response.data;
      } catch (error) {
        console.error('Error al obtener solicitantes:', error);
      }
    };

    const uniquePaises = computed(() => {
      const set = new Set(solicitantes.value.map(s => s.pais).filter(Boolean));
      return [...set].sort();
    });

    const filteredSolicitantes = computed(() => {
      return solicitantes.value.filter(s => {
        const nombreOk = !filterNombre.value ||
          s.nombre_solicitante?.toLowerCase().includes(filterNombre.value.toLowerCase()) ||
          String(s.cuit || '').includes(filterNombre.value);
        const paisOk = !filterPais.value || s.pais === filterPais.value;
        const provinciaOk = !filterProvincia.value ||
          s.provincia?.toLowerCase().includes(filterProvincia.value.toLowerCase());
        return nombreOk && paisOk && provinciaOk;
      });
    });

    const clearFilters = () => {
      filterNombre.value   = '';
      filterPais.value     = '';
      filterProvincia.value = '';
    };

    onMounted(() => {
      fetchSolicitantes();
      document.addEventListener('solicitantes-refresh', fetchSolicitantes);
    });

    onUnmounted(() => {
      document.removeEventListener('solicitantes-refresh', fetchSolicitantes);
    });

    return {
      solicitantes,
      filterNombre, filterPais, filterProvincia,
      uniquePaises, filteredSolicitantes, clearFilters,
    };
  }
};
</script>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
}

.requester-table {
  width: 100%;
  min-width: 800px;
}

.add-border-right {
  border-right: 1px solid gainsboro;
}

.filter-bar {
  margin-bottom: 8px;
}
</style>
