<template>
  <div class="container">
    <div class="button-module">
      <UpdateModule :data="moduloData" />
    </div>

    <div class="button-new-service">
      <NewService :data="servicioData" />
    </div>

    <div class="table-container">
      <!-- La tabla recibirá la lista reactiva -->
      <ArancelesTable :data="arancelesData" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
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
        const res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/aranceles/todos/`);
        if (!res.ok) throw new Error('Error cargando aranceles');
        arancelesData.value = await res.json();
      } catch (err) {
        console.error('Fetch error:', err);
      }
    };

    /* --- 2) WebSocket para cambios en tiempo real --- */
    const initSocket = () => {
      const socket = new WebSocket(`ws://192.168.100.10/ws/mi_canal/`);

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
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  padding: 0;
  margin: 0;
}

.button-new-service {
  margin-left: 0;
}
</style>
