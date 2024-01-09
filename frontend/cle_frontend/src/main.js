import { createApp } from 'vue';
import App from './App.vue';
import router from '../router';
import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap';
import "bootstrap/dist/js/bootstrap.bundle.min.js";  // Importación de Popper.js

const app = createApp(App);

app.use(router).mount('#app');
