<template>
  <div>
    <NewRequester :data="requesterData" />
    <RequesterTable :data="requesterData" />
  </div>
</template>

<script>
import NewRequester from '../components/solicitantes/NewRequester.vue';
import RequesterTable from '../components/solicitantes/RequesterTable.vue';

export default {
  data() {
    return {
      requesterData: [],
      RequesterTable: [],
    };
  },
  components: {
    NewRequester,
    RequesterTable,
  }
};
</script>

<style scoped> 

</style>
