<template>
    <table class="table">
        <thead>
            <tr>
                <th>Nro</th>
                <th>Servicio Solicitado</th>
                <th>Norma</th>
                <th>Cant</th>
                <th>Precio Unitario</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(fila, index) in filas" :key="index">
                <td><input v-model.number="fila.nro_servicio" type="text"></td>
                <td>
                    <div class="mb-3">
                        <input v-model="fila.servicio" type="text" class="form-control" id="servicio" name="servicio" required ref="servicio" @input="buscarServicio(fila.servicio)">
                        <select v-if="(sugerencias && sugerencias.length > 0)" v-model="selectedServicio" @change="seleccionarServicio(selectedServicio)" class="form-select mt-1">
                            <option v-for="sugerencia in sugerencias" :key="sugerencia.nro_servicio" :value="sugerencia">
                            hola    <!-- {{ sugerencia.nro_servicio }} - {{ sugerencia.servicio }} - {{ sugerencia.norma }} - {{ sugerencia.area_tematica }} -->
                            </option>
                        </select>
                    </div>
                </td>
                <td><input v-model.number="fila.norma" type="number"></td>                 
                <td><input v-model.number="fila.cantidad" type="number"></td>
                <td><input v-model.number="fila.precioUnitario" type="number"></td>
                <td><input v-model.number="fila.total" type="number" readonly></td>
            </tr>
        </tbody>
    </table>
    <button @click="agregarServicio">+</button>
</template>
  
<script>
    import { ref } from 'vue';
    import axios from 'axios';
    import { debounce } from 'lodash';

    export default {
        
        setup() {
            const filas = ref([{ nro_servicio: null, servicio: '', norma: '', arancel: '', cantidad: null, precioUnitario: null, total: null }]);
            const sugerencias = ref([]);
            const selectedServicio = ref(null);
            
            const buscarServicio = debounce((term) => {
                console.log('Term de búsqueda:', term);
                if (term && term.trim() !== '') {
                    axios.get('http://localhost:8000/api/presupuestos/buscar_servicios/', {
                        params: { q: term }
                    })
                    .then(response => {
                        sugerencias.value = response.data;
                        console.log(sugerencias);
                    })
                    .catch(error => {
                        console.error('Error al buscar servicios:', error);
                    });
                } else {
                    // Si el término de búsqueda está vacío, limpiar las sugerencias
                    sugerencias.value = [];
                }
            }, 1000); // Tiempo de espera en milisegundos antes de ejecutar la búsqueda


            const seleccionarServicio = () => {
                if (selectedServicio.value) {
                    const servicioSeleccionado = selectedServicio.value;

                    // Realizar una solicitud al backend para obtener los detalles del servicio seleccionado
                    axios.get(`http://localhost:8000/api/presupuestos/seleccionar_servicio/${servicioSeleccionado.nro_servicio}/`)
                        .then(response => {
                            console.log("Respuesta del servidor:", response.data);
                            
                            // Obtener el índice de la fila seleccionada
                            const index = filas.value.findIndex(fila => fila.servicio === servicioSeleccionado.servicio);

                            if (index !== -1) {
                                // Actualizar los campos del formulario con los detalles del servicio
                                filas.value[index].nro_servicio = response.data.nro_servicio;
                                filas.value[index].servicio = response.data.servicio;
                                filas.value[index].norma = response.data.norma;
                                filas.value[index].precioUnitario = response.data.arancel;
                            } else {
                                console.error('Fila no encontrada para el servicio seleccionado:', servicioSeleccionado.servicio);
                            }
                        })
                        .catch(error => {
                            console.error('Error al obtener los detalles del servicio:', error);
                        });
                } else {
                    console.warn('Ningún servicio seleccionado');
                }
            };


            const agregarServicio = () => {
                filas.value.push({ nro_servicio: '', servicio: '', norma: '', cantidad: null, precioUnitario: null, total: null });
            };

            return {
                filas,
                buscarServicio,
                seleccionarServicio,
                agregarServicio,
            };
        }
    };
</script>

<style scoped>

</style>
