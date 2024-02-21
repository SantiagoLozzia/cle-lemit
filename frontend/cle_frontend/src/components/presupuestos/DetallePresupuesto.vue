<template>
    <table class="table">
        <thead>
            <tr>
                <th>Nro</th>
                <th>Servicio Solicitado</th>
                <th>Norma</th>
                <th>Precio Unitario</th>
                <th>Cant</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(fila, index) in filas" :key="index">
                <td><input v-model.number="fila.nro_servicio" type="text" readonly class="col-auto"></td>

                <td>
                    <div class="mb-3">
                        <input v-model="fila.servicio" type="text" class="form-control" id="servicio" name="servicio" ref="servicio" @input="buscarServicio(fila.servicio)">
                        <select v-if="fila.sugerencias && fila.sugerencias.length > 0" @change="seleccionarServicio($event, index)" class="form-select mt-1">
                            <option v-for="sugerencia in fila.sugerencias" :key="sugerencia.nro_servicio" :value="sugerencia.nro_servicio">
                               {{ sugerencia.nro_servicio }} - {{ sugerencia.servicio }} - {{ sugerencia.norma }} - {{ sugerencia.area_tematica }}
                            </option>
                        </select>
                    </div>
                </td>

                <td><input v-model.number="fila.norma" type="text" readonly></td>                 
                <td><input v-model.number="fila.precioUnitario" type="number" readonly></td>
                <td><input v-model.number="fila.cantidad" type="number"></td>
                <td><input v-model.number="fila.total" type="number" readonly></td>
            </tr>
        </tbody>
    </table>
    <button @click="agregarServicio">+</button>
</template>
  
<script>
    import { ref, watch, getCurrentInstance  } from 'vue';
    import axios from 'axios';
    import { debounce } from 'lodash';

    export default {
        setup() {
            const filas = ref([{ nro_servicio: null, servicio: '', norma: '', arancel: '', precioUnitario: null, cantidad: null, total: null, sugerencias: [] }]);
            const { emit } = getCurrentInstance();
            const buscarServicio = debounce((term) => {
                console.log('Term de búsqueda:', term);
                if (term && term.trim() !== '') {
                    axios.get('http://localhost:8000/api/presupuestos/buscar_servicios/', {
                        params: { q: term }
                    })
                    .then(response => {
                        // Asignar las sugerencias directamente a cada fila
                        filas.value.forEach(fila => {
                            fila.sugerencias = response.data;
                        });
                        console.log('algo', response.data);
                    })
                    .catch(error => {
                        console.error('Error al buscar servicios:', error);
                    });
                } else {
                    // Si el término de búsqueda está vacío, limpiar las sugerencias en todas las filas
                    filas.value.forEach(fila => {
                        fila.sugerencias = [];
                    });
                }
            }, 1000); // Tiempo de espera en milisegundos antes de ejecutar la búsqueda

            const seleccionarServicio = (event, index) => {
                console.log('Index:', index);
                const fila = filas.value[index];
                console.log('Fila:', fila);
                const servicioSeleccionado = event.target.value; // Obtener el valor seleccionado del select
                console.log('Servicio seleccionado Id:', servicioSeleccionado);

                if (servicioSeleccionado) {
                    axios.get(`http://localhost:8000/api/presupuestos/seleccionar_servicio/${servicioSeleccionado}/`)
                        .then(response => {
                            console.log("Respuesta del servidor:", response.data);
                            fila.nro_servicio = response.data.nro_servicio;
                            fila.servicio = response.data.servicio;
                            fila.norma = response.data.norma;
                            fila.precioUnitario = response.data.arancel;
                            console.log('luego del autocompletado',fila.sugerencias);
                            fila.sugerencias = []; // Limpiar el array de sugerencias después de seleccionar un servicio
                            console.log('luego del autocompletado',fila.sugerencias);
                        })
                        .catch(error => {
                            console.error('Error al obtener los detalles del servicio:', error);
                        });
                } else {
                    console.warn('Ningún servicio seleccionado');
                }
                
            };


            // Watcher para calcular automáticamente el campo "Total"
            watch(filas, (nuevasFilas) => {
                nuevasFilas.forEach(fila => {
                    // Verificar si la cantidad y el precio unitario son números válidos
                    if (!isNaN(fila.cantidad) && !isNaN(fila.precioUnitario)) {
                        fila.total = fila.cantidad * fila.precioUnitario;
                    } else {
                        // Si la cantidad o el precio unitario no son válidos, establecer el total como null
                        fila.total = null;
                    }
                });
            }, { deep: true }); 
            
            const agregarServicio = () => {
                filas.value.push({ nro_servicio: '', servicio: '', norma: '', precioUnitario: null, cantidad: null, total: null, sugerencias: [] });
                console.log('Se agregó un nuevo servicio. Filas actualizadas:', filas.value); 
            };

            watch(filas, (nuevasFilas) => {
                const total = nuevasFilas.reduce((acc, fila) => acc + fila.total, 0);
                console.log('Calculando subtotal. Filas:', nuevasFilas); 
                console.log('Subtotal calculado:', total); 
                emit('actualizar-subtotal', total);
            }, { deep: true });

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
