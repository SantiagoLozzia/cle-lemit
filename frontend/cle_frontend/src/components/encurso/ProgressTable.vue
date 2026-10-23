<template>
     <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! Se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar. Por favor, inténtalo de nuevo.
    </div>

    <div>
      <div class="filter-bar mb-2 d-flex flex-wrap align-items-center gap-2">
        <select v-if="isAdminOrTecnologicoOrDireccion" v-model="filterArea" class="form-select form-select-sm w-auto">
          <option value="">Todas las áreas</option>
          <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
        </select>
        <select v-model="filterTipoFecha" class="form-select form-select-sm w-auto">
          <option value="solicitud">Solicitud de Servicio</option>
          <option value="orden">Orden de Servicio</option>
        </select>
        <div class="d-flex align-items-center gap-1">
          <small class="text-muted">Desde</small>
          <input type="date" v-model="filterDesde" class="form-control form-control-sm w-auto">
        </div>
        <div class="d-flex align-items-center gap-1">
          <small class="text-muted">Hasta</small>
          <input type="date" v-model="filterHasta" class="form-control form-control-sm w-auto">
        </div>
        <button v-if="filterArea || filterDesde || filterHasta" @click="clearFilters" class="btn btn-sm btn-outline-secondary">✕ Limpiar</button>
      </div>
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
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('nro_dataServicio')">N° <span class="sort-icon">{{ sortKey === 'nro_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('fecha_dataServicio')">Fecha <span class="sort-icon">{{ sortKey === 'fecha_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Area Tematica</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">ST-01 Presupuesto</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Data Servicio</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">ST-02 Solicitud</th>
            <!-- Subcolumnas de Legajo -->
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('nro_legajo')">N° <span class="sort-icon">{{ sortKey === 'nro_legajo' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Fecha</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Legajo</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Factura</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Pago</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center sortable" @click="setSort('plazo_pago')">Plazo <span class="sort-icon">{{ sortKey === 'plazo_pago' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
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
            <th class="add-border-right align-middle text-center">Tipo</th>
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
          <tr v-for="(fila, index) in sortedFilas" :key="index" :class="getRowClass(fila)">

            <!-- Columna Solicitud de Servicio -->

            <td v-if="isAdminOrTecnologicoOrDireccion">{{ fila.nro_dataServicio }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" style="white-space: nowrap;">{{ fila.area_tematica }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              {{ fila.nro_presupuesto }}
              <span v-if="fila.presupuestos_adicionales && fila.presupuestos_adicionales.length > 0" style="color:#888; font-size:11px;">
                , {{ fila.presupuestos_adicionales.map(p => p.nro_presupuesto).join(', ') }}
              </span>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <div style="position: relative; display: inline-flex; justify-content: center; align-items: center;" @click.stop>
                <button class="ds-icon-btn" @click="toggleDSPopup(fila.nro_dataServicio)" title="Data Servicio">
                  <i class="bi bi-file-earmark-check-fill"></i>
                </button>
                <div v-if="openDSPopup === fila.nro_dataServicio" class="opciones-flotantes ds-opciones-flotantes">
                  <div class="opcion" :style="isServiciosTecnologicos ? '--rotation: -120deg' : '--rotation: -90deg'" @click="abrirDataServicio(fila.nro_dataServicio); closeDSPopup()">
                    <i class="bi bi-eye"></i>
                  </div>
                  <div v-if="isServiciosTecnologicos" class="opcion" style="--rotation: -60deg" @click="abrirEditarDataServicio(fila); closeDSPopup()">
                    <i class="bi bi-pencil"></i>
                  </div>
                </div>
              </div>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right">
              <!-- Sin archivos -->
              <template v-if="!fila.adjuntos_solicitud || fila.adjuntos_solicitud.length === 0">
                <div v-if="isServiciosTecnologicos" class="att-empty">
                  <label :for="'solicitud-' + index" style="cursor:pointer;"><i class="bi bi-paperclip"></i></label>
                  <input :id="'solicitud-' + index" style="display:none;" type="file" @change="cargarAdjuntoSolicitud($event, fila.nro_dataServicio)">
                </div>
                <i v-else class="bi bi-stopwatch"></i>
              </template>
              <!-- Con archivos: speed dial -->
              <div v-else style="position: relative; display: inline-flex; justify-content: center; align-items: center;" @click.stop>
                <button class="ds-icon-btn ds-icon-btn--blue" @click="toggleST02Popup(fila.nro_dataServicio)" title="ST-02 Solicitud">
                  <i class="bi bi-files"></i>
                  <span v-if="fila.adjuntos_solicitud.length > 1" class="att-badge-st02">{{ fila.adjuntos_solicitud.length }}</span>
                </button>
                <!-- Speed dial -->
                <div v-if="openST02Popup === fila.nro_dataServicio" class="opciones-flotantes ds-opciones-flotantes">
                  <div class="opcion" :style="isServiciosTecnologicos ? '--rotation: -120deg' : '--rotation: -90deg'" @click="toggleST02FileList(fila.nro_dataServicio); closeST02Popup()">
                    <i class="bi bi-eye"></i>
                  </div>
                  <div v-if="isServiciosTecnologicos" class="opcion" style="--rotation: -60deg">
                    <label :for="'solicitud-add-' + index" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                      <i class="bi bi-plus-lg"></i>
                    </label>
                    <input :id="'solicitud-add-' + index" style="display:none;" type="file" @change="cargarAdjuntoSolicitud($event, fila.nro_dataServicio); closeST02Popup()">
                  </div>
                </div>
                <!-- Lista de archivos (se abre al clickear ojo) -->
                <div v-if="openST02FileList === fila.nro_dataServicio" class="st02-file-popup">
                  <div v-for="f in fila.adjuntos_solicitud" :key="f.id" class="st02-file-row">
                    <span class="st02-file-name" :title="shortFileName(f.archivo)">{{ shortFileName(f.archivo) }}</span>
                    <button class="st02-btn st02-btn-view" @click="viewAttachment(f.archivo)" title="Ver"><i class="bi bi-eye"></i></button>
                    <button v-if="isServiciosTecnologicos" class="st02-btn st02-btn-del" @click="eliminarAdjuntoSolicitud(f.id)" title="Eliminar"><i class="bi bi-trash"></i></button>
                  </div>
                  <div v-if="isServiciosTecnologicos" class="st02-add-row">
                    <label :for="'solicitud-list-add-' + index" class="st02-add-btn">
                      <i class="bi bi-plus-circle"></i> Agregar
                    </label>
                    <input :id="'solicitud-list-add-' + index" style="display:none;" type="file" @change="cargarAdjuntoSolicitud($event, fila.nro_dataServicio)">
                  </div>
                </div>
              </div>
            </td>

            <!-- Columna Legajo -->

            <td v-if="isAdminOrTecnologicoOrDireccion">{{ fila.nro_legajo }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="fecha-columna">{{ fila.fecha_legajo }}</td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="fila.dataServicio_completo && !fila.nro_legajo">
                <div v-if="isAdministracion">
                  <i class="bi bi-plus-circle action-icon" @click="obtenerRangoLab(fila.nro_circuito)"></i>
                </div>
                <div v-else>
                      <i class="bi bi-stopwatch"></i>
                </div>
              </template>
              <template v-else-if="fila.dataServicio_completo && fila.nro_legajo">
                <button
                  :class="fila.labs_adicionales_pendientes > 0 ? 'ds-icon-btn ds-icon-btn--warning' : 'ds-icon-btn'"
                  :title="fila.labs_adicionales_pendientes > 0 ? fila.labs_adicionales_pendientes + ' labs adicionales pendientes de aprobación' : 'Ver Legajo'"
                  @click="fila.labs_adicionales_pendientes > 0 && isAdministracion ? abrirAprobarLabs(fila) : abrirLegajo(fila)"
                >
                  <i class="bi bi-file-earmark-check-fill"></i>
                </button>
              </template>
              <template v-else>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="fila.nro_legajo">
                <AttachmentCell
                  :files="fila.adjuntos_factura"
                  :can-upload="isAdministracion"
                  :can-delete="isAdministracion"
                  :input-id="'factura-' + index"
                  @upload="cargarAdjuntoFactura($event, fila.nro_legajo, fila.nro_circuito)"
                  @delete="eliminarAdjuntoFactura"
                />
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
              <template v-if="fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total'">
                <template v-if="!fila.nros_remitos">
                  <div v-if="isServiciosTecnologicos">
                    <i class="bi bi-plus-circle action-icon" @click="abrirModalRemito(fila)"></i>
                  </div>
                </template>
                <template v-else>
                  <div v-if="isServiciosTecnologicos">
                    <span @click="abrirModalRemito(fila)" style="cursor: pointer;">{{ fila.nros_remitos }}</span>
                  </div>
                  <div v-else>
                    <span>{{ fila.nros_remitos }}</span>
                  </div>
                </template>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <div>
                <template v-if="fila.estado_recepcion">
                  <div v-if="isServiciosTecnologicos">
                    <span v-if="fila.estado_recepcion === 'sin_llegar'" class="no-wrap-column" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Sin Llegar</span>
                    <span v-else-if="fila.estado_recepcion === 'parcial'" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Parcial</span>
                    <span v-else-if="fila.estado_recepcion === 'total'" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Total</span>
                  </div>
                  <div v-else>
                    <span v-if="fila.estado_recepcion === 'sin_llegar'" class="no-wrap-column">Sin Llegar</span>
                    <span v-else-if="fila.estado_recepcion === 'parcial'">Parcial</span>
                    <span v-else-if="fila.estado_recepcion === 'total'">Total</span>
                  </div>
                </template>
                <i v-else-if="isServiciosTecnologicos && fila.nro_legajo" class="bi bi-plus-circle action-icon" @click="abrirModalEstadoMuestras(fila)"></i>
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
                      <i class="bi bi-plus-circle action-icon" @click="abrirModalCrearOrdenServicio(fila)"></i>
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
                  <span @click="abrirModalPlazoOrdenServicio(fila)" style="cursor: pointer;" :title="'Plazo original: ' + fila.plazo_estimado + ' días'">
                    {{ diasRestantesOS(fila) }}
                  </span>
                </div>
                <div v-else>
                  <span :title="'Plazo original: ' + fila.plazo_estimado + ' días'">
                    {{ diasRestantesOS(fila) }}
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
                    <i class="bi bi-plus-circle action-icon" @click="abrirModalCrearSolicitudInterArea(fila)"></i>
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
              <template v-if="fila.nro_solicitudInterarea !== ''">
                <AttachmentCell
                  :files="fila.informes_interarea"
                  :can-upload="!isAdminOrTecnologicoOrDireccion"
                  :can-delete="!isAdminOrTecnologicoOrDireccion"
                  :input-id="'interarea-' + index"
                  @upload="cargarAdjuntoInformeInterarea($event, fila)"
                  @delete="eliminarAdjuntoInformeInterarea"
                />
              </template>
            </td>

            <!-- Columna Fecha Informe de Area (por ciclo) -->
            <td>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <span class="no-wrap-column" v-if="ciclo.fecha_informeArea">{{ ciclo.fecha_informeArea }}</span>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Solicitante -->
            <td style="white-space: nowrap;">
              <template v-if="fila.ordenServicio_completo === true && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                {{ fila.nombre_solicitante }}
              </template>
            </td>

            <!-- Columna Informe Area (por ciclo) -->
            <td>
              <template v-if="fila.ordenServicio_completo === true && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <div v-for="ciclo in fila.ciclos" :key="ciclo.id"
                     class="ciclo-row"
                     :class="{ 'ciclo-row--final': fila.ciclos.some(c => c.tipo === 'final') }">
                  <span v-if="ciclo.adjunto_informeArea" class="attachment-wrap">
                    <i class="bi bi-file-earmark-check-fill action-icon" style="color:#198754; cursor:pointer;"
                       @click.stop="togglePopupInformeArea(ciclo.id)"
                       :title="'Informe ' + (ciclo.tipo === 'parcial' ? 'Parcial' : ciclo.tipo === 'complementario' ? 'Complementario' : 'Final') + ' ' + ciclo.numero"></i>
                    <div v-if="popupInformeAreaId === ciclo.id" class="attach-popup" @click.stop>
                      <button class="attach-popup-item" @mousedown.prevent="abrirArchivo(ciclo.adjunto_informeArea)">
                        <i class="bi bi-eye"></i> Ver
                      </button>
                      <button v-if="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion"
                              class="attach-popup-item"
                              @mousedown.prevent="cambiarTipoCiclo(ciclo, fila)">
                        <i class="bi bi-tag"></i> Cambiar tipo
                      </button>
                      <button v-if="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion"
                              class="attach-popup-item text-danger"
                              @mousedown.prevent="eliminarInformeAreaCiclo(ciclo)">
                        <i class="bi bi-trash"></i> Eliminar
                      </button>
                    </div>
                  </span>
                  <span v-else-if="isAreaJefe || isAreaStandard">
                    <label :for="'inf-area-ciclo-' + ciclo.id" style="cursor:pointer;" title="Subir informe área">
                      <i class="bi bi-paperclip action-icon"></i>
                    </label>
                    <input :id="'inf-area-ciclo-' + ciclo.id" style="display:none;" type="file"
                           @change="seleccionarArchivoInformeAreaCiclo($event, ciclo, fila)">
                  </span>
                  <span v-else><i class="bi bi-stopwatch"></i></span>
                </div>
                <!-- Clip para agregar otro parcial: fila separada debajo del último -->
                <div v-if="(isAreaJefe || isAreaStandard)
                           && fila.ciclos.length > 0
                           && fila.ciclos[fila.ciclos.length-1].adjunto_informeArea
                           && fila.ciclos[fila.ciclos.length-1].tipo === 'parcial'"
                     class="ciclo-row" @click.stop>
                  <label :for="'inf-area-nuevo-' + fila.ciclos[fila.ciclos.length-1].id"
                         style="cursor:pointer;" title="Agregar otro informe parcial">
                    <i class="bi bi-paperclip action-icon"></i>
                  </label>
                  <input :id="'inf-area-nuevo-' + fila.ciclos[fila.ciclos.length-1].id"
                         style="display:none;" type="file"
                         @change="seleccionarArchivoParaNuevoCiclo($event, fila)">
                </div>
              </template>
            </td>

            <!-- Columna Registros de Ensayo (por ciclo) -->
            <td>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id"
                   class="ciclo-row"
                   :class="{ 'ciclo-row--final': fila.ciclos.some(c => c.tipo === 'final') }">
                <AttachmentCell
                  :files="ciclo.registros_ensayo"
                  :can-upload="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion && ciclo.tipo === 'parcial'"
                  :can-delete="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion"
                  :input-id="'registros-ciclo-' + ciclo.id"
                  file-icon="bi bi-folder-check"
                  empty-icon="bi bi-folder-plus"
                  :tooltip-label="(ciclo.tipo === 'parcial' ? 'Parcial' : ciclo.tipo === 'complementario' ? 'Complementario' : 'Final') + ' ' + ciclo.numero"
                  @upload="subirRegistroEnsayoCiclo($event, ciclo)"
                  @delete="eliminarRegistroEnsayoCiclo"
                />
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Estado/Tipo (por ciclo) -->
            <td class="add-border-right">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <span v-if="ciclo.adjunto_informeArea"
                      class="badge"
                      :class="ciclo.tipo === 'complementario' ? 'bg-success' : ciclo.tipo === 'final' ? 'bg-dark' : 'bg-primary'"
                      style="font-size:10px;">
                  {{ ciclo.tipo === 'complementario' ? 'Compl.' : ciclo.tipo === 'final' ? 'Final' : 'Parcial' }}
                </span>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Administracion - Informe Servicio (por ciclo) -->
            <td class="add-border-right">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.adjunto_informeArea && ciclo.registros_ensayo && ciclo.registros_ensayo.length > 0">
                  <!-- Sin informe servicio, sin corrección pendiente -->
                  <template v-if="!ciclo.adjunto_informeServicio && !ciclo.corregir">
                    <div v-if="isAdministracion">
                      <label :for="'inf-serv-ciclo-' + ciclo.id" style="cursor:pointer;" title="Subir informe servicio">
                        <i class="bi bi-paperclip action-icon"></i>
                      </label>
                      <input :id="'inf-serv-ciclo-' + ciclo.id" style="display:none;" type="file"
                             @change="subirInformeServicioCiclo($event, ciclo)">
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <!-- Con informe servicio, sin corrección -->
                  <template v-else-if="ciclo.adjunto_informeServicio && !ciclo.corregir">
                    <i class="bi bi-check-lg" style="color:green;"></i>
                  </template>
                  <!-- Con corrección pendiente -->
                  <template v-else-if="ciclo.corregir">
                    <div v-if="isAdministracion">
                      <i class="bi bi-filetype-pdf action-icon" @click="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe"></i>
                      <label :for="'inf-serv-corr-ciclo-' + ciclo.id" style="cursor:pointer; margin-left:4px;" title="Resubir">
                        <i class="bi bi-upload action-icon"></i>
                      </label>
                      <input :id="'inf-serv-corr-ciclo-' + ciclo.id" style="display:none;" type="file"
                             @change="subirInformeServicioCiclo($event, ciclo)">
                      <i class="bi bi-backspace-fill text-danger action-icon"
                         @click="abrirModalCorreccionesCiclo(ciclo)" title="Ver correcciones" style="font-size:0.8em;"></i>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Revisión Servicios Tecnológicos (por ciclo) -->
            <td class="add-border-right">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.adjunto_informeServicio && !ciclo.revision_confirmada && !ciclo.firma_responsable_area && !ciclo.firma_direccion && !ciclo.corregir">
                  <div v-if="isServiciosTecnologicos">
                    <i class="bi bi-filetype-pdf action-icon" @click="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe"></i>
                    <i class="bi bi-check-circle action-icon text-primary" style="cursor:pointer; margin-left:4px;"
                       @click="abrirModalRevisionCiclo(ciclo)" title="Confirmar revisión"></i>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.revision_confirmada && !ciclo.corregir">
                  <i class="bi bi-check-lg" style="color:green;"></i>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Responsable Área - Firma (por ciclo) -->
            <td class="add-border-right">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.revision_confirmada && !ciclo.firma_responsable_area && !ciclo.firma_direccion && !ciclo.corregir">
                  <div v-if="isAreaJefe">
                    <i class="bi bi-filetype-pdf action-icon" @click="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe"></i>
                    <i class="bi bi-exclamation-triangle action-icon text-warning" style="cursor:pointer; margin-left:4px;"
                       @click="abrirModalAdvertirCorreccionesCiclo(ciclo)" title="Advertir correcciones"></i>
                    <i class="bi bi-pen action-icon text-primary" style="cursor:pointer; margin-left:4px;"
                       @click="abrirModalFirmaResponsableAreaCiclo(ciclo)" title="Firmar"></i>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.firma_responsable_area">
                  <i class="bi bi-check-lg" style="color:green;"></i>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Dirección - Firma (por ciclo) -->
            <td class="add-border-right">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.firma_responsable_area && !ciclo.firma_direccion">
                  <div v-if="isDireccion">
                    <i class="bi bi-filetype-pdf action-icon" @click="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe"></i>
                    <i class="bi bi-pen action-icon text-primary" style="cursor:pointer; margin-left:4px;"
                       @click="abrirModalFirmaDireccionCiclo(ciclo)" title="Firmar"></i>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.firma_direccion">
                  <i class="bi bi-check-lg" style="color:green;"></i>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
            </td>

            <!-- Columna Archivo -->
            <td v-if="isAdminOrTecnologicoOrDireccion">
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
            <div class="d-flex align-items-center gap-2 no-print">
              <button type="button" class="btn btn-sm btn-outline-secondary" @click="imprimirDataServicio" title="Imprimir / Guardar como PDF">
                <i class="bi bi-printer"></i>
              </button>
              <button type="button" class="btn-close" @click="cerrarModalDataServicio" aria-label="Close"></button>
            </div>
          </div>
          <!-- Modal Body -->
          <div class="modal-body">
            <div class="ds-header mb-3">
              <div>
                <div class="ds-doc-title">Data Servicio N° {{ nroDataServicio }}</div>
                <div class="ds-doc-sub">N° Presupuesto: <strong>{{ nroPresupuestoDataServicio }}</strong></div>
              </div>
              <div class="ds-fecha">
                <span class="ds-fecha-label">Fecha</span>
                <span class="ds-fecha-val">{{ fechaDataServicio }}</span>
              </div>
            </div>

            <div class="ds-grid">
              <div class="ds-field">
                <span class="ds-label">Área Temática</span>
                <span class="ds-val">{{ areaDataServicio }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Solicitante</span>
                <span class="ds-val">{{ solicitanteDataServicio }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Obra</span>
                <span class="ds-val">{{ obraDataServicio || '—' }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Cant. Laboratorios</span>
                <span class="ds-val">{{ cantNumLabsDataServicio }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Plazo Estimado</span>
                <span class="ds-val">{{ plazoEstimadoDataServicio }} días</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Arancel</span>
                <span class="ds-val ds-arancel">{{ arancelDataServicio }}</span>
              </div>
              <div class="ds-field ds-field--full">
                <span class="ds-label">Muestras</span>
                <span class="ds-val">{{ muestrasDataServicio }}</span>
              </div>
              <div class="ds-field ds-field--full">
                <span class="ds-label">Observaciones</span>
                <span class="ds-val">{{ observacionesDataServicio || '—' }}</span>
              </div>
            </div>
          </div>
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Editar Data Servicio -->
    <div class="modal" :class="{ 'show': mostrarModalEditarDS }" id="modalEditarDS">
      <div class="modal-dialog modal-dialog-md">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar Data Servicio #{{ editarDS.nro_dataServicio }}</h5>
            <button type="button" class="btn-close" @click="cerrarEditarDataServicio"></button>
          </div>
          <div class="modal-body">
            <!-- Presupuestos -->
            <div class="mb-3">
              <label class="form-label fw-bold">Presupuestos</label>
              <div class="mb-1">
                <span class="badge bg-secondary me-1">Principal: #{{ editarDS.nro_presupuesto }}</span>
                <span v-for="p in editarDS.presupuestos_adicionales" :key="p.nro_presupuesto" class="badge bg-info me-1">
                  #{{ p.nro_presupuesto }} — ${{ p.arancel_presupuesto }}
                  <button type="button" class="btn-close btn-close-white ms-1" style="font-size:8px;" @click="quitarPresupuestoAdicional(p.nro_presupuesto)"></button>
                </span>
              </div>
              <div class="input-group input-group-sm mt-2">
                <input type="number" class="form-control" v-model="editarDS.nuevoPres" placeholder="Nro presupuesto a agregar" />
                <button class="btn btn-outline-secondary" @click="agregarPresupuestoAdicional">Agregar</button>
              </div>
              <div v-if="editarDS.presupuestoInfo" class="mt-1 text-muted" style="font-size:12px;">
                {{ editarDS.presupuestoInfo }}
              </div>
            </div>
            <!-- Total -->
            <div class="mb-3">
              <label class="form-label fw-bold">Total estimado</label>
              <div class="fw-bold text-success">${{ editarDS.totalCalculado }}</div>
            </div>
            <!-- Plazo -->
            <div class="mb-3">
              <label class="form-label fw-bold">Plazo estimado (días)</label>
              <input type="number" class="form-control" v-model="editarDS.plazo_estimado" min="1" />
            </div>
            <!-- Cant. Labs -->
            <div class="mb-3">
              <label class="form-label fw-bold">Cantidad de laboratorios</label>
              <input type="number" class="form-control" v-model="editarDS.cant_numLabs" min="1" />
              <div v-if="parseInt(editarDS.cant_numLabs) > editarDS.cant_numLabs_original" class="form-text text-warning">
                ⚠️ Se agregarán {{ parseInt(editarDS.cant_numLabs) - editarDS.cant_numLabs_original }} lab(s) adicionales — pendientes de aprobación por Administración
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cerrarEditarDataServicio">Cancelar</button>
            <button class="btn btn-primary" @click="guardarEdicionDataServicio">Guardar cambios</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Aprobar Labs Adicionales -->
    <div class="modal" :class="{ 'show': mostrarModalAprobarLabs }" id="modalAprobarLabs">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Labs adicionales pendientes</h5>
            <button type="button" class="btn-close" @click="cerrarAprobarLabs"></button>
          </div>
          <div class="modal-body">
            <p>Circuito <strong>#{{ aprobarLabs.nro_circuito }}</strong></p>
            <p>Se solicitan <strong>{{ aprobarLabs.labs_adicionales_pendientes }}</strong> laboratorio(s) adicional(es).</p>
            <p class="text-muted">Al aprobar, se calculará automáticamente el nuevo rango de números de laboratorio y se añadirá al legajo existente.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cerrarAprobarLabs">Cancelar</button>
            <button class="btn btn-warning" @click="confirmarAprobarLabs">Aprobar y asignar rango</button>
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
            <div class="d-flex align-items-center gap-2 no-print">
              <button type="button" class="btn btn-sm btn-outline-secondary" @click="imprimirLegajo" title="Imprimir / Guardar como PDF">
                <i class="bi bi-printer"></i>
              </button>
              <button type="button" class="btn-close" @click="cerrarModalLegajo" aria-label="Close"></button>
            </div>
          </div>
          <!-- Modal Body -->
          <div class="modal-body lg-body">
            <div class="lg-fecha-row">
              <span class="lg-fecha-label">Fecha</span>
              <span class="lg-fecha-val">{{ fechaLegajoFormateada }}</span>
            </div>
            <div class="lg-title-area">
              <div class="lg-number">Legajo N° {{ nroLegajo }}/{{ añoLegajo }}</div>
              <div class="lg-divider"></div>
            </div>
            <div class="lg-fields">
              <div class="lg-field">
                <span class="lg-label">Solicitante</span>
                <span class="lg-value">{{ nombreSolicitante }}</span>
              </div>
              <div class="lg-field">
                <span class="lg-label">Rango N° Laboratorios</span>
                <span class="lg-value">{{ rangosLaboratorios }}</span>
              </div>
            </div>
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
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-logo"></div>
            <h1 class="modal-title fs-5 fw-bold">{{ osReadOnly ? 'Orden de Servicio N°' + nroOS : 'Crear Orden de Servicio' }}</h1>
            <button type="button" class="btn-close" @click="cerrarModalCrearOrdenServicio"></button>
          </div>
          <div class="modal-body">
            <form class="was-validated">
              <div class="mb-3">
                <label class="form-label">Fecha:</label>
                <input v-model="fechaOS" type="date" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Área Temática:</label>
                <input v-model="areaOS" type="text" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">N° Legajo:</label>
                <input v-model="legajoOS" type="text" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Rangos Laboratorios:</label>
                <input v-model="rangosOS" type="text" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Plazo Estimado:</label>
                <input v-model="plazoOS" type="text" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Solicitante:</label>
                <input v-model="solicitanteOS" type="text" readonly class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Servicios Solicitados:</label>
                <table class="table">
                  <thead>
                    <tr>
                      <th style="text-align:left;">Servicio</th>
                      <th style="text-align:center;">Cantidad</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(servicio, index) in servicioOS" :key="index">
                      <td style="text-align:left;">{{ servicio.servicio }}</td>
                      <td>{{ servicio.cant }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="mb-3">
                <label class="form-label">Muestras:</label>
                <input v-model="muestrasOS" type="text" readonly class="form-control" required />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button v-if="!osReadOnly" type="button" class="btn btn-primary" @click="crearOrdenServicio">Confirmar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCrearOrdenServicio">{{ osReadOnly ? 'Cerrar' : 'Cancelar' }}</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalOrdenServicio }" id="mostrarModalOrdenServicio">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-logo"></div>
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
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
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

    <!-- Modal Tipo de Ciclo -->
    <div class="modal" :class="{ 'show': mostrarModalTipoCiclo }" id="mostrarModalTipoCiclo">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{ esCambioTipo ? 'Cambiar tipo de informe' : 'Tipo de Informe' }}</h4>
            <button type="button" class="btn-close" @click="cerrarModalTipoCiclo"></button>
          </div>
          <div class="modal-body">
            <p>{{ esCambioTipo ? '¿A qué tipo desea cambiar el informe?' : '¿Qué tipo de informe es?' }}</p>
            <small class="text-muted">
              <strong>Parcial:</strong> hay más informes pendientes.<br>
              <strong>Complementario:</strong> complementa parciales anteriores.<br>
              <strong>Final:</strong> es el único informe del circuito.
            </small>
          </div>
          <div class="modal-footer flex-wrap gap-1">
            <template v-if="esCambioTipo">
              <button type="button" class="btn btn-primary" @click="confirmarCambioTipo('parcial')">Parcial</button>
              <button v-if="hayParcialesPrevios" type="button" class="btn btn-success"
                      @click="confirmarCambioTipo('complementario')">Complementario</button>
              <button v-if="!hayParcialesPrevios" type="button" class="btn btn-dark"
                      @click="confirmarCambioTipo('final')">Final</button>
            </template>
            <template v-else>
              <button type="button" class="btn btn-primary" @click="subirInformeAreaCiclo('parcial')">Parcial</button>
              <button v-if="hayParcialesPrevios" type="button" class="btn btn-success"
                      @click="subirInformeAreaCiclo('complementario')">Complementario</button>
              <button v-if="!hayParcialesPrevios" type="button" class="btn btn-dark"
                      @click="subirInformeAreaCiclo('final')">Final</button>
            </template>
            <button type="button" class="btn btn-secondary" @click="cerrarModalTipoCiclo">Cancelar</button>
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

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="crearSolicitudInterArea(fila); cerrarModalCrearSolicitudInterArea">Crear</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCrearSolicitudInterArea">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalSolicitudInterArea }" id="mostrarModalSolicitudInterArea">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-logo"></div>
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
          <!-- Modal Footer -->
          <div class="modal-footer-a4">
            <div class="footer-image"></div>
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
            <button type="button" class="btn btn-primary" @click="corregirCiclo()">Corregido</button>
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
            <button type="button" class="btn btn-primary" @click="confirmarRevisionCiclo()">Si</button>
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
            <button type="button" class="btn btn-primary" @click="advertirCorreccionesCiclo(correccionesNuevas)">Advertir Correcciones</button>
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
            <button type="button" class="btn btn-primary" @click="confirmarFirmaResponsableAreaCiclo()">Si</button>
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
            <button type="button" class="btn btn-primary" @click="confirmarFirmaDireccionCiclo()">Si</button>
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
  import { onMounted, onUnmounted, ref, computed } from 'vue';
  import api from '@/api.js';
  import { AREAS_TEMATICAS } from '@/constants/areas.js';
  import AttachmentCell from './AttachmentCell.vue';

  export default {
    components: { AttachmentCell },
    setup() {

      // Setup General
      const filas = ref([]);

      const sortKey = ref('');
      const sortDir = ref('asc');
      const sortedFilas = computed(() => {
        if (!sortKey.value) return filteredFilas.value;
        return [...filteredFilas.value].sort((a, b) => {
          const valA = ['nro_dataServicio','nro_legajo','plazo_pago'].includes(sortKey.value) ? Number(a[sortKey.value]) : a[sortKey.value];
          const valB = ['nro_dataServicio','nro_legajo','plazo_pago'].includes(sortKey.value) ? Number(b[sortKey.value]) : b[sortKey.value];
          if (valA < valB) return sortDir.value === 'asc' ? -1 : 1;
          if (valA > valB) return sortDir.value === 'asc' ? 1 : -1;
          return 0;
        });
      });
      const setSort = (key) => {
        if (sortKey.value === key) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
        else { sortKey.value = key; sortDir.value = 'asc'; }
      };

      const filterArea = ref('');
      const filterDesde = ref('');
      const filterHasta = ref('');
      const filterTipoFecha = ref('solicitud');
      const uniqueAreas = AREAS_TEMATICAS;

      const parseFechaFila = (s) => {
        if (!s) return '';
        const [d, m, y] = s.split('/');
        return `${y}-${m}-${d}`;
      };

      const todayBuenosAires = () => {
        const parts = new Intl.DateTimeFormat('en-CA', {
          timeZone: 'America/Argentina/Buenos_Aires',
          year: 'numeric', month: '2-digit', day: '2-digit'
        }).format(new Date());
        const [y, m, d] = parts.split('-').map(Number);
        return new Date(y, m - 1, d);
      };

      const diasRestantesOS = (fila) => {
        if (!fila.ordenServicio_completo || !fila.fecha_ordenServicio || !fila.plazo_estimado) return null;
        const fechaISO = parseFechaFila(fila.fecha_ordenServicio);
        if (!fechaISO || fechaISO.length < 10) return null;
        const [y, m, d] = fechaISO.split('-').map(Number);
        const inicio = new Date(y, m - 1, d);
        const hoy = todayBuenosAires();
        const diasTranscurridos = Math.floor((hoy - inicio) / 86400000);
        return Number(fila.plazo_estimado) - diasTranscurridos;
      };

      const getRowClass = (fila) => {
        if (fila.firma_direccion === true) return '';
        const restantes = diasRestantesOS(fila);
        if (restantes === null) return '';
        if (restantes <= 3) return 'row-urgente';
        if (restantes <= 7) return 'row-alerta';
        return '';
      };

      const filteredFilas = computed(() => filas.value.filter(f => {
        const areaOk = !filterArea.value || f.area_tematica === filterArea.value;
        const fechaRaw = filterTipoFecha.value === 'orden' ? f.fecha_ordenServicio : f.fecha_dataServicio;
        const fecha = parseFechaFila(fechaRaw);
        const desdeOk = !filterDesde.value || fecha >= filterDesde.value;
        const hastaOk = !filterHasta.value || fecha <= filterHasta.value;
        return areaOk && desdeOk && hastaOk;
      }));

      const clearFilters = () => {
        filterArea.value = '';
        filterDesde.value = '';
        filterHasta.value = '';
        filterTipoFecha.value = 'solicitud';
      };
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
      // Popup Data Servicio
      const openDSPopup = ref(null);
      const toggleDSPopup = (nro) => {
        filaSeleccionada.value = null;
        openST02Popup.value = null;
        openST02FileList.value = null;
        const newVal = openDSPopup.value === nro ? null : nro;
        openDSPopup.value = newVal;
        if (newVal !== null) document.dispatchEvent(new CustomEvent('speed-dial-open'));
      };
      const closeDSPopup = () => { openDSPopup.value = null; };

      // Popup ST-02 Solicitud (speed dial + file list)
      const openST02Popup = ref(null);
      const openST02FileList = ref(null);
      const toggleST02Popup = (nro) => {
        filaSeleccionada.value = null;
        openDSPopup.value = null;
        openST02FileList.value = null;
        const newVal = openST02Popup.value === nro ? null : nro;
        openST02Popup.value = newVal;
        if (newVal !== null) document.dispatchEvent(new CustomEvent('speed-dial-open'));
      };
      const closeST02Popup = () => { openST02Popup.value = null; };
      const toggleST02FileList = (nro) => {
        openST02FileList.value = openST02FileList.value === nro ? null : nro;
      };
      const shortFileName = (archivo) => {
        const name = archivo ? archivo.split('/').pop() : '';
        return name.length > 28 ? name.slice(0, 25) + '...' : name;
      };
      const viewAttachment = (archivo) => {
        window.open(window.location.origin + '/media/' + archivo, '_blank');
      };

      // Editar Data Servicio
      const mostrarModalEditarDS = ref(false);
      const editarDS = ref({
        nro_dataServicio: null,
        nro_circuito: null,
        nro_presupuesto: null,
        presupuestos_adicionales: [],
        plazo_estimado: null,
        cant_numLabs: null,
        cant_numLabs_original: null,
        nuevoPres: '',
        presupuestoInfo: '',
        totalCalculado: 0,
      });

      const abrirEditarDataServicio = (fila) => {
        editarDS.value = {
          nro_dataServicio: fila.nro_dataServicio,
          nro_circuito: fila.nro_circuito,
          nro_presupuesto: fila.nro_presupuesto,
          presupuestos_adicionales: [...(fila.presupuestos_adicionales || [])],
          plazo_estimado: fila.plazo_estimado_ds,
          cant_numLabs: fila.cant_numLabs,
          cant_numLabs_original: fila.cant_numLabs,
          nuevoPres: '',
          presupuestoInfo: '',
          totalCalculado: 0,
        };
        mostrarModalEditarDS.value = true;
      };

      const cerrarEditarDataServicio = () => { mostrarModalEditarDS.value = false; };

      const agregarPresupuestoAdicional = async () => {
        const nro = editarDS.value.nuevoPres;
        if (!nro) return;
        try {
          const res = await api.get(`/encurso/presupuesto_seleccionado/${nro}/`);
          editarDS.value.presupuestoInfo = `Presupuesto #${nro} — ${res.data.nombre_solicitante}`;
          // Lo guardamos directamente (se persiste al guardar)
          if (!editarDS.value.presupuestos_adicionales.find(p => p.nro_presupuesto === parseInt(nro))) {
            editarDS.value.presupuestos_adicionales.push({ nro_presupuesto: parseInt(nro), arancel_presupuesto: res.data.arancel_presupuesto || '—' });
          }
          editarDS.value.nuevoPres = '';
        } catch {
          editarDS.value.presupuestoInfo = 'Presupuesto no encontrado.';
        }
      };

      const quitarPresupuestoAdicional = (nro) => {
        editarDS.value.presupuestos_adicionales = editarDS.value.presupuestos_adicionales.filter(p => p.nro_presupuesto !== nro);
      };

      const guardarEdicionDataServicio = async () => {
        const { nro_dataServicio, plazo_estimado, cant_numLabs, presupuestos_adicionales } = editarDS.value;
        try {
          // Guardar plazo y labs
          await api.patch(`/encurso/editar_dataservicio/${nro_dataServicio}/`, {
            plazo_estimado,
            cant_numLabs,
          });
          // Agregar presupuestos adicionales nuevos
          for (const p of presupuestos_adicionales) {
            await api.patch(`/encurso/editar_dataservicio/${nro_dataServicio}/`, {
              nro_presupuesto_adicional: p.nro_presupuesto,
            });
          }
          cerrarEditarDataServicio();
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al editar Data Servicio:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Aprobar Labs Adicionales
      const mostrarModalAprobarLabs = ref(false);
      const aprobarLabs = ref({ nro_circuito: null, labs_adicionales_pendientes: 0 });

      const abrirAprobarLabs = (fila) => {
        aprobarLabs.value = { nro_circuito: fila.nro_circuito, labs_adicionales_pendientes: fila.labs_adicionales_pendientes };
        mostrarModalAprobarLabs.value = true;
      };

      const cerrarAprobarLabs = () => { mostrarModalAprobarLabs.value = false; };

      const confirmarAprobarLabs = async () => {
        try {
          await api.post(`/encurso/aprobar_labs_adicionales/${aprobarLabs.value.nro_circuito}/`);
          cerrarAprobarLabs();
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al aprobar labs:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

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
      const osReadOnly = ref(false);
      const mostrarModalOrdenServicio = ref(false);
      const mostrarModalPlazoOrdenServicio = ref(false);
      // Setup Ciclos de Informe
      const mostrarModalTipoCiclo = ref(false);
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
      const correccionesNuevas = ref('');
      const mostrarModalFirmaResponsableArea = ref(false);

      // Setup Direccion - Firma
      const mostrarModalFirmaDireccion = ref(false);

      // Setup Archivar
      const mostrarModalArchivar = ref(false);


      //methods

      const fetchData = () => {
          api.get('/encurso/obtener_todoencurso/')
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
                const solicitudInterAreaCorrespondiente = data.solicitudes_inter_area.find(solicitudes_inter_area => solicitudes_inter_area.nro_circuito === solicitud.nro_circuito);
                // Arrays multi-adjunto
                const adjuntos_solicitud = (data.adjuntos_solicitud || [])
                  .filter(a => a.data_servicio === solicitud.nro_dataServicio)
                  .map(a => ({ id: a.id, archivo: a.archivo }));

                const adjuntos_factura = legajoCorrespondiente
                  ? (data.adjuntos_factura || [])
                    .filter(a => a.legajo === legajoCorrespondiente.nro_legajo)
                    .map(a => ({ id: a.id, archivo: a.archivo }))
                  : [];

                const ciclos = (data.ciclos || [])
                  .filter(c => c.nro_circuito === solicitud.nro_circuito)
                  .map(c => ({
                    id: c.id,
                    numero: c.numero,
                    tipo: c.tipo,
                    adjunto_informeArea: c.adjunto_informeArea,
                    fecha_informeArea: c.fecha_informeArea ? formatDate(c.fecha_informeArea) : '',
                    registros_ensayo: (c.registros_ensayo || []).map(r => ({ id: r.id, archivo: r.archivo })),
                    adjunto_informeServicio: c.adjunto_informeServicio,
                    fecha_informeServicio: c.fecha_informeServicio ? formatDate(c.fecha_informeServicio) : '',
                    correcciones: c.correcciones,
                    corregir: c.corregir,
                    revision_confirmada: c.revision_confirmada,
                    firma_responsable_area: c.firma_responsable_area,
                    firma_direccion: c.firma_direccion,
                  }));

                const informes_interarea = (data.informes_inter_area || [])
                  .filter(ii => ii.nro_circuito === solicitud.nro_circuito)
                  .map(ii => ({ id: ii.nro_informeInterarea, archivo: ii.adjunto_informeInterarea }));

                const ultimoCiclo = ciclos.length > 0 ? ciclos[ciclos.length - 1] : null;

                // Construir la fila de la tabla combinando datos de solicitudes, legajos, recepciones, etc.
                const fila = {
                  // Solicitud
                  nro_dataServicio: solicitud.nro_dataServicio,
                  fecha_dataServicio: formatDate(solicitud.fecha_dataServicio),
                  area_tematica: formatAreaTematica(solicitud.area_tematica),
                  nro_presupuesto: solicitud.nro_presupuesto,
                  presupuestos_adicionales: solicitud.presupuestos_adicionales || [],
                  plazo_estimado_ds: solicitud.plazo_estimado,
                  cant_numLabs: solicitud.cant_numLabs,
                  adjuntos_solicitud,
                  nro_circuito: solicitud.nro_circuito,
                  dataServicio_completo: solicitud.completo,
                  // Legajo
                  nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo : '',
                  fecha_legajo: legajoCorrespondiente ? formatDate(legajoCorrespondiente.fecha_legajo) : '',
                  adjuntos_factura,
                  pago: legajoCorrespondiente ? legajoCorrespondiente.pago : '',
                  plazo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago : '',
                  legajo_completo: legajoCorrespondiente ? legajoCorrespondiente.completo : '',
                  labs_adicionales_pendientes: legajoCorrespondiente ? (legajoCorrespondiente.labs_adicionales_pendientes || 0) : 0,
                  // Recepcion
                  nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.nros_remitos : '',
                  estado_recepcion: recepcionCorrespondiente ? recepcionCorrespondiente.estado_recepcion : '',
                  plazo_muestras: recepcionCorrespondiente ? recepcionCorrespondiente.plazo_muestras : '',
                  // Orden de Servicio
                  nro_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.nro_ordenServicio : '',
                  fecha_ordenServicio: ordenCorrespondiente ? formatDate(ordenCorrespondiente.fecha_ordenServicio) : '',
                  plazo_estimado: solicitud.plazo_estimado,
                  ordenServicio_completo: ordenCorrespondiente ? ordenCorrespondiente.completo : '',
                  // Ciclos de Informe
                  ciclos,
                  firma_direccion: ultimoCiclo ? ultimoCiclo.firma_direccion : false,
                  nombre_solicitante: solicitud.nombre_solicitante,
                  // Solicitud Inter Area
                  nro_solicitudInterarea: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.nro_solicitudInterarea : '',
                  fecha_solicitudInterarea: solicitudInterAreaCorrespondiente ? formatDate(solicitudInterAreaCorrespondiente.fecha_solicitudInterarea) : '',
                  inter_areaTematica: solicitudInterAreaCorrespondiente ? formatAreaTematica(solicitudInterAreaCorrespondiente.inter_areaTematica) : '',
                  muestras_solicitudIa: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.muestras_solicitudIa : '',
                  num_labs: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.num_labs : '',
                  observaciones: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.observaciones : '',
                  // Informe Inter Area
                  nro_solicitudInterarea_ia: solicitudInterAreaCorrespondiente ? solicitudInterAreaCorrespondiente.nro_solicitudInterarea : '',
                  informes_interarea,
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

      // Cierra todos los speed dials al hacer click fuera o al abrir un AttachmentCell
      const closeAllPopups = () => {
        openDSPopup.value = null;
        openST02Popup.value = null;
        openST02FileList.value = null;
        filaSeleccionada.value = null;
        popupInformeAreaId.value = null;
      };

      onMounted(() => {
        fetchData();
        document.addEventListener('click', closeAllPopups);
        document.addEventListener('att-cell-open', closeAllPopups);
        document.addEventListener('encurso-refresh', fetchData);
      });

      onUnmounted(() => {
        document.removeEventListener('click', closeAllPopups);
        document.removeEventListener('att-cell-open', closeAllPopups);
        document.removeEventListener('encurso-refresh', fetchData);
      });

      const triggerFileInput = () => {
      document.getElementById('fileInput').click();
      };

      // SOLICITUD DE SERVICIO

      // DS - Data Servicio
      const abrirDataServicio = (nro_dataServicio) => {
          api.get(`/encurso/obtener_dataservicio/${nro_dataServicio}/`)
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
          api.post('/encurso/guardar_adjuntosolicitudservicio/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
                  fetchData();
                  showSuccessAlert.value = true;
                  setTimeout(() => { showSuccessAlert.value = false; }, 3000);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
                  showErrorAlert.value = true;
                  setTimeout(() => { showErrorAlert.value = false; }, 3000);
              });
      };

      // LEGAJO

      // Legajo - Crear
      const obtenerRangoLab = (nro_circuito) => {
        // Realizar la llamada a la API para obtener el rango de laboratorios
        api.get(`/encurso/obtener_rangoLab/${nro_circuito}/`)
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
        api.post('/encurso/crear_legajo/', nuevoLegajo.value)
        .then(response => {
          console.log(response)
          cerrarModalCrearLegajo();
          fetchData();

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
          api.get(`/encurso/obtener_legajo/${nro_circuito}/`)
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
          api({
              method: 'get',
              url: `encurso/generar_pdf_legajo/${nro_circuito}/`,
              responseType: 'blob'
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
          api.post('/encurso/guardar_adjuntofactura/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
                  fetchData();
                  showSuccessAlert.value = true;
                  setTimeout(() => { showSuccessAlert.value = false; }, 3000);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
                  showErrorAlert.value = true;
                  setTimeout(() => { showErrorAlert.value = false; }, 3000);
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
          const response = await api.put(`/encurso/guardar_pago_legajo/${nro_circuito}/`, {
            pago: pagoLegajoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Pago de Legajo actualizado correctamente:', pagoLegajoNuevo);
            mostrarModalPagoLegajo.value = false;  // Cerrar el modal
            fetchData();
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
          const response = await api.put(`/encurso/cambiar_plazo_pago/${nro_circuito}/`, {
            plazo_pago: plazoPagoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Plazo de Pago actualizado correctamente:', plazoPagoNuevo);
            mostrarModalPlazoPago.value = false;  // Cerrar el modal
            fetchData();
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

      const abrirArchivo = (adjunto) => {
        window.open(window.location.origin + '/media/' + adjunto, '_blank');
      };

      const abrirVistaPreliminar = (adjunto) => {
        urlPdf.value = window.location.origin + '/media/' + adjunto;
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
          const response = await api.put(`/encurso/cambiar_remito/${nro_circuito}/`, {
            nros_remitos: remitoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Numero de Remito actualizado correctamente:', remitoNuevo);
            mostrarModalRemito.value = false;
            fetchData();
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
          const response = await api.put(`/encurso/guardar_estado_recepcion/${nro_circuito}/`, {
            estado_recepcion: estadoMuestrasNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Estado de recepción de muestras actualizado correctamente:', estadoMuestrasNuevo);
            mostrarModalEstadoMuestras.value = false;  // Cerrar el modal
            fetchData();
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
          const response = await api.put(`/encurso/cambiar_plazo_muestras/${nro_circuito}/`, {
            plazo_muestras: plazoMuestrasNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Plazo de muestras actualizado correctamente:', plazoMuestrasNuevo);
            mostrarModalPlazoMuestras.value = false;  // Cerrar el modal
            fetchData();
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

      const abrirModalCrearOrdenServicio = async (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        try {
          const res = await api.get(`/encurso/preview_ordenservicio/${fila.nro_circuito}/`);
          const d = res.data;
          fechaOS.value = d.fecha_ordenServicio;
          areaOS.value = d.area_tematica;
          legajoOS.value = d.nro_legajo;
          rangosOS.value = d.rangos_laboratorios;
          plazoOS.value = d.plazo_estimado;
          solicitanteOS.value = d.nombre_solicitante;
          servicioOS.value = d.servicio_solicitado.map(s => ({ servicio: s.servicio, cant: s.cant }));
          muestrasOS.value = d.muestras;
          observacionesOS.value = '';
        } catch (e) {
          console.error('Error al cargar preview OS:', e);
        }
        mostrarModalCrearOrdenServicio.value = true;
      };

      const cerrarModalCrearOrdenServicio = () => {
        mostrarModalCrearOrdenServicio.value = false;
        osReadOnly.value = false;
      };
      
      const crearOrdenServicio = async () => {
          const nro_circuito = numeroCircuitoGlobal.value;
          console.log('numero circuito en crear orden circuito:', nro_circuito)
          try {
              const response = await api.post(`/encurso/crear_ordenservicio/${nro_circuito}/`);
              console.log('Orden de servicio creada exitosamente:', response.data);
              mostrarModalCrearOrdenServicio.value = false;
              fetchData();
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
      const abrirOrdenServicio = async (fila) => {
          const nro_circuito = fila.nro_circuito;
          try {
              const response = await api.get(`/encurso/obtener_orden_servicio/${nro_circuito}/`);
              const { nro_ordenServicio, fecha_ordenServicio, area_tematica, nro_legajo, rangos_laboratorios, plazo_estimado, nombre_solicitante, servicio_solicitado, muestras, observaciones } = response.data;
              nroOS.value = nro_ordenServicio;
              fechaOS.value = fecha_ordenServicio;
              areaOS.value = formatAreaTematica(area_tematica);
              legajoOS.value = nro_legajo;
              rangosOS.value = rangos_laboratorios;
              plazoOS.value = plazo_estimado;
              solicitanteOS.value = nombre_solicitante;
              servicioOS.value = servicio_solicitado;
              muestrasOS.value = muestras;
              observacionesOS.value = observaciones;
              osReadOnly.value = true;
              mostrarModalCrearOrdenServicio.value = true;
          } catch (error) {
              console.error('Error al obtener la orden de servicio:', error);
              showErrorAlert.value = true;
              setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
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
        api.defaults.withCredentials = true;
        try {
            // Realizar la petición para actualizar el plazo de orden de servicio en la base de datos
            const response = await api.put(`/encurso/cambiar_plazo_estimado/${nro_circuito}/`, {
                plazo_estimado: plazoEstimadoNuevo
            }, {
                withCredentials: true 
            });

            // Verificar si la actualización fue exitosa
            if (response.status === 200) {
                console.log('Plazo de orden de servicio actualizado correctamente:', plazoEstimadoNuevo);
                mostrarModalPlazoOrdenServicio.value = false;  // Cerrar el modal
                fetchData();
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

      // CICLOS DE INFORME

      const cicloSeleccionado = ref(null);
      const archivoPendiente = ref(null);
      const filaParaNuevoCiclo = ref(null);
      const esCambioTipo = ref(false);
      const cicloParaCambioTipo = ref(null);

      const mostrarClipParaNuevoParcial = (fila) => {
        return (isAreaJefe.value || isAreaStandard.value)
          && fila.ordenServicio_completo === true
          && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')
          && fila.ciclos.length > 0
          && fila.ciclos[fila.ciclos.length - 1].adjunto_informeArea
          && fila.ciclos[fila.ciclos.length - 1].tipo === 'parcial';
      };

      const puedeCrearNuevoCiclo = (fila) => {
        if (!fila.ciclos || fila.ciclos.length === 0) return true;
        if (fila.ciclos.some(c => c.tipo === 'final')) return false;
        const ultimo = fila.ciclos[fila.ciclos.length - 1];
        return ultimo.firma_direccion === true;
      };

      const crearCiclo = async (fila) => {
        try {
          await api.post(`/encurso/crear_ciclo/${fila.nro_circuito}/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al crear ciclo:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const popupInformeAreaId = ref(null);
      const hayParcialesPrevios = ref(false);

      const togglePopupInformeArea = (cicloId) => {
        popupInformeAreaId.value = popupInformeAreaId.value === cicloId ? null : cicloId;
      };

      const eliminarInformeAreaCiclo = async (ciclo) => {
        if (!confirm('¿Eliminar el informe de área? Esta acción no se puede deshacer.')) return;
        popupInformeAreaId.value = null;
        try {
          await api.delete(`/encurso/informe_area_ciclo/${ciclo.id}/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al eliminar informe área:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const seleccionarArchivoInformeAreaCiclo = (event, ciclo, fila) => {
        archivoPendiente.value = event.target.files[0];
        cicloSeleccionado.value = ciclo;
        filaParaNuevoCiclo.value = null;
        hayParcialesPrevios.value = fila
          ? fila.ciclos.some(c => c.tipo === 'parcial' && c.adjunto_informeArea)
          : false;
        mostrarModalTipoCiclo.value = true;
      };

      const seleccionarArchivoParaNuevoCiclo = (event, fila) => {
        const file = event.target.files[0];
        if (!file) return;
        archivoPendiente.value = file;
        cicloSeleccionado.value = null;
        filaParaNuevoCiclo.value = fila;
        hayParcialesPrevios.value = true;
        mostrarModalTipoCiclo.value = true;
      };

      const subirInformeAreaCiclo = async (tipo) => {
        mostrarModalTipoCiclo.value = false;
        const archivo = archivoPendiente.value;
        let ciclo = cicloSeleccionado.value;

        if (!ciclo && filaParaNuevoCiclo.value) {
          try {
            const resp = await api.post(`/encurso/crear_ciclo/${filaParaNuevoCiclo.value.nro_circuito}/`);
            ciclo = resp.data;
          } catch (error) {
            console.error('Error al crear ciclo:', error);
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 3000);
            archivoPendiente.value = null;
            filaParaNuevoCiclo.value = null;
            return;
          }
        }

        if (!archivo || !ciclo) return;
        const formData = new FormData();
        formData.append('archivo', archivo);
        formData.append('tipo', tipo);
        try {
          await api.post(`/encurso/subir_informe_area_ciclo/${ciclo.id}/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al subir informe área:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        } finally {
          archivoPendiente.value = null;
          cicloSeleccionado.value = null;
          filaParaNuevoCiclo.value = null;
        }
      };

      const cambiarTipoCiclo = (ciclo, fila) => {
        popupInformeAreaId.value = null;
        cicloParaCambioTipo.value = ciclo;
        esCambioTipo.value = true;
        hayParcialesPrevios.value = fila
          ? fila.ciclos.some(c => c.id !== ciclo.id && c.tipo === 'parcial' && c.adjunto_informeArea)
          : false;
        mostrarModalTipoCiclo.value = true;
      };

      const confirmarCambioTipo = async (tipo) => {
        mostrarModalTipoCiclo.value = false;
        esCambioTipo.value = false;
        const ciclo = cicloParaCambioTipo.value;
        cicloParaCambioTipo.value = null;
        if (!ciclo) return;
        try {
          await api.patch(`/encurso/cambiar_tipo_ciclo/${ciclo.id}/`, { tipo });
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al cambiar tipo:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const cerrarModalTipoCiclo = () => {
        mostrarModalTipoCiclo.value = false;
        archivoPendiente.value = null;
        cicloSeleccionado.value = null;
        filaParaNuevoCiclo.value = null;
        esCambioTipo.value = false;
        cicloParaCambioTipo.value = null;
      };

      const subirRegistroEnsayoCiclo = async (event, ciclo) => {
        const archivo = event.target.files[0];
        const formData = new FormData();
        formData.append('archivo', archivo);
        try {
          await api.post(`/encurso/subir_registro_ensayo_ciclo/${ciclo.id}/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al subir registro ensayo:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const eliminarRegistroEnsayoCiclo = async (id) => {
        if (!confirm('¿Eliminar el registro de ensayo?')) return;
        try {
          await api.delete(`/encurso/registro_ensayo_ciclo/${id}/`);
          fetchData();
        } catch (e) { console.error('Error al eliminar registro ensayo:', e); }
      };

      // INTER AREA

      // Inter Area - Crear Solicitud Inter Area

      const obtenerServicios = async (nro_circuito) => {
        try {
          const response = await api.get(`/encurso/obtener_servicios/${nro_circuito}/`);
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

          // Enviar datos al backend usando api
          api.post('/encurso/crear_solicitud_interarea/', nuevaSolicitudInterarea.value)
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
          api.get(`/encurso/obtener_solicitud_interarea/${nro_circuito}/`)
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
          api.post('/encurso/guardar_adjuntoinformeinterarea/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
                  fetchData();
                  showSuccessAlert.value = true;
                  setTimeout(() => { showSuccessAlert.value = false; }, 3000);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
                  showErrorAlert.value = true;
                  setTimeout(() => { showErrorAlert.value = false; }, 3000);
              });
        };
      
      // Administracion - Informe Servicio por Ciclo
      const subirInformeServicioCiclo = async (event, ciclo) => {
        const archivo = event.target.files[0];
        const formData = new FormData();
        formData.append('archivo', archivo);
        try {
          await api.post(`/encurso/subir_informe_servicio_ciclo/${ciclo.id}/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          console.error('Error al subir informe servicio:', error);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const abrirModalCorreccionesCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        correcciones.value = ciclo.correcciones || '';
        mostrarModalCorreccionesInformeServicio.value = true;
      };

      const cerrarModalCorreccionesInformeServicio = () => {
        mostrarModalCorreccionesInformeServicio.value = false;
      };

      const corregirCiclo = async () => {
        const ciclo = cicloSeleccionado.value;
        if (!ciclo) return;
        try {
          await api.put(`/encurso/corregir_ciclo/${ciclo.id}/`);
          mostrarModalCorreccionesInformeServicio.value = false;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalCorreccionesInformeServicio.value = false;
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

      // Servicios Tecnológicos - Revisión por Ciclo
      const abrirModalRevisionCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        mostrarModalRevision.value = true;
      };

      const cerrarModalRevision = () => {
        mostrarModalRevision.value = false;
      };

      const confirmarRevisionCiclo = async () => {
        const ciclo = cicloSeleccionado.value;
        if (!ciclo) return;
        try {
          await api.put(`/encurso/confirmar_revision_ciclo/${ciclo.id}/`);
          mostrarModalRevision.value = false;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalRevision.value = false;
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };


      const toggleOpciones = (index) => {
        openDSPopup.value = null;
        openST02Popup.value = null;
        openST02FileList.value = null;
        const newVal = filaSeleccionada.value === index ? null : index;
        filaSeleccionada.value = newVal;
        if (newVal !== null) document.dispatchEvent(new CustomEvent('speed-dial-open'));
      };

      // Responsable del Área - Firma por Ciclo

      const abrirModalAdvertirCorreccionesCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        correccionesNuevas.value = '';
        mostrarModalAdvertirCorrecciones.value = true;
      };

      const cerrarModalAdvertirCorrecciones = () => {
        mostrarModalAdvertirCorrecciones.value = false;
      };

      const advertirCorreccionesCiclo = async (correccionesNuevas) => {
        const ciclo = cicloSeleccionado.value;
        if (!ciclo) return;
        try {
          await api.put(`/encurso/advertir_correcciones_ciclo/${ciclo.id}/`, { correcciones: correccionesNuevas });
          mostrarModalAdvertirCorrecciones.value = false;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalAdvertirCorrecciones.value = false;
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

      const abrirModalFirmaResponsableAreaCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        mostrarModalFirmaResponsableArea.value = true;
      };

      const cerrarModalFirmaResponsableArea = () => {
        mostrarModalFirmaResponsableArea.value = false;
      };

      const confirmarFirmaResponsableAreaCiclo = async () => {
        const ciclo = cicloSeleccionado.value;
        if (!ciclo) return;
        try {
          await api.put(`/encurso/confirmar_firma_responsable_area_ciclo/${ciclo.id}/`);
          mostrarModalFirmaResponsableArea.value = false;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalFirmaResponsableArea.value = false;
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

      // Dirección - Firma por Ciclo
      const abrirModalFirmaDireccionCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        mostrarModalFirmaDireccion.value = true;
      };

      const cerrarModalFirmaDireccion = () => {
        mostrarModalFirmaDireccion.value = false;
      };

      const confirmarFirmaDireccionCiclo = async () => {
        const ciclo = cicloSeleccionado.value;
        if (!ciclo) return;
        try {
          await api.put(`/encurso/confirmar_firma_direccion_ciclo/${ciclo.id}/`);
          mostrarModalFirmaDireccion.value = false;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalFirmaDireccion.value = false;
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
              const response = await api.put(
                  `/encurso/archivar_circuito/${nroCircuito}/`
              );
              console.log('Archivado correctamente:', response.data);
              mostrarModalArchivar.value = false;
              fetchData();

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

        const eliminarAdjuntoSolicitud = async (id) => {
          if (!confirm('¿Eliminar el adjunto ST-02?')) return;
          try {
            await api.delete(`/encurso/adjunto_solicitud/${id}/`);
            fetchData();
          } catch (e) { console.error('Error al eliminar adjunto solicitud:', e); }
        };

        const eliminarAdjuntoFactura = async (id) => {
          if (!confirm('¿Eliminar la factura?')) return;
          try {
            await api.delete(`/encurso/adjunto_factura/${id}/`);
            fetchData();
          } catch (e) { console.error('Error al eliminar factura:', e); }
        };

        const eliminarAdjuntoInformeInterarea = async (id) => {
          if (!confirm('¿Eliminar el informe interárea?')) return;
          try {
            await api.delete(`/encurso/informe_interarea/${id}/`);
            fetchData();
          } catch (e) { console.error('Error al eliminar informe interárea:', e); }
        };


        const imprimirDataServicio = () => { window.print(); };
        const imprimirLegajo = () => { window.print(); };

        const fechaLegajoFormateada = computed(() => {
          if (!fechaLegajo.value) return '';
          const [y, m, d] = fechaLegajo.value.split('-');
          return `${d}/${m}/${y}`;
        });

      return {
        // General
        filas,
        sortKey, sortDir, sortedFilas, setSort,
        filterArea, filterDesde, filterHasta, filterTipoFecha, uniqueAreas, clearFilters,
        getRowClass,
        diasRestantesOS,
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
        eliminarAdjuntoSolicitud,
        // Popup Data Servicio
        openDSPopup,
        toggleDSPopup,
        closeDSPopup,
        // Popup ST-02 Solicitud
        openST02Popup,
        openST02FileList,
        toggleST02Popup,
        closeST02Popup,
        toggleST02FileList,
        shortFileName,
        viewAttachment,
        // Editar Data Servicio
        mostrarModalEditarDS,
        editarDS,
        abrirEditarDataServicio,
        cerrarEditarDataServicio,
        agregarPresupuestoAdicional,
        quitarPresupuestoAdicional,
        guardarEdicionDataServicio,
        mostrarModalAprobarLabs,
        aprobarLabs,
        abrirAprobarLabs,
        cerrarAprobarLabs,
        confirmarAprobarLabs,
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
        eliminarAdjuntoFactura,
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
        osReadOnly,
        abrirModalCrearOrdenServicio,
        cerrarModalCrearOrdenServicio,
        abrirOrdenServicio,
        mostrarModalOrdenServicio,
        cerrarModalOrdenServicio,
        cambiarPlazoOrdenServicio,
        abrirModalPlazoOrdenServicio,
        cerrarModalPlazoOrdenServicio,
        mostrarModalPlazoOrdenServicio,
        // Ciclos de Informe
        mostrarModalTipoCiclo,
        mostrarClipParaNuevoParcial,
        puedeCrearNuevoCiclo,
        crearCiclo,
        popupInformeAreaId,
        hayParcialesPrevios,
        togglePopupInformeArea,
        eliminarInformeAreaCiclo,
        seleccionarArchivoInformeAreaCiclo,
        seleccionarArchivoParaNuevoCiclo,
        subirInformeAreaCiclo,
        cambiarTipoCiclo,
        confirmarCambioTipo,
        esCambioTipo,
        cerrarModalTipoCiclo,
        subirRegistroEnsayoCiclo,
        eliminarRegistroEnsayoCiclo,
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
        eliminarAdjuntoInformeInterarea,
        // Administracion - Informe Servicio
        subirInformeServicioCiclo,
        abrirModalCorreccionesCiclo,
        cerrarModalCorreccionesInformeServicio,
        mostrarModalCorreccionesInformeServicio,
        correcciones,
        corregirCiclo,
        // Servicios Tecnologicos - Revision
        abrirModalRevisionCiclo,
        cerrarModalRevision,
        mostrarModalRevision,
        confirmarRevisionCiclo,
        mostrarOpciones,
        filaSeleccionada,
        toggleOpciones,
        // Responsable del Area - Firma
        abrirModalAdvertirCorreccionesCiclo,
        cerrarModalAdvertirCorrecciones,
        mostrarModalAdvertirCorrecciones,
        advertirCorreccionesCiclo,
        correccionesNuevas,
        abrirModalFirmaResponsableAreaCiclo,
        cerrarModalFirmaResponsableArea,
        mostrarModalFirmaResponsableArea,
        confirmarFirmaResponsableAreaCiclo,
        // Direccion - Firma
        abrirModalFirmaDireccionCiclo,
        cerrarModalFirmaDireccion,
        mostrarModalFirmaDireccion,
        confirmarFirmaDireccionCiclo,
        // Archivar
        abrirModalArchivar,
        cerrarModalArchivar,
        imprimirDataServicio,
        imprimirLegajo,
        fechaLegajoFormateada,
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

  .table tbody tr:nth-child(even) {
    background-color: #f0f6fa;
  }

  .table tbody tr:hover {
    background-color: #daeaf3;
  }

  /* Alertas de plazo */
  .table tbody tr.row-alerta,
  .table tbody tr.row-alerta:nth-child(even) {
    background-color: #fff8e1 !important;
  }
  .table tbody tr.row-alerta:hover { background-color: #ffecb3 !important; }

  .table tbody tr.row-urgente,
  .table tbody tr.row-urgente:nth-child(even) {
    background-color: #fde8ea !important;
  }
  .table tbody tr.row-urgente:hover { background-color: #f5c2c7 !important; }

  /* Fila de ciclo - espacio mínimo entre ciclos */
  .ciclo-row {
    min-height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 1px 0;
  }

  .ciclo-row--final {
    justify-content: center;
  }

  .attachment-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
  }

  .attach-popup {
    position: absolute;
    bottom: calc(100% + 6px);
    left: 50%;
    transform: translateX(-50%);
    z-index: 1060;
    background: white;
    border: 1px solid #c0c7d0;
    border-radius: 6px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.16);
    min-width: 110px;
    padding: 4px 0;
  }

  .attach-popup-item {
    display: flex;
    align-items: center;
    gap: 6px;
    width: 100%;
    padding: 5px 12px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.82rem;
    white-space: nowrap;
    text-align: left;
  }

  .attach-popup-item:hover {
    background-color: #f0f4f8;
  }

  /* Ícono de acción (+ crear) */
  .action-icon {
    cursor: pointer;
    font-size: 17px;
    color: #026290;
    transition: color 0.15s, transform 0.15s;
  }
  .action-icon:hover {
    color: #014f73;
    transform: scale(1.18);
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
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    z-index: 50;
  }

  /* Override para el speed dial de Data Servicio: origen centrado en el botón */
  .ds-opciones-flotantes {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 200;
  }

  .opcion {
    position: absolute;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #026290;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    transform: rotate(var(--rotation)) translate(60px) rotate(calc(-1 * var(--rotation)));
    transition: transform 0.25s ease, background-color 0.15s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  }

  .opcion i {
    font-size: 16px;
    cursor: pointer;
  }

  .opcion:hover {
    transform: rotate(var(--rotation)) translate(70px) rotate(calc(-1 * var(--rotation)));
  }

  /* Opciones del DS: blanco con borde teal para contrastar con header */
  .ds-opciones-flotantes .opcion {
    background-color: white;
    border: 2px solid #026290;
    color: #026290;
  }

  .ds-opciones-flotantes .opcion:hover {
    background-color: #026290;
    color: white;
  }


</style>

<style>
/* ── Estilos pantalla para el nuevo layout del modal Data Servicio ── */
.ds-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 10px;
  border-bottom: 2px solid #026290;
}
.ds-doc-title { font-size: 1.1rem; font-weight: 700; color: #026290; }
.ds-doc-sub   { font-size: 0.85rem; color: #555; margin-top: 2px; }
.ds-fecha     { display: flex; flex-direction: column; align-items: flex-end; }
.ds-fecha-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #888; }
.ds-fecha-val   { font-weight: 600; font-size: 0.95rem; }

.ds-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2px;
  margin-top: 10px;
}
.ds-field {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  background: #f8f9fa;
}
.ds-field:nth-child(odd)  { background: #f8f9fa; }
.ds-field:nth-child(even) { background: #fff; border-left: 1px solid #e9ecef; }
.ds-field--full { grid-column: 1 / -1; background: #fff !important; border-top: 1px solid #e9ecef; border-left: none !important; }
.ds-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em; color: #026290; margin-bottom: 2px; }
.ds-val   { font-weight: 600; font-size: 0.92rem; }
.ds-arancel { color: #198754; font-size: 1rem; }

/* ── Legajo carátula ── */
.lg-body {
  display: flex;
  flex-direction: column;
  padding: 28px 36px 36px;
}
.lg-fecha-row {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-bottom: 52px;
}
.lg-fecha-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #026290;
}
.lg-fecha-val {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
}
.lg-title-area {
  margin-bottom: 52px;
}
.lg-number {
  font-size: 2.6rem;
  font-weight: 800;
  color: #026290;
  line-height: 1.1;
  letter-spacing: -0.01em;
}
.lg-divider {
  width: 64px;
  height: 4px;
  background: #026290;
  margin-top: 12px;
  border-radius: 2px;
}
.lg-fields {
  display: flex;
  gap: 16px;
}
.lg-field {
  flex: 1;
  background: #f0f5fb;
  border-left: 4px solid #026290;
  padding: 16px 20px;
  border-radius: 0 6px 6px 0;
}
.lg-label {
  display: block;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #026290;
  margin-bottom: 6px;
}
.lg-value {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1a1a1a;
}

/* ── Impresión ── */
@page {
  margin: 0;
  size: A4;
}

@media print {
  body * { visibility: hidden; }

  /* Solo el modal abierto (clase .show) es visible al imprimir */
  #modalAbrirDataServicio.show,
  #modalAbrirDataServicio.show *,
  #modalAbrirLegajo.show,
  #modalAbrirLegajo.show * { visibility: visible; }

  #modalAbrirDataServicio.show,
  #modalAbrirLegajo.show {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    background: white;
    z-index: 9999;
    display: block !important;
  }

  #modalAbrirDataServicio .no-print,
  #modalAbrirLegajo .no-print { display: none !important; visibility: hidden; }

  #modalAbrirDataServicio.show .modal-dialog-a4,
  #modalAbrirLegajo.show .modal-dialog-a4 {
    box-shadow: none;
    margin: 0;
    max-width: 100%;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  #modalAbrirDataServicio.show .modal-content,
  #modalAbrirLegajo.show .modal-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  #modalAbrirDataServicio.show .modal-body,
  #modalAbrirLegajo.show .modal-body {
    flex: 1;
    padding: 20px 30px 120px 30px;
    overflow: visible;
  }

  /* Footer pegado al fondo de la hoja */
  #modalAbrirDataServicio.show .modal-footer-a4,
  #modalAbrirLegajo.show .modal-footer-a4 {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
  }

  /* Forzar imagenes de fondo */
  #modalAbrirDataServicio.show .modal-logo,
  #modalAbrirDataServicio.show .footer-image,
  #modalAbrirLegajo.show .modal-logo,
  #modalAbrirLegajo.show .footer-image {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
    visibility: visible !important;
  }

  /* Grid Data Servicio en 2 columnas al imprimir */
  .ds-grid { gap: 1px; border: 1px solid #dee2e6; }
  .ds-field { border: none; border-bottom: 1px solid #dee2e6; }
  .ds-field--full { border-top: 1px solid #dee2e6; }
  .ds-field:nth-child(odd)  { print-color-adjust: exact; -webkit-print-color-adjust: exact; }

  /* Legajo: centrar verticalmente en la hoja */
  #modalAbrirLegajo.show .modal-body {
    justify-content: center;
    padding: 20px 36px 140px;
  }
  /* Forzar colores en los bloques de campos */
  .lg-field { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
  .lg-number { color: #026290 !important; }
  .lg-divider { background: #026290 !important; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
  .lg-label { color: #026290 !important; }
}

.ds-icon-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1.5px solid #28a745;
  background: white;
  color: #28a745;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  padding: 0;
  transition: background 0.15s, color 0.15s;
}
.ds-icon-btn:hover {
  background: #28a745;
  color: white;
}
.ds-icon-btn--warning {
  border-color: #e6a817;
  color: #e6a817;
}
.ds-icon-btn--warning:hover {
  background: #e6a817;
  color: white;
}
.ds-icon-btn--blue {
  border-color: #026290;
  color: #026290;
  position: relative;
}
.ds-icon-btn--blue:hover {
  background: #026290;
  color: white;
}
.att-badge-st02 {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #026290;
  color: white;
  border-radius: 50%;
  width: 15px;
  height: 15px;
  font-size: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}
.st02-file-popup {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.18);
  min-width: 210px;
  z-index: 300;
  padding: 4px 0;
}
.st02-file-row {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  gap: 4px;
  border-bottom: 1px solid #f0f0f0;
}
.st02-file-row:last-of-type { border-bottom: none; }
.st02-file-name {
  flex: 1;
  font-size: 11px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
}
.st02-btn {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  padding: 0;
  background: transparent;
  color: #026290;
  flex-shrink: 0;
}
.st02-btn:hover { background: #e8f4f8; }
.st02-btn-del { color: #dc3545; }
.st02-btn-del:hover { background: #fde8ea; }
.st02-add-row {
  display: flex;
  align-items: center;
  padding: 6px 8px 4px;
  border-top: 1px solid #e8e8e8;
}
.st02-add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #026290;
  cursor: pointer;
  font-weight: 500;
}
.st02-add-btn:hover { text-decoration: underline; }
</style>
  