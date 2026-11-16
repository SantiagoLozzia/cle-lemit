<template>
    <div>
      <div>
        <div class="button-container">
          <button class="btn btn-primary float-start ms-2 mt-4 custom-shadow-btn" @click="mostrarFormulario">+ Data Servicio</button>
        </div>

        <div class="modal" :class="{ 'show': mostrarModal }" id="modalNuevoDataServicio">
          <div class="modal-dialog-a4">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5 fw-bold">Nuevo Data Servicio</h1>
                <button type="button" class="btn-close" @click="cerrarModal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form class="was-validated">

                  <div class="mb-3">
                    <label for="fecha_dataServicio" class="form-label text-left">Fecha:</label>
                    <input v-model="nuevoDataServicio.fecha_dataServicio" type="date" readonly class="form-control" id="fecha_dataServicio" name="fecha_dataServicio" required />
                  </div>

                  <div class="mb-3">
                      <label for="nro_presupuesto" class="form-label text-left">N° Presupuesto:</label>
                      <select v-model="selectedPresupuesto" @click="buscarSugerencias" @change="presupuestoSeleccionado(selectedPresupuesto)" class="form-select mt-1">
                          <option v-for="sugerencia in sugerencias" :key="sugerencia.nro_presupuesto" :value="sugerencia.nro_presupuesto">
                              {{ sugerencia.nro_presupuesto }} - {{ sugerencia.nombre_solicitante }}
                          </option>
                      </select>
                  </div>

                  <div class="mb-3">
                    <label for="obra" class="form-label text-left">Obra:</label>
                    <input v-model="nuevoDataServicio.obra" type="text" class="form-control" id="obra" name="obra"/>
                  </div>

                  <div class="mb-3">
                      <label for="muestras" class="form-label text-left">Muestras:</label>
                      <textarea v-model="nuevoDataServicio.muestras" class="form-control" id="muestras" name="muestras" required style="resize: vertical;"></textarea>
                  </div>

                  <div class="mb-3">
                    <label for="plazo_estimado" class="form-label text-left">Plazo Estimado:</label>
                    <input v-model="nuevoDataServicio.plazo_estimado" type="number" class="form-control" id="plazo_estimado" name="plazo_estimado" required />
                  </div>

                  <div class="mb-3">
                    <label for="cant_numLabs" class="form-label text-left">Cantidad N° Laboratorios:</label>
                    <input v-model="nuevoDataServicio.cant_numLabs" type="number" class="form-control" id="cant_numLabs" name="cant_numLabs" required />
                  </div>

                  <div class="mb-3">
                    <label for="observaciones" class="form-label text-left">Observaciones:</label>
                    <input v-model="nuevoDataServicio.observaciones" type="text" class="form-control" id="observaciones" name="observaciones" />
                  </div>

                  <div class="mb-3">
                    <label for="email_factura" class="form-label text-left">Email factura:</label>
                    <input v-model="nuevoDataServicio.email_factura" type="email" class="form-control" id="email_factura" name="email_factura" placeholder="email@ejemplo.com" />
                  </div>

                  <div class="mb-3">
                    <label for="email_informe_tecnico" class="form-label text-left">Email informe técnico:</label>
                    <input v-model="nuevoDataServicio.email_informe_tecnico" type="email" class="form-control" id="email_informe_tecnico" name="email_informe_tecnico" placeholder="email@ejemplo.com" />
                  </div>

                  <!-- Concepto de Facturación -->
                  <div class="mb-3">
                    <label class="form-label text-left">Concepto de Facturación:</label>
                    <select v-model="conceptoAgregar" @change="agregarConcepto" class="form-select form-select-sm">
                      <option value="">Seleccionar concepto para agregar...</option>
                      <option v-for="c in conceptosDisponibles" :key="c.id" :value="c">{{ c.nombre }}</option>
                    </select>
                    <div class="concepto-box mt-2" v-if="conceptosSeleccionados.length > 0">
                      <span v-for="c in conceptosSeleccionados" :key="c.id"
                            class="badge d-flex align-items-center gap-1"
                            style="background:#026290; font-size:12px; padding:5px 10px; cursor:pointer;"
                            @click="quitarConcepto(c)">
                        {{ c.nombre }} <i class="bi bi-x" style="font-size:11px;"></i>
                      </span>
                    </div>
                  </div>

                  <button @click="crearDataServicio" type="button" class="btn btn-primary w-100">Guardar</button>
                </form>
              </div>
            </div>
          </div>
        </div>

        <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
          ¡Éxito! El Data Servicio se ha creado correctamente.
        </div>
        <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
          ¡Error! Ha ocurrido un problema al guardar el Data Servicio. Por favor, inténtalo de nuevo.
        </div>

      </div>
      </div>
  </template>

  <script>
    import api from '@/api.js';
    import { ref, computed, onMounted, nextTick } from 'vue';

    export default {
      components: {
      },

      setup() {
        const inputProps = ref({ placeholder: 'Buscar solicitante' });
        const sugerencias = ref([]);
        const selectedPresupuesto = ref(null);
        const nuevoDataServicio = ref({
            fecha_dataServicio: null,
            obra: null,
            muestras:null,
            plazo_estimado: null,
            cant_numLabs: null,
            email_factura: null,
            email_informe_tecnico: null,
        });
        const mostrarModal = ref(false);
        const showSuccessAlert = ref(false);
        const showErrorAlert = ref(false);

        // Conceptos de Facturación
        const catalogoConceptos = ref([]);
        const conceptosSeleccionados = ref([]);
        const conceptoAgregar = ref('');
        const conceptosDisponibles = computed(() =>
          catalogoConceptos.value.filter(c => !conceptosSeleccionados.value.some(x => x.id === c.id))
        );

        const agregarConcepto = () => {
          if (!conceptoAgregar.value) return;
          conceptosSeleccionados.value.push(conceptoAgregar.value);
          conceptoAgregar.value = '';
        };

        const quitarConcepto = (c) => {
          conceptosSeleccionados.value = conceptosSeleccionados.value.filter(x => x.id !== c.id);
        };

        const fetchCatalogoConceptos = () => {
          api.get('/aranceles/conceptos/').then(res => { catalogoConceptos.value = res.data; }).catch(() => {});
        };

        const mostrarFormulario = () => {
          const today = new Date();
          const year = today.getFullYear();
          let month = today.getMonth() + 1;
          let day = today.getDate();
          if (month < 10) month = '0' + month;
          if (day < 10) day = '0' + day;
          const formattedDate = `${year}-${month}-${day}`;

          nuevoDataServicio.value = {
            fecha_dataServicio: formattedDate,
            obra: null,
            muestras:null,
            plazo_estimado: null,
            cant_numLabs: null,
            email_factura: null,
            email_informe_tecnico: null,
          };
          conceptosSeleccionados.value = [];
          conceptoAgregar.value = '';
          mostrarModal.value = true;
        };

        const cerrarModal = () => {
          mostrarModal.value = false;
          sugerencias.value = '';
        };

        const crearDataServicio = () => {
          if (!nuevoDataServicio.value.plazo_estimado || !nuevoDataServicio.value.cant_numLabs) {
            return;
          }
          api.post('/encurso/crear_dataServicio/', nuevoDataServicio.value)
            .then(async response => {
              const nroDS = response.data.nro_dataServicio;
              // Asignar conceptos si se seleccionaron
              if (conceptosSeleccionados.value.length > 0 && nroDS) {
                try {
                  await api.patch(`/encurso/actualizar_conceptos_ds/${nroDS}/`, {
                    conceptos_facturacion: conceptosSeleccionados.value.map(c => c.id),
                  });
                } catch (e) {
                  console.error('Error asignando conceptos:', e);
                }
              }
              cerrarModal();
              nuevoDataServicio.value = {
                fecha_dataServicio: null,
                obra: null,
                muestras:null,
                plazo_estimado: null,
                cant_numLabs: null,
                email_factura: null,
                email_informe_tecnico: null,
              };
              conceptosSeleccionados.value = [];
              nextTick(() => document.dispatchEvent(new CustomEvent('encurso-refresh')));
              showSuccessAlert.value = true;
              setTimeout(() => { showSuccessAlert.value = false; }, 3000);
            })
            .catch(error => {
              console.error('Error al guardar el Data Servicio:', error);
              cerrarModal();
              showErrorAlert.value = true;
              setTimeout(() => { showErrorAlert.value = false; }, 5000);
            });
        };

        const buscarSugerencias = () => {
            api.get('/encurso/buscar_presupuestos/')
              .then(response => {
                sugerencias.value = response.data;
              })
              .catch(error => {
                console.error('Error al buscar presupuestos:', error);
              });
        };

        const presupuestoSeleccionado = () => {
          api.get(`/encurso/presupuesto_seleccionado/${selectedPresupuesto.value}/`)
            .then(response => {
              nuevoDataServicio.value.nro_presupuesto = response.data.nro_presupuesto;
            })
            .catch(error => {
              console.error('Error al obtener los detalles del solicitante:', error);
            });
        };

        onMounted(() => {
          fetchCatalogoConceptos();
        });

        return {
          inputProps,
          sugerencias,
          nuevoDataServicio,
          mostrarModal,
          showSuccessAlert,
          showErrorAlert,
          buscarSugerencias,
          selectedPresupuesto,
          presupuestoSeleccionado,
          mostrarFormulario,
          cerrarModal,
          crearDataServicio,
          catalogoConceptos,
          conceptosSeleccionados,
          conceptoAgregar,
          conceptosDisponibles,
          agregarConcepto,
          quitarConcepto,
        };
      }
    };
  </script>

  <style scoped>
  .concepto-box {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    min-height: 42px;
  }
  </style>
