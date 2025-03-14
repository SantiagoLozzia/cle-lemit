import { createApp } from 'vue';
import App from './App.vue';
import router from '../router';
import vSelect from 'vue-select';
import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap';
import "bootstrap/dist/js/bootstrap.bundle.min.js";  // Importación de Popper.js
import 'bootstrap-icons/font/bootstrap-icons.css';
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

const app = createApp(App);

app.component('v-select', vSelect);
app.use(router);
app.mount('#app');

// Añadir Axios a las propiedades globales
app.config.globalProperties.$axios = axios;
