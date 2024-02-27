<template>
  <div>
    <!-- Este componente no renderiza nada directamente -->
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
// eslint-disable-next-line no-unused-vars
import { emit } from 'vue';
import axios from 'axios';

export default {
  props: {
    subcolumnasSolicitud: Array
  },
  setup(props, { emit }) {
    const subColumnasHijo = ref(props.subcolumnasSolicitud);

    // const filas = ref([
    //     'nro_dataServicio', 'fecha_dataServicio', 'area_tematica', 'nro_presupuesto', 'doc_dataServicio', 'adjunto_solicitudServicio', 'nro_legajo', 'fecha', 'doc_legajo', 'adjunto_factura', 'pago_legajo', 'plazo_pago', 'nros_remitos', 'muestras', 'plazo', 'doc_ordenServicio', 'plazo', 'fecha', 'area_tematica', 'adjunto_informe'
    //   ]);


    // Método para obtener los datos de la API y completar el array
    const fetchData = () => {
      axios.get('api/encurso/obtener_serviciosencurso/')
        .then(response => {
          console.log('Los DataServicio en curso son:', response.data)
          subColumnasHijo.value = response.data;
          // console.log('subcolumnasHijo:', subColumnasHijo.value)
          emit('update-subcolumnas', response.data);
        })
        .catch(error => {
          console.error('Error al obtener datos:', error);
        });
    };

    // Llamamos a fetchData cuando el componente se monta
    onMounted(() => {
      fetchData();
    });

    return {
      subColumnasHijo,
    };
  },
};
</script>

<style scoped>
/* Estilos específicos para tu componente */
</style>
