<template>
  <div>
    <template v-if="!isLoginPage">
      <HeaderComponent class="header-fixed" />
      <HorizontalMenu :user-permissions="userPermissions" class="menu-fixed" />
    </template>
    <div :class="isLoginPage ? '' : 'content-wrapper'">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import HeaderComponent from './components/HeaderComponent.vue';
import HorizontalMenu from './components/HorizontalMenu.vue';
// import VueGoodTablePlugin from 'vue-good-table';
// import 'vue-good-table/dist/vue-good-table.css';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    HorizontalMenu,
  },
  setup() {
    const userPermissions = ref({
      option1: true,
      option2: false,
      // ... y así sucesivamente
    });

    const router = useRouter();
    const route = useRoute();
    const isLoginPage = computed(() => route.path === '/userlogin');

    // Función para verificar la expiración del token
    const checkTokenExpiry = () => {
      const token = sessionStorage.getItem('token');
      if (token) {
        const expiryTime = JSON.parse(atob(token.split('.')[1])).exp;
        if (Date.now() >= expiryTime * 1000) {
          // Token expirado
          sessionStorage.removeItem('token');
          router.push('/login'); // Redirige a la página de login
        }
      }
    };

    onMounted(() => {
      document.title = "Circuito Legajo Electronico";
      checkTokenExpiry();
      // Configura un intervalo para revisar periódicamente
      setInterval(checkTokenExpiry, 60000); // Revisa cada minuto
    });

    return {
      userPermissions,
      isLoginPage,
    };
  },
};
</script>

<style>
@import "~bootstrap-icons/font/bootstrap-icons.css";

html {
  font-size: 13px;
}

body {
  background-color: #cccccc !important;
}

.header-fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.menu-fixed {
  position: fixed;
  top: 70px; /* Ajustar este valor al tamaño del header */
  left: 0;
  width: 100%;
  z-index: 999;
}

.content-wrapper {
  margin-top: 130px;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
}


.table {
    background-color: white;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.4);
}

.table td {
    padding: 15px;
    vertical-align: middle;
    text-align: center; /* Centra el texto horizontalmente */
}

.table th {
  background-color: #026290 !important;
  /* background-color: #557A95 !important; */
  color: white !important;
}

.table th.sortable {
  cursor: pointer;
  user-select: none;
}
.table th.sortable:hover {
  filter: brightness(1.18);
}
.sort-icon {
  font-size: 0.72em;
  opacity: 0.75;
  margin-left: 3px;
}

.custom-shadow-btn {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.4);
}

.fecha-columna {
  white-space: nowrap; /* Evita que el contenido de la columna se divida en múltiples líneas */
  overflow: hidden; /* Oculta el contenido excedente */
  text-overflow: ellipsis; /* Agrega puntos suspensivos (...) al final del texto que no se muestra */
}

.bi {
  font-size: 24px;
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
  background-color: white;
  color: #026290;
  padding: 16px 20px;
  border-bottom: 3px solid #026290;
}

.modal-header .modal-title,
.modal-header h1,
.modal-header h4,
.modal-header h5 {
  color: #026290;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.modal-logo {
  width: 100%;
  height: 80px;
  background-image: url('@/assets/membrete_lemit.jpeg');
                    /* url('@/assets/logo_cic_modal.png'),  */
                    /* url('@/assets/logo_ministerio_modal.png'), */
                    /* url('@/assets/logo_pba_modal.png'); */
  background-size: contain; 
  background-repeat: no-repeat; 
  background-position: center; 
  margin-right: 10px; /* Espacio entre los logos y el título */
}

.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog-a4 {
  width: 210mm;
  max-width: 100%;
  max-height: 90vh;
  margin: auto;
}

.modal-dialog {
  max-width: 440px;
  width: calc(100% - 2rem);
  margin: auto;
}

.modal-dialog-md {
  max-width: 660px;
}

.modal-content {
  /* background-color: blue; */
  padding: 1.25rem;
  border: 1px solid #888;
  width: 100%;
  margin-bottom: 1.875rem;
  text-align: left;
}

.modal-footer-a4 {
  display: flex;
  justify-content: space-between; /* Para separar la imagen de los botones */
  align-items: center; /* Para alinear verticalmente los elementos */
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}

.modal-footer-a4 .footer-image {
  width: 100%;
  height: 80px;
  background-image: url('@/assets/pie_pagina_lemit.jpeg'); /* Ruta a la imagen */
  background-size: contain; /* Asegura que la imagen se ajuste dentro del contenedor */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  background-position: center; /* Centra la imagen en el contenedor */
}

.modal-footer-a4 .btn {
  margin-left: 0.5rem;
}

.modal-footer .btn {
  width: 45%; /* Establece el ancho de los botones */
}

.modal-dialog-a4 .modal-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-dialog-a4 .modal-body {
  overflow-y: auto;
  flex: 1;
}

@media print {
  .modal-dialog-a4 {
    max-height: none;
  }
  .modal-dialog-a4 .modal-content {
    max-height: none;
  }
  .modal-dialog-a4 .modal-body {
    overflow-y: visible;
  }

  #mostrarModalPresupuesto.show,
  #mostrarModalPresupuesto.show * { visibility: visible; }

  #mostrarModalPresupuesto.show {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    background: white;
    z-index: 9999;
    display: block !important;
  }

  #mostrarModalPresupuesto .no-print { display: none !important; visibility: hidden; }

  #mostrarModalPresupuesto.show .modal-dialog-a4 {
    box-shadow: none;
    margin: 0;
    max-width: 100%;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  #mostrarModalPresupuesto.show .modal-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  #mostrarModalPresupuesto.show .modal-body {
    flex: 1;
    padding: 20px 30px 120px 30px;
    overflow: visible;
  }

  #mostrarModalPresupuesto.show .modal-footer-a4 {
    position: fixed;
    bottom: 0; left: 0;
    width: 100%;
  }

  #mostrarModalPresupuesto.show .modal-logo,
  #mostrarModalPresupuesto.show .footer-image {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
    visibility: visible !important;
  }
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}

.alert-success {
  position: fixed !important;
  width: 100%;
}

.alert-danger {
  position: fixed !important;
  width: 100%;
}

.form-select {
  font-size: 16px;
  padding: 6px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  width: 100%;
  appearance: none;
  padding-right: 2.25rem; /* Espaciado para el ícono */
}

/* Espaciado para el ícono de flecha en el desplegable */
.form-select::after {
  content: '\25BC'; /* Código de la flecha hacia abajo */
  position: absolute;
  right: 10px; 
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none; 
}

.form-select:focus {
  border-color: #007bff; /* Color de resaltado cuando el desplegable está enfocado */
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25); /* Efecto de resaltado cuando está enfocado */
}

</style>
