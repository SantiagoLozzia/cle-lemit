import { createApp } from 'vue';
import App from './App.vue';
import router from '../router';
import Vue3Select from 'vue3-select';
import 'vue3-select/dist/vue3-select.css';
import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap';
import "bootstrap/dist/js/bootstrap.bundle.min.js";  // Importación de Popper.js
import axios from 'axios';

// Función para obtener el token CSRF de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Configurar Axios para incluir el token CSRF y credenciales
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
axios.defaults.withCredentials = true;

// Configurar Axios para incluir el token JWT en el encabezado de autorización
const token = sessionStorage.getItem('token');
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const app = createApp(App);

app.component('Vue3Select', Vue3Select);
app.use(router);
app.mount('#app');

// Añadir Axios a las propiedades globales
app.config.globalProperties.$axios = axios;
