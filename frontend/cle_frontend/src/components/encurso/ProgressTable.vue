<template>
     <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! Se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar. Por favor, inténtalo de nuevo.
    </div>

    <div>
      <table class="table table-hover">
        <thead class="text-center">
          <tr>
            <th v-if="isAdminOrTecnologicoOrDireccion" colspan="6" class="add-border-right align-middle text-center">Solicitud de Servicio</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" colspan="6" class="add-border-right align-middle text-center">Legajo</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" colspan="3" class="add-border-right align-middle text-center">Recepcion</th>
            <th colspan="3" class="add-border-right align-middle text-center">Orden de Servicio</th>
            <th v-if="isTecnologicoOrDireccionOrArea" colspan="4" class="add-border-right align-middle text-center">Inter Area</th>
            <th colspan="5" class="add-border-right align-middle text-center">Informe de Area</th>
            <!-- <th colspan="1" class="add-border-right align-middle text-center">Informe Area</th> -->
            <th colspan="1" class="add-border-right align-middle text-center">Administracion</th>
            <th colspan="1" class="add-border-right align-middle text-center">Servicios Tecnologicos</th>
            <th colspan="1" class="add-border-right align-middle text-center">Responsable Area</th>
            <th colspan="1" class="add-border-right align-middle text-center">Direccion</th>
            <th  v-if="isAdminOrTecnologicoOrDireccion" colspan="1" class="align-middle text-center">Archivo</th>
          </tr>
          <tr>
            <!-- Subcolumnas de Solicitud de Servicio -->
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">N°</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Fecha</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Area Tematica</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">ST-01 Presupuesto</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Data Servicio</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">ST-02 Solicitud</th>
            <!-- Subcolumnas de Legajo -->
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">N°</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Fecha</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Legajo</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Factura</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Pago</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">Plazo</th>
            <!-- Subcolumnas de Recepcion -->
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">ST-03 Recepcion</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Muestras</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">Plazo</th>
            <!-- Subcolumnas de Orden de Servicio -->
            <th class="align-middle text-center">Fecha</th>
            <th class="align-middle text-center">ST-05 Orden</th>
            <th class="add-border-right align-middle text-center">Plazo</th>
            <!-- Subcolumnas de Inter Area -->
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Fecha</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Solicitud</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Inter-Area</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="add-border-right align-middle text-center">Informe</th>
            <!-- Subcolumnas de Informe de Area -->
            <th class="align-middle text-center">Fecha</th>
            <th class="align-middle text-center">Solicitante</th>
            <th class="align-middle text-center">Informe Area</th>
            <th class="align-middle text-center">Registros de Ensayo</th>
            <th class="add-border-right align-middle text-center">Estado</th>
            <!-- Subcolumnas de Administracion -->
            <th class="add-border-right align-middle text-center">Formato</th>
            <!-- Subcolumnas de Servicios Tecnologicos -->
            <th class="add-border-right align-middle text-center">Revision</th>
            <!-- Subcolumnas de Responsable Area -->
            <th class="add-border-right align-middle text-center">Firma</th>
            <!-- Subcolumnas de Direccion -->
            <th class="add-border-right align-middle text-center">Firma</th>
            <!-- Subcolumnas de Archivo -->
            <th  v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">Archivar</th>
          </tr>
        </thead>
        <tbody >
          <tr v-for="(fila, index) in filas" :key="index">

            <!-- Columna Solicitud de Servicio -->

            <td v-if="isAdminOrTecnologicoOrDireccion">{{ fila.nro_dataServicio }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" style="white-space: nowrap;">{{ fila.area_tematica }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion">{{ fila.nro_presupuesto }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion"><i class="bi bi-file-earmark-check-fill text-success"  style="cursor: pointer;" @click="abrirDataServicio(fila.nro_dataServicio)"></i></td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right">
              <template v-if="fila.adjunto_solicitudServicio === null">
                <div v-if="isServiciosTecnologicos" class="custom-file">
                  <label class="custom-file-label"  style="cursor: pointer;" :for="'fileInputAdjuntoSolicitud-' + index">
                    <i class="bi bi-paperclip"></i>
                  </label>
                  <input :id="'fileInputAdjuntoSolicitud-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoSolicitud($event, fila.nro_dataServicio)">
                </div>
                <div v-else> 
                      <i class="bi bi-stopwatch"></i>
                </div>
              </template>
              <template v-else>
                <i class="bi bi-file-earmark-word" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_solicitudServicio)"></i>
              </template>
            </td>

            <!-- Columna Legajo -->

            <td v-if="isAdminOrTecnologicoOrDireccion">{{ fila.nro_legajo }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="fecha-columna">{{ fila.fecha_legajo }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="fila.dataServicio_completo && !fila.nro_legajo">
                <div v-if="isAdministracion">
                  <i class="bi bi-plus-square"  style="cursor: pointer;" @click="obtenerRangoLab(fila.nro_circuito)"></i>
                </div>
                <div v-else>
                      <i class="bi bi-stopwatch"></i>
                </div>
              </template>
              <template v-else-if="fila.dataServicio_completo && fila.nro_legajo">
                  <i class="bi bi-file-earmark-check-fill text-success"  style="cursor: pointer;" @click="abrirLegajo(fila)"></i>
              </template>
              <template v-else>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="fila.nro_legajo && !fila.adjunto_factura">
                  <!-- Si nro_legajo está completo y adjunto_factura está vacío, mostrar el botón de cargar archivo -->
                  <div v-if="isAdministracion" class="custom-file">
                      <!-- El icono de Bootstrap es clicleable y activa el input de tipo file -->
                      <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoFactura-' + index">
                          <i class="bi bi-paperclip"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputAdjuntoFactura-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoFactura($event, fila.nro_legajo, fila.nro_circuito)">
                  </div>
                  <div v-else>
                      <i class="bi bi-stopwatch"></i>
                  </div>
              </template>
              <template v-else-if="fila.nro_legajo && fila.adjunto_factura">
                  <!-- Si nro_legajo está completo y adjunto_factura está completo, mostrar el icono del archivo -->
                  <i class="bi bi-file-earmark-word" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_factura)"></i>
              </template>
              <template v-else>
                  <!-- Si nro_legajo está vacío, entonces adjunto_factura también debe estar vacío -->
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
                <div v-if="fila.pago !== undefined && fila.pago !== null">
                  <div v-if="isAdministracion">
                      <!-- Mostrar el valor de fila.pago -->
                      <span v-if="fila.pago === 0" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">0%</span>
                      <span v-else-if="fila.pago === 50" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">50%</span>
                      <span v-else-if="fila.pago === 100" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">100%</span>
                  </div>
                  <div v-else>
                      <span v-if="fila.pago === 0">0%</span>
                      <span v-else-if="fila.pago === 50">50%</span>
                      <span v-else-if="fila.pago === 100">100%</span>
                  </div>
                </div>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right">
                <div v-if="isAdministracion">
                  <span @click="abrirModalPlazoPago(fila)" style="cursor: pointer;">
                    {{ fila.plazo_pago }}
                  </span>
                </div>
                <div v-else>
                  {{ fila.plazo_pago }}
                </div>
            </td>

            <!-- Columna Recepcion -->

            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="(fila.nros_remitos === null) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <div v-if="isServiciosTecnologicos">
                  <i class="bi bi-plus-square" style="cursor: pointer;" @click="abrirModalRemito(fila)"></i>
                </div>
              </template>
              <template v-if="(fila.remitos !== null) && (fila.estado_recepcion == 'parcial' || fila.estado_recepcion == 'total')">
                <div v-if="isServiciosTecnologicos">
                  <span @click="abrirModalRemito(fila)" style="cursor: pointer;">
                    {{ fila.nros_remitos }}
                  </span>
                </div>
                <div v-else>
                  <span>
                    {{ fila.nros_remitos }}
                  </span>
                </div>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <div>
                <span v-if="(fila.pago == 50 ||fila.pago == 100) && (fila.estado_recepcion !== undefined && fila.estado_recepcion !== null)">
                    <div v-if="isServiciosTecnologicos">
                      <span v-if="fila.estado_recepcion === 'sin_llegar'" class="no-wrap-column" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Sin Llegar</span>
                      <span v-else-if="fila.estado_recepcion === 'parcial'" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Parcial</span>
                      <span v-else-if="fila.estado_recepcion === 'total'"  @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Total</span>
                    </div> 
                    <div v-else>
                      <span v-if="fila.estado_recepcion === 'sin_llegar'" class="no-wrap-column">Sin Llegar</span>
                      <span v-else-if="fila.estado_recepcion === 'parcial'">Parcial</span>
                      <span v-else-if="fila.estado_recepcion === 'total'">Total</span>
                    </div>
                </span>
                <span v-else-if="isServiciosTecnologicos" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">&nbsp;</span>
              </div>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right">
              <div v-if="isServiciosTecnologicos">
                <span v-if="fila.legajo_completo" @click="abrirModalPlazoMuestras(fila)" style="cursor: pointer;">
                  {{ fila.plazo_muestras }}
                </span>
                <span v-else>
                  <!-- Este span estará vacío -->
                </span>
              </div>
              <div v-else>
                <span v-if="fila.legajo_completo">
                  {{ fila.plazo_muestras }}
                </span>
                <span v-else>
                  <!-- Este span estará vacío -->
                </span>
              </div>  
            </td>

            <!-- Columna Orden de Servicio -->

            <td>
              <template v-if="(fila.nro_ordenServicio  !== '' ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <span class="no-wrap-column">
                  {{ fila.fecha_ordenServicio }}
                </span>
              </template>
              <template v-else>
              
              </template>
            </td>
            <td>
              <template v-if="(fila.ordenServicio_completo === '' || fila.ordenServicio_completo === false) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                  <div v-if="isServiciosTecnologicos">
                      <i class="bi bi-plus-square" style="cursor: pointer;" @click="abrirModalCrearOrdenServicio(fila)"></i>
                  </div>
                  <div v-else>
                      <i class="bi bi-stopwatch"></i>
                  </div>
              </template>
              <template v-if="(fila.ordenServicio_completo  === true ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <i class="bi bi-clipboard2"  style="cursor: pointer;" @click="abrirOrdenServicio(fila)"></i>
              </template>
            </td>
            <td class="add-border-right">
              <template v-if="(fila.ordenServicio_completo  === true ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <div v-if="isServiciosTecnologicos">
                  <span @click="abrirModalPlazoOrdenServicio(fila)" style="cursor: pointer;">
                    {{ fila.plazo_estimado }}
                  </span>
                </div>
                <div v-else>
                  <span>
                    {{ fila.plazo_estimado }}
                  </span>
                </div>
              </template>
              <template v-else>
                
              </template>
            </td>

            <!-- Columna Inter Area -->

            <td v-if="isTecnologicoOrDireccionOrArea">
              <template v-if="(fila.nro_solicitudInterarea !== '')">
                <span class="no-wrap-column">
                  <div style="display: flex; flex-direction: column;">
                    {{ fila.fecha_solicitudInterarea }}
                  </div>
                </span>
              </template>
              <template v-else>
              <!-- vacio -->
              </template>
            </td>
            <td v-if="isTecnologicoOrDireccionOrArea">
              <template v-if="(fila.ordenServicio_completo === '') || (fila.ordenServicio_completo === false)">
                  <!-- vacio -->
              </template>
              <template v-if="(fila.ordenServicio_completo === true) && (fila.nro_solicitudInterarea === '')">
                  <div v-if="isAdminOrTecnologicoOrDireccion">
                    -
                  </div>
                  <div v-else style="display: flex; flex-direction: column;">
                    <i class="bi bi-plus-square" style="cursor: pointer;" @click="abrirModalCrearSolicitudInterArea(fila)"></i> 
                  </div>
              </template>
              <template v-else-if="(fila.ordenServicio_completo === true) && (fila.nro_solicitudInterarea !== '')">
                <span>
                  <i class="bi bi-clipboard2"   style="cursor: pointer;" @click="abrirSolicitudInterArea(fila)"></i>
                </span>
              </template>
            </td>
            <td v-if="isTecnologicoOrDireccionOrArea" style="white-space: nowrap;">
              {{ fila.inter_areaTematica }}
            </td>
            <td v-if="isTecnologicoOrDireccionOrArea" class="add-border-right">
              <template v-if="(fila.nro_solicitudInterarea !== '') && (fila.adjunto_informeInterarea === '')">
                <div v-if="isAdminOrTecnologicoOrDireccion">
                      <i class="bi bi-stopwatch"></i>
                </div>
                <div v-else class="custom-file">
                  <label class="custom-file-label"  style="cursor: pointer;" :for="'fileInputAdjuntoInformeInterarea-' + index">
                    <i class="bi bi-paperclip"></i>
                  </label>
                  <input :id="'fileInputAdjuntoInformeInterarea-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeInterarea($event, fila)">
                </div>
              </template>
              <template v-else-if="(fila.nro_solicitudInterarea !== '') && (fila.adjunto_informeInterarea !== '')">
                <i class="bi bi-file-earmark-word" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_informeInterarea)"></i>
              </template>
            </td>

            <!-- Columna Informe de Area -->

            <td>
              <template v-if="(fila.adjunto_informeArea)">
                <span class="no-wrap-column">
                  {{ fila.fecha_informeArea }}
                </span>
              </template>
              <template v-else>

              </template>
            </td>
            <td style="white-space: nowrap;">
              <template v-if="(fila.ordenServicio_completo  === true ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                {{ fila.nombre_solicitante }}
              </template>
              <template v-else>
              
              </template>
            </td>
            <td>
              <template v-if="(fila.adjunto_informeArea === '') && (fila.ordenServicio_completo === true)">
                  <div v-if="isAdminOrTecnologicoOrDireccion">
                      <i class="bi bi-stopwatch"></i>
                  </div>
                  <div v-else class="custom-file">
                      <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeArea-' + index">
                          <i class="bi bi-paperclip"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputAdjuntoInformeArea-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeArea($event, fila)">
                  </div>
              </template>
              <template v-else-if="fila.adjunto_informeArea !== ''">
                <div v-if="fila.estado_informeArea === 'total'">
                  <i class="bi bi-file-earmark-word" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_informeArea)"></i>
                </div>
                <div v-else>
                  <i class="bi bi-file-earmark-word" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_informeArea)"></i>
                  <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeArea-' + index">
                          <i class="bi bi-paperclip"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputAdjuntoInformeArea-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeArea($event, fila)">
                </div>
              </template>

              <template v-if="(fila.informes_parciales  !== '' ) && (fila.informes_parciales !== 'null')">
                {{ fila.informes_parciales }}
              </template>

            </td>
            
            <!-- Registros de Ensayo -->
            <td>
              <template v-if="(fila.adjunto_informeArea !== '') || (fila.adjunto_informeArea !== null)">
                <div v-if="fila.registros_ensayo" style="position: relative;">
                  <!-- Icono principal -->
                  <i class="bi bi-folder-check" style="cursor: pointer;" @click="toggleOpciones(index)"></i>

                  <!-- Opciones flotantes en semi-círculo -->
                    <div v-if="filaSeleccionada === index" class="opciones-flotantes">
                        <div class="opcion" style="--rotation: -30deg;">
                          <i class="bi bi-eye" @click="abrirArchivo(fila.registros_ensayo)"></i>
                        </div>

                        <!-- Ícono que llama a cargarRegistrosEnsayo -->
                        <div class="opcion" style="--rotation: 0deg;">
                          <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputRegistrosEnsayo-' + index">
                            <i class="bi bi-upload"></i>
                          </label>
                          <input :id="'fileInputRegistrosEnsayo-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarRegistrosEnsayo($event, fila)">
                        </div>
                    </div> 
                </div> 
                <div v-else>
                  <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputRegistrosEnsayo-' + index">
                          <i class="bi bi-folder-plus"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputRegistrosEnsayo-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarRegistrosEnsayo($event, fila)">
                </div>
              </template>
            </td>

            

            <td class="add-border-right">
              <template v-if="fila.estado_informeArea === 'sin_informe'">
                <!-- Si el estado es 'sin_informe', muestra en blanco -->
              </template>
              <template v-else-if="fila.estado_informeArea === 'parcial'">
                <div v-if="isAreaJefe || isAreaStandard">
                  <span @click="cambiarEstadoInformeArea(fila)" style="cursor: pointer;">Parcial</span>
                </div>
                <div v-else>
                  <span>Parcial</span>
                </div>
              </template>
              <template v-else-if="fila.estado_informeArea === 'total'">
                <div v-if="isAreaJefe || isAreaStandard">
                  <span @click="cambiarEstadoInformeArea(fila)" style="cursor: pointer;">Total</span>
                </div>
                <div v-else>
                  <span>Total</span>
                </div>
              </template>
            </td>

            <!-- Columna Administracion - Formato -->
            <td class="add-border-right">
              <template v-if="(fila.estado_informeArea === 'parcial') || (fila.estado_informeArea === 'total')">
                  <template v-if="(fila.adjunto_informeServicio === '') || (fila.adjunto_informeServicio === null) && (fila.corregir === false)">
                      <div v-if="isAdministracion" class="custom-file">
                        <label class="custom-file-label"  style="cursor: pointer;" :for="'fileInputAdjuntoInformeServicio-' + index">
                          <i class="bi bi-paperclip"></i>
                        </label>
                        <input :id="'fileInputAdjuntoInformeServicio-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeServicio($event, fila)">
                      </div>
                      <div v-else>
                        <i class="bi bi-stopwatch"></i>
                      </div>
                  </template>
                  <template v-if="(fila.adjunto_informeServicio !== '') && (fila.adjunto_informeServicio !== null ) && (fila.corregir === false)">
                    <i class="bi bi-check-lg" style="color: green;"></i>
                  </template>
                  <template v-if="(fila.corregir === true)">


                    <div v-if="isAdministracion" style="position: relative; justify-content: center; align-items: center;">

                        <!-- Icono principal -->
                        <i class="bi bi-filetype-pdf" style="cursor: pointer;" @click="toggleOpciones(index)"></i>

                        <!-- Opciones flotantes en semi-círculo -->
                        <div v-if="filaSeleccionada === index" class="opciones-flotantes">
                            <div class="opcion" style="--rotation: -30deg;">
                              <i class="bi bi-eye" @click="abrirArchivo(fila.adjunto_informeServicio)"></i>
                            </div>

                            <!-- Ícono que llama a cargarAdjuntoInformeServicio -->
                            <div class="opcion" style="--rotation: 0deg;">
                              <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeServicio-' + index">
                                <i class="bi bi-upload"></i>
                              </label>
                              <input :id="'fileInputAdjuntoInformeServicio-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeServicio($event, fila)">
                            </div>
                        </div> 
                        <i class="bi bi-backspace-fill text-danger" @click="abrirModalCorreccionesInformeServicio(fila)" style="cursor: pointer; font-size: 0.8em;"></i>
                      </div> 
                      <div v-else>
                        <i class="bi bi-stopwatch"></i>
                      </div>
                     
                  </template>
              </template>
            </td>
            

            <!-- Columna Servicios Tecnologicos - Revision -->
            <td class="add-border-right">
              <template v-if="(fila.adjunto_informeServicio !== '') && (fila.adjunto_informeServicio !== null ) && (fila.revision === false) && (fila.firma_area === false) && (fila.firma_direccion === false) && (fila.corregir === false)">
                <div v-if="isServiciosTecnologicos" style="position: relative;">
                  <!-- Icono principal -->
                  <i class="bi bi-filetype-pdf" style="cursor: pointer;" @click="toggleOpciones(index)"></i>

                  <!-- Opciones flotantes en semi-círculo -->
                  <div v-if="filaSeleccionada === index" class="opciones-flotantes">
                    <div class="opcion" style="--rotation: -30deg;">
                      <i class="bi bi-eye" @click="abrirArchivo(fila.adjunto_informeServicio)"></i>
                    </div>

                    <!-- Ícono que llama a cargarAdjuntoInformeServicio -->
                    <div class="opcion" style="--rotation: 0deg;">
                      <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeServicio-' + index">
                        <i class="bi bi-upload"></i>
                      </label>
                      <input :id="'fileInputAdjuntoInformeServicio-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeServicio($event, fila)">
                    </div>

                    <div class="opcion" style="--rotation: 30deg;">
                      <i class="bi bi-check-circle" @click="abrirModalRevision(fila)"></i>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <i class="bi bi-stopwatch"></i>
                </div>
              </template>
              <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.corregir === false)">
                <i class="bi bi-check-lg" style="color: green;"></i>
              </template>
            </td>

            <!-- Columna Responsable Area - Firma -->
            <td class="add-border-right">
                <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.firma_area === false) && (fila.firma_direccion === false) && (fila.corregir === false)">
                  <div v-if="isAreaJefe" style="position: relative;">
                    <!-- Icono principal -->
                    <i class="bi bi-filetype-pdf" style="cursor: pointer;" @click="toggleOpciones(index)"></i>

                    <!-- Opciones flotantes en semi-círculo -->
                    <div v-if="filaSeleccionada === index" class="opciones-flotantes">
                      <div class="opcion" style="--rotation: -30deg;">
                        <i class="bi bi-eye" @click="abrirArchivo(fila.adjunto_informeServicio)"></i>
                      </div>

                      <!-- Ícono que llama a cargarAdjuntoInformeServicio -->
                      <div class="opcion" style="--rotation: 0deg;">
                        <i class="bi bi-exclamation-triangle" @click="abrirModalAdvertirCorrecciones(fila)"></i>
                      </div>

                      <div class="opcion" style="--rotation: 30deg;">
                        <i class="bi bi-pen" @click="abrirModalFirmaResponsableArea(fila)"></i>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <i class="bi bi-stopwatch"></i>
                  </div>
                </template>
                <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.firma_area === true)">
                  <i class="bi bi-check-lg" style="color: green;"></i>
                </template>
            </td>

            <!-- Columna Direccion - Firma-->
            <td class="add-border-right">
                <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.firma_area === false) && (fila.firma_direccion === false)">
              
                </template>
                <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.firma_area === true) && (fila.firma_direccion === false)">
                  <div v-if="isDireccion">
                    <i class="bi bi-filetype-pdf" @click="abrirArchivo(fila.adjunto_informeServicio)" style="cursor: pointer;"></i>
                    <label class="custom-file-label"  style="cursor: pointer;" :for="'fileInputAdjuntoInformeServicioFirmado-' + index">
                      <i class="bi bi-paperclip"></i>
                    </label>
                    <input :id="'fileInputAdjuntoInformeServicioFirmado-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeServicioFirmado($event, fila)">
                    <i class="bi bi-pen" style="cursor: pointer;" @click="abrirModalFirmaDireccion(fila)"></i>
                  </div>
                  <div v-else>
                    <i class="bi bi-stopwatch"></i>
                  </div>
                </template>
                <template v-if="(fila.adjunto_informeServicio !== '') && (fila.revision === true) && (fila.firma_area === true) && (fila.firma_direccion === true)">
                  <i class="bi bi-check-lg" style="color: green;"></i>
                </template>
            </td>

            <!-- Columna Archivo -->
            <td  v-if="isAdminOrTecnologicoOrDireccion">
              <button @click="abrirModalArchivar(fila)" class="btn btn-link"><i class="bi bi-archive-fill"></i></button>
            </td>
            
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modales Data Servicio -->
    <div class="modal" :class="{ 'show': mostrarModalDataServicio }" id="modalAbrirDataServicio">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <div class="modal-logo"></div>
            <button type="button" class="btn-close" @click="cerrarModalDataServicio" aria-label="Close"></button>
          </div>
          <!-- Modal Body -->
          <div class="modal-body">
            <form class="was-validated">

              <div class="d-flex justify-content-between align-items-center">
                  <h1 class="modal-title fs-5 fw-bold mb-0">Data Servicio N° {{ nroDataServicio }}</h1>
                  <div class="mb-0 ms-3">
                      <span class="form-label">Fecha: <strong>{{ fechaDataServicio }}</strong></span>
                  </div>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">N° Presupuesto:</label>
                <span><strong>{{ nroPresupuestoDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Area Temática:</label>
                <span><strong>{{ areaDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Solicitante:</label>
                <span><strong>{{ solicitanteDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Obra:</label>
                <span><strong>{{ obraDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Cantidad Num Laboratorios:</label>
                <span><strong>{{ cantNumLabsDataServicio }}</strong></span>
              </div>
              
              <div class="mb-3">
                <label class="form-label text-left">Plazo Estimado:</label>
                <span><strong>{{ plazoEstimadoDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Muestras:</label>
                <span><strong>{{ muestrasDataServicio }}</strong></span>
              </div>

              <div class="mb-3">
                <label class="form-label text-left">Arancel:</label>
                <span><strong>{{ arancelDataServicio }}</strong></span>
              </div>
              
              <div class="mb-3">
                <label for="observacionesDataServicio" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesDataServicio" type="text" class="form-control" id="observacionesDataServicio" name="observacionesDataServicio" readonly required />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Legajo -->
    <div class="modal" :class="{ 'show': mostrarModalCrearLegajo }" id="modalCrearLegajo">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Nuevo Legajo</h1>
            <button type="button" class="btn-close" @click="cerrarModalCrearLegajo" aria-label="Close"></button>
          </div>
          <!-- Modal Body -->
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fecha_nuevoLegajo" class="form-label text-left">Fecha:</label>
                  <input v-model="nuevoLegajo.fecha_legajo" type="date" readonly class="form-control" id="fecha_nuevoLegajo" name="fecha_nuevoLegajo" required />
              </div>

              <div class="mb-3">
                <label for="rango_nums" class="form-label text-left">Rango Numeros de Laboratorios:</label>
                <input v-model="nuevoLegajo.rangos_laboratorios" type="text" class="form-control" id="rango_nums" name="rango_nums" readonly required />
              </div>
              <button type="button" class="btn btn-primary" @click="crearLegajo">Crear</button>
              <button type="button" class="btn btn-secondary" @click="cerrarModalCrearLegajo">Cerrar</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalLegajo }" id="modalAbrirLegajo">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <div class="modal-logo"></div>
            <div><i class="bi bi-download" style="cursor: pointer;" @click="descargarLegajoPDF"></i></div>
            <button type="button" class="btn-close" @click="cerrarModalLegajo" aria-label="Close"></button>
          </div>
          <!-- Modal Body -->
          <div class="modal-body">
            <form class="was-validated">
              <h1 class="modal-title fs-5 fw-bold">Legajo N° {{ nroLegajo }}/{{ añoLegajo }}</h1>
              <div class="mb-3">
                  <label for="fechaLegajo" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaLegajo" type="date" readonly class="form-control" id="fechaLegajo" name="fechaLegajo" required />
              </div>

              <div class="mb-3">
                <label for="rangosLaboratorios" class="form-label text-left">Rango Numeros de Laboratorios:</label>
                <input v-model="rangosLaboratorios" type="text" class="form-control" id="rangosLaboratorios" name="rangosLaboratorios" readonly required />
              </div>

              <div class="mb-3">
                <label for="nombreSolicitante" class="form-label text-left">Solicitante:</label>
                <input v-model="nombreSolicitante" type="text" class="form-control" id="nombreSolicitante" name="nombreSolicitante" readonly required />
              </div>
            </form>
          </div>
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalPagoLegajo }" id="mostrarModalPagoLegajo">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Pago de Legajo</h4>
            <button type="button" class="btn-close" @click="cerrarModalPagoLegajo"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="0" name="tipoPagoLegajo">
              <label class="form-check-label">0 %</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="50" name="tipoPagoLegajo">
              <label class="form-check-label">50 %</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="100" name="tipoPagoLegajo">
              <label class="form-check-label">100 %</label>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="guardarPagoLegajo(pagoLegajoNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalPagoLegajo">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="modal" :class="{ 'show': mostrarModalPlazoPago }" id="mostrarModalPlazoPago">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Plazo Pago de Legajo</h4>
            <button type="button" class="btn-close" @click="cerrarModalPlazoPago"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="plazoLegajo">Ingrese Nuevo Plazo de Pago de Legajo:</label>
              <input 
                id="plazoLegajo" 
                class="form-control" 
                type="number" 
                v-model.number="plazoPagoNuevo" 
                @input="validarNumeroEntero" 
                min="0" 
                step="1"
                required>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="cambiarPlazoPago(plazoPagoNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalPlazoPago">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Recepcion -->
    <div class="modal" :class="{ 'show': mostrarModalRemito }" id="mostrarModalRemito">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Remito</h4>
            <button type="button" class="btn-close" @click="cerrarModalRemito"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="nrosRemitos">Ingrese nuevo Numero de Remito:</label>
              <input type="text" v-model="remitoNuevo" required>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="cambiarRemito(remitoNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRemito">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalEstadoMuestras }" id="modalEstadoMuestras">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Estado de muestras</h4>
            <button type="button" class="btn-close" @click="cerrarModalEstadoMuestras"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="estadoMuestrasNuevo" value="sin_llegar" name="estadoMuestras">
              <label class="form-check-label">Sin Llegar</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="estadoMuestrasNuevo" value="parcial" name="estadoMuestras">
              <label class="form-check-label">Parcial</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="estadoMuestrasNuevo" value="total" name="estadoMuestras">
              <label class="form-check-label">Total</label>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="guardarEstadoMuestras(estadoMuestrasNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalEstadoMuestras">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalPlazoMuestras }" id="mostrarModalPlazoMuestras">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Plazo Muestras</h4>
            <button type="button" class="btn-close" @click="cerrarModalPlazoMuestras"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="plazoMuestras">Ingrese Nuevo Plazo de Recepcion de Muestras:</label>
              <input 
                id="plazoMuestras" 
                class="form-control" 
                type="number" 
                v-model.number="plazoMuestrasNuevo" 
                @input="validarNumeroEntero" 
                min="0" 
                step="1"
                required>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="cambiarPlazoMuestras(plazoMuestrasNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalPlazoMuestras">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Orden de Servicio -->
    <div class="modal" :class="{ 'show': mostrarModalCrearOrdenServicio }" id="mostrarModalCrearOrdenServicio">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Crear Orden de Servicio</h4>
            <button type="button" class="btn-close" @click="cerrarModalCrearOrdenServicio"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div>
              Desea crear el ST-05 Orden de Servicio correspondiente?
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="crearOrdenServicio(fila); cerrarModal">Si</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCrearOrdenServicio">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalOrdenServicio }" id="mostrarModalOrdenServicio">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Orden de Servicio N°{{ nroOS }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalOrdenServicio" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fechaOS" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaOS" type="date" readonly class="form-control" id="fechaOS" name="fechaOS" required />
              </div>
              
              <div class="mb-3">
                <label for="areaOS" class="form-label text-left">Area Tematica</label>
                <input v-model="areaOS" type="text" class="form-control" id="areaOS" name="areaOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="legajoOS" class="form-label text-left">N° Legajo:</label>
                <input v-model="legajoOS" type="text" class="form-control" id="legajoOS" name="legajoOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="rangosOS" class="form-label text-left">Rangos Laboratorios:</label>
                <input v-model="rangosOS" type="text" class="form-control" id="rangosOS" name="rangosOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="plazoOS" class="form-label text-left">Plazo Estimado:</label>
                <input v-model="plazoOS" type="text" class="form-control" id="plazoOS" name="plazoOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="solicitanteOS" class="form-label text-left">Solicitante:</label>
                <input v-model="solicitanteOS" type="text" class="form-control" id="solicitanteOS" name="solicitanteOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="servicioOS" class="form-label text-left">Servicios Solicitados:</label>
                <table class="table">
                  <thead>
                    <tr>
                      <th style="text-align: left;">Servicio</th>
                      <th style="text-align: center !important;">Cantidad</th>
                    </tr>
                  </thead>
                  <tbody>
                    <!-- Iterar sobre servicioOS para mostrar cada servicio y cantidad -->
                    <tr v-for="(servicio, index) in servicioOS" :key="index">
                      <td style="text-align: left;">{{ servicio.servicio }}</td>
                      <td>{{ servicio.cant }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="mb-3">
                <label for="muestrasOS" class="form-label text-left">Muestras:</label>
                <input v-model="muestrasOS" type="text" class="form-control" id="muestrasOS" name="muestrasOS" readonly required />
              </div>

              <div class="mb-3">
                <label for="observacionesOS" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesOS" type="text" class="form-control" id="observacionesOS" name="observacionesOS" readonly required />
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalPlazoOrdenServicio }" id="mostrarModalPlazoOrdenServicio">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Plazo Estimado</h4>
            <button type="button" class="btn-close" @click="cerrarModalPlazoOrdenServicio"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="plazoEstimado">Ingrese Nuevo Plazo de Estimado para la Orden de Servicio:</label>
              <input 
                id="plazoEstimado" 
                class="form-control" 
                type="number" 
                v-model.number="plazoEstimadoNuevo" 
                @input="validarNumeroEntero" 
                min="0" 
                step="1"
                required>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="cambiarPlazoOrdenServicio(plazoEstimadoNuevo); cerrarModal">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalPlazoOrdenServicio">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Informe Area -->
    <div class="modal" :class="{ 'show': mostrarModalEstadoInformeArea }" id="mostrarModalEstadoInformeArea">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Estado de Informe de Area</h4>
            <button type="button" class="btn-close" @click="cerrarModalEstadoInformeArea"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="estadoInformeAreaNuevo" value="parcial" name="estadoInformeAreaNuevo">
              <label class="form-check-label">Parcial</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="estadoInformeAreaNuevo" value="total" name="estadoInformeAreaNuevo">
              <label class="form-check-label">Total</label>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="guardarEstadoInformeArea(estadoInformeAreaNuevo)">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalEstadoInformeArea">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Inter Area -->
    <div class="modal" :class="{ 'show': mostrarModalCrearSolicitudInterArea }" id="mostrarModalCrearSolicitudInterArea">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Crear Solicitud Inter Area</h1>
            <button type="button" class="btn-close" @click="cerrarModalCrearSolicitudInterArea" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fecha_solicitudInterarea" class="form-label text-left">Fecha:</label>
                  <input v-model="nuevaSolicitudInterarea.fecha_solicitudInterarea" type="date" class="form-control" id="fecha_solicitudInterarea" name="fecha_solicitudInterarea" readonly required />
              </div>
              
              <div class="mb-3">
                <label for="areaTematica_origen" class="form-label text-left">Area Temática:</label>
                <input v-model="nuevaSolicitudInterarea.areaTematica_origen" type="text" class="form-control" id="areaTematica_origen" name="areaTematica_origen" readonly required />
              </div>

              <div class="mb-3">
                <label for="inter_areaTematica" class="form-label text-left">Inter Area Temática</label>
                <select v-model="nuevaSolicitudInterarea.inter_areaTematica" class="form-select" id="inter_areaTematica" name="inter_areaTematica" required>
                  <option v-for="(option, key) in inter_areaTematicaOptions" :key="key" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
              </div>
              
              {{console.log('serviciosDisponibles dentro del modal', serviciosDisponibles)}}

              <div class="mb-3">
                <label for="servicios_solicitudInterarea" class="form-label text-left">Seleccionar los Servicios para el Inter Area correspondiente:</label>
                <select v-model="servicioSeleccionadoTemporal" @change="moverServicioSeleccionado" multiple class="form-control" id="servicios_solicitudInterarea" style="width: calc(100% - 20px); height: 150px; white-space: nowrap; overflow-x: auto; margin: 0 10px;">
                  <option v-for="servicio in serviciosDisponibles.servicio_solicitado" :key="servicio.servicio" :value="servicio" :title="servicio.servicio">
                    {{ servicio.cant }} {{ servicio.servicio }}(cod: {{ servicio.nro_servicio}})
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="servicios_seleccionados" class="form-label text-left">Servicios Seleccionados:</label>
                <div>
                  <div v-for="(servicio, index) in serviciosSeleccionados" :key="index" style="margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                    <span>{{ servicio.cant }} {{ servicio.servicio }}(cod: {{ servicio.nro_servicio}})</span>
                    <button type="button" @click="eliminarServicioSeleccionado(index)" class="btn btn-danger btn-sm">X</button>
                  </div>
                </div>
              </div>

              {{console.log('servicios seleccionados dentro del modal', serviciosSeleccionados)}}

              <div class="mb-3">
                <label for="num_labs" class="form-label text-left">Numeros de Laboratorio para Inter Area (opcional):</label>
                <input v-model="nuevaSolicitudInterarea.num_labs" type="text" class="form-control" id="num_labs" name="num_labs"/>
              </div>

              <div class="mb-3">
                <label for="muestras_solicitudIa" class="form-label text-left">Muestras a entregar:</label>
                <input v-model="nuevaSolicitudInterarea.muestras_solicitudIa" type="text" class="form-control" id="muestras_solicitudIa" name="muestras_solicitudIa" required />
              </div>

              <div class="mb-3">
                <label for="observaciones_interArea" class="form-label text-left">Observaciones:</label>
                <input v-model="nuevaSolicitudInterarea.observaciones_interArea" type="text" class="form-control" id="observaciones_interArea" name="observaciones_interArea" />
              </div>
            </form>

            <!-- Modal Footer -->
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" @click="crearSolicitudInterArea(fila); cerrarModalCrearSolicitudInterArea">Crear</button>
              <button type="button" class="btn btn-secondary" @click="cerrarModalCrearSolicitudInterArea">Cancelar</button>
            </div>
            
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalSolicitudInterArea }" id="mostrarModalSolicitudInterArea">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5 fw-bold">Solicitud Inter Area N°{{ nroSolicitudInterArea }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalSolicitudInterArea" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                  <label for="fechaSolicitudInterArea" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaSolicitudInterArea" type="date" readonly class="form-control" id="fechaSolicitudInterArea" name="fechaSolicitudInterArea"/>
              </div>

              <div class="mb-3">
                <label for="areaTematicaOrigen" class="form-label text-left">Area Tematica Solicitante</label>
                <input v-model="areaTematicaOrigen" type="text" class="form-control" id="areaTematicaOrigen" name="areaTematicaOrigen" readonly required />
              </div>

              <div class="mb-3">
                <label for="interAreaSolicitudInterArea" class="form-label text-left">Inter Area Tematica</label>
                <input v-model="interAreaSolicitudInterArea" type="text" class="form-control" id="interAreaSolicitudInterArea" name="interAreaSolicitudInterArea" readonly/>
              </div>

              <div class="mb-3">
                <label for="servicioSolicitudInterArea" class="form-label text-left">Servicios Solicitados:</label>
                <table class="table">
                  <thead>
                    <tr>
                      <th style="text-align: left;">Servicio</th>
                      <th style="text-align: center !important;">Cantidad</th>
                    </tr>
                  </thead>
                  <tbody>
                    <!-- Iterar sobre servicioSolicitudInterArea para mostrar cada servicio y cantidad -->
                    <tr v-for="(servicio, index) in servicioSolicitudInterArea" :key="index">
                      <td style="text-align: left;">{{ servicio.servicio }}</td>
                      <td>{{ servicio.cant }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="mb-3">
                <label for="muestrasSolicitudInterArea" class="form-label text-left">Muestras:</label>
                <input v-model="muestrasSolicitudInterArea" type="text" class="form-control" id="muestrasSolicitudInterArea" name="muestrasSolicitudInterArea" readonly/>
              </div>

              <div class="mb-3">
                <label for="numLabsSolicitudInterArea" class="form-label text-left">Numeros Laboratorios:</label>
                <input v-model="numLabsSolicitudInterArea" type="text" class="form-control" id="numLabsSolicitudInterArea" name="numLabsSolicitudInterArea" readonly/>
              </div>

              <div class="mb-3">
                <label for="observacionesSolicitudInterArea" class="form-label text-left">Observaciones:</label>
                <input v-model="observacionesSolicitudInterArea" type="text" class="form-control" id="observacionesSolicitudInterArea" name="observacionesSolicitudInterArea" readonly/>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Formato Adminsitracion -->
    <div v-if="mostrarModalPDFpreliminar" class="pdf-modal">
      <div class="pdf-modal-content">
        <span @click="cerrarModalPDFpreliminar" class="pdf-close">&times;</span>
        <iframe :src="urlPdf" width="100%" height="600px" frameborder="0" style="border: none;"></iframe>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalCorreccionesInformeServicio }" id="mostrarModalCorreccionesInformeServicio">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Correcciones</h4>
            <button type="button" class="btn-close" @click="cerrarModalCorreccionesInformeServicio"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <p v-if="correcciones">{{ correcciones }}</p>
              <p v-else>No hay correcciones disponibles.</p>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="corregirInformeServicio(); cerrarModalCorreccionesInformeServicio">Corregido</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCorreccionesInformeServicio">Cerrar</button>
          </div>
        </div>
      </div>
    </div>


    <!-- Modales Revision -->
    <div class="modal" :class="{ 'show': mostrarModalRevision }" id="mostrarModalRevision">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Revision</h4>
            <button type="button" class="btn-close" @click="cerrarModalRevision"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div>
              Revision correcta?
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="confirmarRevision(fila); cerrarModal">Si</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRevision">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Firma Responsable Area -->

    <div class="modal" :class="{ 'show': mostrarModalAdvertirCorrecciones }" id="mostrarModalAdvertirCorrecciones">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Advertir Correcciones</h4>
            <button type="button" class="btn-close" @click="cerrarModalAdvertirCorrecciones"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="correcciones">Ingrese observaciones o correcciones sobre el informe:</label>
              <textarea 
                id="correcciones" 
                class="form-control" 
                v-model="correccionesNuevas" 
                rows="5" 
                placeholder="Escriba aquí las correcciones..."
                required>
              </textarea>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="advertirCorrecciones(correccionesNuevas); cerrarModal">Advertir Correcciones</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalAdvertirCorrecciones">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalFirmaResponsableArea }" id="mostrarModalFirmaResponsableArea">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Firma Responsable del Area</h4>
            <button type="button" class="btn-close" @click="cerrarModalFirmaResponsableArea"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div>
              Firmar?
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="confirmarFirmaResponsableArea(fila); cerrarModal">Si</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalFirmaResponsableArea">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Firma Dirección -->
    <div class="modal" :class="{ 'show': mostrarModalFirmaDireccion }" id="mostrarModalFirmaDireccion">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Firma Dirección</h4>
            <button type="button" class="btn-close" @click="cerrarModalFirmaDireccion"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div>
              Firmar?
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="confirmarFirmaDireccion(fila); cerrarModal">Si</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalFirmaDireccion">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Archivo -->
    <div class="modal" :class="{ 'show': mostrarModalArchivar }" id="mostrarModalArchivar">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Archivo</h4>
            <button type="button" class="btn-close" @click="cerrarModalArchivar"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div>
              Archivar?
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="enviarArchivar(fila); cerrarModal">Si</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalArchivar">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
   
    
</template>
  
<script>
  import { onMounted, ref} from 'vue';
  import axios from 'axios';

  export default {  
    components: {
    },
    setup() {

      // Setup General
      const filas = ref([]);
      const numeroCircuitoGlobal = ref(null);
      const showSuccessAlert = ref(false);
      const showErrorAlert = ref(false);

      // Determinar el rol del usuario
      const userRole = sessionStorage.getItem('role');
      // Determinar el area tematica del usuario
      const userAreaTematica = sessionStorage.getItem('area_tematica');

      // Función para verificar el rol y determinar qué columnas mostrar
      const isAdminOrTecnologicoOrDireccion = ref(userRole === 'servicios_tecnologicos' || userRole === 'administracion' || userRole === 'direccion');
      const isServiciosTecnologicos = ref(userRole === 'servicios_tecnologicos');
      const isAdministracion = ref(userRole === 'administracion');
      const isDireccion = ref(userRole === 'direccion');
      const isAreaJefe = ref(userRole === 'area_jefe');
      const isAreaStandard = ref(userRole === 'area_standard');
      const isTecnologicoOrDireccionOrArea = ref(userRole === 'servicios_tecnologicos' || userRole === 'direccion' || userRole === 'area_jefe' || userRole === 'area_standard' );

      // Setup Data Servicio
      const mostrarModalDataServicio = ref(false);
      const nroDataServicio = ref(); 
      const fechaDataServicio = ref();
      const obraDataServicio = ref();
      const cantNumLabsDataServicio = ref();
      const plazoEstimadoDataServicio = ref();
      const muestrasDataServicio = ref();
      const nroPresupuestoDataServicio = ref();
      const areaDataServicio = ref();
      const solicitanteDataServicio = ref();
      const arancelDataServicio = ref();
      const observacionesDataServicio = ref();
      // Setup Legajo
      const nuevoLegajo = ref({
        fecha_legajo: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
        rangos_laboratorios: '',
        pago: 0,
        plazo_pago: 30,
        nuevo_ultimo_numero: '',
        nro_circuito: null,
      });
      const nroLegajo = ref();
      const fechaLegajo = ref();
      const rangosLaboratorios = ref();
      const nombreSolicitante = ref();
      const añoLegajo = ref();
      const mostrarModalCrearLegajo = ref(false);
      const mostrarModalLegajo = ref(false);
      const mostrarModalPagoLegajo = ref(false);
      const mostrarModalPlazoPago = ref(false);
      // Setup Recepcion
      const nuevoRecepcion = ref ({
        nros_remitos: '',
        estado_recepcion: '',
        plazo_muestras: 30,
      });
      const remitoNuevo = ref();
      const mostrarModalRemito = ref(false);
      const mostrarModalEstadoMuestras = ref(false);
      const mostrarModalPlazoMuestras = ref(false);
      // Setup Orden de Servicio
      const nroOS = ref();
      const fechaOS = ref();
      const areaOS = ref();
      const legajoOS = ref();
      const rangosOS = ref();
      const plazoOS = ref();
      const solicitanteOS = ref();
      const servicioOS = ref();
      const muestrasOS = ref();
      const observacionesOS = ref();
      const mostrarModalCrearOrdenServicio = ref(false);
      const mostrarModalOrdenServicio = ref(false);
      const mostrarModalPlazoOrdenServicio = ref(false);
      // Setup Informe Area
      const mostrarModalEstadoInformeArea = ref(false);
      const guardarEstadoInformeArea = ref(null); 
      // Setup Inter Area
      const serviciosDisponibles = ref([]);
      const serviciosSeleccionados = ref([]);
      const servicioSeleccionadoTemporal = ref([]);

      const inter_areaTematicaOptions = ref([
          { value: 'durabilidad', label: 'Durabilidad' },
          { value: 'ensayos_mecanicos', label: 'Ensayos Mecánicos' },
          { value: 'geologia', label: 'Geología' },
          { value: 'hormigones', label: 'Hormigones' },
          { value: 'metalurgia', label: 'Metalurgia' },
          { value: 'patrimonio', label: 'Patrimonio' },
          { value: 'quimica', label: 'Química' },
          { value: 'tecnologia_vial', label: 'Tecnología Vial' },
          { value: 'estudios_especiales', label: 'Estudios Especiales' },
          { value: 'servicios_tecnologicos', label: 'Servicios Tecnológicos' },
          { value: 'direccion', label: 'Dirección' },
      ]);
      const nuevaSolicitudInterarea = ref({
        fecha_solicitudInterarea: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
        areaTematica_origen: '',
        inter_areaTematica: '',
        num_labs: '',
        servicios_solicitudInterarea: [
          {
            nro_servicio: '',
            servicio: '',
            cant: 0,
          }
        ],
        nro_circuito: null,
      });
      const nroSolicitudInterArea = ref();
      const fechaSolicitudInterArea = ref();
      const areaTematicaOrigen = ref();
      const interAreaSolicitudInterArea = ref();
      const muestrasSolicitudInterArea = ref();
      const numLabsSolicitudInterArea = ref();
      const observacionesSolicitudInterArea = ref();
      const servicioSolicitudInterArea = ref();
      
      const mostrarModalCrearSolicitudInterArea = ref(null);
      const mostrarModalSolicitudInterArea = ref(false);

      // Setup Formato Administracion
      const mostrarModalPDFpreliminar = ref(false);
      const urlPdf = ref('');
      const mostrarModalCorreccionesInformeServicio = ref(false);
      const correcciones = ref(null);

      // Setup Servicios Tecnologicos - Revision
      const mostrarModalRevision = ref(false);
      const mostrarOpciones = ref(false); // Ref para controlar la visibilidad de las opciones
      const filaSeleccionada = ref(null); // Ref para controlar la fila que muestra opciones

      // Setup Responsable del Area - Firma
      const mostrarModalAdvertirCorrecciones = ref(false);
      // const correccionesNuevas = ref('');
      const mostrarModalFirmaResponsableArea = ref(false);

      // Setup Direccion - Firma
      const mostrarModalFirmaDireccion = ref(false);

      // Setup Archivar
      const mostrarModalArchivar = ref(false);


      //methods

      const fetchData = () => {
          axios.get('api/encurso/obtener_todoencurso/')
            .then(response => {
              const data = response.data;

              // Obtener el área temática del usuario
              const userAreaTematica = formatAreaTematica(sessionStorage.getItem('area_tematica')); 

              // Ordenar los datos por nro_dataServicio
              const sortedSolicitudes = data.solicitudes.sort((a, b) => a.nro_dataServicio - b.nro_dataServicio);

              // Filtrar y construir las filas de la tabla
              const filteredFilas = sortedSolicitudes.reduce((acc, solicitud) => {
                // Buscar los objetos correspondientes
                const legajoCorrespondiente = data.legajos.find(legajo => legajo.nro_circuito === solicitud.nro_circuito);
                const recepcionCorrespondiente = data.recepciones.find(recepciones => recepciones.nro_circuito === solicitud.nro_circuito);
                const ordenCorrespondiente = data.ordenes_servicio.find(ordenes_servicio => ordenes_servicio.nro_circuito === solicitud.nro_circuito);
                const informeAreaCorrespondiente = data.informes_area.find(informes_area => informes_area.nro_circuito === solicitud.nro_circuito);
                const solicitudInterAreaCorrespondiente = data.solicitudes_inter_area.find(solicitudes_inter_area => solicitudes_inter_area.nro_circuito === solicitud.nro_circuito);
                const InformeInterareaCorrespondiente = data.informes_inter_area.find(informes_inter_area => informes_inter_area.nro_circuito === solicitud.nro_circuito);
                const InformeServicioCorrespondiente = data.informes_servicio.find(informes_servicio => informes_servicio.nro_circuito === solicitud.nro_circuito);

                // Construir la fila de la tabla combinando datos de solicitudes, legajos, recepciones, etc.
                const fila = {
                  // Solicitud
                  nro_dataServicio: solicitud.nro_dataServicio,
                  fecha_dataServicio: formatDate(solicitud.fecha_dataServicio),
                  area_tematica: formatAreaTematica(solicitud.area_tematica),
                  nro_presupuesto: solicitud.nro_presupuesto,
                  adjunto_solicitudServicio: solicitud.adjunto_solicitudServicio,
                  nro_circuito: solicitud.nro_circuito,
                  dataServicio_completo: solicitud.completo,
                  // Legajo
                  nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo : '',
                  fecha_legajo: legajoCorrespondiente ? formatDate(legajoCorrespondiente.fecha_legajo) : '',
                  adjunto_factura: legajoCorrespondiente ? legajoCorrespondiente.adjunto_factura : '',
                  pago: legajoCorrespondiente ? legajoCorrespondiente.pago : '',
                  plazo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago : '',
                  legajo_completo: legajoCorrespondiente ? legajoCorrespondiente.completo : '',
                  // Recepcion
                  nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.nros_remitos : '',
                  estado_recepcion: recepcionCorrespondiente ? recepcionCorrespondiente.estado_recepcion : '',
                  plazo_muestras: recepcionCorrespondiente ? recepcionCorrespondiente.plazo_muestras : '',
                  // Orden de Servicio
                  nro_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.nro_ordenServicio : '',
                  fecha_ordenServicio: ordenCorrespondiente ? formatDate(ordenCorrespondiente.fecha_ordenServicio) : '',
                  plazo_estimado: solicitud.plazo_estimado,
                  ordenServicio_completo: ordenCorrespondiente ? ordenCorrespondiente.completo : '',
                  // Informe Area
                  fecha_informeArea: informeAreaCorrespondiente ? formatDate(informeAreaCorrespondiente.fecha_informeArea) : '',
                  nombre_solicitante: solicitud.nombre_solicitante,
                  estado_informeArea: informeAreaCorrespondiente ? informeAreaCorrespondiente.estado_informeArea : '',
                  adjunto_informeArea: informeAreaCorrespondiente ? informeAreaCorrespondiente.adjunto_informeArea : '',
                  registros_ensayo: informeAreaCorrespondiente ? informeAreaCorrespondiente.registros_ensayo : '',
                  // Informes Parciales
                  informesParciales: informeAreaCorrespondiente ? informeAreaCorrespondiente.informes_parciales : [],
                  // Solicitud Inter Area
                  nro_solicitudInterarea: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.nro_solicitudInterarea : '',
                  fecha_solicitudInterarea: solicitudInterAreaCorrespondiente ? formatDate(solicitudInterAreaCorrespondiente.fecha_solicitudInterarea) : '',
                  inter_areaTematica: solicitudInterAreaCorrespondiente ? formatAreaTematica(solicitudInterAreaCorrespondiente.inter_areaTematica) : '',
                  muestras_solicitudIa: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.muestras_solicitudIa : '',
                  num_labs: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.num_labs : '',
                  observaciones: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.observaciones : '',
                  // Informe Inter Area
                  nro_informeInterarea: InformeInterareaCorrespondiente ? InformeInterareaCorrespondiente.nro_informeInterarea : '',
                  fecha_informeInterarea: InformeInterareaCorrespondiente ? formatDate(InformeInterareaCorrespondiente.fecha_informeInterarea) : '',
                  adjunto_informeInterarea: InformeInterareaCorrespondiente ? InformeInterareaCorrespondiente.adjunto_informeInterarea : '',
                  // Informe Servicio
                  nro_informeServicio: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.nro_informeServicio : '',
                  fecha_informeServicio: InformeServicioCorrespondiente ? formatDate(InformeServicioCorrespondiente.fecha_informeServicio) : '',
                  adjunto_informeServicio: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.adjunto_informeServicio : '',
                  corregir: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.corregir : '',
                  correcciones: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.correcciones : '',
                  revision: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.revision : '',
                  firma_area: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.firma_area : '',
                  firma_direccion: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.firma_direccion : '',
                  informeServicio_completo: InformeServicioCorrespondiente ? InformeServicioCorrespondiente.completo : '',
                };

                // Filtrar las filas según el área temática del usuario, excepto si es servicios_tecnologicos, administracion, o direccion
                if (userAreaTematica === 'Servicios Tecnologicos' || 
                    userAreaTematica === 'Administracion' || 
                    userAreaTematica === 'Direccion' || 
                    (fila.area_tematica === userAreaTematica && fila.nro_ordenServicio) ||
                    (fila.inter_areaTematica === userAreaTematica)) { 
                  acc.push(fila);
                }
                return acc;
              }, []);

              // Actualizar el estado con las filas filtradas
              filas.value = filteredFilas;
              console.log('Area del usuario', userAreaTematica)
              // console.log('AREA DE LA FILA', area_tematica)
            })
            .catch(error => {
              console.error('Error al obtener datos:', error);
            });
      };


      // Función para formatear el campo fecha
      const formatDate = (dateString) => {
            const [year, month, day] = dateString.split('-');
            return `${day}/${month}/${year}`;
        };

      // Función para formatear el campo area_tematica
      const formatAreaTematica = (areaTematica) => {
        return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      };

      // Función para desformatear el campo area_tematica
      const desformatearAreaTematica = (areaTematica) => {
        return areaTematica
          .toLowerCase() // Convierte todo a minúsculas
          .replace(/ /g, '_'); // Reemplaza los espacios por guiones bajos
      };

      // Llamamos a fetchData cuando el componente se monta
      onMounted(() => {
        fetchData();
      });

      const triggerFileInput = () => {
      document.getElementById('fileInput').click();
      };

      // SOLICITUD DE SERVICIO

      // DS - Data Servicio
      const abrirDataServicio = (nro_dataServicio) => {
          axios.get(`api/encurso/obtener_dataservicio/${nro_dataServicio}/`)
              .then(response => {
                  // Obtener los datos del data servicio de la respuesta
                  const { nro_dataServicio, fecha_dataServicio, obra, cant_numLabs, plazo_estimado, muestras, nro_presupuesto, area_tematica, nombre_solicitante, arancel_presupuesto, observaciones } = response.data;

                  // Asignar los datos a variables en el contexto del componente
                  nroDataServicio.value = nro_dataServicio;
                  fechaDataServicio.value = formatDate(fecha_dataServicio);
                  obraDataServicio.value = obra;
                  cantNumLabsDataServicio.value = cant_numLabs;
                  plazoEstimadoDataServicio.value = plazo_estimado;
                  muestrasDataServicio.value = muestras;
                  nroPresupuestoDataServicio.value = nro_presupuesto;
                  areaDataServicio.value = formatAreaTematica(area_tematica);
                  solicitanteDataServicio.value = nombre_solicitante ;
                  arancelDataServicio.value = formatArancel(arancel_presupuesto);
                  observacionesDataServicio.value = observaciones ;

                  // Mostrar el modal para mostrar los detalles del data servicio
                  mostrarModalDataServicio.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos del legajo:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };
      
      const cerrarModalDataServicio = () => {
        console.log('CERRAR MODAL')
        mostrarModalDataServicio.value = false;
      };

      // DS - ST-02 Solicitud
      const cargarAdjuntoSolicitud = (event, nroDataServicio) => {
          console.log('adjunto solicitud')
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          console.log('Archivo seleccionado:',archivoSeleccionado)
          console.log('nroDataServicio para cargar archivo', nroDataServicio)
          console.log('Evento para cargar archivo', event)
          // Crear un objeto FormData para enviar el archivo al servidor
          const formData = new FormData();
          console.log('FORM DATA PARA CARGAR ARCHIVO', formData)
          formData.append('archivo', archivoSeleccionado);
          formData.append('nroDataServicio', nroDataServicio); // Agregar el número de servicio

          // Realizar una petición POST al servidor para guardar el archivo
          axios.post('api/encurso/guardar_adjuntosolicitudservicio/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };

      // LEGAJO

      // Legajo - Crear
      const obtenerRangoLab = (nro_circuito) => {
        // Realizar la llamada a la API para obtener el rango de laboratorios
        axios.get(`/api/encurso/obtener_rangoLab/${nro_circuito}/`)
            .then(response => {
                // Si la llamada es exitosa, obtén el rango de laboratorios del cuerpo de la respuesta
                const rangoLab = response.data.rangoLab;
                const nuevo_ultimo_numero = response.data.ultimo_numero;
                // console.log('Rango:', rangoLab);
                // console.log('Ultimo Numero =',nuevo_ultimo_numero); 
                // Crea el nuevo legajo con el rango de laboratorios obtenido
                nuevoLegajo.value = {
                    fecha_legajo: new Date().toISOString().substring(0, 10), 
                    rangos_laboratorios: rangoLab, // Asignar el rango de laboratorios obtenido
                    pago: 0,
                    plazo_pago: 30,
                    nuevo_ultimo_numero: nuevo_ultimo_numero,
                    nro_circuito: nro_circuito,
                };

                // Muestra el modal una vez que se ha creado el legajo
                mostrarModalCrearLegajo.value = true;
            })
            .catch(error => {
                console.error('Error al obtener el rango de laboratorios:', error);
                // Manejar el error de la llamada a la API
            });
      };

      const crearLegajo = () => {
        // console.log('Datos del nuevo legajo:', nuevoLegajo.value);
        axios.post('api/encurso/crear_legajo/', nuevoLegajo.value)
        .then(response => {
          console.log(response)
          cerrarModalCrearLegajo();

          nuevoLegajo.value = {
            fecha_legajo: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
            rangos_laboratorios: '',
            pago: 0,
            plazo_pago: 30,
            nuevo_ultimo_numero: '',
            nro_circuito: null,
          };

          showSuccessAlert.value = true;

          setTimeout(() => {
            showSuccessAlert.value = false;
          }, 3000);
        })
        .catch(error => {
          console.error('Error al guardar el arancel:', error);
          cerrarModalCrearLegajo.value = false;
          showErrorAlert.value = true;

          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        });
      };

      const cerrarModalCrearLegajo = () => {
        mostrarModalCrearLegajo.value = false;
      };

      // Legajo - Abrir
      const abrirLegajo = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          const nro_circuito = numeroCircuitoGlobal.value;
          axios.get(`api/encurso/obtener_legajo/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos del legajo de la respuesta
                  const { nro_legajo, fecha_legajo, rangos_laboratorios, nombre_solicitante } = response.data;

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroLegajo.value = nro_legajo;
                  fechaLegajo.value = fecha_legajo;
                  rangosLaboratorios.value = rangos_laboratorios;
                  nombreSolicitante.value = nombre_solicitante;

                 // Obtener el año actual de fechaLegajo
                const year = new Date(fecha_legajo).getFullYear();

                // Asignar el año a la propiedad `value` del ref `añoLegajo`
                añoLegajo.value = year;

                  // Mostrar el modal para mostrar los detalles del legajo
                  mostrarModalLegajo.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos del legajo:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };

      const descargarLegajoPDF = () => {
          const nro_circuito = numeroCircuitoGlobal.value;
          axios({
              method: 'get',
              url: `/api/encurso/generar_pdf_legajo/${nro_circuito}/`, // Ajusta la URL a tu endpoint en el backend
              responseType: 'blob' // Indicamos que esperamos una respuesta de tipo archivo binario (PDF)
          })
          .then((response) => {
              // Crear un enlace temporal para descargar el archivo
              const url = window.URL.createObjectURL(new Blob([response.data]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', 'informe.pdf'); // Nombre del archivo a descargar
              document.body.appendChild(link);
              link.click();
              link.remove(); // Eliminar el enlace temporal
          })
          .catch((error) => {
              console.error('Error al descargar el PDF:', error);
          });
      };

      const cerrarModalLegajo = () => {
        // console.log('CERRAR MODAL') 
        // console.log('modal legajo', mostrarModalLegajo.value )
        mostrarModalLegajo.value = false;
        console.log('modal legajo despues', mostrarModalLegajo.value )
      };

      // Legajo - Factura
      const cargarAdjuntoFactura = (event, nroLegajo, nroCircuito) => {
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          // console.log('NRO DATA SERVICIO PARA CARGAR ARCHIVO', nroLegajo)
          // console.log('EVENTO PARA CARGAR ARCHIVO', event)
          // Crear un objeto FormData para enviar el archivo al servidor
          const formData = new FormData();
          // console.log('FORM DATA PARA CARGAR ARCHIVO', formData)
          formData.append('archivo', archivoSeleccionado);
          formData.append('nroLegajo', nroLegajo); // Agregar el número de legajo
          formData.append('nroCircuito', nroCircuito); // Agregar el número de circuito para crear instancia de Recepcion

          // Realizar una petición POST al servidor para guardar el archivo
          axios.post('api/encurso/guardar_adjuntofactura/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };

      // Legajo - Pago
      const abrirModalPagoLegajo = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        // console.log('Pago Legajo en abrirModalPagoLegajo',fila.pago)
        // console.log('Numero Circuito en abrirModalPagoLegajo',numeroCircuitoGlobal.value)
        mostrarModalPagoLegajo.value = true;
      };

      const cerrarModalPagoLegajo = () => {
        mostrarModalPagoLegajo.value = false;
      };

      const guardarPagoLegajo = async (pagoLegajoNuevo) => {
        // console.log('numero Circuito en guardarPagoLegajo', numeroCircuitoGlobal.value)
        // console.log('pagoLegajoNuevo en guardarPagoLegajo', pagoLegajoNuevo)
        const nro_circuito = numeroCircuitoGlobal.value;
        try {
          // Realizar la petición para actualizar el pago del legajo en la base de datos
          const response = await axios.put(`/api/encurso/guardar_pago_legajo/${nro_circuito}/`, {
            pago: pagoLegajoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Pago de Legajo actualizado correctamente:', pagoLegajoNuevo);
            mostrarModalPagoLegajo.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            console.error('Error al actualizar el Pago de Legajo:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          } 
        } catch (error) {
          console.error('Error al cambiar el Pago de Legajo:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };

      // Legajo - Plazo Pago
      const abrirModalPlazoPago = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        console.log('Plazo de Pago actual en abrirModalPlazoPago',fila.plazo_pago)
        console.log('Numero Circuito en abrirModalPlazoPago',numeroCircuitoGlobal.value)
        mostrarModalPlazoPago.value = true;
      };

      const cerrarModalPlazoPago = () => {
        mostrarModalPlazoPago.value = false;
      };

      const cambiarPlazoPago = async (plazoPagoNuevo) => {
        const nro_circuito = numeroCircuitoGlobal.value;
        try {
          // Realizar la petición para actualizar el plazo de muestras en la base de datos
          const response = await axios.put(`/api/encurso/cambiar_plazo_pago/${nro_circuito}/`, {
            plazo_pago: plazoPagoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Plazo de Pago actualizado correctamente:', plazoPagoNuevo);
            mostrarModalPlazoPago.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            mostrarModalPlazoPago.value = false;
            console.error('Error al actualizar el Plazo del Pago:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          mostrarModalPlazoPago.value = false;
          console.error('Error al cambiar el Plazo del Pago:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };

      // Para abrir venntana para adjuntar cualquier archivo
      const abrirArchivo = (adjunto) => {
        console.log('valor de adjunto:', adjunto)
        const urlCompleta = 'http://localhost:8000' + adjunto;
        window.open(urlCompleta, '_blank');
      };

      const abrirVistaPreliminar = (adjunto) => {
        console.log('pdf preliminar', adjunto)
        // Construir la URL completa
        urlPdf.value = 'http://localhost:8000' + adjunto;
        console.log('urlPDF', urlPdf)
        mostrarModalPDFpreliminar.value = true;
      };

      const cerrarModalPDFpreliminar = () => {
        mostrarModalPDFpreliminar.value = false;
      };

      const formatArancel = (arancel) => {
          // Verificar si arancel es numérico
          if (!isNaN(arancel)) {
              // Convertir a número entero y formatear con signo $ y separación de miles
              return '$ ' + parseFloat(arancel).toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
          } else {
              // Si no es numérico, devolver el valor sin formato
              return arancel;
          }
      };


      // RECEPCION

      // Recepcion - ST03 - Recepcion (Remitos)
      const abrirModalRemito = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        remitoNuevo.value = fila.nros_remitos;
        mostrarModalRemito.value = true;
      };

      const cerrarModalRemito = () => {
        mostrarModalRemito.value = false;
        remitoNuevo.value = '';
      };

      const cambiarRemito = async (remitoNuevo) => {
        // console.log('Numero Circuito en cambiarRemito', numeroCircuitoGlobal.value)
        // console.log('remitoNuevo en cambiarRemito', remitoNuevo)
        const nro_circuito = numeroCircuitoGlobal.value;
        try {
          // Realizar la petición para actualizar el numero de remito en la base de datos
          const response = await axios.put(`/api/encurso/cambiar_remito/${nro_circuito}/`, {
            nros_remitos: remitoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Numero de Remito actualizado correctamente:', remitoNuevo);
            mostrarModalRemito.value = false;  
            remitoNuevo = '';
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            mostrarModalRemito.value = false;
            console.error('Error al actualizar el numero de Remito:', response.statusText);
            showErrorAlert.value = true;
            remitoNuevo = '';
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          mostrarModalRemito.value = false;
          remitoNuevo = '';
          console.error('Error al cambiar el numero de Remito:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };

      // Recepcion - Estado Muestras
      const abrirModalEstadoMuestras = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        // console.log('Estado Recepcion en abrirModalEstadoMuestras',fila.estado_recepcion)
        // console.log('Numero Circuito en abrirModalEstadoMuestras',numeroCircuitoGlobal.value)
        mostrarModalEstadoMuestras.value = true;
      };

      const cerrarModalEstadoMuestras = () => {
        mostrarModalEstadoMuestras.value = false;
      };

      const guardarEstadoMuestras = async (estadoMuestrasNuevo) => {
        // console.log('numero Circuito en guardarEstadoMuestras', numeroCircuitoGlobal.value)
        // console.log('estadoMuestrasNuevo en guardarEstadoMuestras', estadoMuestrasNuevo)
        const nro_circuito = numeroCircuitoGlobal.value;
        try {
          // Realizar la petición para actualizar el estado de la recepción de muestras en la base de datos
          const response = await axios.put(`/api/encurso/guardar_estado_recepcion/${nro_circuito}/`, {
            estado_recepcion: estadoMuestrasNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Estado de recepción de muestras actualizado correctamente:', estadoMuestrasNuevo);
            mostrarModalEstadoMuestras.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            // Llamar a crearOrdenServicio si la actualización fue exitosa
            // await crearOrdenServicio(nro_circuito);

            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            console.error('Error al actualizar el estado de la recepción de muestras:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          console.error('Error al cambiar el estado de la recepción de muestras:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };
      
      // Recepcion - Plazo Muestras  
      const abrirModalPlazoMuestras = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        // console.log('Plazo Muestras actual en abrirModalPlazoMuestras',fila.plazo_muestras)
        // console.log('Numero Circuito en abrirModalPlazoMuestras',numeroCircuitoGlobal.value)
        mostrarModalPlazoMuestras.value = true;
      };

      const cerrarModalPlazoMuestras = () => {
        mostrarModalPlazoMuestras.value = false;
      };

      const cambiarPlazoMuestras = async (plazoMuestrasNuevo) => {
        // console.log('Numero Circuito en cambiarPlazoMuestras', numeroCircuitoGlobal.value)
        // console.log('plazoMuestrasNuevo en cambiarPlazoMuestras', plazoMuestrasNuevo)
        const nro_circuito = numeroCircuitoGlobal.value;
        try {
          // Realizar la petición para actualizar el plazo de muestras en la base de datos
          const response = await axios.put(`/api/encurso/cambiar_plazo_muestras/${nro_circuito}/`, {
            plazo_muestras: plazoMuestrasNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Plazo de muestras actualizado correctamente:', plazoMuestrasNuevo);
            mostrarModalPlazoMuestras.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            mostrarModalPlazoMuestras.value = false;
            console.error('Error al actualizar el plazo de las muestras:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          mostrarModalPlazoMuestras.value = false;
          console.error('Error al cambiar el plazo de las muestras:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };
      
      const numeroEntero = ref(0);

      function validarNumeroEntero(event) {
        const valor = parseInt(event.target.value, 10);
        if (!isNaN(valor) && valor >= 0) {
          numeroEntero.value = valor;
        } else {
          event.target.value = numeroEntero.value;
        }
      }

      // ORDEN DE SERVICIO

      // OS - Archivo

      const abrirModalCrearOrdenServicio = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        mostrarModalCrearOrdenServicio.value = true;
      };

      const cerrarModalCrearOrdenServicio = () => {
        mostrarModalCrearOrdenServicio.value = false;
      };
      
      const crearOrdenServicio = async () => {
          const nro_circuito = numeroCircuitoGlobal.value;
          console.log('numero circuito en crear orden circuito:', nro_circuito)
          try {
              const response = await axios.post(`http://localhost:8000/api/encurso/crear_ordenservicio/${nro_circuito}/`);
              console.log('Orden de servicio creada exitosamente:', response.data);
              mostrarModalCrearOrdenServicio.value = false;
              showSuccessAlert.value = true;
              setTimeout(() => {
                  showSuccessAlert.value = false;
              }, 3000);
          } catch (error) {
              console.error('Error al crear la orden de servicio:', error);
              mostrarModalCrearOrdenServicio.value = false;
              showErrorAlert.value = true;
              setTimeout(() => {
                  showErrorAlert.value = false;
              }, 5000);
          }
      };

      // OS - Abrir Orden de Servicio
      const abrirOrdenServicio = (fila) => {
          const nro_circuito = fila.nro_circuito;
          axios.get(`api/encurso/obtener_orden_servicio/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos de la orden de servicio de la respuesta
                  const { nro_ordenServicio, fecha_ordenServicio, area_tematica, nro_legajo, rangos_laboratorios, plazo_estimado, nombre_solicitante,servicio_solicitado, muestras, observaciones } = response.data;

                  // Asignar los datos de la orden de servicio a variables en el contexto del componente
                  nroOS.value = nro_ordenServicio;
                  fechaOS.value = fecha_ordenServicio; 
                  areaOS.value = formatAreaTematica(area_tematica);
                  legajoOS.value = nro_legajo;
                  rangosOS.value= rangos_laboratorios;
                  plazoOS.value= plazo_estimado;
                  solicitanteOS.value= nombre_solicitante;
                  servicioOS.value = servicio_solicitado;
                  muestrasOS.value= muestras;
                  observacionesOS.value= observaciones;
                  // Mostrar el modal para mostrar los detalles del legajo
                  mostrarModalOrdenServicio.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos de la orden de servicio:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
      };

      const cerrarModalOrdenServicio = () => {
        mostrarModalOrdenServicio.value = false;
      };

       // OS - Plazo

      const abrirModalPlazoOrdenServicio = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        mostrarModalPlazoOrdenServicio.value = true;
      };

      const cerrarModalPlazoOrdenServicio = () => {
        mostrarModalPlazoOrdenServicio.value = false;
      };

      const cambiarPlazoOrdenServicio = async (plazoEstimadoNuevo) => {
        const nro_circuito = numeroCircuitoGlobal.value;
        axios.defaults.withCredentials = true;
        try {
            // Realizar la petición para actualizar el plazo de orden de servicio en la base de datos
            const response = await axios.put(`http://localhost:8000/api/encurso/cambiar_plazo_estimado/${nro_circuito}/`, {
                plazo_estimado: plazoEstimadoNuevo
            }, {
                withCredentials: true 
            });

            // Verificar si la actualización fue exitosa
            if (response.status === 200) {
                console.log('Plazo de orden de servicio actualizado correctamente:', plazoEstimadoNuevo);
                mostrarModalPlazoOrdenServicio.value = false;  // Cerrar el modal
                showSuccessAlert.value = true;
                
                setTimeout(() => {
                    showSuccessAlert.value = false;
                }, 3000);

            } else {
                mostrarModalPlazoOrdenServicio.value = false;
                console.error('Error al actualizar el plazo de orden de servicio:', response.statusText);
                showErrorAlert.value = true;
                setTimeout(() => {
                    showErrorAlert.value = false;
                }, 5000);
            }
        } catch (error) {
            mostrarModalPlazoOrdenServicio.value = false;
            console.error('Error al cambiar el plazo de orden de servicio:', error);
            showErrorAlert.value = true;
            setTimeout(() => {
                showErrorAlert.value = false;
            }, 5000);
        }
      };

      // INFORME AREA

      // Informe Area - Adjunto
      const cargarAdjuntoInformeArea = async (event, fila) => {
        const nro_circuito = fila.nro_circuito;
        const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
        const formData = new FormData();
        formData.append('archivo', archivoSeleccionado);
        formData.append('nroCircuito', nro_circuito); // Agregar el número de circuito

        try {
          const estadoInformeAreaNuevo = await abrirModalEstadoInformeArea(fila);
          formData.append('estadoInformeAreaNuevo', estadoInformeAreaNuevo); // Agregar el estado del informe

          // Realizar una petición POST al servidor para guardar el archivo
          const response = await axios.post('api/encurso/guardar_adjunto_informearea/', formData);
          console.log('Archivo guardado exitosamente:', response.data);
        } catch (error) {
          console.error('Error al guardar el archivo:', error);
        }
      };

      // Informe Area - Registros Ensayos
      const cargarRegistrosEnsayo = async (event, fila) => {
        const nro_circuito = fila.nro_circuito;
        const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
        const formData = new FormData();
        formData.append('archivo', archivoSeleccionado);
        formData.append('nroCircuito', nro_circuito); // Agregar el número de circuito

        // Realizar una petición POST al servidor para guardar el archivo
        axios.post('api/encurso/guardar_registros_ensayo/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };

      // Informe Area - Estado (Se llama cuando se adjunte informe area)
      const abrirModalEstadoInformeArea = (fila) => {
        return new Promise((resolve) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          mostrarModalEstadoInformeArea.value = true;

          const guardarEstado = (estado) => {
            mostrarModalEstadoInformeArea.value = false;
            resolve(estado);
          };

          guardarEstadoInformeArea.value = guardarEstado;
        });
      };

      const cerrarModalEstadoInformeArea = () => {
        mostrarModalEstadoInformeArea.value = false;
      };

      // INTER AREA

      // Inter Area - Crear Solicitud Inter Area

      const obtenerServicios = async (nro_circuito) => {
        try {
          const response = await axios.get(`http://localhost:8000/api/encurso/obtener_servicios/${nro_circuito}/`);
          serviciosDisponibles.value = response.data;
          console.log('servicios disponibles dentro de obtenerServicios', serviciosDisponibles);
        } catch (error) {
          console.error('Error al obtener los servicios:', error);
          throw error; 
        }
      };

      // Función para agregar un servicio seleccionado
      const agregarServicioSeleccionado = (servicio) => {
        serviciosSeleccionados.value.push(servicio);
      };

      // Función para eliminar un servicio seleccionado
      const eliminarServicioSeleccionado = (index) => {
        const servicio = serviciosSeleccionados.value[index];
        serviciosDisponibles.value.servicio_solicitado.push(servicio);
        serviciosSeleccionados.value.splice(index, 1);
      };

      const moverServicioSeleccionado = () => {
        servicioSeleccionadoTemporal.value.forEach(servicio => {
          serviciosSeleccionados.value.push({ ...servicio, cantidadSeleccionada: 1 });
          const index = serviciosDisponibles.value.servicio_solicitado.indexOf(servicio);
          if (index > -1) {
            serviciosDisponibles.value.servicio_solicitado.splice(index, 1);
          }
        });
        servicioSeleccionadoTemporal.value = [];
      };

      const abrirModalCrearSolicitudInterArea = async (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;

        try {
          await obtenerServicios(numeroCircuitoGlobal.value);
          nuevaSolicitudInterarea.value.nro_circuito = fila.nro_circuito;
          nuevaSolicitudInterarea.value.areaTematica_origen = fila.area_tematica;
          mostrarModalCrearSolicitudInterArea.value = true;
        } catch (error) {
          console.error('Error al obtener servicios:', error);
          // Manejar el error según sea necesario
        }
      };

      const cerrarModalCrearSolicitudInterArea = () => {
        mostrarModalCrearSolicitudInterArea.value = false;
        serviciosDisponibles.value = [];
        serviciosSeleccionados.value = [];
        servicioSeleccionadoTemporal.value = [];
        // Limpiar el formulario
        nuevaSolicitudInterarea.value = {
                fecha_solicitudInterarea: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
                areaTematica_origen: '',
                inter_areaTematica: '',
                num_labs: '',
                servicios_solicitudInterarea: [
                  {
                    nro_servicio: '',
                    servicio: '',
                    cant: 0,
                  }
                ],
                nro_circuito: null,
              };
      };

      const crearSolicitudInterArea = () => {
          // // Validar campos obligatorios
          // if (!nuevoPresupuesto.value.contacto || !nuevoPresupuesto.value.email || !nuevoPresupuesto.value.area_tematica || nuevoPresupuesto.value.subtotal === null || nuevoPresupuesto.value.descuento === null) {
          //   return;
          // }

          // Limpiar los servicios seleccionados antes de sincronizarlos
            nuevaSolicitudInterarea.value.servicios_solicitudInterarea = [];

          /// Sincronizar los servicios seleccionados con el objeto nuevaSolicitudInterarea
          serviciosSeleccionados.value.forEach(servicio => {
            nuevaSolicitudInterarea.value.servicios_solicitudInterarea.push({
              nro_servicio: servicio.nro_servicio,
              servicio: servicio.servicio,
              cant: servicio.cant,
            });
          });

          nuevaSolicitudInterarea.value.areaTematica_origen = desformatearAreaTematica(nuevaSolicitudInterarea.value.areaTematica_origen);
          
          console.log('nueva solicitud interarea envianda al backend',nuevaSolicitudInterarea)

          // Enviar datos al backend usando Axios
          axios.post('http://localhost:8000/api/encurso/crear_solicitud_interarea/', nuevaSolicitudInterarea.value)
            .then(response => {
              console.log(response.data);
              cerrarModalCrearSolicitudInterArea();

              // Limpiar los array
              serviciosDisponibles.value = [];
              serviciosSeleccionados.value = [];
              servicioSeleccionadoTemporal.value = [];
              // Limpiar el formulario y mostrar la alerta de éxito
              nuevaSolicitudInterarea.value = {
                fecha_solicitudInterarea: new Date().toISOString().substring(0, 10), 
                areaTematica_origen: '',
                inter_areaTematica: '',
                num_labs: '',
                servicios_solicitudInterarea: [
                  {
                    nro_servicio: '',
                    servicio: '',
                    cant: 0,
                  }
                ],
                nro_circuito: null,
              };

              showSuccessAlert.value = true;

              setTimeout(() => {
                showSuccessAlert.value = false;
              }, 3000);
            })
            .catch(error => {
              console.error('Error al crear la solicitud inter area:', error);
              cerrarModalCrearSolicitudInterArea();

              // Limpiar los array
              serviciosDisponibles.value = [];
              serviciosSeleccionados.value = [];
              servicioSeleccionadoTemporal.value = [];
              // Limpiar el formulario y mostrar la alerta de error
              nuevaSolicitudInterarea.value = {
                fecha_solicitudInterarea: new Date().toISOString().substring(0, 10), 
                areaTematica_origen: '',
                inter_areaTematica: '',
                num_labs: '',
                servicios_solicitudInterarea: [
                  {
                    nro_servicio: '',
                    servicio: '',
                    cant: 0,
                  }
                ],
                nro_circuito: null,
              };
              // Imprimir detalles del error
              console.error('Error details:', error.response.data);

              showErrorAlert.value = true;

              setTimeout(() => {
                showErrorAlert.value = false;
              }, 5000);
            });
      };


      // Inter Area - Abrir Solicitud Inter Area
      const abrirSolicitudInterArea = (fila) => {
          const nro_circuito = fila.nro_circuito;
          axios.get(`api/encurso/obtener_solicitud_interarea/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos de la solicitud inter area de la respuesta
                  const { nro_solicitudInterarea, fecha_solicitudInterarea, areaTematica_origen, inter_areaTematica, muestras_solicitudIa, num_labs, observaciones, servicio_solicitado  } = response.data;

                  // Asignar los datos a variables en el contexto del componente
                  nroSolicitudInterArea.value = nro_solicitudInterarea;
                  fechaSolicitudInterArea.value = fecha_solicitudInterarea;
                  areaTematicaOrigen.value = formatAreaTematica(areaTematica_origen);
                  interAreaSolicitudInterArea.value = formatAreaTematica(inter_areaTematica);
                  muestrasSolicitudInterArea.value = muestras_solicitudIa;
                  numLabsSolicitudInterArea.value = num_labs;
                  observacionesSolicitudInterArea.value = observaciones;
                  servicioSolicitudInterArea.value = servicio_solicitado;

                  console.log('abrirSolicitudInterArea', response)
                  // Mostrar el modal para mostrar los detalles de la solicitud inter area
                  mostrarModalSolicitudInterArea.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos de la solicitud inter area:', error);
                  // Manejar el error, mostrar un mensaje al usuario, etc.
              });
        };

        const cerrarModalSolicitudInterArea = () => {
          mostrarModalSolicitudInterArea.value = false;
        };

        const cargarAdjuntoInformeInterarea = (event, fila) => {
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          const formData = new FormData();

          formData.append('archivo', archivoSeleccionado);
          formData.append('nro_solicitudInterarea', fila.nro_solicitudInterarea); 
          formData.append('nro_circuito', fila.nro_circuito); 

          // Realizar una petición POST al servidor para guardar el archivo
          axios.post('api/encurso/guardar_adjuntoinformeinterarea/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
        };
      
      // Administracion - Formato
      const cargarAdjuntoInformeServicio = (event, fila) => {
        const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
        const formData = new FormData();

        formData.append('archivo', archivoSeleccionado);
        formData.append('nro_circuito', fila.nro_circuito); 

        // Realizar una petición POST al servidor para guardar o reemplazar el archivo
        axios.post('api/encurso/guardar_adjuntoinformeservicio/', formData)
          .then(response => {
            console.log('Archivo guardado exitosamente:', response.data);
            
            // Actualizar la referencia al nuevo archivo en la fila después de guardar
            fila.adjunto_informeServicio = response.data.nuevo_adjunto_url; // Suponiendo que el backend devuelve la URL del nuevo archivo
          })
          .catch(error => {
            console.error('Error al guardar el archivo:', error);
          });
      };

      const abrirModalCorreccionesInformeServicio = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        mostrarModalCorreccionesInformeServicio.value = true;

        // Realiza la solicitud al backend usando Axios
        axios.get(`/api/encurso/obtener_correcciones/${numeroCircuitoGlobal.value}/`)
          .then((response) => {
            // Asigna la respuesta a correcciones.value
            correcciones.value = response.data.correcciones; // Asegúrate de que la respuesta tenga esta estructura
          })
          .catch((error) => {
            console.error("Error al obtener las correcciones:", error);
            // En caso de error, puedes asignar un valor predeterminado o manejarlo como prefieras
            correcciones.value = "Error al obtener correcciones.";
          });
      };

      const cerrarModalCorreccionesInformeServicio = () => {
        mostrarModalCorreccionesInformeServicio.value = false;
      };

      const corregirInformeServicio = async () => {
        const nro_circuito = numeroCircuitoGlobal.value;
        // console.log('nro circuito', nro_circuito)
        // console.log('correcciones', correcciones.value)
        try {
          const response = await axios.put(`/api/encurso/corregir_informe_servicio/${nro_circuito}/`);
            
          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Revisiones corregidas correctamente:', nro_circuito);
            mostrarModalCorreccionesInformeServicio.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            mostrarModalCorreccionesInformeServicio.value = false;
            console.error('Error al actualizar Revisiones:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          mostrarModalCorreccionesInformeServicio.value = false;
          console.error('Error al actualizar Revisiones:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };

        
      // Servicios Tecnologicos - Revision
      const abrirModalRevision = (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        mostrarModalRevision.value = true;
      };

      const cerrarModalRevision = () => {
        mostrarModalRevision.value = false;
      };

      const confirmarRevision = async () => {
            const nroCircuito = numeroCircuitoGlobal.value;
            try {
                const response = await axios.put(
                    `http://localhost:8000/api/encurso/confirmar_revision/${nroCircuito}/`
                );
                console.log('Revisión confirmada correctamente:', response.data);
                mostrarModalRevision.value = false;
                showSuccessAlert.value = true;
                setTimeout(() => {
                    showSuccessAlert.value = false;
                }, 3000);

            } catch (error) {
                console.error('Error al confirmar revisión:', error);
                // Manejar errores
                mostrarModalRevision.value = false;
                showErrorAlert.value = true; 
                setTimeout(() => {
                    showErrorAlert.value = false;
                }, 5000);
            }
      };


      const toggleOpciones = (index) => {
        if (filaSeleccionada.value === index) {
          filaSeleccionada.value = null; // Ocultar si ya está seleccionada
        } else {
          filaSeleccionada.value = index; // Mostrar opciones para la fila seleccionada
          console.log('Fila seleccionada:', filaSeleccionada.value);
        }
      };

      // Responsable del Area - Firma

      const abrirModalAdvertirCorrecciones = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          mostrarModalAdvertirCorrecciones.value = true;
      }

      const cerrarModalAdvertirCorrecciones = () => {
          mostrarModalAdvertirCorrecciones.value = false;
      };

      const advertirCorrecciones = async (correccionesNuevas) => {
        const nroCircuito = numeroCircuitoGlobal.value;
        try {
            const response = await axios.put(
                `http://localhost:8000/api/encurso/advertir_correcciones/${nroCircuito}/`, {
                correcciones: correccionesNuevas
            }
            );
            console.log('Correcciones advertidas correctamente:', response.data);
            console.log(correccionesNuevas)
            mostrarModalAdvertirCorrecciones.value = false;
            showSuccessAlert.value = true;
              setTimeout(() => {
                  showSuccessAlert.value = false;
              }, 3000);

        } catch (error) {
            console.error('Error al advertir correcciones:', error);
            mostrarModalAdvertirCorrecciones.value = false;
            showErrorAlert.value = true; 
              setTimeout(() => {
                  showErrorAlert.value = false;
              }, 5000);
        }
      };

        const abrirModalFirmaResponsableArea = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          mostrarModalFirmaResponsableArea.value = true;
        };

        const cerrarModalFirmaResponsableArea = () => {
          mostrarModalFirmaResponsableArea.value = false;
        };

        const confirmarFirmaResponsableArea = async () => {
          const nroCircuito = numeroCircuitoGlobal.value;
          try {
              const response = await axios.put(
                  `http://localhost:8000/api/encurso/confirmar_firma_responsable_area/${nroCircuito}/`
              );
              console.log('Firma Responsable Area confirmada correctamente:', response.data);
              mostrarModalFirmaResponsableArea.value = false;
              showSuccessAlert.value = true;
                setTimeout(() => {
                    showSuccessAlert.value = false;
                }, 3000);

          } catch (error) {
              console.error('Error al confirmar Firma Responsable Area:', error);
              mostrarModalFirmaResponsableArea.value = false;
              showErrorAlert.value = true; 
                setTimeout(() => {
                    showErrorAlert.value = false;
                }, 5000);
          }
        };

        // Direccion - Firma
        const abrirModalFirmaDireccion = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          mostrarModalFirmaDireccion.value = true;
        };

        const cerrarModalFirmaDireccion = () => {
          mostrarModalFirmaDireccion.value = false;
        };

        const cargarAdjuntoInformeServicioFirmado = (event, fila) => {
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          const formData = new FormData();

          formData.append('archivo', archivoSeleccionado);
          formData.append('nro_circuito', fila.nro_circuito); 

          // Realizar una petición POST al servidor para guardar o reemplazar el archivo
          axios.post('api/encurso/guardar_adjuntoinformeserviciofirmado/', formData)
            .then(response => {
              console.log('Archivo guardado exitosamente:', response.data);
              showSuccessAlert.value = true;
                setTimeout(() => {
                    showSuccessAlert.value = false;
                }, 3000);
              // Actualizar la referencia al nuevo archivo en la fila después de guardar
              fila.adjunto_informeServicio = response.data.nuevo_adjunto_url; // Suponiendo que el backend devuelve la URL del nuevo archivo
            })
            .catch(error => {
              console.error('Error al guardar el archivo:', error);
              showErrorAlert.value = true; 
                setTimeout(() => {
                    showErrorAlert.value = false;
                }, 5000);
            });
        };

        const confirmarFirmaDireccion = async () => {
          const nroCircuito = numeroCircuitoGlobal.value;
          try {
              const response = await axios.put(
                  `http://localhost:8000/api/encurso/confirmar_firma_direccion/${nroCircuito}/`
              );
              console.log('Firma Dirección confirmada correctamente:', response.data);
              mostrarModalFirmaDireccion.value = false;
              showSuccessAlert.value = true;
                setTimeout(() => {
                    showSuccessAlert.value = false;
                }, 3000);

          } catch (error) {
              console.error('Error al confirmar Firma Dirección:', error);
              mostrarModalFirmaDireccion.value = false;
              showErrorAlert.value = true; 
                setTimeout(() => {
                    showErrorAlert.value = false;
                }, 5000);
          }
        };

        // Archivar
        const abrirModalArchivar = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          mostrarModalArchivar.value = true;
        };

        const cerrarModalArchivar = () => {
          mostrarModalArchivar.value = false;
        };

        const enviarArchivar = async () => {
          const nroCircuito = numeroCircuitoGlobal.value;
          try {
              const response = await axios.put(
                  `http://localhost:8000/api/encurso/archivar_circuito/${nroCircuito}/`
              );
              console.log('Archivado correctamente:', response.data);
              mostrarModalArchivar.value = false;

              showSuccessAlert.value = true;
              setTimeout(() => {
                showSuccessAlert.value = false;
              }, 3000);

              // Manejar la respuesta como sea necesario
          } catch (error) {
              console.error('Error al archivar:', error);
              mostrarModalArchivar.value = false;

              showErrorAlert.value = true;

              setTimeout(() => {
                showErrorAlert.value = false;
              }, 5000);
          }
        };


      return {
        // General
        filas,
        validarNumeroEntero,
        formatDate,
        formatArancel,
        desformatearAreaTematica,
        showSuccessAlert,
        showErrorAlert,
        abrirArchivo,
        abrirVistaPreliminar,
        mostrarModalPDFpreliminar,
        cerrarModalPDFpreliminar,
        triggerFileInput,
        isAdminOrTecnologicoOrDireccion,
        isServiciosTecnologicos,
        isAdministracion,
        isDireccion,
        isAreaJefe,
        isAreaStandard,
        isTecnologicoOrDireccionOrArea,
        userAreaTematica,
        // Solicitud de Servicio
        abrirDataServicio,
        nroDataServicio,
        fechaDataServicio,
        obraDataServicio,
        cantNumLabsDataServicio,
        plazoEstimadoDataServicio,
        muestrasDataServicio,
        nroPresupuestoDataServicio,
        areaDataServicio,
        solicitanteDataServicio,
        arancelDataServicio,
        observacionesDataServicio,
        mostrarModalDataServicio,
        cargarAdjuntoSolicitud,
        // Legajo
        nuevoLegajo,
        obtenerRangoLab,
        abrirLegajo,
        nroLegajo,
        fechaLegajo,
        rangosLaboratorios,
        nombreSolicitante,
        añoLegajo,
        mostrarModalCrearLegajo,
        mostrarModalLegajo,
        descargarLegajoPDF,
        cargarAdjuntoFactura,
        mostrarModalPagoLegajo,
        mostrarModalPlazoPago,
        cerrarModalCrearLegajo,
        cerrarModalDataServicio,
        cerrarModalLegajo,
        crearLegajo,
        abrirModalPagoLegajo,
        cerrarModalPagoLegajo,
        guardarPagoLegajo,
        abrirModalPlazoPago,
        cerrarModalPlazoPago,
        cambiarPlazoPago,
        // Recepcion
        nuevoRecepcion,
        remitoNuevo,
        abrirModalRemito,
        cerrarModalRemito,
        mostrarModalRemito,
        cambiarRemito,
        abrirModalEstadoMuestras,
        cerrarModalEstadoMuestras,
        mostrarModalEstadoMuestras,
        guardarEstadoMuestras,
        abrirModalPlazoMuestras,
        cerrarModalPlazoMuestras,
        mostrarModalPlazoMuestras,
        cambiarPlazoMuestras,
        // Orden de Servicio
        nroOS,
        fechaOS,
        areaOS,
        legajoOS,
        rangosOS,
        plazoOS,
        solicitanteOS,
        servicioOS,
        muestrasOS,
        observacionesOS,
        crearOrdenServicio,
        mostrarModalCrearOrdenServicio,
        abrirModalCrearOrdenServicio,
        cerrarModalCrearOrdenServicio,
        abrirOrdenServicio,
        mostrarModalOrdenServicio,
        cerrarModalOrdenServicio,
        cambiarPlazoOrdenServicio,
        abrirModalPlazoOrdenServicio,
        cerrarModalPlazoOrdenServicio,
        mostrarModalPlazoOrdenServicio,
        // Informe Area
        cargarAdjuntoInformeArea,
        abrirModalEstadoInformeArea,
        cerrarModalEstadoInformeArea,
        mostrarModalEstadoInformeArea,
        guardarEstadoInformeArea,
        cargarRegistrosEnsayo,
        // Inter Area
        serviciosDisponibles,
        serviciosSeleccionados,
        servicioSeleccionadoTemporal,
        inter_areaTematicaOptions,
        nuevaSolicitudInterarea,
        obtenerServicios,
        agregarServicioSeleccionado,
        eliminarServicioSeleccionado,
        moverServicioSeleccionado,
        abrirModalCrearSolicitudInterArea,
        cerrarModalCrearSolicitudInterArea,
        mostrarModalCrearSolicitudInterArea,
        crearSolicitudInterArea,
        abrirSolicitudInterArea,
        cerrarModalSolicitudInterArea,
        mostrarModalSolicitudInterArea,
        nroSolicitudInterArea,
        fechaSolicitudInterArea,
        interAreaSolicitudInterArea,
        areaTematicaOrigen,
        muestrasSolicitudInterArea,
        numLabsSolicitudInterArea,
        observacionesSolicitudInterArea,
        servicioSolicitudInterArea,
        cargarAdjuntoInformeInterarea,
        // Administracion - Formato
        cargarAdjuntoInformeServicio,
        abrirModalCorreccionesInformeServicio,
        cerrarModalCorreccionesInformeServicio,
        mostrarModalCorreccionesInformeServicio,
        correcciones,
        corregirInformeServicio,
        // Servicios Tecnologicos - Revision
        abrirModalRevision,
        cerrarModalRevision,
        mostrarModalRevision,
        confirmarRevision,
        mostrarOpciones,
        filaSeleccionada,
        toggleOpciones,
        // Responsable del Area - Firma 
        abrirModalAdvertirCorrecciones,
        cerrarModalAdvertirCorrecciones,
        mostrarModalAdvertirCorrecciones,
        advertirCorrecciones,
        abrirModalFirmaResponsableArea,
        cerrarModalFirmaResponsableArea,
        mostrarModalFirmaResponsableArea,
        confirmarFirmaResponsableArea,
        // Direccion - Firma
        abrirModalFirmaDireccion,
        cerrarModalFirmaDireccion,
        mostrarModalFirmaDireccion,
        cargarAdjuntoInformeServicioFirmado,
        confirmarFirmaDireccion,
        // Archivar
        abrirModalArchivar,
        cerrarModalArchivar,
        mostrarModalArchivar,
        enviarArchivar,
      };
    },
  };
</script>
  
<style scoped>

  /* Agrega un borde vertical a la derecha de las subcolumnas específicas */
  .add-border-right {
    border-right: 1px solid gainsboro; /* Establece el borde derecho */
  }

  .radio-options input[type="radio"] {
    display: inline-block;
    margin-right: 5px;
  }

  .radio-options label {
    font-size: 10px;
  }

  .btn-group {
    display: inline-block; 
  }

  .radio-options {
    text-align: left;
  }

  .radio-options input[type="radio"] {
    display: inline-block;
    margin-right: 10px; 
  }

  .radio-options label {
    font-size: 12px; 
  }

  .no-wrap-column {
    white-space: nowrap;
  }

  #servicios_solicitudInterarea {
    width: 100%;
    height: 150px;
    white-space: nowrap;
    overflow-x: auto;
  }

  #servicios_solicitudInterarea option {
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Estilos específicos para el modal PDF */
  .pdf-modal {
    display: block; 
    position: fixed; 
    z-index: 1050; 
    left: 0;
    top: 0;
    width: 100%; 
    height: 100%; 
    overflow: auto; 
    background-color: rgba(0,0,0,0.5); 
  }

  .pdf-modal-content {
    background-color: #fefefe;
    margin: 5% auto; 
    padding: 20px;
    border: 1px solid #888;
    width: 80%; 
    max-width: 1000px;
  }

  .pdf-close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .pdf-close:hover,
  .pdf-close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }

  .opciones-flotantes {
    position: absolute;
    top: -30px; /* Ajusta según el espacio que quieras arriba */
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
  }

  .opcion {
    position: absolute;
    width: 40px;  /* Tamaño del ícono */
    height: 40px; /* Tamaño del ícono */
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #026290; /* Color de fondo */
    border-radius: 50%;  /* Hace que sea un círculo */
    color: white;  /* Color del ícono */
    transform: rotate(var(--rotation)) translate(60px) rotate(calc(-1 * var(--rotation))); /* Semi círculo */
    transition: transform 0.3s ease;
  }

  .opcion i {
    font-size: 20px; /* Ajusta el tamaño del ícono */
    cursor: pointer;
  }

  .opcion:hover {
    transform: rotate(var(--rotation)) translate(70px) rotate(calc(-1 * var(--rotation))); /* Aumenta la distancia cuando haces hover */
  }


</style>
  