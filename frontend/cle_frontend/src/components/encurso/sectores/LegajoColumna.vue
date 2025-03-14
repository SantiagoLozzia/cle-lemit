<template>
    <div>
      <p v-for="subcolumna in subcolumnas">{{ subcolumna }}</p>
      <!-- Aquí puedes usar v-for para iterar sobre los datos y mostrarlos en la columna -->
    </div>
</template>
  
<script>
  export default {
    props: {
      subcolumnas: Array
    },
  };
</script>
  
<style scoped>
  /* Estilos específicos para tu componente */
</style>
  