<template>
  <div class="aranceles-view">
    <div class="actions-bar">
      <UpdateModule />
      <NewService @arancel-creado="fetchAranceles" />
    </div>
    <ArancelesTable :data="arancelesData" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api.js';
import UpdateModule     from '../components/aranceles/UpdateModule.vue';
import ArancelesTable   from '../components/aranceles/ArancelesTable.vue';
import NewService       from '../components/aranceles/NewService.vue';

export default {
  components: { UpdateModule, NewService, ArancelesTable },

  setup() {
    const moduloData    = ref([]);
    const servicioData  = ref([]);
    const arancelesData = ref([]);

    /* --- 1) Carga inicial vía HTTP --- */
    const fetchAranceles = async () => {
      try {
        const response = await api.get('/aranceles/todos/');
        arancelesData.value = response.data;
      } catch (err) {
        console.error('Fetch error:', err.message);
      }
    };

    /* --- 2) WebSocket para cambios en tiempo real --- */
    const initSocket = () => {
      const token = sessionStorage.getItem('token');
      if (!token) return;

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const socket = new WebSocket(`${protocol}//${window.location.host}/ws/mi_canal/`, ['jwt', token]);

      socket.onopen = () => {
        console.log('✅ Conexión WebSocket establecida');
      };

      socket.onmessage = (event) => {
        console.log('📩 Mensaje recibido:', event.data); // Depurar mensaje crudo
        try {
          const data = JSON.parse(event.data);
          console.log('📋 Datos parseados:', data);
          if (data.aranceles_action === 'add' && data.servicio) {
            arancelesData.value.push(data.servicio); // Agregar nueva fila
          } else {
            console.log('⚠️ Formato de datos no esperado:', data);
          }
        } catch (err) {
          console.error('❌ Error parseando mensaje:', err);
        }
      };

      socket.onerror = (error) => {
        console.error('❌ Error en WebSocket:', error);
      };

      socket.onclose = () => {
        console.log('🔌 Conexión WebSocket cerrada');
        setTimeout(initSocket, 5000); // Reintentar cada 5s
      };
    };

    /* --- Montaje --- */
    onMounted(() => {
      fetchAranceles();
      initSocket();
    });

    return { moduloData, servicioData, arancelesData };
  }
};
</script>

<style scoped>
.aranceles-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.actions-bar {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 0;
}

.actions-bar :deep(.btn) {
  min-width: 160px;
}
</style>
