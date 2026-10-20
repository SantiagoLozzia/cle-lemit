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
                <th class="col-action">Acción</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(fila, index) in filas" :key="index">
                <td>
                    <input v-model.number="fila.nro_servicio" type="text" readonly required class="col-auto">
                </td>
                <td>
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
                        :class="{ 'input-required': fila.nro_servicio && !fila.cant }"
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

  <!-- Teleport al body para evitar clipping por overflow-x del wrapper -->
  <Teleport to="body">
    <ul
      v-if="dropdownVisible && sugerenciasActivas.length > 0"
      class="sugerencias-lista-global"
      :style="dropdownStyle"
    >
      <li
        v-for="sugerencia in sugerenciasActivas"
        :key="sugerencia.nro_servicio"
        @mousedown.prevent="seleccionarServicio(sugerencia, activeDropdownIndex)"
      >
        <span class="sug-nombre">{{ sugerencia.servicio }}</span>
        <span class="sug-meta">Nº{{ sugerencia.nro_servicio }}{{ sugerencia.norma ? ' · ' + sugerencia.norma : '' }}</span>
      </li>
    </ul>
  </Teleport>

  <button @click="agregarServicio" class="btn btn-sm btn-outline-primary mt-3 mb-2">+ Agregar servicio</button>
</template>

<script>
import { ref, computed, watch, getCurrentInstance, onMounted } from 'vue';
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
        const serviciosSeleccionados = ref(new Set());
        const { emit } = getCurrentInstance();

        // Estado del dropdown teleportado
        const activeDropdownIndex = ref(-1);
        const dropdownVisible = ref(false);
        const dropdownPosition = ref({ top: 0, left: 0, width: 0 });

        const sugerenciasActivas = computed(() => {
            if (activeDropdownIndex.value === -1) return [];
            return filas.value[activeDropdownIndex.value]?.sugerencias || [];
        });

        const dropdownStyle = computed(() => ({
            position: 'fixed',
            top: dropdownPosition.value.top + 'px',
            left: dropdownPosition.value.left + 'px',
            minWidth: Math.max(dropdownPosition.value.width, 460) + 'px',
        }));

        const obtenerModulo = async () => {
            try {
                const response = await api.get('/aranceles/obtener_modulo/');
                moduloValor.value = response.data.valor;
            } catch (error) {
                console.error('Error al obtener el valor del módulo:', error);
            }
        };

        const buscarServicio = debounce((event, index) => {
            const term = event.target.value;
            const rect = event.target.getBoundingClientRect();
            dropdownPosition.value = {
                top: rect.bottom + 4,
                left: rect.left,
                width: rect.width,
            };
            activeDropdownIndex.value = index;

            if (term && term.trim() !== '') {
                api.get('/presupuestos/buscar_servicios/', { params: { q: term } })
                .then(response => {
                    const sugerenciasFiltradas = response.data.filter(s =>
                        !serviciosSeleccionados.value.has(s.nro_servicio)
                    );
                    filas.value[index].sugerencias = sugerenciasFiltradas;
                    dropdownVisible.value = sugerenciasFiltradas.length > 0;
                })
                .catch(error => {
                    console.error('Error al buscar servicios:', error);
                });
            } else {
                filas.value[index].sugerencias = [];
                dropdownVisible.value = false;
            }
        }, 1000);

        const seleccionarServicio = (sugerencia, index) => {
            dropdownVisible.value = false;
            activeDropdownIndex.value = -1;
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
            setTimeout(() => {
                if (activeDropdownIndex.value === index) {
                    filas.value[index].sugerencias = [];
                    dropdownVisible.value = false;
                    activeDropdownIndex.value = -1;
                }
            }, 200);
        };

        // Watcher para recalcular el subtotal y emitir los cambios
        watch(filas, (nuevasFilas) => {
            nuevasFilas.forEach(fila => {
                if (!isNaN(fila.cant) && !isNaN(fila.precioUnitario) && fila.nro_servicio) {
                    fila.subtotal = fila.cant * fila.precioUnitario;
                } else {
                    fila.subtotal = null;
                }
            });
            const detallesParaBackend = nuevasFilas.map(fila => ({
                nro_servicio: fila.nro_servicio,
                cant: fila.cant,
                subtotal: fila.subtotal
            }));
            detallePresupuesto.value = detallesParaBackend;
            emit('detallePresupuesto', detallePresupuesto);
        }, { deep: true });

        watch(filas, (nuevasFilas) => {
            const total = nuevasFilas.reduce((acc, fila) => acc + fila.subtotal, 0);
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
            dropdownVisible,
            sugerenciasActivas,
            dropdownStyle,
            activeDropdownIndex,
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

.input-required {
    border-color: #dc3545 !important;
    background-color: #fff8f8;
}
</style>

<!-- Sin scoped: el Teleport renderiza en body, fuera del scope del componente -->
<style>
.sugerencias-lista-global {
    list-style: none;
    margin: 0;
    padding: 0;
    max-height: 300px;
    overflow-y: auto;
    background: white;
    border: 1px solid #c0c7d0;
    border-radius: 6px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    z-index: 9999;
}

.sugerencias-lista-global li {
    padding: 7px 12px;
    cursor: pointer;
    border-bottom: 1px solid #f0f0f0;
}

.sugerencias-lista-global li:last-child {
    border-bottom: none;
}

.sugerencias-lista-global li:hover {
    background-color: #e8f0fe;
}

.sugerencias-lista-global .sug-nombre {
    display: block;
    font-size: 0.83rem;
    font-weight: 500;
    color: #212529;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sugerencias-lista-global .sug-meta {
    display: block;
    font-size: 0.72rem;
    color: #6c757d;
    margin-top: 1px;
}
</style>
