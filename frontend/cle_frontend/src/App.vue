<template>
  <div>
    <HeaderComponent />
    <HorizontalMenu :user-permissions="userPermissions" />
    <router-view></router-view>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import HeaderComponent from './components/HeaderComponent.vue';
import HorizontalMenu from './components/HorizontalMenu.vue';
// import VueGoodTablePlugin from 'vue-good-table';
// import 'vue-good-table/dist/vue-good-table.css';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    HorizontalMenu,
    // VueGoodTable: VueGoodTablePlugin.VueGoodTable,
  },
  setup() {
    // Estado reactivo
    const userPermissions = ref({
      option1: true,
      option2: false,
      // ... y así sucesivamente
    });

    // Efecto secundario al montar el componente
    onMounted(() => {
      document.title = "Circuito Legajo Electronico";
    });

    // Devolver el estado y los efectos secundarios
    return {
      userPermissions,
    };
  },
};
</script>

<style>
@import "~bootstrap-icons/font/bootstrap-icons.css";

body {
  background-color: #ccc;
  zoom:0.7;
}

.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  align-items: inherit !important;
  margin-bottom: 2rem !important;
  text-align: left !important;
  background-color: rgba(0, 0, 0, 0.5);
  overflow: auto;
}

.modal-header {
  /* background-color: #026290; */
  background-color: white;
  color: black;
  padding: 20px;
}

.modal-logo {
  width: 1000px; /* Ajusta el ancho del logo según sea necesario */
  height: 80px; /* Ajusta la altura del logo según sea necesario */
  background-image: url('@/assets/membrete_lemit.jpeg');
                    /* url('@/assets/logo_cic_modal.png'),  */
                    /* url('@/assets/logo_ministerio_modal.png'), */
                    /* url('@/assets/logo_pba_modal.png'); */
  background-size: contain; 
  background-repeat: no-repeat; 
  background-position: center; 
  margin-right: 10px; /* Espacio entre los logos y el título */
}

.modal-footer-a4 {
  display: flex;
  justify-content: space-between; /* Para separar la imagen de los botones */
  align-items: center; /* Para alinear verticalmente los elementos */
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}

.modal-footer-a4 .footer-image {
  width: 1000px; /* Ajusta el ancho de la imagen según sea necesario */
  height: 80px; /* Ajusta la altura de la imagen según sea necesario */
  background-image: url('@/assets/pie_pagina_lemit.jpeg'); /* Ruta a tu imagen */
  background-size: contain; /* Asegura que la imagen se ajuste dentro del contenedor */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  background-position: center; /* Centra la imagen en el contenedor */
}

.modal-footer-a4 .btn {
  margin-left: 0.5rem;
}

.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog-a4 {
  width: 210mm; /* Ancho de una hoja A4 */
  max-width: 100%; /* Asegúrate de que no exceda el ancho de la ventana */
  height: 297mm; /* Alto de una hoja A4 */
  max-height: 100%; /* Asegúrate de que no exceda el alto de la ventana */
  margin: auto; /* Centrará el modal en la pantalla */
}

.modal-content {
  /* background-color: blue; */
  padding: 1.25rem;
  border: 1px solid #888;
  width: 80%; 
  margin-bottom: 1.875rem; 
  text-align: left;
}

.modal-footer .btn {
  width: 45%; /* Establece el ancho de los botones */
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
