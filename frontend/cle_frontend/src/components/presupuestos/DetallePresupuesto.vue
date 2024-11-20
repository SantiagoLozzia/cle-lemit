<template>
    <table class="table table-hover"> 
        <thead class="text-center">
            <tr>
                <th class="col-nro">Nro</th>
                <th class="col-servicio">Servicio Solicitado</th>
                <th class="col-norma">Norma</th>
                <th class="col-precio">Precio Unitario</th>
                <th class="col-cant">Cant</th>
                <th class="col-total">Total</th>
                <th class="col-action">Acción</th> <!-- Columna para el botón de cruz -->
            </tr>
        </thead>
        <tbody>
            <tr v-for="(fila, index) in filas" :key="index">
                <td>
                    <input v-model.number="fila.nro_servicio" type="text" readonly required class="col-auto">
                </td>

                <td>
                    <div class="mb-3 position-relative">
                        <input 
                            v-model="fila.servicio" 
                            type="text" 
                            class="form-control" 
                            @input="buscarServicio($event, index)" 
                            :title="fila.servicio" 
                            :readonly="!fila.editable" 
                            required
                        >
                        
                        <select 
                            v-if="fila.sugerencias.length > 0" 
                            v-model="fila.servicioSeleccionado"
                            @change="seleccionarServicio($event, index)" 
                            class="form-select position-absolute" 
                            style="display: block;"
                        >
                            <option 
                                v-for="sugerencia in fila.sugerencias" 
                                :key="sugerencia.nro_servicio" 
                                :value="sugerencia.nro_servicio"
                            >
                            {{ sugerencia.nro_servicio }} - {{ sugerencia.servicio }} - {{ sugerencia.norma }} - {{ sugerencia.area_tematica }}
                            </option>
                        </select>

                    </div>
                </td>

                <td>
                    <input 
                        v-model.number="fila.norma" 
                        type="text" 
                        class="text-center" 
                        readonly 
                        required
                        :title="fila.norma"
                    >
                </td>                 
                <td>
                    <input 
                        v-model.number="fila.precioUnitario" 
                        type="number" 
                        class="text-end" 
                        readonly
                        :title="fila.precioUnitario"
                    >
                </td>
                <td>
                    <input 
                        v-model.number="fila.cant" 
                        type="number" 
                        class="text-end"
                        :title="fila.cant"
                    >
                </td>
                <td>
                    <input 
                        v-model.number="fila.subtotal" 
                        type="number" 
                        class="text-end" 
                        readonly
                        :title="fila.subtotal"
                    >
                </td>
                <td>
                    <button
                      type="button"
                      class="btn-close"
                      @click="eliminarFila(index)"
                      aria-label="Close"
                    ></button>
                </td>
            </tr>
        </tbody>
    </table>
    <button @click="agregarServicio">+</button>
</template>

<script>
import { ref, watch, getCurrentInstance, onMounted } from 'vue';
import axios from 'axios';
import { debounce } from 'lodash';

