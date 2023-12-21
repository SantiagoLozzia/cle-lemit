// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from '../router';
// import 'bootstrap/dist/css/bootstrap.css';
// import 'bootstrap-vue/dist/bootstrap-vue.css';
// import { BootstrapVue } from 'bootstrap-vue';

const app = createApp(App);

app.use(router).mount('#app');
// Usa BootstrapVue
// app.use(router).use(BootstrapVue).mount('#app');