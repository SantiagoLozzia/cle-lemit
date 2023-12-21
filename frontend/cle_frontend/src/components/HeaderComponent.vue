<template>
    <header class="header-container">
      <div class="logo-container">
        <!-- Asegúrate de ajustar la ruta del logo -->
        <img alt="Logo" src="../assets/logo_L.png" class="logo">
      </div>
      <!-- Otros elementos del encabezado, como el título, menú, etc. -->
    </header>
  </template>
  
  <script>
  export default {
    // Datos y métodos de tu componente Header
  };
  </script>
  
  <style scoped>
  .header-container {
    background-color: #026290;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .logo {
    width: 40px; /* Ajusta el tamaño del logo según tus necesidades */
  }
  
  </style>  