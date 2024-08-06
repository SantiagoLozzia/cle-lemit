<template>
    <header class="header-container">
      <div class="logo-container">
        <img alt="Logo" :src="logoPath" class="logo">
      </div>
    </header>
</template>
  
<script>
  import logo from '@/assets/logo_L.png';
  
  export default {
    data() {
      return {
        logoPath: logo
      };
    }
  };
</script>
  
<style scoped>
 .header-container {
   background-color: #026290;
   padding: 10px;
   display: flex;
   justify-content: space-between;
   align-items: center;
   width: 160%;
  }
  
  .logo {
    width: 40px; /* Ajusta el tamaño del logo según tus necesidades */
  }
  
</style>  