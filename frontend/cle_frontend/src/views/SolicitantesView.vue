<template>
  <div>
    <NewRequester v-if="esAdministracion" />
    <RequesterTable />
  </div>
</template>

<script>
import { computed } from 'vue';
import NewRequester from '../components/solicitantes/NewRequester.vue';
import RequesterTable from '../components/solicitantes/RequesterTable.vue';

export default {
  components: { NewRequester, RequesterTable },
  setup() {
    const esAdministracion = computed(() => sessionStorage.getItem('role') === 'administracion');
    return { esAdministracion };
  }
};
</script>