export default {
    setup() {
        const filas = ref([{
            nro_servicio: null,
            servicio: '',
            norma: '',
            precioUnitario: null,
            cant: null,
            subtotal: null,
            sugerencias: [],
            editable: true,
        }]);

        const moduloValor = ref();
        const detallePresupuesto = ref([]);
        const serviciosSeleccionados = ref(new Set()); // Conjunto para almacenar los servicios seleccionados
        const { emit } = getCurrentInstance();

        const obtenerModulo = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/aranceles/obtener_modulo/');
                moduloValor.value = response.data.valor;
                console.log('valor modulo', moduloValor.value);
            } catch (error) {
                console.error('Error al obtener el valor del módulo:', error);
            }
        };

        const buscarServicio = debounce((event, index) => {
            const term = event.target.value;
            console.log('Term de búsqueda:', term);
            if (term && term.trim() !== '') {
                axios.get('http://localhost:8000/api/presupuestos/buscar_servicios/', {
                    params: { q: term }
                })
                .then(response => {
                    // Filtrar las sugerencias para eliminar los servicios ya seleccionados
                    const sugerenciasFiltradas = response.data.filter(sugerencia => 
                        !serviciosSeleccionados.value.has(sugerencia.nro_servicio)
                    );
                    filas.value[index].sugerencias = sugerenciasFiltradas;
                    console.log('Sugerencias filtradas para fila:', index, sugerenciasFiltradas);
                })
                .catch(error => {
                    console.error('Error al buscar servicios:', error);
                });
            } else {
                filas.value[index].sugerencias = [];
            }
        }, 1000);

        const seleccionarServicio = (event, index) => {
            const fila = filas.value[index];
            const servicioSeleccionado = event.target.value;

            console.log('Servicio seleccionado:', servicioSeleccionado);

            if (servicioSeleccionado) {
                axios.get(`http://localhost:8000/api/presupuestos/seleccionar_servicio/${servicioSeleccionado}/`)
                    .then(response => {
                        fila.nro_servicio = response.data.nro_servicio;
                        fila.servicio = response.data.servicio;
                        fila.norma = response.data.norma;
                        const arancel = response.data.arancel;
                        fila.precioUnitario = parseInt(arancel) * parseInt(moduloValor.value);
                        fila.sugerencias = [];
                        fila.editable = false;
                        // Añadir servicio seleccionado a un conjunto de servicios ya seleccionados
                        serviciosSeleccionados.value.add(fila.nro_servicio);
                    })
                    .catch(error => {
                        console.error('Error al obtener los detalles del servicio:', error);
                    });
            } else {
                console.warn('Ningún servicio seleccionado');
            }
        };

        // Watcher para recalcular el subtotal y emitir los cambios
        watch(filas, (nuevasFilas) => {
            nuevasFilas.forEach(fila => {
                if (!isNaN(fila.cant) && !isNaN(fila.precioUnitario)) {
                    fila.subtotal = fila.cant * fila.precioUnitario;
                    console.log('>>>calculando subtotal', fila.subtotal)
                } else {
                    fila.subtotal = null;
                }   
            });
            detallePresupuesto.value = [...nuevasFilas];
            console.log('Emitiendo detallePresupuesto:', detallePresupuesto.value);
            emit('detalle-Presupuesto', detallePresupuesto.value); 
        }, { deep: true });

        watch(filas, (nuevasFilas) => {
                const total = nuevasFilas.reduce((acc, fila) => acc + fila.subtotal, 0);
                // console.log('Calculando subtotal. Filas:', nuevasFilas); 
                // console.log('Subtotal calculado:', total); 
                emit('actualizar-subtotal', total);
        }, { deep: true });


        const agregarServicio = () => {
            filas.value.push({
                nro_servicio: '',
                servicio: '',
                norma: '',
                precioUnitario: null,
                cant: null,
                subtotal: null,
                sugerencias: [],
                editable: true,
            });
        };

        const eliminarFila = (index) => {
            if (filas.value.length > 1) {
                const servicioEliminado = filas.value[index].nro_servicio;
                if (servicioEliminado) {
                    // Remover el servicio del conjunto de seleccionados si se elimina
                    serviciosSeleccionados.value.delete(servicioEliminado);
                }
                filas.value.splice(index, 1);
            } else {
                limpiarFila(index);
            }
        };

        const limpiarFila = (index) => {
            const servicioEliminado = filas.value[index].nro_servicio;
            if (servicioEliminado) {
                serviciosSeleccionados.value.delete(servicioEliminado);
            }
            filas.value[index] = {
                nro_servicio: '',
                servicio: '',
                norma: '',
                precioUnitario: '',
                cant: '',
                subtotal: '',
                sugerencias: [],
                editable: true,
            };
        };

        onMounted(() => {
            obtenerModulo();
        });

        return {
            filas,
            moduloValor,
            obtenerModulo,
            buscarServicio,
            seleccionarServicio,
            agregarServicio,
            detallePresupuesto,
            eliminarFila,
        };
    }
};
</script>


<style scoped>
table {
    width: 100%; /* Hace que la tabla ocupe el 100% del ancho del contenedor */
    table-layout: fixed; /* Opcional: Permite que las celdas tengan un tamaño fijo */
    overflow-wrap: break-word; /* Hace que las palabras se ajusten */
}

input,
select {
    width: 100%; /* Hace que los elementos se ajusten al 100% del ancho de su contenedor */
    box-sizing: border-box; /* Incluye padding y borde en el ancho total */
}

.col-nro {
    width: 60px; /* Ajusta el ancho de la columna Nro */
}

.col-servicio {
    width: 300px; /* Ajusta el ancho de la columna Servicio Solicitado */
}

.col-norma,
.col-precio,
.col-cant,
.col-total {
    width: 100px; /* Ajusta el ancho de las demás columnas */
}

.col-action {
    width: 60px; /* Ajusta el ancho de la columna de acción */
}

.position-relative {
    position:
    relative; 
}

.position-absolute { 
    position: absolute; 
}

input, select { 
    text-overflow: ellipsis;
    overflow: hidden; 
}

.btn-secondary { 
    padding: 0; 
    border-radius: 50%; 
    width: 20px; 
    height: 20px; 
    line-height: 1; 
    font-size: 12px; 
    color: #6c757d; 
    background-color: #f8f9fa; 
} 

.form-select {
    max-height: 200px; /* Ajusta la altura máxima del dropdown si es necesario */
    overflow-y: auto; /* Agrega un scroll si hay muchas opciones */
}


</style>