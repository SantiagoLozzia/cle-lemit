<template>
  <div>
    <NewRequester :data="requesterData" />
  </div>
</template>

<script>
import NewRequester from '../components/solicitantes/NewRequester.vue';

export default {
  data() {
    return {
      requesterData: [], 
    };
  },
  components: {
    NewRequester,
  }
};
</script>

<style scoped> 

</style>
