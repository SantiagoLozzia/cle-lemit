<template>
  <div class="tabla-wrapper">
    <table class="table table-hover table-sm">
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
                            @blur="cerrarSugerencias(index)"
                            :title="fila.servicio"
                            :readonly="!fila.editable"
                            required
                        >
                        <ul v-if="fila.sugerencias.length > 0" class="sugerencias-lista">
                            <li
                                v-for="sugerencia in fila.sugerencias"
                                :key="sugerencia.nro_servicio"
                                @mousedown.prevent="seleccionarServicio(sugerencia, index)"
                            >
                                <span class="sug-nombre">{{ sugerencia.servicio }}</span>
                                <span class="sug-meta">Nº{{ sugerencia.nro_servicio }}{{ sugerencia.norma ? ' · ' + sugerencia.norma : '' }}</span>
                            </li>
                        </ul>
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
  </div>
  <button @click="agregarServicio" class="btn btn-sm btn-outline-primary mt-1">+ Agregar servicio</button>
</template>

<script>
import { ref, watch, getCurrentInstance, onMounted } from 'vue';
import api from '@/api.js';
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
                const response = await api.get('/aranceles/obtener_modulo/');
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
                api.get('/presupuestos/buscar_servicios/', {
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

        const seleccionarServicio = (sugerencia, index) => {
            const fila = filas.value[index];
            if (!sugerencia?.nro_servicio) return;
            api.get(`/presupuestos/seleccionar_servicio/${sugerencia.nro_servicio}/`)
                .then(response => {
                    fila.nro_servicio = response.data.nro_servicio;
                    fila.servicio = response.data.servicio;
                    fila.norma = response.data.norma;
                    fila.precioUnitario = parseInt(response.data.arancel) * parseInt(moduloValor.value);
                    fila.sugerencias = [];
                    fila.editable = false;
                    serviciosSeleccionados.value.add(fila.nro_servicio);
                })
                .catch(error => {
                    console.error('Error al obtener los detalles del servicio:', error);
                });
        };

        const cerrarSugerencias = (index) => {
            setTimeout(() => { filas.value[index].sugerencias = []; }, 200);
        };

        // Watcher para recalcular el subtotal y emitir los cambios
        watch(filas, (nuevasFilas) => {
            nuevasFilas.forEach(fila => {
                if (!isNaN(fila.cant) && !isNaN(fila.precioUnitario) && fila.nro_servicio) {
                fila.subtotal = fila.cant * fila.precioUnitario;
                console.log('>>>calculando subtotal para fila', fila);
                } else {
                fila.subtotal = null;
                console.log('>>>subtotal no calculado para fila', fila);
                }   
            });
            // Crear un array con solo los campos necesarios para el backend
            const detallesParaBackend = nuevasFilas.map(fila => ({
                nro_servicio: fila.nro_servicio,
                cant: fila.cant,
                subtotal: fila.subtotal
            }));
            detallePresupuesto.value = detallesParaBackend;
            console.log('Emitiendo detallePresupuesto:', JSON.stringify(detallePresupuesto.value, null, 2));
            emit('detallePresupuesto', detallePresupuesto);
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
            cerrarSugerencias,
            agregarServicio,
            detallePresupuesto,
            eliminarFila,
        };
    }
};
</script>


<style scoped>
.tabla-wrapper {
    overflow-x: auto;
    width: 100%;
}

table {
    min-width: 700px;
    table-layout: fixed;
}

input {
    width: 100%;
    box-sizing: border-box;
    text-overflow: ellipsis;
    overflow: hidden;
    font-size: 0.85rem;
    padding: 2px 4px;
    border: 1px solid #ced4da;
    border-radius: 4px;
}

.col-nro      { width: 55px; }
.col-servicio { width: auto; }
.col-norma    { width: 110px; }
.col-precio   { width: 110px; }
.col-cant     { width: 70px; }
.col-total    { width: 100px; }
.col-action   { width: 44px; }

.position-relative { position: relative; }

/* Lista de sugerencias de servicios */
.sugerencias-lista {
    list-style: none;
    margin: 0;
    padding: 0;
    position: absolute;
    top: 100%;
    left: 0;
    width: 420px;
    max-height: 240px;
    overflow-y: auto;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1050;
}

.sugerencias-lista li {
    padding: 6px 10px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    border-bottom: 1px solid #f0f0f0;
}

.sugerencias-lista li:hover {
    background-color: rgba(18, 100, 189, 0.1);
}

.sug-nombre {
    font-size: 0.82rem;
    font-weight: 500;
    color: #212529;
    white-space: normal;
    line-height: 1.3;
}

.sug-meta {
    font-size: 0.73rem;
    color: #6c757d;
    margin-top: 1px;
}
</style>