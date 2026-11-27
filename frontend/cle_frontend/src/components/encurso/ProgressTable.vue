<template>
     <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! Se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar. Por favor, inténtalo de nuevo.
    </div>

    <div class="pt-inner">
      <div class="filter-bar">
        <select v-if="isAdminOrTecnologicoOrDireccion" v-model="filterArea" class="filter-ctrl">
          <option value="">Todas las áreas</option>
          <option v-for="area in uniqueAreas" :key="area" :value="area">{{ area }}</option>
        </select>
        <select v-model="filterTipoFecha" class="filter-ctrl">
          <option value="solicitud">Solicitud de Servicio</option>
          <option value="orden">Orden de Servicio</option>
        </select>
        <div class="filter-date-range">
          <span class="fdr-label">Desde</span>
          <input type="date" v-model="filterDesde" class="fdr-input">
          <span class="fdr-sep"></span>
          <span class="fdr-label">Hasta</span>
          <input type="date" v-model="filterHasta" class="fdr-input">
        </div>
        <button v-if="filterArea || filterDesde || filterHasta" @click="clearFilters" class="filter-clear">✕ Limpiar</button>
        <div class="d-flex gap-1 ms-auto">
          <button @click="manualRefresh" class="btn btn-sm btn-outline-secondary" title="Actualizar datos">
            <i class="bi bi-arrow-clockwise" :class="{ 'spin-icon': refreshCargando }"></i>
          </button>
          <button @click="toggleSilencio"
                  class="btn btn-sm"
                  :class="silenciado ? 'btn-outline-danger' : 'btn-outline-secondary'"
                  :title="silenciado ? 'Alertas de sonido silenciadas — click para activar' : 'Silenciar alertas de sonido'">
            <i :class="silenciado ? 'bi bi-bell-slash' : 'bi bi-bell'"></i>
          </button>
        </div>
      </div>

      <!-- Banner de actualizaciones disponibles -->
      <div v-if="hayActualizaciones"
           class="alert alert-info d-flex align-items-center justify-content-between mb-2 py-2"
           style="border-left: 4px solid #0dcaf0;">
        <div class="small">
          <i class="bi bi-arrow-clockwise me-2"></i>
          Hay cambios disponibles de otros usuarios.
        </div>
        <button class="btn btn-sm btn-primary ms-3 text-nowrap" @click="aplicarActualizaciones">
          Actualizar ahora
        </button>
      </div>

      <!-- Alertas plazo vencido -->
      <div v-for="alerta in alertasPlazos" :key="alerta.key"
           class="alert alert-danger d-flex align-items-center justify-content-between mb-2 py-2"
           style="border-left: 4px solid #7b0000;">
        <div class="small">
          <i class="bi bi-clock-history me-2"></i>
          <strong>Plazo vencido — Circuito #{{ alerta.nro_circuito }}:</strong>
          {{ alerta.mensaje }}
        </div>
        <div class="d-flex gap-2 ms-3">
          <button class="btn btn-sm btn-outline-light text-nowrap" @click="extenderPlazoPorAlerta(alerta)">
            <i class="bi bi-calendar-plus me-1"></i>Extender plazo
          </button>
          <button class="btn btn-sm btn-light text-nowrap" @click="abrirModalArchivarConMotivo(alerta)">
            <i class="bi bi-archive me-1"></i>Archivar
          </button>
        </div>
      </div>

      <div class="table-scroll-wrapper">
      <table class="table table-hover mb-0">
        <thead class="text-center sticky-thead">
          <tr>
            <th v-if="isTecnologicoOrDireccion" colspan="6" class="add-border-right align-middle text-center">Solicitud de Servicio</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" colspan="6" class="add-border-right align-middle text-center">Legajo</th>
            <th v-if="isTecnologicoOrDireccion" colspan="3" class="add-border-right align-middle text-center">Recepcion</th>
            <th v-if="isTecnologicoOrDireccion" colspan="2" class="add-border-right align-middle text-center">Orden de Servicio</th>
            <th v-if="isAreaJefe || isAreaStandard" colspan="1" class="align-middle text-center">Legajo</th>
            <th v-if="isAreaJefe || isAreaStandard" colspan="1" class="add-border-right align-middle text-center">Orden de Servicio</th>
            <th v-if="isTecnologicoOrDireccionOrArea" colspan="5" class="add-border-right align-middle text-center">Inter Area</th>
            <th colspan="6" class="add-border-right align-middle text-center">Informe de Area</th>
            <!-- <th colspan="1" class="add-border-right align-middle text-center">Informe Area</th> -->
            <th colspan="1" class="add-border-right align-middle text-center">Administracion</th>
            <th colspan="1" class="add-border-right align-middle text-center">Servicios Tecnologicos</th>
            <th colspan="1" class="add-border-right align-middle text-center">Administracion</th>
            <th colspan="1" class="add-border-right align-middle text-center">Responsable Area</th>
            <th colspan="1" class="add-border-right align-middle text-center">Direccion</th>
            <th  v-if="isAdminOrTecnologicoOrDireccion" colspan="1" class="align-middle text-center">Archivo</th>
            <th colspan="1" class="align-middle text-center"></th>
          </tr>
          <tr>
            <!-- Subcolumnas de Solicitud de Servicio -->
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('nro_dataServicio')">N° <span class="sort-icon">{{ sortKey === 'nro_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('fecha_dataServicio')">Fecha <span class="sort-icon">{{ sortKey === 'fecha_dataServicio' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">Area Tematica</th>
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">ST-01 Presupuesto</th>
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">Data Servicio</th>
            <th v-if="isTecnologicoOrDireccion" class="add-border-right align-middle text-center">ST-02 Solicitud</th>
            <!-- Subcolumnas de Legajo -->
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center sortable" @click="setSort('nro_legajo')">N° <span class="sort-icon">{{ sortKey === 'nro_legajo' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Fecha</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Legajo</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Factura</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="align-middle text-center">Pago</th>
            <th v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center sortable" @click="setSort('plazo_pago')">Plazo <span class="sort-icon">{{ sortKey === 'plazo_pago' ? (sortDir === 'asc' ? '↑' : '↓') : '⇅' }}</span></th>
            <!-- Subcolumnas de Recepcion -->
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">ST-03 Recepcion</th>
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">Muestras</th>
            <th v-if="isTecnologicoOrDireccion" class="add-border-right align-middle text-center">Plazo</th>
            <!-- Subcolumnas de Orden de Servicio -->
            <th v-if="isTecnologicoOrDireccion" class="align-middle text-center">Fecha</th>
            <th v-if="isTecnologicoOrDireccion" class="add-border-right align-middle text-center">ST-05 Orden</th>
            <!-- Subcolumnas Legajo + OS para área -->
            <th v-if="isAreaJefe || isAreaStandard" class="align-middle text-center">N°</th>
            <th v-if="isAreaJefe || isAreaStandard" class="add-border-right align-middle text-center">OS</th>
            <!-- Subcolumnas de Inter Area -->
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Fecha / Área</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Informe IA</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Registros IA</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="align-middle text-center">Tipo IA</th>
            <th v-if="isTecnologicoOrDireccionOrArea" class="add-border-right align-middle text-center">Plazo IA</th>
            <!-- Subcolumnas de Informe de Area -->
            <th class="align-middle text-center">Fecha</th>
            <th class="align-middle text-center">Solicitante</th>
            <th class="align-middle text-center">Informe Area</th>
            <th class="align-middle text-center">Registros de Ensayo</th>
            <th class="align-middle text-center">Tipo</th>
            <th class="add-border-right align-middle text-center">Plazo</th>
            <!-- Subcolumnas de Administracion -->
            <th class="add-border-right align-middle text-center">Formato</th>
            <!-- Subcolumnas de Servicios Tecnologicos -->
            <th class="add-border-right align-middle text-center">Revision</th>
            <!-- Subcolumnas de Administracion PDF -->
            <th class="add-border-right align-middle text-center">PDF</th>
            <!-- Subcolumnas de Responsable Area -->
            <th class="add-border-right align-middle text-center">Firma</th>
            <!-- Subcolumnas de Direccion -->
            <th class="add-border-right align-middle text-center">Firma</th>
            <!-- Subcolumnas de Archivo -->
            <th  v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right align-middle text-center">Archivar</th>
            <th class="align-middle text-center"></th>
          </tr>
        </thead>
        <tbody >
          <tr v-for="(fila, index) in sortedFilas" :key="index" :class="getRowClass(fila)">

            <!-- Columna Solicitud de Servicio -->

            <td v-if="isTecnologicoOrDireccion">{{ fila.nro_dataServicio }}</td>
            <td v-if="isTecnologicoOrDireccion" class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <td v-if="isTecnologicoOrDireccion" style="white-space: nowrap;">{{ fila.area_tematica }}</td>
            <td v-if="isTecnologicoOrDireccion">
              {{ fila.nro_presupuesto }}
              <span v-if="fila.presupuestos_adicionales && fila.presupuestos_adicionales.length > 0" style="color:#888; font-size:11px;">
                , {{ fila.presupuestos_adicionales.map(p => p.nro_presupuesto).join(', ') }}
              </span>
            </td>
            <td v-if="isTecnologicoOrDireccion">
              <div style="position: relative; display: inline-flex; justify-content: center; align-items: center;" @click.stop>
                <button class="ds-icon-btn" @click="toggleDSPopup(fila.nro_dataServicio)" title="Data Servicio">
                  <i class="bi bi-file-earmark-check-fill"></i>
                </button>
                <div v-if="openDSPopup === fila.nro_dataServicio" class="opciones-flotantes ds-opciones-flotantes">
                  <div class="opcion" :style="isServiciosTecnologicos ? '--rotation: -120deg' : '--rotation: -90deg'" @click="abrirDataServicio(fila.nro_dataServicio, fila); closeDSPopup()">
                    <i class="bi bi-eye"></i>
                  </div>
                  <div v-if="isServiciosTecnologicos" class="opcion" style="--rotation: -60deg" @click="abrirEditarDataServicio(fila); closeDSPopup()">
                    <i class="bi bi-pencil"></i>
                  </div>
                </div>
              </div>
            </td>
            <td v-if="isTecnologicoOrDireccion" class="add-border-right">
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
                  :class="(fila.labs_adicionales_pendientes > 0 || fila.monto_adicional_pendiente) ? 'ds-icon-btn ds-icon-btn--warning' : 'ds-icon-btn'"
                  :title="fila.labs_adicionales_pendientes > 0 ? fila.labs_adicionales_pendientes + ' labs adicionales pendientes de aprobación' : fila.monto_adicional_pendiente ? 'Nuevo presupuesto/monto pendiente de revisión' : 'Ver Legajo'"
                  @click="(fila.labs_adicionales_pendientes > 0 || fila.monto_adicional_pendiente) && isAdministracion ? abrirAprobarLabs(fila) : abrirLegajo(fila)"
                >
                  <i class="bi bi-file-earmark-check-fill"></i>
                </button>
              </template>
              <template v-else>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <template v-if="fila.nro_legajo">
                <button class="st-sd-trigger"
                        :style="pendienteFactura(fila) === null ? '' : pendienteFactura(fila) > 0 ? 'border-color:#ffc107; color:#b8860b;' : 'border-color:#198754; color:#198754;'"
                        @click.stop="abrirDatosFacturacion(fila)"
                        title="Ver datos de facturación">
                  <i class="bi bi-receipt" style="font-size:13px;"></i>
                  <span v-if="pendienteFactura(fila) !== null"
                        class="st-sd-badge"
                        :style="pendienteFactura(fila) > 0 ? 'background:#ffc107;' : 'background:#198754;'"></span>
                </button>
              </template>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion">
                <div v-if="fila.pago !== undefined && fila.pago !== null">
                  <div v-if="isAdministracion">
                      <span @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;"
                            :class="[labelPagoBadgeClass(fila.pago), fila.adjuntos_factura && fila.adjuntos_factura.length > 0 && !pagoEsCompleto(fila.pago) ? 'pago-pulse' : '']">
                        {{ labelPago(fila.pago) }}
                      </span>
                  </div>
                  <div v-else>
                      <span :class="[labelPagoBadgeClass(fila.pago), fila.adjuntos_factura && fila.adjuntos_factura.length > 0 && !pagoEsCompleto(fila.pago) ? 'pago-pulse' : '']">{{ labelPago(fila.pago) }}</span>
                  </div>
                </div>
            </td>
            <td v-if="isAdminOrTecnologicoOrDireccion" class="add-border-right">
                <template v-if="pagoEsCompleto(fila.pago)">-</template>
                <template v-else>
                  <div v-if="isAdministracion">
                    <span @click="abrirModalPlazoPago(fila)" style="cursor: pointer;">
                      <span class="plazo-badge" :class="plazoCriticidad(fila.plazo_pago)">{{ fila.plazo_pago }}</span>
                    </span>
                  </div>
                  <div v-else>
                    <span class="plazo-badge" :class="plazoCriticidad(fila.plazo_pago)">{{ fila.plazo_pago }}</span>
                  </div>
                </template>
            </td>

            <!-- Columna Recepcion -->

            <td v-if="isTecnologicoOrDireccion">
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
            <td v-if="isTecnologicoOrDireccion">
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
            <td v-if="isTecnologicoOrDireccion" class="add-border-right">
              <template v-if="fila.estado_recepcion === 'total'">-</template>
              <template v-else>
                <div v-if="isServiciosTecnologicos">
                  <span v-if="fila.legajo_completo" @click="abrirModalPlazoMuestras(fila)" style="cursor: pointer;">
                    <span class="plazo-badge" :class="plazoCriticidad(fila.plazo_muestras)">{{ fila.plazo_muestras }}</span>
                  </span>
                </div>
                <div v-else>
                  <span v-if="fila.legajo_completo">
                    <span class="plazo-badge" :class="plazoCriticidad(fila.plazo_muestras)">{{ fila.plazo_muestras }}</span>
                  </span>
                </div>
              </template>
            </td>

            <!-- Columna Orden de Servicio -->

            <td v-if="isTecnologicoOrDireccion">
              <template v-if="(fila.nro_ordenServicio  !== '' ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <span class="no-wrap-column">
                  {{ fila.fecha_ordenServicio }}
                </span>
              </template>
              <template v-else>

              </template>
            </td>
            <td v-if="isTecnologicoOrDireccion" class="add-border-right">
              <template v-if="(fila.ordenServicio_completo === '' || fila.ordenServicio_completo === false) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                  <div v-if="isServiciosTecnologicos">
                      <i class="bi bi-plus-circle action-icon" @click="abrirModalCrearOrdenServicio(fila)"></i>
                  </div>
                  <div v-else>
                      <i class="bi bi-stopwatch"></i>
                  </div>
              </template>
              <template v-if="(fila.ordenServicio_completo  === true ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <div style="position:relative; display:inline-block;">
                  <i class="bi bi-clipboard2" style="cursor: pointer;"
                     :style="fila.os_modificada ? 'color:#b8860b;' : ''"
                     :title="fila.os_modificada ? 'Orden de Servicio modificada — hay cambios pendientes de revisar' : 'Ver Orden de Servicio'"
                     @click="abrirOrdenServicio(fila)"></i>
                  <span v-if="fila.os_modificada"
                        style="position:absolute; top:-4px; right:-4px; width:8px; height:8px; border-radius:50%; background:#ffc107; display:block;"></span>
                </div>
              </template>
            </td>

            <!-- N° Legajo para área e inter-área -->
            <td v-if="isAreaJefe || isAreaStandard" style="text-align:center; vertical-align:middle; font-weight:bold; white-space:nowrap;">
              {{ fila.nro_legajo || '—' }}
            </td>
            <!-- Orden de Servicio para área (solo si es el área principal, no inter-área) -->
            <td v-if="isAreaJefe || isAreaStandard" class="add-border-right" style="text-align:center; vertical-align:middle;">
              <template v-if="!esSoloInterAreaEnFila(fila) && fila.ordenServicio_completo === true && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <div style="position:relative; display:inline-block;">
                  <i class="bi bi-clipboard2" style="cursor:pointer;"
                     :style="fila.os_modificada ? 'color:#b8860b;' : ''"
                     :title="fila.os_modificada ? 'Orden de Servicio modificada — hay cambios pendientes de revisar' : 'Ver Orden de Servicio'"
                     @click="abrirOrdenServicio(fila)"></i>
                  <span v-if="fila.os_modificada"
                        style="position:absolute; top:-4px; right:-4px; width:8px; height:8px; border-radius:50%; background:#ffc107; display:block;"></span>
                </div>
              </template>
            </td>

            <!-- Columna Inter Area — Fecha / Área -->
            <td v-if="isTecnologicoOrDireccionOrArea" style="text-align:center;">
              <div v-for="ia in fila.solicitudes_interarea" :key="ia.id"
                class="ciclo-row ia-row"
                :class="{ 'ia-row-pendiente': iaDebeParpadear(ia) }">
                <span class="no-wrap-column" style="font-size:0.78rem">{{ ia.fecha }}</span>
                <span class="no-wrap-column ia-area-label" style="font-size:0.78rem">{{ ia.inter_areaTematica }}</span>
                <i v-if="!isAdministracion" class="bi bi-clipboard2 action-icon" style="font-size:0.9rem" @click="abrirSolicitudInterArea(ia)"></i>
              </div>
              <div v-if="mostrarBotonAgregarIA(fila)" class="ciclo-row">
                <i class="bi bi-plus-circle action-icon" @click="abrirModalCrearSolicitudInterArea(fila)" title="Nueva solicitud inter-área"></i>
              </div>
              <div v-for="ciclo in (mostrarBotonAgregarIA(fila) ? fila.ciclos.slice(1) : fila.ciclos)" :key="'ia-fecha-sp-' + ciclo.id" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
            </td>

            <!-- Columna Inter Area — Estado Informe IA -->
            <td v-if="isTecnologicoOrDireccionOrArea">
              <div v-for="ia in fila.solicitudes_interarea" :key="ia.id" class="ciclo-row" style="height:50px">
                <!-- Estado informe según rol -->
                <template v-if="esPrincipalDeIA(ia)">
                  <!-- Área principal: ve estado de confirmación -->
                  <div v-if="ia.estado_correc_informe === 'rechazado'" class="ia-estado" style="position:relative; display:inline-flex; align-items:center;" title="Informe rechazado — esperando corrección del inter-área">
                    <i class="bi bi-clock" style="color:#95a5a6"></i>
                    <i class="bi bi-sticky-fill"
                       style="position:absolute; top:-6px; left:calc(100% - 3px); font-size:13px; color:#f39c12; z-index:10;"></i>
                  </div>
                  <div v-else-if="ia.estado_correc_informe === 'subido'" class="st-sd-cell ia-estado" @click.stop>
                    <button class="st-sd-trigger ia-blink" @click.stop="togglePopupConfirmIA(ia.id)" title="Ver / Confirmar / Rechazar informe corregido" style="border-color:#2980b9;color:#2980b9;">
                      <i class="bi bi-file-earmark-word" style="font-size:13px; color:#2b579a;"></i>
                      <span class="st-sd-badge" style="background:#2980b9;"></span>
                    </button>
                    <i class="bi bi-sticky-fill"
                       style="position:absolute; top:-6px; left:calc(100% + 4px); font-size:13px; color:#e74c3c; cursor:pointer; z-index:10;"
                       @click.stop="verComentarioRechazoIA(ia, 'informe')" title="Ver nota de rechazo anterior"></i>
                    <div v-if="popupConfirmIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -120deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea); popupConfirmIAId = null" title="Ver informe">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="confirmarInterareaPrincipal(ia); popupConfirmIAId = null" title="Confirmar">
                        <i class="bi bi-check-lg"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -60deg" @click.stop="abrirModalRechazarIA(ia); popupConfirmIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="!ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea && ultimoCicloIA(ia).registros_ensayo && ultimoCicloIA(ia).registros_ensayo.length" class="st-sd-cell ia-estado" @click.stop>
                    <button class="st-sd-trigger ia-blink" @click.stop="togglePopupConfirmIA(ia.id)" title="Ver / Confirmar / Rechazar" style="border-color:#2980b9;color:#2980b9;">
                      <i class="bi bi-file-earmark-word" style="font-size:13px; color:#2b579a;"></i>
                      <span class="st-sd-badge" style="background:#2980b9;"></span>
                    </button>
                    <div v-if="popupConfirmIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -120deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea); popupConfirmIAId = null" title="Ver informe">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="confirmarInterareaPrincipal(ia); popupConfirmIAId = null" title="Confirmar">
                        <i class="bi bi-check-lg"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -60deg" @click.stop="abrirModalRechazarIA(ia); popupConfirmIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <span v-else-if="ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea" class="ia-estado" title="Informe confirmado — click para abrir" style="position:relative; display:inline-flex; align-items:center; cursor:pointer;" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea)">
                    <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </span>
                  <span v-else-if="ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea" class="ia-estado" title="Esperando registros del inter-área">
                    <i class="bi bi-clock" style="color:#95a5a6"></i>
                  </span>
                  <span v-else class="ia-estado" title="Esperando informe del inter-área">
                    <i class="bi bi-clock" style="color:#95a5a6"></i>
                  </span>
                </template>
                <template v-else-if="esInterAreaDeIA(ia)">
                  <!-- Inter-área: ve qué hacer -->
                  <div v-if="ia.estado_correc_informe === 'rechazado'" class="st-sd-cell ia-estado" @click.stop>
                    <button class="st-sd-trigger" style="border-color:#2b579a; color:#2b579a;"
                            @click.stop="togglePopupCorreccionIA(ia.id)" title="Ver / Reemplazar informe rechazado">
                      <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                    </button>
                    <i class="bi bi-sticky-fill"
                       style="position:absolute; top:-6px; left:calc(100% + 4px); font-size:13px; color:#e74c3c; cursor:pointer; z-index:10;"
                       @click.stop="verComentarioRechazoIA(ia, 'informe')" title="Ver nota de rechazo"></i>
                    <div v-if="popupCorreccionIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -120deg"
                           @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea); popupCorreccionIAId = null" title="Ver informe">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion" style="--rotation: -60deg" title="Reemplazar informe">
                        <label :for="'ia-informe-corr-' + ia.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                          <i class="bi bi-arrow-repeat"></i>
                        </label>
                        <input :id="'ia-informe-corr-' + ia.id" style="display:none;" type="file"
                               accept=".doc,.docx,.odt,.rtf"
                               @change="subirInformeAreaCicloIA($event, ia); popupCorreccionIAId = null">
                      </div>
                    </div>
                  </div>
                  <span v-else-if="ia.estado_correc_informe === 'subido'" class="ia-estado" title="Corrección enviada — esperando revisión del área principal">
                    <i class="bi bi-clock" style="color:#e67e22"></i>
                  </span>
                  <span v-else-if="ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea" class="ia-estado" title="Informe inter-área — click para abrir" style="cursor:pointer;" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea)">
                    <i class="bi bi-file-earmark-word" style="color:#026290; font-size:22px;"></i>
                  </span>
                  <span v-else class="ia-estado">
                    <label :for="'ia-informe-area-' + ia.id" style="cursor:pointer;" title="Subir informe inter-área">
                      <i class="bi bi-paperclip action-icon"></i>
                    </label>
                    <input :id="'ia-informe-area-' + ia.id" style="display:none;" type="file"
                           accept=".doc,.docx,.odt,.rtf"
                           @change="subirInformeAreaCicloIA($event, ia)">
                  </span>
                </template>
                <template v-else>
                  <!-- Resto: ve estado genérico -->
                  <span v-if="ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea" class="ia-estado" title="Informe inter-área — click para abrir" style="cursor:pointer;" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea)">
                    <i class="bi bi-file-earmark-word" style="color:#026290; font-size:22px;"></i>
                  </span>
                  <span v-else class="ia-estado" title="Esperando informe">
                    <i class="bi bi-clock" style="color:#95a5a6"></i>
                  </span>
                </template>
              </div>
              <div v-if="mostrarBotonAgregarIA(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              <template v-if="!esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in (mostrarBotonAgregarIA(fila) ? fila.ciclos.slice(1) : fila.ciclos)" :key="'ia-inf-sp-' + ciclo.id" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              </template>
            </td>

            <!-- Columna Inter Area — Estado Registros IA -->
            <td v-if="isTecnologicoOrDireccionOrArea">
              <div v-for="ia in fila.solicitudes_interarea" :key="ia.id" class="ciclo-row" style="height:50px">
                <template v-if="ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea">
                  <template v-if="esPrincipalDeIA(ia)">
                    <span v-if="ia.estado_correc_registros === 'rechazado'" class="ia-estado" title="Registros rechazados — esperando corrección">
                      <i class="bi bi-sticky-fill ia-papelito" style="color:#f39c12"></i>
                    </span>
                    <span v-else-if="ia.estado_correc_registros === 'subido'" class="ia-estado ia-blink" title="Corrección subida — confirmar">
                      <i class="bi bi-circle-fill" style="color:#e67e22"></i>
                      <button class="btn btn-xs btn-success ms-1" style="font-size:0.65rem;padding:1px 4px" @click="confirmarCorreccionRegistrosAP(ia)">OK</button>
                    </span>
                    <span v-else-if="ia.estado_correc_registros === 'confirmado'" class="ia-estado" title="Corrección de registros confirmada">
                      <i class="bi bi-check-circle-fill" style="color:#026290"></i>
                    </span>
                    <AttachmentCell v-else-if="ia.confirmado_ap && ultimoCicloIA(ia).registros_ensayo && ultimoCicloIA(ia).registros_ensayo.length"
                      :files="ultimoCicloIA(ia).registros_ensayo || []"
                      :can-upload="false"
                      :can-delete="false"
                      :input-id="'ia-registros-confirmed-' + ultimoCicloIA(ia).id"
                      file-icon="bi bi-folder-check"
                      empty-icon="bi bi-stopwatch"
                      tooltip-label="Registros IA confirmados"
                      @upload="() => {}"
                      @delete="() => {}"
                    />
                    <span v-else-if="ultimoCicloIA(ia).registros_ensayo && ultimoCicloIA(ia).registros_ensayo.length && !ia.estado_correc_informe && !ia.confirmado_ap" class="ia-estado ia-blink" title="Registros subidos — pendiente revisión">
                      <i class="bi bi-circle-fill" style="color:#2980b9"></i>
                    </span>
                    <span v-else class="ia-estado" title="Esperando registros del inter-área">
                      <i class="bi bi-clock" style="color:#95a5a6"></i>
                    </span>
                  </template>
                  <template v-else-if="esInterAreaDeIA(ia)">
                    <span v-if="ia.estado_correc_registros === 'rechazado'" class="ia-estado" :title="'Registros rechazados: ' + (ia.comentario_rechazo_ap || '')">
                      <i class="bi bi-sticky-fill ia-papelito" style="color:#e74c3c;cursor:pointer" @click="verComentarioRechazoIA(ia, 'registros')"></i>
                    </span>
                    <span v-else-if="ia.estado_correc_registros === 'subido'" class="ia-estado" title="Corrección enviada">
                      <i class="bi bi-clock" style="color:#e67e22"></i>
                    </span>
                    <AttachmentCell v-else
                      :files="ultimoCicloIA(ia).registros_ensayo || []"
                      :can-upload="true"
                      :can-delete="true"
                      :input-id="'ia-registros-' + ultimoCicloIA(ia).id"
                      file-icon="bi bi-folder-check"
                      empty-icon="bi bi-folder-plus"
                      tooltip-label="Registros IA"
                      @upload="subirRegistroEnsayoCicloIA($event, ultimoCicloIA(ia))"
                      @delete="eliminarRegistroEnsayoCicloIA"
                    />
                  </template>
                  <template v-else>
                    <AttachmentCell
                      :files="ultimoCicloIA(ia).registros_ensayo || []"
                      :can-upload="false"
                      :can-delete="false"
                      :input-id="'ia-registros-view-' + ultimoCicloIA(ia).id"
                      file-icon="bi bi-folder-check"
                      empty-icon="bi bi-stopwatch"
                      tooltip-label="Registros IA"
                      @upload="() => {}"
                      @delete="() => {}"
                    />
                  </template>
                </template>
              </div>
              <div v-if="mostrarBotonAgregarIA(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              <template v-if="!esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in (mostrarBotonAgregarIA(fila) ? fila.ciclos.slice(1) : fila.ciclos)" :key="'ia-reg-sp-' + ciclo.id" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              </template>
            </td>

            <!-- Columna Tipo IA -->
            <td v-if="isTecnologicoOrDireccionOrArea">
              <div v-for="ia in fila.solicitudes_interarea" :key="ia.id" class="ciclo-row" style="height:50px">
                <span class="badge"
                      :class="ia.tipo === 'resultado' ? 'bg-success' : ia.tipo === 'complementario' ? 'bg-secondary' : 'bg-primary'"
                      style="font-size:10px;"
                      :style="esPrincipalDeIA(ia) ? 'cursor:pointer; text-decoration:underline dotted;' : ''"
                      :title="esPrincipalDeIA(ia) ? 'Cambiar tipo' : tipoIALabel(ia.tipo)"
                      @click.stop="esPrincipalDeIA(ia) && abrirModalTipoIA(ia, fila)">
                  {{ tipoIALabel(ia.tipo) }}
                </span>
              </div>
              <div v-if="mostrarBotonAgregarIA(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              <template v-if="!esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in (mostrarBotonAgregarIA(fila) ? fila.ciclos.slice(1) : fila.ciclos)" :key="'ia-tipo-sp-' + ciclo.id" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              </template>
            </td>

            <!-- Columna Plazo IA -->
            <td v-if="isTecnologicoOrDireccionOrArea" class="add-border-right" style="text-align:center;">
              <div v-for="ia in fila.solicitudes_interarea" :key="'plazo-ia-' + ia.id" class="ciclo-row" style="height:50px;">
                <span v-if="ia.plazo" class="plazo-badge">{{ ia.plazo }}</span>
              </div>
              <div v-if="mostrarBotonAgregarIA(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              <template v-if="!esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in (mostrarBotonAgregarIA(fila) ? fila.ciclos.slice(1) : fila.ciclos)" :key="'plazo-ia-csp-' + ciclo.id" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" style="visibility:hidden;"><i class="bi bi-stopwatch"></i></div>
              </template>
            </td>

            <!-- Columna Fecha Informe de Area (por ciclo) -->
            <td>
              <div v-for="ia in fila.solicitudes_interarea" :key="'fecha-ia-sp-' + ia.id" class="ia-sp"></div>
              <template v-if="!esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                  <span class="no-wrap-column" v-if="ciclo.fecha_informeArea">{{ ciclo.fecha_informeArea }}</span>
                </div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Solicitante -->
            <td style="white-space: nowrap;">
              <template v-if="fila.ordenServicio_completo === true && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total') && !esSoloInterAreaEnFila(fila)">
                {{ fila.nombre_solicitante }}
              </template>
            </td>

            <!-- Columna Informe Area (por ciclo) -->
            <td>
              <div v-for="ia in fila.solicitudes_interarea" :key="'infarea-ia-sp-' + ia.id" class="ia-sp"></div>
              <template v-if="fila.ordenServicio_completo === true && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total') && !esSoloInterAreaEnFila(fila)">
                <div v-for="ciclo in fila.ciclos" :key="ciclo.id"
                     class="ciclo-row"
                     :class="{ 'ciclo-row--final': fila.ciclos.some(c => c.tipo === 'final') }">
                  <!-- Rechazo de ST hacia área: mostrar informe de servicio en esta columna -->
                  <span v-if="ciclo.rechazo_st_destino === 'area' && ciclo.adjunto_informeServicio"
                        style="display:inline-flex; align-items:center; gap:4px;">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290;"
                       @click.stop="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe de servicio"></i>
                    <i class="bi bi-sticky-fill" style="color:#9c7cc7; cursor:pointer; font-size:14px;"
                       @click.stop="abrirModalVerRechazoST(ciclo)" title="Ver nota de rechazo de ST"></i>
                  </span>
                  <span v-else-if="ciclo.adjunto_informeArea" class="attachment-wrap" style="position:relative; display:inline-flex; align-items:center;">
                    <i class="bi bi-file-earmark-word action-icon" style="color:#026290; cursor:pointer; font-size:22px;"
                       @click.stop="togglePopupInformeArea(ciclo.id)"
                       :title="'Informe ' + (ciclo.tipo === 'parcial' ? 'Parcial' : ciclo.tipo === 'complementario' ? 'Complementario' : 'Final') + ' ' + ciclo.numero"></i>
                    <i v-if="ciclo.rechazo_area_destino === 'area' && !ciclo.revision_confirmada"
                       class="bi bi-sticky-fill"
                       style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                       @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo del responsable de área"></i>
                    <div v-if="popupInformeAreaId === ciclo.id"
                         class="st-sd-dial" @click.stop>
                      <div class="st-sd-opcion" style="--rotation: -120deg"
                           @click.stop="abrirArchivo(ciclo.adjunto_informeArea); popupInformeAreaId = null" title="Ver">
                        <i class="bi bi-eye"></i>
                      </div>
                      <template v-if="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion && esMiAreaEsteFila(fila)">
                        <label class="st-sd-opcion" style="--rotation: -60deg; cursor:pointer;" title="Reemplazar"
                               :for="'reemplazar-inf-area-' + ciclo.id" @click.stop="popupInformeAreaId = null">
                          <i class="bi bi-arrow-repeat"></i>
                        </label>
                        <input :id="'reemplazar-inf-area-' + ciclo.id" style="display:none;" type="file"
                               accept=".doc,.docx,.odt,.rtf"
                               @change="reemplazarInformeAreaCiclo($event, ciclo)">
                      </template>
                    </div>
                  </span>
                  <span v-else-if="(isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila)" style="display:inline-flex; align-items:center; gap:4px;">
                    <label :for="'inf-area-ciclo-' + ciclo.id" style="cursor:pointer;" title="Subir informe área">
                      <i class="bi bi-paperclip action-icon"></i>
                    </label>
                    <input :id="'inf-area-ciclo-' + ciclo.id" style="display:none;" type="file"
                           accept=".doc,.docx,.odt,.rtf"
                           @change="seleccionarArchivoInformeAreaCiclo($event, ciclo, fila)">
                    <i v-if="ciclo.rechazo_area_destino === 'area' && !ciclo.revision_confirmada"
                       class="bi bi-sticky-fill" style="color:#ffc107; cursor:pointer; font-size:14px;"
                       @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo del responsable de área"></i>
                  </span>
                  <span v-else><i class="bi bi-stopwatch"></i></span>
                </div>
                <!-- Sin ciclos: clip para área, reloj para otros -->
                <div v-if="fila.ciclos.length === 0" class="ciclo-row">
                  <span v-if="(isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila)">
                    <label :for="'inf-area-primer-' + fila.nro_circuito" style="cursor:pointer;" title="Subir primer informe área">
                      <i class="bi bi-paperclip action-icon"></i>
                    </label>
                    <input :id="'inf-area-primer-' + fila.nro_circuito" style="display:none;" type="file"
                           accept=".doc,.docx,.odt,.rtf"
                           @change="seleccionarArchivoParaNuevoCiclo($event, fila)">
                  </span>
                  <span v-else><i class="bi bi-stopwatch"></i></span>
                </div>
                <!-- Clip para agregar otro parcial: fila separada debajo del último -->
                <div v-if="(isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila)
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
                         accept=".doc,.docx,.odt,.rtf"
                         @change="seleccionarArchivoParaNuevoCiclo($event, fila)">
                </div>
              </template>
            </td>

            <!-- Columna Registros de Ensayo (por ciclo) -->
            <td>
              <div v-for="ia in fila.solicitudes_interarea" :key="'reg-ia-sp-' + ia.id" class="ia-sp"></div>
              <template v-if="mostrarInformeAreaEnFila(fila) && !esSoloInterAreaEnFila(fila)">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id"
                   class="ciclo-row"
                   :class="{ 'ciclo-row--final': fila.ciclos.some(c => c.tipo === 'final') }">
                <AttachmentCell
                  :files="ciclo.registros_ensayo"
                  :can-upload="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion && esMiAreaEsteFila(fila)"
                  :can-delete="(isAreaJefe || isAreaStandard) && !ciclo.firma_direccion && esMiAreaEsteFila(fila)"
                  :input-id="'registros-ciclo-' + ciclo.id"
                  file-icon="bi bi-folder-check"
                  empty-icon="bi bi-folder-plus"
                  :tooltip-label="(ciclo.tipo === 'parcial' ? 'Parcial' : ciclo.tipo === 'complementario' ? 'Complementario' : 'Final') + ' ' + ciclo.numero"
                  @upload="subirRegistroEnsayoCiclo($event, ciclo)"
                  @delete="eliminarRegistroEnsayoCiclo"
                />
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Estado/Tipo (por ciclo) -->
            <td>
              <div v-for="ia in fila.solicitudes_interarea" :key="'tipo-ia-sp-' + ia.id" class="ia-sp"></div>
              <template v-if="mostrarInformeAreaEnFila(fila) && !esSoloInterAreaEnFila(fila)">
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <span v-if="ciclo.adjunto_informeArea"
                      class="badge"
                      :class="ciclo.tipo === 'complementario' ? 'bg-success' : ciclo.tipo === 'final' ? 'bg-dark' : 'bg-primary'"
                      :style="'font-size:10px;' + ((isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila) && !ciclo.firma_direccion && !ciclo.adjunto_informeServicio ? ' cursor:pointer; text-decoration:underline dotted;' : '')"
                      :title="(isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila) && !ciclo.firma_direccion && !ciclo.adjunto_informeServicio ? 'Cambiar tipo' : ''"
                      @click.stop="(isAreaJefe || isAreaStandard) && esMiAreaEsteFila(fila) && !ciclo.firma_direccion && !ciclo.adjunto_informeServicio && cambiarTipoCiclo(ciclo, fila)">
                  {{ ciclo.tipo === 'complementario' ? 'Compl.' : ciclo.tipo === 'final' ? 'Final' : 'Parcial' }}
                </span>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Plazo (por ciclo) -->
            <td class="add-border-right" style="text-align:center;">
              <!-- Spacers IA -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'plazo-ciclo-ia-sp-' + ia.id" class="ia-sp"></div>
              <template v-if="(fila.ordenServicio_completo === true) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total') && !esSoloInterAreaEnFila(fila)">
                <!-- Sin ciclos todavía: plazo general -->
                <div v-if="fila.ciclos.length === 0" class="ciclo-row">
                  <span class="plazo-badge">{{ fila.plazo_estimado }}</span>
                </div>
                <!-- Un badge por ciclo -->
                <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                  <span class="plazo-badge">
                    {{ plazoCiclo(ciclo, fila) !== null ? plazoCiclo(ciclo, fila) : fila.plazo_estimado }}
                  </span>
                </div>
                <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Administracion - Informe Servicio (por ciclo) -->
            <td class="add-border-right">
              <template v-if="!esSoloInterAreaEnFila(fila)">
              <!-- IA pipeline — Admin -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'adm-ia-' + ia.id" class="ciclo-row" style="height:50px">
                <template v-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia)">
                  <template v-if="!ultimoCicloIA(ia).adjunto_informeServicio && !ultimoCicloIA(ia).corregir">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger ia-blink" @click.stop="togglePopupFormatoIA(ultimoCicloIA(ia).id)" title="Formato institucional IA pendiente" style="border-color:#e67e22; color:#e67e22;">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge" style="background:#e67e22;"></span>
                      </button>
                      <div v-if="popupFormatoIAId === ultimoCicloIA(ia).id" class="st-sd-dial" @click.stop>
                        <div class="st-sd-opcion" style="--rotation: -120deg"
                             @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea); popupFormatoIAId = null" title="Ver informe IA">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" style="--rotation: -60deg" title="Subir formato institucional">
                          <label :for="'ia-inf-serv-' + ultimoCicloIA(ia).id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-upload"></i>
                          </label>
                          <input :id="'ia-inf-serv-' + ultimoCicloIA(ia).id" type="file" style="display:none;" accept=".doc,.docx,.odt,.rtf"
                                 @change="subirInformeServicioCicloIA($event, ultimoCicloIA(ia)); popupFormatoIAId = null">
                        </div>
                      </div>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <template v-else-if="ultimoCicloIA(ia).corregir">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger" style="border-color:#2b579a; color:#2b579a;"
                              @click.stop="togglePopupFormatoIA(ultimoCicloIA(ia).id)" title="Ver / Reemplazar informe IA">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge"></span>
                      </button>
                      <div v-if="popupFormatoIAId === ultimoCicloIA(ia).id" class="st-sd-dial">
                        <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio)" title="Ver Word IA">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" style="--rotation: -90deg" title="Reemplazar archivo">
                          <label :for="'ia-reemplazar-' + ultimoCicloIA(ia).id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-arrow-repeat"></i>
                          </label>
                          <input :id="'ia-reemplazar-' + ultimoCicloIA(ia).id" type="file" style="display:none;" accept=".doc,.docx,.odt,.rtf" @change="subirInformeServicioCicloIA($event, ultimoCicloIA(ia))">
                        </div>
                      </div>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <template v-else-if="ultimoCicloIA(ia).adjunto_informeServicio">
                    <div style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px; cursor:pointer;"
                         @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio)" title="Ver Word IA"></i>
                      <i class="bi bi-check-circle-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                    </div>
                  </template>
                </template>
                <template v-else-if="!ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea && ultimoCicloIA(ia).adjunto_informeServicio">
                  <div style="position:relative; display:inline-flex; align-items:center;">
                    <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px; cursor:pointer;"
                       @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio)" title="Ver formato institucional IA"></i>
                    <i class="bi bi-check-circle-fill"
                       style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
                <template v-else-if="!ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeArea && !ultimoCicloIA(ia).adjunto_informeServicio">
                  <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger ia-blink" @click.stop="togglePopupPDFAdminIA(ia.id)" title="Informe Inter-Área — aplicar formato institucional" style="border-color:#e67e22; color:#e67e22;">
                      <i class="bi bi-file-earmark-word" style="font-size:13px; color:#e67e22;"></i>
                      <span class="st-sd-badge" style="background:#e67e22;"></span>
                    </button>
                    <div v-if="popupPDFAdminIAId === ia.id" class="st-sd-dial" @click.stop>
                      <div class="st-sd-opcion" style="--rotation: -120deg"
                           @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeArea); popupPDFAdminIAId = null" title="Ver informe IA">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion" style="--rotation: -60deg" title="Subir formato institucional">
                        <label :for="'ia-fmt-inst-' + ultimoCicloIA(ia).id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                          <i class="bi bi-upload"></i>
                        </label>
                        <input :id="'ia-fmt-inst-' + ultimoCicloIA(ia).id" type="file" style="display:none;" accept=".doc,.docx,.odt,.rtf"
                               @change="subirInformeServicioCicloIA($event, ultimoCicloIA(ia)); popupPDFAdminIAId = null">
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <span v-else style="visibility:hidden;"><i class="bi bi-stopwatch"></i></span>
              </div>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.adjunto_informeArea && ciclo.registros_ensayo && ciclo.registros_ensayo.length > 0">
                  <!-- Sin informe servicio, sin corrección pendiente -->
                  <template v-if="!ciclo.adjunto_informeServicio && !ciclo.corregir">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger ia-blink" @click.stop="togglePopupFormato(ciclo.id)"
                              :title="ciclo.tipo_cambiado_admin ? '⚠ El tipo de informe fue modificado · Formato institucional pendiente' : 'Formato institucional pendiente'"
                              style="border-color:#e67e22; color:#e67e22; position:relative;">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge" style="background:#e67e22;"></span>
                        <span v-if="ciclo.tipo_cambiado_admin"
                              style="position:absolute; top:-5px; right:-5px; background:#e67e22; color:#fff; border-radius:50%; width:12px; height:12px; font-size:9px; display:flex; align-items:center; justify-content:center; font-weight:bold; line-height:1;">!</span>
                      </button>
                      <div v-if="popupFormatoId === ciclo.id" class="st-sd-dial" @click.stop>
                        <div v-if="ciclo.tipo_cambiado_admin" class="st-sd-opcion" style="--rotation: -150deg; background:#e67e22; color:#fff;"
                             @click.stop="confirmarTipoCambioAdmin(ciclo); popupFormatoId = null" title="OK: enterado del cambio de tipo">
                          <i class="bi bi-check-lg"></i>
                        </div>
                        <div class="st-sd-opcion" :style="ciclo.tipo_cambiado_admin ? '--rotation: -105deg' : '--rotation: -120deg'"
                             @click.stop="abrirArchivo(ciclo.adjunto_informeArea); popupFormatoId = null" title="Ver informe área">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" :style="ciclo.tipo_cambiado_admin ? '--rotation: -60deg' : '--rotation: -60deg'" title="Subir formato institucional">
                          <label :for="'inf-serv-ciclo-' + ciclo.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-upload"></i>
                          </label>
                          <input :id="'inf-serv-ciclo-' + ciclo.id" style="display:none;" type="file"
                                 accept=".doc,.docx,.odt,.rtf"
                                 @change="subirInformeServicioCiclo($event, ciclo); popupFormatoId = null">
                        </div>
                      </div>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <!-- Con informe servicio, rechazado a administración por Dirección -->
                  <template v-else-if="ciclo.adjunto_informeServicio && !ciclo.corregir && ciclo.rechazo_destino === 'administracion'">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger" style="border-color:#2b579a; color:#2b579a;"
                              @click.stop="togglePopupFormato(ciclo.id)" title="Ver / Reemplazar informe">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge"></span>
                      </button>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-6px; left:calc(100% + 4px); font-size:13px; color:#dc3545; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazo(ciclo)" title="Ver nota de rechazo de Dirección"></i>
                      <div v-if="popupFormatoId === ciclo.id" class="st-sd-dial">
                        <div class="st-sd-opcion" style="--rotation: -120deg"
                             @click.stop="abrirArchivo(ciclo.adjunto_informeServicio); popupFormatoId = null" title="Ver Word">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" style="--rotation: -60deg" title="Reemplazar informe">
                          <label :for="'inf-rechazado-' + ciclo.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-arrow-repeat"></i>
                          </label>
                          <input :id="'inf-rechazado-' + ciclo.id" style="display:none;" type="file"
                                 accept=".doc,.docx,.odt,.rtf"
                                 @change="subirInformeServicioCiclo($event, ciclo)">
                        </div>
                      </div>
                    </div>
                    <div v-else-if="isServiciosTecnologicos || isDireccion"
                         style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-stopwatch"></i>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#dc3545; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazo(ciclo)" title="Ver nota de rechazo de Dirección"></i>
                    </div>
                    <i v-else-if="isAreaJefe || isAreaStandard" class="bi bi-stopwatch"></i>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <!-- Con informe servicio, rechazado a administración por ST -->
                  <template v-else-if="ciclo.adjunto_informeServicio && !ciclo.corregir && ciclo.rechazo_st_destino === 'administracion'">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger" style="border-color:#2b579a; color:#2b579a;"
                              @click.stop="togglePopupFormato(ciclo.id)" title="Ver / Reemplazar informe">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge"></span>
                      </button>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-6px; left:calc(100% + 4px); font-size:13px; color:#9c7cc7; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoST(ciclo)" title="Ver nota de rechazo de ST"></i>
                      <div v-if="popupFormatoId === ciclo.id" class="st-sd-dial">
                        <div class="st-sd-opcion" style="--rotation: -120deg"
                             @click.stop="abrirArchivo(ciclo.adjunto_informeServicio); popupFormatoId = null" title="Ver Word">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" style="--rotation: -60deg" title="Reemplazar informe">
                          <label :for="'inf-rechazado-st-' + ciclo.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-arrow-repeat"></i>
                          </label>
                          <input :id="'inf-rechazado-st-' + ciclo.id" style="display:none;" type="file"
                                 accept=".doc,.docx,.odt,.rtf"
                                 @change="subirInformeServicioCiclo($event, ciclo)">
                        </div>
                      </div>
                    </div>
                    <div v-else-if="isServiciosTecnologicos || isDireccion"
                         style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-stopwatch"></i>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#9c7cc7; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoST(ciclo)" title="Ver nota de rechazo de ST"></i>
                    </div>
                    <i v-else-if="isAreaJefe || isAreaStandard" class="bi bi-stopwatch"></i>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <!-- Con informe servicio, rechazado a administración por Área -->
                  <template v-else-if="ciclo.adjunto_informeServicio && !ciclo.corregir && ciclo.rechazo_area_destino === 'administracion'">
                    <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                      <button class="st-sd-trigger" style="border-color:#2b579a; color:#2b579a;"
                              @click.stop="togglePopupFormato(ciclo.id)" title="Ver / Reemplazar informe">
                        <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                        <span class="st-sd-badge"></span>
                      </button>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-6px; left:calc(100% + 4px); font-size:13px; color:#ffc107; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo de Área"></i>
                      <div v-if="popupFormatoId === ciclo.id" class="st-sd-dial">
                        <div class="st-sd-opcion" style="--rotation: -120deg"
                             @click.stop="abrirArchivo(ciclo.adjunto_informeServicio); popupFormatoId = null" title="Ver Word">
                          <i class="bi bi-eye"></i>
                        </div>
                        <div class="st-sd-opcion" style="--rotation: -60deg" title="Reemplazar informe">
                          <label :for="'inf-rechazado-area-admin-' + ciclo.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                            <i class="bi bi-arrow-repeat"></i>
                          </label>
                          <input :id="'inf-rechazado-area-admin-' + ciclo.id" style="display:none;" type="file"
                                 accept=".doc,.docx,.odt,.rtf"
                                 @change="subirInformeServicioCiclo($event, ciclo)">
                        </div>
                      </div>
                    </div>
                    <div v-else-if="isServiciosTecnologicos || isDireccion"
                         style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-stopwatch"></i>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo de Área"></i>
                    </div>
                    <div v-else-if="isAreaJefe || isAreaStandard"
                         style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-stopwatch"></i>
                      <i class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo enviada"></i>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                  <!-- Con informe servicio, sin corrección -->
                  <template v-else-if="ciclo.adjunto_informeServicio && !ciclo.corregir">
                    <div style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px;" title="Informe de servicio"></i>
                      <i class="bi bi-check-circle-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                      <i v-if="ciclo.historial_correcciones && ciclo.historial_correcciones.some(c => c.tipo === 'st' && c.estado === 'pendiente' && c.destinatario === 'administracion')"
                         class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% + 9px); font-size:12px; color:#9c7cc7; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerCorrecciones(ciclo)"
                         :title="ciclo.historial_correcciones.filter(c => c.tipo === 'st' && c.estado === 'pendiente' && c.destinatario === 'administracion').length + ' corrección(es) de ST pendiente(s)'"></i>
                      <i v-if="ciclo.historial_correcciones && ciclo.historial_correcciones.some(c => c.tipo === 'area' && c.estado === 'pendiente' && c.destinatario === 'administracion')"
                         class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% + 21px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerCorrecciones(ciclo)"
                         :title="ciclo.historial_correcciones.filter(c => c.tipo === 'area' && c.estado === 'pendiente' && c.destinatario === 'administracion').length + ' corrección(es) de Área pendiente(s)'"></i>
                      <i v-if="ciclo.historial_correcciones && ciclo.historial_correcciones.some(c => c.tipo === 'direccion' && c.estado === 'pendiente' && c.destinatario === 'administracion')"
                         class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% + 33px); font-size:12px; color:#dc3545; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerCorrecciones(ciclo)"
                         :title="ciclo.historial_correcciones.filter(c => c.tipo === 'direccion' && c.estado === 'pendiente' && c.destinatario === 'administracion').length + ' corrección(es) de Dirección pendiente(s)'"></i>
                    </div>
                  </template>
                  <!-- Con corrección pendiente -->
                  <template v-else-if="ciclo.corregir">
                    <div v-if="isAdministracion">
                      <i class="bi bi-filetype-pdf action-icon" @click="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver informe"></i>
                      <label :for="'inf-serv-corr-ciclo-' + ciclo.id" style="cursor:pointer; margin-left:4px;" title="Resubir">
                        <i class="bi bi-upload action-icon"></i>
                      </label>
                      <input :id="'inf-serv-corr-ciclo-' + ciclo.id" style="display:none;" type="file"
                             accept=".doc,.docx,.odt,.rtf"
                             @change="subirInformeServicioCiclo($event, ciclo)">
                      <i class="bi bi-backspace-fill text-danger action-icon"
                         @click="abrirModalCorreccionesCiclo(ciclo)" title="Ver correcciones" style="font-size:0.8em;"></i>
                    </div>
                    <i v-else class="bi bi-stopwatch"></i>
                  </template>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Revisión Servicios Tecnológicos (por ciclo) -->
            <td class="add-border-right">
              <template v-if="!esSoloInterAreaEnFila(fila)">
              <!-- IA pipeline — ST -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'st-ia-' + ia.id" class="ciclo-row" style="height:50px">
                <template v-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).adjunto_informeServicio && !ultimoCicloIA(ia).revision_confirmada && !ultimoCicloIA(ia).corregir">
                  <div v-if="isServiciosTecnologicos" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupSTIA(ia.id)" title="Revisar informe IA">
                      <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupSTIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio)" title="Ver">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="confirmarRevisionCicloIA(ia)" title="Confirmar OK">
                        <i class="bi bi-check-lg"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -30deg" @click.stop="abrirModalRechazoSTIA(ultimoCicloIA(ia)); popupSTIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).revision_confirmada">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio)">
                    <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
                <span v-else style="visibility:hidden;"><i class="bi bi-stopwatch"></i></span>
              </div>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.adjunto_informeServicio && !ciclo.revision_confirmada && !ciclo.firma_responsable_area && !ciclo.firma_direccion && !ciclo.corregir && (!ciclo.rechazo_area_destino || ciclo.rechazo_area_destino === 'st') && !ciclo.rechazo_st_destino">
                  <div v-if="isServiciosTecnologicos" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupST(ciclo.id)"
                            :title="stReemplazadoIds.has(ciclo.id) ? 'Archivo reemplazado — abrí para confirmar' : 'Informe ST ' + ciclo.numero">
                      <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                      <span v-if="!stReemplazadoIds.has(ciclo.id)" class="st-sd-badge"></span>
                      <span v-if="stReemplazadoIds.has(ciclo.id)" class="st-sd-badge st-sd-badge--confirmar"></span>
                    </button>
                    <i v-if="ciclo.rechazo_destino === 'st'" class="bi bi-sticky-fill"
                       style="position:absolute; top:-6px; left:calc(100% - 4px); font-size:13px; color:#dc3545; cursor:pointer; z-index:10;"
                       @click.stop="abrirModalVerRechazo(ciclo)"
                       title="Ver nota de rechazo de Dirección"></i>
                    <i v-if="ciclo.rechazo_area_destino === 'st' || ciclo.rechazo_area_destino === 'area'" class="bi bi-sticky-fill"
                       style="position:absolute; top:-6px; left:calc(100% + 8px); font-size:13px; color:#ffc107; cursor:pointer; z-index:10;"
                       @click.stop="abrirModalVerRechazoArea(ciclo)"
                       title="Ver nota de rechazo de Área"></i>
                    <div v-if="popupSTId === ciclo.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ciclo.adjunto_informeServicio)" title="Ver">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion" style="--rotation: -105deg" title="Reemplazar archivo">
                        <label :for="'st-reemplazar-' + ciclo.id" style="cursor:pointer; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
                          <i class="bi bi-arrow-repeat"></i>
                        </label>
                        <input :id="'st-reemplazar-' + ciclo.id" type="file" style="display:none;" accept=".doc,.docx,.odt,.rtf" @change="seleccionarArchivoSTCorregido($event, ciclo)">
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -60deg" @click.stop="confirmarRevisionST(ciclo)" title="Confirmar OK">
                        <i class="bi bi-check-lg"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -15deg" @click.stop="abrirModalRechazoST(ciclo); popupSTId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="isAdministracion || isDireccion"
                       style="display:inline-flex; flex-direction:column; align-items:center; gap:2px;">
                    <div style="position:relative; display:inline-flex; align-items:center;">
                      <i class="bi bi-stopwatch"></i>
                      <i v-if="ciclo.rechazo_destino === 'st'" class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#dc3545; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazo(ciclo)" title="Ver nota de rechazo de Dirección"></i>
                      <i v-if="ciclo.rechazo_area_destino === 'st' || ciclo.rechazo_area_destino === 'area'" class="bi bi-sticky-fill"
                         style="position:absolute; top:-5px; left:calc(100% + 9px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                         @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo de Área"></i>
                    </div>
                  </div>
                  <div v-else style="position:relative; display:inline-flex; align-items:center;">
                    <i class="bi bi-stopwatch"></i>
                    <i v-if="(isAreaJefe || isAreaStandard) && (ciclo.rechazo_area_destino === 'st' || ciclo.rechazo_area_destino === 'area')"
                       class="bi bi-sticky-fill"
                       style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                       @click.stop="abrirModalVerRechazoArea(ciclo)" title="Ver nota de rechazo enviada"></i>
                  </div>
                </template>
                <template v-else-if="ciclo.revision_confirmada && !ciclo.corregir">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ciclo.adjunto_informeServicio)"
                       title="Ver informe de servicio (Word)">
                    <i class="bi bi-file-earmark-word" style="color:#2b579a; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill"
                       style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna PDF Admin (por ciclo) -->
            <td class="add-border-right">
              <template v-if="!esSoloInterAreaEnFila(fila)">
              <!-- IA pipeline — PDF Admin -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'pdf-ia-' + ia.id" class="ciclo-row" style="height:50px">
                <template v-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).revision_confirmada && !ultimoCicloIA(ia).pdf_confirmado_admin && !ultimoCicloIA(ia).corregir">
                  <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupPDFAdminIA(ia.id)" title="Generar PDF IA"
                            style="border-color:#e67e22; color:#e67e22;">
                      <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupPDFAdminIAId === ia.id" class="st-sd-dial" @click.stop>
                      <div class="st-sd-opcion" style="--rotation: -120deg"
                           @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio); popupPDFAdminIAId = null" title="Ver Word">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion" style="--rotation: -60deg; border-color:#dc3545; color:#dc3545;"
                           :class="generandoPDFIAId === ia.id ? 'st-sd-opcion--generando' : ''"
                           @click.stop="generandoPDFIAId !== ia.id && generarPDFCicloIA(ia)" title="Convertir a PDF">
                        <i v-if="generandoPDFIAId === ia.id" class="bi bi-hourglass-split" style="animation: spin 1.2s linear infinite;"></i>
                        <i v-else class="bi bi-filetype-pdf"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).pdf_confirmado_admin">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio_pdf)">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:16px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
                <span v-else style="visibility:hidden;"><i class="bi bi-stopwatch"></i></span>
              </div>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.revision_confirmada && !ciclo.pdf_confirmado_admin && !ciclo.firma_responsable_area && !ciclo.firma_direccion && !ciclo.corregir">
                  <div v-if="isAdministracion" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger ia-blink" @click.stop="togglePopupPDFAdmin(ciclo.id)" title="Formato institucional pendiente — Ver / Convertir a PDF"
                            style="border-color:#e67e22; color:#e67e22;">
                      <i class="bi bi-file-earmark-word" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupPDFAdminId === ciclo.id" class="st-sd-dial" @click.stop>
                      <div class="st-sd-opcion" style="--rotation: -120deg"
                           @click.stop="abrirArchivo(ciclo.adjunto_informeServicio); popupPDFAdminId = null" title="Ver Word editable">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion" style="--rotation: -60deg; border-color:#dc3545; color:#dc3545;"
                           :class="generandoPDFId === ciclo.id ? 'st-sd-opcion--generando' : ''"
                           @click.stop="generandoPDFId !== ciclo.id && generarPDFServicioCiclo(ciclo)" title="Convertir a PDF">
                        <i v-if="generandoPDFId === ciclo.id" class="bi bi-hourglass-split" style="animation: spin 1.2s linear infinite;"></i>
                        <i v-else class="bi bi-filetype-pdf"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.pdf_confirmado_admin && !ciclo.corregir">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ciclo.adjunto_informeServicio_pdf)"
                       title="Ver PDF confirmado por Administración">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Responsable Área - Firma (por ciclo) -->
            <td class="add-border-right">
              <template v-if="!esSoloInterAreaEnFila(fila)">
              <!-- IA pipeline — Firma Área (inter-área jefe primero, luego jefe área principal) -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'area-ia-' + ia.id" class="ciclo-row" style="height:50px">
                <!-- Paso 1: firma del jefe inter-área -->
                <template v-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).pdf_confirmado_admin && !ultimoCicloIA(ia).firma_responsable_area && !ultimoCicloIA(ia).corregir">
                  <div v-if="isAreaJefe && esInterAreaDeIA(ia)" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupAreaIA(ia.id)" title="Opciones firma IA">
                      <i class="bi bi-filetype-pdf" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupAreaIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_informeServicio_pdf); popupAreaIAId = null" title="Ver PDF IA">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="abrirModalFirmaAreaCicloIA(ultimoCicloIA(ia)); popupAreaIAId = null" title="Firmar">
                        <i class="bi bi-pen"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -30deg" @click.stop="abrirModalRechazoAreaIA(ultimoCicloIA(ia)); popupAreaIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <!-- Paso 2: firma del jefe área principal -->
                <template v-else-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).firma_responsable_area && !ultimoCicloIA(ia).firma_responsable_ap && !ultimoCicloIA(ia).corregir">
                  <div v-if="esPrincipalDeIA(ia)" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupAPIA(ia.id)" title="Opciones firma área principal IA">
                      <i class="bi bi-filetype-pdf" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupAPIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_firmado_area || ultimoCicloIA(ia).adjunto_informeServicio_pdf); popupAPIAId = null" title="Ver PDF firmado área">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="abrirModalFirmaAPCicloIA(ultimoCicloIA(ia)); popupAPIAId = null" title="Firmar">
                        <i class="bi bi-pen"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -30deg" @click.stop="abrirModalRechazoAPIA(ultimoCicloIA(ia)); popupAPIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <!-- Ambas firmas completadas -->
                <template v-else-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).firma_responsable_ap">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_firmado_ap || ultimoCicloIA(ia).adjunto_firmado_area || ultimoCicloIA(ia).adjunto_informeServicio_pdf)">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:16px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
                <span v-else style="visibility:hidden;"><i class="bi bi-stopwatch"></i></span>
              </div>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.pdf_confirmado_admin && !ciclo.firma_responsable_area && !ciclo.firma_direccion && !ciclo.corregir">
                  <div v-if="isAreaJefe" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupArea(ciclo.id)" title="Opciones">
                      <i class="bi bi-filetype-pdf" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupAreaId === ciclo.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -135deg" @click.stop="abrirArchivo(ciclo.adjunto_informeServicio_pdf); popupAreaId = null" title="Ver informe PDF">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="abrirModalFirmaResponsableAreaCiclo(ciclo); popupAreaId = null" title="Firmar">
                        <i class="bi bi-pen"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -45deg" @click.stop="abrirModalRechazoArea(ciclo); popupAreaId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else-if="isAreaStandard" class="bi bi-filetype-pdf action-icon" style="color:#026290;"
                     @click.stop="abrirArchivo(ciclo.adjunto_informeServicio_pdf)" title="Ver informe PDF"></i>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.firma_responsable_area">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ciclo.adjunto_firmado_area || ciclo.adjunto_informeServicio_pdf)"
                       title="Ver informe firmado por responsable de área">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                    <i v-if="ciclo.historial_correcciones && ciclo.historial_correcciones.some(c => c.tipo === 'area' && c.estado === 'pendiente' && c.destinatario === 'administracion')"
                       class="bi bi-sticky-fill"
                       style="position:absolute; top:-5px; left:calc(100% + 9px); font-size:12px; color:#ffc107; cursor:pointer; z-index:10;"
                       @click.stop.prevent="abrirModalVerCorrecciones(ciclo)"
                       :title="ciclo.historial_correcciones.filter(c => c.tipo === 'area' && c.estado === 'pendiente' && c.destinatario === 'administracion').length + ' corrección(es) de Área pendiente(s)'"></i>
                  </div>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Dirección - Firma (por ciclo) -->
            <td class="add-border-right">
              <template v-if="!esSoloInterAreaEnFila(fila)">
              <!-- IA pipeline — Firma Dirección -->
              <div v-for="ia in fila.solicitudes_interarea" :key="'dir-ia-' + ia.id" class="ciclo-row" style="height:50px">
                <template v-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).firma_responsable_ap && !ultimoCicloIA(ia).firma_direccion">
                  <div v-if="isDireccion" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupDirIA(ia.id)" title="Opciones firma dirección IA">
                      <i class="bi bi-filetype-pdf" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupDirIAId === ia.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_firmado_ap || ultimoCicloIA(ia).adjunto_firmado_area || ultimoCicloIA(ia).adjunto_informeServicio_pdf); popupDirIAId = null" title="Ver PDF firmado AP">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="abrirModalFirmaDireccionCicloIA(ultimoCicloIA(ia)); popupDirIAId = null" title="Firmar">
                        <i class="bi bi-pen"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -30deg" @click.stop="abrirModalRechazoDireccionIA(ultimoCicloIA(ia)); popupDirIAId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ia.genera_informe_parcial && ia.confirmado_ap && ultimoCicloIA(ia) && ultimoCicloIA(ia).firma_direccion">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ultimoCicloIA(ia).adjunto_firmado_direccion || ultimoCicloIA(ia).adjunto_firmado_ap || ultimoCicloIA(ia).adjunto_firmado_area || ultimoCicloIA(ia).adjunto_informeServicio_pdf)">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:16px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                  </div>
                </template>
                <span v-else style="visibility:hidden;"><i class="bi bi-stopwatch"></i></span>
              </div>
              <div v-for="ciclo in fila.ciclos" :key="ciclo.id" class="ciclo-row">
                <template v-if="ciclo.firma_responsable_area && !ciclo.firma_direccion">
                  <div v-if="isDireccion" class="st-sd-cell" @click.stop>
                    <button class="st-sd-trigger" @click.stop="togglePopupDir(ciclo.id)" title="Opciones">
                      <i class="bi bi-filetype-pdf" style="font-size:13px;"></i>
                      <span class="st-sd-badge"></span>
                    </button>
                    <div v-if="popupDirId === ciclo.id" class="st-sd-dial">
                      <div class="st-sd-opcion" style="--rotation: -150deg" @click.stop="abrirArchivo(ciclo.adjunto_firmado_area || ciclo.adjunto_informeServicio_pdf); popupDirId = null" title="Ver informe PDF firmado por área">
                        <i class="bi bi-eye"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--ok" style="--rotation: -90deg" @click.stop="abrirModalFirmaDireccionCiclo(ciclo); popupDirId = null" title="Firmar">
                        <i class="bi bi-pen"></i>
                      </div>
                      <div class="st-sd-opcion st-sd-opcion--danger" style="--rotation: -30deg" @click.stop="abrirModalRechazoDireccion(ciclo); popupDirId = null" title="Rechazar">
                        <i class="bi bi-x-lg"></i>
                      </div>
                    </div>
                  </div>
                  <i v-else class="bi bi-stopwatch"></i>
                </template>
                <template v-else-if="ciclo.firma_direccion">
                  <div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;"
                       @click.stop="abrirArchivo(ciclo.adjunto_firmado_direccion || ciclo.adjunto_firmado_area || ciclo.adjunto_informeServicio_pdf)"
                       title="Ver informe firmado por dirección">
                    <i class="bi bi-filetype-pdf action-icon" style="color:#026290; font-size:22px;"></i>
                    <i class="bi bi-check-circle-fill" style="position:absolute; top:-5px; left:calc(100% - 3px); font-size:12px; color:#026290; z-index:10;"></i>
                    <i v-if="ciclo.historial_correcciones && ciclo.historial_correcciones.some(c => c.tipo === 'direccion' && c.estado === 'pendiente' && c.destinatario === 'administracion')"
                       class="bi bi-sticky-fill"
                       style="position:absolute; top:-5px; left:calc(100% + 9px); font-size:12px; color:#dc3545; cursor:pointer; z-index:10;"
                       @click.stop.prevent="abrirModalVerCorrecciones(ciclo)"
                       :title="ciclo.historial_correcciones.filter(c => c.tipo === 'direccion' && c.estado === 'pendiente' && c.destinatario === 'administracion').length + ' corrección(es) de Dirección pendiente(s)'"></i>
                  </div>
                </template>
              </div>
              <div v-if="mostrarClipParaNuevoParcial(fila)" class="ciclo-row" aria-hidden="true" style="visibility:hidden;"><i class="bi bi-paperclip action-icon"></i></div>
              </template>
            </td>

            <!-- Columna Archivo -->
            <td v-if="isAdminOrTecnologicoOrDireccion">
              <button @click="abrirModalArchivar(fila)" class="btn btn-link"><i class="bi bi-archive-fill"></i></button>
            </td>

            <!-- Columna Historial -->
            <td>
              <button @click="abrirModalHistorial(fila)" class="btn btn-link p-0" title="Ver historial del circuito">
                <i class="bi bi-activity" style="font-size:1.1rem; color:#6c757d;"></i>
              </button>
            </td>
            
          </tr>
        </tbody>
      </table>
      </div>
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
              <div class="ds-field">
                <span class="ds-label">Email factura</span>
                <span class="ds-val">{{ emailFacturaDataServicio || '—' }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Email informe técnico</span>
                <span class="ds-val">{{ emailInformeTecnicoDataServicio || '—' }}</span>
              </div>
              <div v-if="conceptosDS.length > 0" class="ds-field ds-field--full">
                <span class="ds-label">Conceptos de Facturación</span>
                <span class="ds-val d-flex flex-wrap gap-1">
                  <span v-for="c in conceptosDS" :key="c.id"
                        class="badge" style="background:#026290; font-size:12px; padding:4px 9px;">
                    {{ c.nombre }}
                  </span>
                </span>
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
                  <button v-if="!editarDS.tieneFacturas" type="button" class="btn-close btn-close-white ms-1" style="font-size:8px;" @click="quitarPresupuestoAdicional(p.nro_presupuesto)"></button>
                </span>
                <div v-if="editarDS.tieneFacturas && editarDS.presupuestos_adicionales.length > 0" class="mt-1 text-muted" style="font-size:11px;">
                  <i class="bi bi-lock-fill"></i> No se pueden quitar presupuestos con facturas ya cargadas.
                </div>
              </div>
              <div v-if="presupuestosDisponibles.length > 0" class="input-group input-group-sm mt-2">
                <select class="form-select" v-model="editarDS.nuevoPres">
                  <option value="">— Seleccioná un presupuesto —</option>
                  <option v-for="p in presupuestosDisponibles" :key="p.nro_presupuesto" :value="p.nro_presupuesto">
                    #{{ p.nro_presupuesto }} — ${{ p.arancel_presupuesto }}
                  </option>
                </select>
                <button class="btn btn-outline-secondary" @click="agregarPresupuestoAdicional" :disabled="!editarDS.nuevoPres">Agregar</button>
              </div>
              <div v-else class="mt-2 text-muted" style="font-size:12px;">
                No hay presupuestos compatibles disponibles (misma empresa y área).
              </div>
            </div>
            <!-- Plazo -->
            <div class="mb-3">
              <label class="form-label fw-bold">Plazo estimado (días)</label>
              <div class="d-flex gap-2 align-items-end">
                <div style="flex:1;">
                  <label class="form-label text-muted mb-1" style="font-size:12px;">Plazo actual</label>
                  <input type="number" class="form-control form-control-sm" :value="editarDS.plazo_original" disabled style="background:#f8f9fa; color:#6c757d;" />
                </div>
                <div style="flex:1;">
                  <label class="form-label text-muted mb-1" style="font-size:12px;">Plazo adicional</label>
                  <input type="number" class="form-control form-control-sm" v-model.number="editarDS.plazo_adicional" min="0" placeholder="0" />
                </div>
                <div class="pb-1 text-muted" style="white-space:nowrap;">= {{ (editarDS.plazo_original || 0) + (editarDS.plazo_adicional || 0) }} días</div>
              </div>
            </div>
            <!-- Cant. Labs -->
            <div class="mb-3">
              <label class="form-label fw-bold">Cantidad de laboratorios</label>
              <div class="d-flex gap-2 align-items-end">
                <div style="flex:1;">
                  <label class="form-label text-muted mb-1" style="font-size:12px;">Labs actuales</label>
                  <input type="number" class="form-control form-control-sm" :value="editarDS.cant_numLabs_original" disabled style="background:#f8f9fa; color:#6c757d;" />
                </div>
                <div style="flex:1;">
                  <label class="form-label text-muted mb-1" style="font-size:12px;">Labs adicionales</label>
                  <input type="number" class="form-control form-control-sm" v-model.number="editarDS.labs_adicionales" min="0" placeholder="0" />
                </div>
                <div class="pb-1 text-muted" style="white-space:nowrap;">= {{ (editarDS.cant_numLabs_original || 0) + (editarDS.labs_adicionales || 0) }}</div>
              </div>
              <div v-if="editarDS.labs_adicionales > 0" class="form-text text-warning mt-1">
                ⚠️ Se agregarán {{ editarDS.labs_adicionales }} lab(s) adicionales — pendientes de aprobación por Administración
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
            <p v-if="aprobarLabs.labs_adicionales_pendientes > 0">
              Se solicitan <strong>{{ aprobarLabs.labs_adicionales_pendientes }}</strong> laboratorio(s) adicional(es).
              <span class="text-muted" style="font-size:12px;">Se calculará el nuevo rango automáticamente.</span>
            </p>
            <p v-if="aprobarLabs.monto_adicional_pendiente" class="text-warning mb-1">
              <i class="bi bi-exclamation-triangle-fill"></i> Se agregó un nuevo presupuesto con monto adicional. Verificar y actualizar la factura.
            </p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cerrarAprobarLabs">Cancelar</button>
            <button class="btn btn-primary" @click="confirmarAprobarLabs">Aprobar y asignar rango</button>
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
                <label class="form-label text-left">N° de Laboratorio{{ nuevoLegajo.rangos_laboratorios && nuevoLegajo.rangos_laboratorios.includes('-') ? 's (rango)' : '' }}:</label>
                <div class="rango-lab-display">
                  <span class="rango-lab-num">{{ nuevoLegajo.rangos_laboratorios ? nuevoLegajo.rangos_laboratorios.split('/')[0] : '—' }}</span>
                  <span class="rango-lab-anio">/ {{ nuevoLegajo.rangos_laboratorios ? nuevoLegajo.rangos_laboratorios.split('/')[1] : '' }}</span>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="crearLegajo">Crear</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCrearLegajo">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalLegajo }" id="modalAbrirLegajo">
      <div class="modal-dialog-a4">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header" style="flex-direction: column; align-items: stretch; gap: 6px;">
            <ISOHeader :config="configFormularioLegajo" :versionDoc="versionLegajo" />
            <div class="d-flex justify-content-end gap-2 no-print">
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
                <span class="lg-label">Números de Laboratorio</span>
                <span class="lg-value">{{ rangosLaboratorios }}</span>
              </div>
            </div>
          </div>
          <!-- Historial de revisiones -->
          <div v-if="configFormularioLegajo.revisiones && configFormularioLegajo.revisiones.length" class="revision-history-wrapper">
            <table class="revision-history-table">
              <thead>
                <tr><th colspan="4" class="revision-title">Historial de Revisiones</th></tr>
                <tr><th>Versión</th><th>Fecha</th><th>Descripción</th><th>Aprobado por</th></tr>
              </thead>
              <tbody>
                <tr v-for="rev in configFormularioLegajo.revisiones" :key="rev.version">
                  <td class="text-center">{{ rev.version }}</td>
                  <td class="text-center">{{ rev.fecha }}</td>
                  <td>{{ rev.descripcion }}</td>
                  <td>{{ rev.aprobado_por }}</td>
                </tr>
              </tbody>
            </table>
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
              <label class="form-check-label">0%</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="100" name="tipoPagoLegajo">
              <label class="form-check-label">100%</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="no_arancelado" name="tipoPagoLegajo">
              <label class="form-check-label">No arancelado</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" v-model="pagoLegajoNuevo" value="pago_diferido" name="tipoPagoLegajo">
              <label class="form-check-label">Pago diferido <small class="text-muted">(el director no puede firmar hasta que se regularice)</small></label>
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
            <h4 class="modal-title">Remito/s</h4>
            <button type="button" class="btn-close" @click="cerrarModalRemito"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <div class="form-group">
              <label for="nrosRemitos">Número/s de remito/s asociado/s:</label>
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
          <div class="modal-header" :style="osReadOnly ? 'flex-direction: column; align-items: stretch; gap: 6px;' : ''">
            <ISOHeader v-if="osReadOnly" :config="configFormularioOS" :versionDoc="versionOS" />
            <div class="d-flex align-items-center gap-2" :class="osReadOnly ? 'justify-content-between' : ''">
              <h1 class="modal-title fs-5 fw-bold">{{ osReadOnly ? 'Orden de Servicio N°' + nroOS : 'Crear Orden de Servicio' }}</h1>
              <div class="d-flex gap-2 no-print">
                <button v-if="osReadOnly" type="button" class="btn btn-sm btn-outline-secondary" @click="imprimirOS" title="Imprimir / Guardar como PDF">
                  <i class="bi bi-printer"></i>
                </button>
                <button v-if="!osModificadaActual" type="button" class="btn-close" @click="cerrarModalCrearOrdenServicio"></button>
              </div>
            </div>
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
                <label class="form-label">Números de Laboratorio:</label>
                <input v-model="rangosOS" type="text" readonly class="form-control" required />
                <div v-if="osModificadaActual && nuevoRangoOS" class="mt-1">
                  <span style="background:#fff3cd; border:1px solid #ffc107; padding:2px 10px; border-radius:4px; font-size:13px; font-weight:600;">
                    Nuevo: {{ nuevoRangoOS }}
                  </span>
                </div>
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
                    <tr v-for="(servicio, index) in servicioOS" :key="index"
                        :style="servicio.es_adicional ? 'background:#fff3cd; font-weight:600;' : ''">
                      <td style="text-align:left;">
                        {{ servicio.servicio }}
                        <span v-if="servicio.es_adicional" style="font-size:10px; background:#ffc107; color:#000; padding:1px 5px; border-radius:4px; margin-left:4px;">Nuevo</span>
                      </td>
                      <td>{{ servicio.cant }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="mb-3">
                <label class="form-label">Muestras:</label>
                <input v-model="muestrasOS" type="text" readonly class="form-control" required />
              </div>

              <!-- Configuración de parciales — solo ST -->
              <div v-if="isServiciosTecnologicos" class="mb-3 mt-2">
                <hr class="my-3">
                <label class="form-label fw-semibold mb-2">
                  Parciales <span class="text-muted" style="font-size:0.8rem">· <em>opcional</em></span>
                </label>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <label class="form-label mb-0" style="white-space:nowrap; min-width:130px; font-size:0.9rem;">Máx. parciales:</label>
                  <input v-model.number="osMaxParciales" type="number" min="1" max="20"
                         class="form-control form-control-sm" style="width:75px;"
                         @input="sincronizarPlazosOS" />
                </div>
                <div v-if="osMaxParciales > 0">
                  <div v-for="n in osMaxParciales" :key="n" class="d-flex align-items-center gap-2 mb-1">
                    <label class="form-label mb-0" style="font-size:0.85rem; white-space:nowrap; min-width:130px;">
                      Plazo parcial {{ n }} (días):
                    </label>
                    <input v-model.number="osPlazosArr[n-1]" type="number" min="1"
                           class="form-control form-control-sm" style="width:75px;" />
                  </div>
                </div>
                <!-- Guardar config (solo modo lectura / OS ya creada) -->
                <div v-if="osReadOnly" class="mt-2">
                  <button type="button" class="btn btn-sm btn-outline-primary no-print" @click="guardarConfigParciales">
                    <i class="bi bi-save me-1"></i>Guardar
                  </button>
                </div>
              </div>
            </form>
          </div>
          <!-- Historial de revisiones (solo en modo lectura) -->
          <div v-if="osReadOnly && configFormularioOS.revisiones && configFormularioOS.revisiones.length" class="revision-history-wrapper">
            <table class="revision-history-table">
              <thead>
                <tr><th colspan="4" class="revision-title">Historial de Revisiones</th></tr>
                <tr><th>Versión</th><th>Fecha</th><th>Descripción</th><th>Aprobado por</th></tr>
              </thead>
              <tbody>
                <tr v-for="rev in configFormularioOS.revisiones" :key="rev.version">
                  <td class="text-center">{{ rev.version }}</td>
                  <td class="text-center">{{ rev.fecha }}</td>
                  <td>{{ rev.descripcion }}</td>
                  <td>{{ rev.aprobado_por }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="osReadOnly" class="modal-footer-a4 no-print">
            <div style="flex:1"></div>
            <button v-if="osModificadaActual" type="button" class="btn btn-primary" @click="aceptarOrdenServicio">Aceptar cambios</button>
            <button v-if="!osModificadaActual" type="button" class="btn btn-secondary" @click="cerrarModalCrearOrdenServicio">Cerrar</button>
          </div>
          <div v-else class="modal-footer">
            <button type="button" class="btn btn-primary" @click="crearOrdenServicio">Confirmar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCrearOrdenServicio">Cancelar</button>
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
                <label for="rangosOS" class="form-label text-left">Números de Laboratorio:</label>
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
          <div class="modal-footer flex-column gap-2 align-items-stretch">
            <template v-if="esCambioTipo">
              <button type="button" class="btn btn-outline-primary w-100 text-start px-3" @click="confirmarCambioTipo('parcial')">
                <i class="bi bi-file-earmark-text me-2"></i>Parcial
              </button>
              <button type="button" class="btn btn-outline-secondary w-100 text-start px-3"
                      :disabled="(!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) || filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario')"
                      :title="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') ? 'No permitido: hay una inter-área complementaria en este circuito' : (!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) ? 'Requiere al menos un informe o inter-área parcial previo' : ''"
                      @click="(hayParcialesPrevios || filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') && confirmarCambioTipo('complementario')">
                <i class="bi bi-layers me-2"></i>Complementario
              </button>
              <button v-if="!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')" type="button" class="btn btn-outline-dark w-100 text-start px-3"
                      :disabled="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario')"
                      :title="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') ? 'No permitido: hay una inter-área complementaria en este circuito' : ''"
                      @click="!filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') && confirmarCambioTipo('final')">
                <i class="bi bi-check2-all me-2"></i>Final
              </button>
            </template>
            <template v-else>
              <button type="button" class="btn btn-outline-primary w-100 text-start px-3" @click="subirInformeAreaCiclo('parcial')">
                <i class="bi bi-file-earmark-text me-2"></i>Parcial
              </button>
              <button type="button" class="btn btn-outline-secondary w-100 text-start px-3"
                      :disabled="(!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) || filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario')"
                      :title="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') ? 'No permitido: hay una inter-área complementaria en este circuito' : (!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) ? 'Requiere al menos un informe o inter-área parcial previo' : ''"
                      @click="(hayParcialesPrevios || filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')) && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') && subirInformeAreaCiclo('complementario')">
                <i class="bi bi-layers me-2"></i>Complementario
              </button>
              <button v-if="!hayParcialesPrevios && !filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'parcial')" type="button" class="btn btn-outline-dark w-100 text-start px-3"
                      :disabled="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario')"
                      :title="filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') ? 'No permitido: hay una inter-área complementaria en este circuito' : ''"
                      @click="!filaModalTipoCiclo?.solicitudes_interarea?.some(ia => ia.tipo === 'complementario') && subirInformeAreaCiclo('final')">
                <i class="bi bi-check2-all me-2"></i>Final
              </button>
            </template>
            <hr class="my-1">
            <button type="button" class="btn btn-secondary w-100" @click="cerrarModalTipoCiclo">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Tipo IA -->
    <div class="modal" :class="{ 'show': mostrarModalTipoIA }" id="mostrarModalTipoIA">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Cambiar tipo de inter-área</h4>
            <button type="button" class="btn-close" @click="cerrarModalTipoIA"></button>
          </div>
          <div class="modal-body">
            <p>¿A qué tipo desea cambiar el inter-área?</p>
            <small class="text-muted">
              <strong>Parcial:</strong> hay más informes pendientes.<br>
              <strong>Resultado:</strong> el inter-área entrega resultados directamente.<br>
              <strong>Complementario:</strong> complementa al área principal; no habilita nuevas IAs ni ciclos.
            </small>
          </div>
          <div class="modal-footer flex-column gap-2 align-items-stretch">
            <button type="button" class="btn btn-outline-primary w-100 text-start px-3" @click="confirmarCambioTipoIA('parcial')">
              <i class="bi bi-file-earmark-text me-2"></i>Parcial
            </button>
            <button type="button" class="btn btn-outline-success w-100 text-start px-3" @click="confirmarCambioTipoIA('resultado')">
              <i class="bi bi-clipboard-check me-2"></i>Resultado
            </button>
            <button type="button" class="btn btn-outline-secondary w-100 text-start px-3"
                    :disabled="filaModalTipoIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo))"
                    :title="filaModalTipoIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo)) ? 'No permitido: el informe de área ya tiene un cierre (final o complementario)' : ''"
                    @click="!filaModalTipoIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo)) && confirmarCambioTipoIA('complementario')">
              <i class="bi bi-layers me-2"></i>Complementario
            </button>
            <hr class="my-1">
            <button type="button" class="btn btn-secondary w-100" @click="cerrarModalTipoIA">Cancelar</button>
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
            <form @submit.prevent>
              <!-- Selector principal: tipo de inter-área -->
              <div class="mb-4">
                <label class="form-label fw-bold fs-6">Tipo de inter-área</label>
                <div class="d-flex gap-3">
                  <button type="button"
                    class="btn flex-fill py-3 ia-tipo-btn"
                    :class="nuevaSolicitudInterarea.tipo === 'parcial' ? 'btn-primary' : 'btn-outline-primary'"
                    @click="nuevaSolicitudInterarea.tipo = 'parcial'; nuevaSolicitudInterarea.genera_informe_parcial = true; erroresIA.tipo = null">
                    <i class="bi bi-file-earmark-text d-block mb-1" style="font-size:1.5rem"></i>
                    <strong>Parcial</strong>
                    <small class="d-block text-muted" style="font-size:0.72rem">El inter-área produce su propio informe que pasa por administración, ST, firma y dirección</small>
                  </button>
                  <button type="button"
                    class="btn flex-fill py-3 ia-tipo-btn"
                    :class="nuevaSolicitudInterarea.tipo === 'resultado' ? 'btn-secondary' : 'btn-outline-secondary'"
                    @click="nuevaSolicitudInterarea.tipo = 'resultado'; nuevaSolicitudInterarea.genera_informe_parcial = false; erroresIA.tipo = null">
                    <i class="bi bi-clipboard-check d-block mb-1" style="font-size:1.5rem"></i>
                    <strong>Resultado</strong>
                    <small class="d-block text-muted" style="font-size:0.72rem">El inter-área entrega resultados directamente al área principal sin informe propio</small>
                  </button>
                  <button type="button"
                    class="btn flex-fill py-3 ia-tipo-btn"
                    :class="nuevaSolicitudInterarea.tipo === 'complementario' ? '' : 'btn-outline-secondary'"
                    :style="nuevaSolicitudInterarea.tipo === 'complementario' ? 'background:#8e44ad; color:#fff; border-color:#8e44ad;' : ''"
                    :disabled="filaParaCrearIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo))"
                    :title="filaParaCrearIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo)) ? 'No permitido: el informe de área ya tiene un cierre (final o complementario)' : ''"
                    @click="!filaParaCrearIA?.ciclos?.some(c => ['final','complementario'].includes(c.tipo)) && (nuevaSolicitudInterarea.tipo = 'complementario', nuevaSolicitudInterarea.genera_informe_parcial = false, erroresIA.tipo = null)">
                    <i class="bi bi-layers d-block mb-1" style="font-size:1.5rem"></i>
                    <strong>Complementario</strong>
                    <small class="d-block text-muted" style="font-size:0.72rem">Informe complementario; no habilita nuevo parcial ni nueva inter-área</small>
                  </button>
                </div>
                <div v-if="erroresIA.tipo" class="ia-error-msg">{{ erroresIA.tipo }}</div>
              </div>

              <hr class="my-3">

              <!-- Todos los campos debajo se deshabilitan hasta que se elija un tipo -->
              <fieldset :disabled="!nuevaSolicitudInterarea.tipo" :class="{ 'ia-fieldset-disabled': !nuevaSolicitudInterarea.tipo }">

              <div class="mb-3">
                  <label for="fecha_solicitudInterarea" class="form-label text-left">Fecha:</label>
                  <input v-model="nuevaSolicitudInterarea.fecha_solicitudInterarea" type="date" class="form-control" id="fecha_solicitudInterarea" name="fecha_solicitudInterarea" readonly />
              </div>

              <div class="mb-3">
                <label for="areaTematica_origen" class="form-label text-left">Area Temática:</label>
                <input v-model="nuevaSolicitudInterarea.areaTematica_origen" type="text" class="form-control" id="areaTematica_origen" name="areaTematica_origen" readonly />
              </div>

              <div class="mb-3">
                <label for="inter_areaTematica" class="form-label text-left">Inter Area Temática</label>
                <select v-model="nuevaSolicitudInterarea.inter_areaTematica"
                  class="form-select" :class="{ 'is-invalid': erroresIA.inter_areaTematica }"
                  id="inter_areaTematica" name="inter_areaTematica"
                  @change="erroresIA.inter_areaTematica = null">
                  <option value="">— Seleccionar —</option>
                  <option v-for="(option, key) in inter_areaTematicaOptions" :key="key" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
                <div v-if="erroresIA.inter_areaTematica" class="ia-error-msg">{{ erroresIA.inter_areaTematica }}</div>
              </div>

              <!-- Servicios de la orden de servicio (checkboxes) -->
              <div class="mb-3">
                <label class="form-label fw-semibold" style="font-size:0.85rem">Servicios de la Orden de Servicio</label>
                <div v-if="serviciosDisponibles.servicio_solicitado && serviciosDisponibles.servicio_solicitado.length" class="ia-os-list">
                  <label v-for="sv in serviciosDisponibles.servicio_solicitado" :key="sv.nro_servicio" class="ia-os-item">
                    <input type="checkbox" :checked="isServicioOSSeleccionado(sv)" @change="toggleServicioOS(sv, $event.target.checked); erroresIA.servicios = null">
                    <span class="ia-os-label">
                      <strong>{{ sv.cant }}×</strong> {{ sv.servicio }}
                      <small v-if="sv.norma" class="text-muted"> · {{ sv.norma }}</small>
                    </span>
                  </label>
                </div>
                <p v-else class="text-muted small mb-0">Sin servicios en la OS.</p>
                <div v-if="erroresIA.servicios" class="ia-error-msg">{{ erroresIA.servicios }}</div>
              </div>

              <hr class="my-3">

              <!-- Servicio adicional del catálogo -->
              <div class="mb-3">
                <label class="form-label fw-semibold" style="font-size:0.85rem">
                  Servicio adicional <small class="text-muted fw-normal">(no incluido en la OS) · <em>opcional</em></small>
                </label>
                <input v-model="busquedaArancel" type="text" class="form-control form-control-sm mb-1" placeholder="Buscar en catálogo de servicios...">
                <div v-if="busquedaArancel.trim()" class="ia-arancel-resultados">
                  <div v-for="a in arancelFiltrado" :key="a.nro_servicio" class="ia-arancel-item" @click="seleccionarArancel(a)">
                    {{ a.servicio }}<small v-if="a.norma" class="text-muted"> · {{ a.norma }}</small>
                  </div>
                  <div v-if="arancelFiltrado.length === 0" class="text-muted small p-2">Sin resultados</div>
                </div>
                <div v-if="arancelAdicional" class="d-flex align-items-center gap-2 mt-1 p-2 bg-light rounded">
                  <span class="flex-grow-1 small">{{ arancelAdicional.servicio }}<small v-if="arancelAdicional.norma" class="text-muted"> · {{ arancelAdicional.norma }}</small></span>
                  <input v-model.number="cantidadAdicional" type="number" min="1" class="form-control form-control-sm" style="width:70px" placeholder="Cant.">
                  <button type="button" class="btn btn-sm btn-primary" @click="agregarArancel; erroresIA.servicios = null">Agregar</button>
                  <button type="button" class="btn btn-sm btn-outline-secondary" @click="arancelAdicional = null">✕</button>
                </div>
              </div>

              <!-- Lista unificada de seleccionados -->
              <div class="mb-3" v-if="serviciosSeleccionados.length">
                <label class="form-label fw-semibold" style="font-size:0.85rem">Servicios a solicitar</label>
                <div class="ia-seleccionados-list">
                  <div v-for="(sv, i) in serviciosSeleccionados" :key="i" class="ia-seleccionado-item">
                    <span class="flex-grow-1 small"><strong>{{ sv.cant }}×</strong> {{ sv.servicio }}<small v-if="sv.norma" class="text-muted"> · {{ sv.norma }}</small></span>
                    <button type="button" class="btn btn-sm btn-outline-danger py-0 px-2" @click="quitarServicioSeleccionado(i)">✕</button>
                  </div>
                </div>
              </div>

              <!-- Números de laboratorio picker (solo para Parcial/Complementario) -->
              <div class="mb-3" v-if="nuevaSolicitudInterarea.tipo === 'parcial' || nuevaSolicitudInterarea.tipo === 'complementario'">
                <label class="form-label fw-semibold" style="font-size:0.85rem">
                  Números de Laboratorio <span class="text-danger">*</span>
                </label>
                <div v-if="labsDisponiblesIA.length">
                  <!-- Trigger -->
                  <button type="button"
                    ref="labsPickerTriggerRef"
                    class="lab-cal-trigger"
                    :class="{ 'lab-cal-trigger--open': labsPickerAbierto, 'lab-cal-trigger--error': erroresIA.num_labs }"
                    @click="abrirLabsPicker">
                    <span v-if="!labsSeleccionadosIA.length" class="text-muted">Seleccionar números de laboratorio...</span>
                    <span v-else>{{ labsSeleccionadosIA.map(l => l.numero).join(', ') }} / {{ labsSeleccionadosIA[0]?.anio }}</span>
                    <i class="bi bi-grid-3x3-gap" style="font-size:0.78rem; flex-shrink:0;"></i>
                  </button>
                  <div v-if="erroresIA.num_labs" class="ia-error-msg">{{ erroresIA.num_labs }}</div>
                  <!-- Popup flotante vía Teleport (position: fixed, encima de todo) -->
                  <Teleport to="body">
                    <!-- Overlay transparente para cerrar al hacer click afuera -->
                    <div v-if="labsPickerAbierto" class="lab-cal-overlay" @click="labsPickerAbierto = false"></div>
                    <div v-if="labsPickerAbierto" class="lab-cal-popup" :style="labsPickerStyle">
                      <div class="lab-cal-header">
                        <span class="fw-semibold" style="font-size:0.82rem; color:#026290;">
                          Nros de Lab · {{ labsDisponiblesIA[0]?.anio }}
                          <span class="text-muted fw-normal ms-1" style="font-size:0.75rem;">({{ labsDisponiblesIA.length }})</span>
                        </span>
                        <div class="d-flex gap-2 align-items-center">
                          <button type="button" class="btn btn-link btn-sm py-0 px-1 text-primary" style="font-size:0.75rem" @click.stop="labsDisponiblesIA.forEach(l => l.seleccionado = true); erroresIA.num_labs = null">Todos</button>
                          <button type="button" class="btn btn-link btn-sm py-0 px-1 text-danger" style="font-size:0.75rem" @click.stop="labsDisponiblesIA.forEach(l => l.seleccionado = false)">Limpiar</button>
                          <button type="button" class="lab-cal-close" @click.stop="labsPickerAbierto = false">✕</button>
                        </div>
                      </div>
                      <div class="lab-cal-grid">
                        <span
                          v-for="lab in labsDisponiblesIA"
                          :key="lab.numero + '/' + lab.anio"
                          class="lab-cal-cell"
                          :class="{ 'lab-cal-cell--selected': lab.seleccionado }"
                          @click.stop="lab.seleccionado = !lab.seleccionado; erroresIA.num_labs = null">
                          {{ lab.numero }}
                        </span>
                      </div>
                      <div v-if="labsSeleccionadosIA.length" class="lab-cal-footer">
                        {{ labsSeleccionadosIA.map(l => l.numero).join(', ') }} / {{ labsSeleccionadosIA[0]?.anio }}
                      </div>
                      <div class="lab-cal-confirm">
                        <button type="button" class="btn btn-sm btn-primary w-100" @click.stop="labsPickerAbierto = false">
                          <i class="bi bi-check2 me-1"></i>Aceptar
                        </button>
                      </div>
                    </div>
                  </Teleport>
                </div>
                <p v-else class="text-muted small mb-1">Sin números de laboratorio disponibles para este circuito.</p>
              </div>

              <div class="mb-3">
                <label for="muestras_solicitudIa" class="form-label text-left">Muestras a entregar:</label>
                <input v-model="nuevaSolicitudInterarea.muestras_solicitudIa" type="text"
                  class="form-control" :class="{ 'is-invalid': erroresIA.muestras }"
                  id="muestras_solicitudIa" name="muestras_solicitudIa"
                  @input="erroresIA.muestras = null" />
                <div v-if="erroresIA.muestras" class="ia-error-msg">{{ erroresIA.muestras }}</div>
              </div>

              <div class="mb-3">
                <label for="observaciones_interArea" class="form-label text-left">Observaciones:</label>
                <input v-model="nuevaSolicitudInterarea.observaciones_interArea" type="text" class="form-control" id="observaciones_interArea" name="observaciones_interArea" />
              </div>

              <div class="mb-3">
                <label for="plazo_interArea" class="form-label text-left">
                  Plazo (días) <span class="text-danger">*</span>
                </label>
                <input v-model.number="nuevaSolicitudInterarea.plazo" type="number" min="1"
                       :class="['form-control', erroresIA.plazo ? 'is-invalid' : '']"
                       id="plazo_interArea" style="width:120px;"
                       @input="erroresIA.plazo = null" />
                <div v-if="erroresIA.plazo" class="ia-error-msg">{{ erroresIA.plazo }}</div>
              </div>

              </fieldset>
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

    <!-- Modal Rechazar Inter-Área -->
    <div class="modal" :class="{ 'show': mostrarModalRechazarIA }" id="modalRechazarIA">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Rechazar solicitud inter-área</h5>
            <button type="button" class="btn-close" @click="cerrarModalRechazarIA"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">¿Qué se rechaza?</label>
              <div class="d-flex gap-2 flex-wrap">
                <button type="button"
                  class="btn btn-lg flex-fill ia-tipo-btn"
                  :class="tipoRechazoIA === 'informe' ? 'btn-warning' : 'btn-outline-warning'"
                  @click="tipoRechazoIA = 'informe'">
                  <i class="bi bi-file-earmark-text me-1"></i> Informe
                </button>
                <button type="button"
                  class="btn btn-lg flex-fill ia-tipo-btn"
                  :class="tipoRechazoIA === 'registros_ensayo' ? 'btn-warning' : 'btn-outline-warning'"
                  @click="tipoRechazoIA = 'registros_ensayo'">
                  <i class="bi bi-clipboard-data me-1"></i> Registros de ensayo
                </button>
                <button type="button"
                  class="btn btn-lg flex-fill ia-tipo-btn"
                  :class="tipoRechazoIA === 'ambos' ? 'btn-danger' : 'btn-outline-danger'"
                  @click="tipoRechazoIA = 'ambos'">
                  <i class="bi bi-exclamation-triangle me-1"></i> Ambos
                </button>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Comentario / motivo del rechazo</label>
              <textarea v-model="comentarioRechazoIA" class="form-control" rows="4" placeholder="Describí qué debe corregir el inter-área..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="rechazarInterareaPrincipal" :disabled="!comentarioRechazoIA.trim()">Rechazar</button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRechazarIA">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Comentario de Rechazo IA -->
    <div class="modal" :class="{ 'show': mostrarModalComentarioRechazo }" id="modalComentarioRechazoIA">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Rechazo del área principal</h5>
            <button type="button" class="btn-close" @click="cerrarModalComentarioRechazo"></button>
          </div>
          <div class="modal-body">
            <p class="mb-1"><strong>Tipo:</strong>
              <span v-if="tipoRechazoVer === 'informe'">Informe</span>
              <span v-else-if="tipoRechazoVer === 'registros_ensayo'">Registros de ensayo</span>
              <span v-else-if="tipoRechazoVer === 'ambos'">Informe y Registros de ensayo</span>
            </p>
            <p class="mb-0"><strong>Comentario:</strong></p>
            <p class="mt-1 p-2 bg-light rounded">{{ comentarioRechazoVer || '—' }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalComentarioRechazo">Cerrar</button>
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


    <!-- Modal Registrar Corrección ST -->
    <div class="modal" :class="{ 'show': mostrarModalCorreccionST }" id="modalCorreccionST">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">¿Registrar corrección?</h5>
            <button type="button" class="btn-close" @click="cerrarModalCorreccionST"></button>
          </div>
          <div class="modal-body">
            <textarea v-model="textoCorreccionST" class="form-control" rows="10"></textarea>
          </div>
          <div class="modal-footer flex-wrap gap-1">
            <button type="button" class="btn btn-primary" @click="registrarCorreccionST" :disabled="!textoCorreccionST.trim()">
              Registrar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalCorreccionST">
              No registrar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Correcciones ST -->
    <div class="modal" :class="{ 'show': mostrarModalVerCorrecciones }" id="modalVerCorrecciones">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Correcciones registradas</h5>
            <button type="button" class="btn-close" @click="cerrarModalVerCorrecciones"></button>
          </div>
          <div class="modal-body">
            <div v-if="cicloVerCorrecciones && cicloVerCorrecciones.historial_correcciones && cicloVerCorrecciones.historial_correcciones.length > 0">
              <div v-for="(c, idx) in cicloVerCorrecciones.historial_correcciones" :key="c.id"
                   class="border rounded p-3 mb-2"
                   :style="c.estado === 'confirmada'
                     ? 'background:#f0fff4; opacity:0.7; border-left: 4px solid ' + {st:'#9c7cc7',area:'#ffc107',direccion:'#dc3545'}[c.tipo] + ' !important;'
                     : 'background:#fffdf0; border-left: 4px solid ' + {st:'#9c7cc7',area:'#ffc107',direccion:'#dc3545'}[c.tipo] + ' !important;'">
                <div class="d-flex justify-content-between align-items-start mb-1">
                  <div>
                    <strong style="font-size:12px; color:#888;">Corrección {{ idx + 1 }}</strong>
                    <span style="font-size:11px; color:#6c757d; margin-left:6px;">
                      de <em>{{ { st: 'ST', area: 'Área', direccion: 'Dirección' }[c.tipo] }}</em>
                      → a <em>{{ { administracion: 'Administración', st: 'ST', area: 'Área', direccion: 'Dirección' }[c.destinatario] }}</em>
                    </span>
                    <span v-if="c.estado === 'confirmada'" style="color:#198754; font-size:11px; margin-left:6px;">✓ Confirmada</span>
                  </div>
                  <small class="text-muted">{{ new Date(c.fecha).toLocaleString('es-AR') }}</small>
                </div>
                <p class="mb-0" style="white-space:pre-wrap;">{{ c.descripcion }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary btn-sm" @click="cerrarModalVerCorrecciones">Cerrar</button>
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
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Firma Responsable del Área</h4>
            <button type="button" class="btn-close" @click="cerrarModalFirmaResponsableArea"></button>
          </div>
          <div class="modal-body">
            <template v-if="firmaUsuarioUrl">
              <p class="text-muted small mb-2">Se usará tu firma guardada:</p>
              <div class="text-center">
                <img :src="firmaUsuarioUrl" alt="Firma" style="max-width:100%; max-height:120px; border:1px solid #dee2e6; border-radius:4px; background:#fafafa; padding:8px;">
              </div>
            </template>
            <template v-else>
              <p class="text-muted small mb-2">Dibujá tu firma en el recuadro:</p>
              <div class="firma-canvas-wrapper">
                <canvas
                  ref="signatureCanvas"
                  width="1120" height="300"
                  @mousedown="startSignature"
                  @mousemove="drawSignature"
                  @mouseup="stopSignature"
                  @mouseleave="stopSignature"
                  @touchstart.prevent="startSignatureTouch"
                  @touchmove.prevent="drawSignatureTouch"
                  @touchend="stopSignature">
                </canvas>
              </div>
              <button type="button" class="btn btn-sm btn-outline-secondary mt-2" @click="limpiarFirma">
                <i class="bi bi-arrow-counterclockwise"></i> Limpiar
              </button>
            </template>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="confirmarFirmaResponsableAreaCiclo"
                    :disabled="!firmaUsuarioUrl && !firmaHecha">
              <i class="bi bi-pen"></i> Firmar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalFirmaResponsableArea">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Firma Dirección -->
    <div class="modal" :class="{ 'show': mostrarModalFirmaDireccion }" id="mostrarModalFirmaDireccion">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Firma Dirección</h4>
            <button type="button" class="btn-close" @click="cerrarModalFirmaDireccion"></button>
          </div>
          <div class="modal-body">
            <template v-if="firmaUsuarioUrl">
              <p class="text-muted small mb-2">Se usará tu firma guardada:</p>
              <div class="text-center">
                <img :src="firmaUsuarioUrl" alt="Firma" style="max-width:100%; max-height:120px; border:1px solid #dee2e6; border-radius:4px; background:#fafafa; padding:8px;">
              </div>
            </template>
            <template v-else>
              <p class="text-muted small mb-2">Dibujá tu firma en el recuadro:</p>
              <div class="firma-canvas-wrapper">
                <canvas
                  ref="signatureCanvasDir"
                  width="1120" height="300"
                  @mousedown="startSignatureDir"
                  @mousemove="drawSignatureDir"
                  @mouseup="stopSignatureDir"
                  @mouseleave="stopSignatureDir"
                  @touchstart.prevent="startSignatureDirTouch"
                  @touchmove.prevent="drawSignatureDirTouch"
                  @touchend="stopSignatureDir">
                </canvas>
              </div>
              <button type="button" class="btn btn-sm btn-outline-secondary mt-2" @click="limpiarFirmaDir">
                <i class="bi bi-arrow-counterclockwise"></i> Limpiar
              </button>
            </template>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="confirmarFirmaDireccionCiclo"
                    :disabled="!firmaUsuarioUrl && !firmaHechaDir">
              <i class="bi bi-pen"></i> Firmar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalFirmaDireccion">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Rechazo Responsable Área -->
    <div class="modal" :class="{ 'show': mostrarModalRechazoArea }" id="mostrarModalRechazoArea">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#ffc107;">
            <h5 class="modal-title" style="color:#b8860b;">Rechazar Informe — Responsable Área</h5>
            <button type="button" class="btn-close" @click="cerrarModalRechazoArea"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted small mb-3">
              El informe volverá al paso seleccionado. Si elegís <strong>Área</strong>, el informe de Administración/ST se conserva y podrás volver a firmarlo o rechazarlo nuevamente.
            </p>
            <div class="mb-3">
              <label class="form-label fw-semibold">Enviar de vuelta a:</label>
              <div class="d-flex gap-3">
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoAreaDestino" value="st"> &nbsp;Servicios Tecnológicos
                </label>
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoAreaDestino" value="administracion"> &nbsp;Administración
                </label>
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoAreaDestino" value="area"> &nbsp;Área
                </label>
              </div>
            </div>
            <div class="mb-2">
              <label class="form-label fw-semibold">Nota de corrección:</label>
              <textarea v-model="rechazoAreaNota" class="form-control" rows="4"
                        placeholder="Describí los cambios necesarios..." style="border-color:#ffc107;"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="confirmarRechazoArea"
                    :disabled="!rechazoAreaDestino || !rechazoAreaNota.trim()">
              <i class="bi bi-x-circle"></i> Rechazar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRechazoArea">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Rechazo Firma AP -->
    <div class="modal" :class="{ 'show': mostrarModalRechazoAPIA }" id="mostrarModalRechazoAPIA">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#ffc107;">
            <h5 class="modal-title" style="color:#b8860b;">Rechazar Firma — Área Principal</h5>
            <button type="button" class="btn-close" @click="cerrarModalRechazoAPIA"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted small mb-3">
              La firma del área principal será removida. Si elegís <strong>Área</strong>, también se borra la firma del jefe inter-área y deberá volver a firmar.
            </p>
            <div class="mb-3">
              <label class="form-label fw-semibold">Enviar de vuelta a:</label>
              <div class="d-flex gap-3">
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoAPIADestino" value="area"> &nbsp;Jefe Inter-Área
                </label>
              </div>
            </div>
            <div class="mb-2">
              <label class="form-label fw-semibold">Nota de corrección (opcional):</label>
              <textarea v-model="rechazoAPIANota" class="form-control" rows="3"
                        placeholder="Describí los cambios necesarios..." style="border-color:#ffc107;"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="confirmarRechazoAPIA">
              <i class="bi bi-x-circle"></i> Rechazar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRechazoAPIA">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Datos de Facturación -->
    <div class="modal" :class="{ 'show': mostrarModalFacturacion }" id="mostrarModalFacturacion">
      <div class="modal-dialog modal-dialog-md">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#198754;">
            <h5 class="modal-title" style="color:#198754;">Datos de Facturación</h5>
            <button type="button" class="btn-close" @click="mostrarModalFacturacion = false"></button>
          </div>
          <div class="modal-body">
            <h6 class="text-muted fw-bold mb-2">Empresa</h6>
            <div class="ds-grid mb-3">
              <div class="ds-field">
                <span class="ds-label">ID Solicitante</span>
                <span class="ds-val">#{{ datosFacturacion.empresa?.nro_solicitante }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Nombre</span>
                <span class="ds-val">{{ datosFacturacion.empresa?.nombre }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">CUIT</span>
                <span class="ds-val">{{ datosFacturacion.empresa?.cuit }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Dirección</span>
                <span class="ds-val">{{ datosFacturacion.empresa?.direccion }}, {{ datosFacturacion.empresa?.localidad }}, {{ datosFacturacion.empresa?.provincia }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Teléfono</span>
                <span class="ds-val">{{ datosFacturacion.empresa?.telefono }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Email empresa</span>
                <span class="ds-val">{{ datosFacturacion.empresa?.email || '—' }}</span>
              </div>
            </div>
            <h6 class="text-muted fw-bold mb-2">Contactos del servicio</h6>
            <div class="ds-grid mb-3">
              <div class="ds-field">
                <span class="ds-label">N° Presupuesto</span>
                <span class="ds-val fw-bold">#{{ datosFacturacion.nro_presupuesto }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Email factura</span>
                <span class="ds-val">{{ datosFacturacion.email_factura || '—' }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Email informe técnico</span>
                <span class="ds-val">{{ datosFacturacion.email_informe_tecnico || '—' }}</span>
              </div>
            </div>
            <hr>
            <div class="ds-grid mb-3">
              <div class="ds-field">
                <span class="ds-label">Total Data Servicio</span>
                <span class="ds-val fw-bold">{{ formatArancel(datosFacturacion.total_dataservicio) }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Total facturado</span>
                <span class="ds-val fw-bold" style="color:#198754;">{{ formatArancel(datosFacturacion.total_facturado) }}</span>
              </div>
              <div class="ds-field">
                <span class="ds-label">Pendiente</span>
                <span class="ds-val fw-bold" :style="parseFloat(datosFacturacion.pendiente) > 0 ? 'color:#dc3545;' : 'color:#198754;'">
                  {{ formatArancel(datosFacturacion.pendiente) }}
                </span>
              </div>
            </div>
            <div v-if="datosFacturacion.conceptos_facturacion && datosFacturacion.conceptos_facturacion.length > 0" class="mb-3">
              <h6 class="text-muted fw-bold mb-2">Conceptos de Facturación</h6>
              <div class="d-flex flex-wrap gap-1">
                <span v-for="c in datosFacturacion.conceptos_facturacion" :key="c.id"
                      class="badge" style="background:#026290; font-size:12px; padding:5px 10px;">
                  {{ c.nombre }}
                </span>
              </div>
            </div>
            <hr v-if="datosFacturacion.conceptos_facturacion && datosFacturacion.conceptos_facturacion.length > 0">
            <h6 class="text-muted fw-bold mb-2">Facturas cargadas</h6>
            <div v-if="!datosFacturacion.facturas || datosFacturacion.facturas.length === 0"
                 class="text-muted" style="font-size:13px; margin-bottom:8px;">
              Sin facturas cargadas.
            </div>
            <table v-else class="table table-sm table-bordered" style="font-size:13px;">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Monto</th>
                  <th>Archivo</th>
                  <th v-if="isAdministracion"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in datosFacturacion.facturas" :key="f.id">
                  <td>{{ f.fecha }}</td>
                  <td>{{ f.monto ? formatArancel(f.monto) : '—' }}</td>
                  <td>
                    <i class="bi bi-file-earmark" style="cursor:pointer; font-size:18px;"
                       @click="abrirArchivo(f.archivo)" title="Ver factura"></i>
                  </td>
                  <td v-if="isAdministracion">
                    <i class="bi bi-trash" style="cursor:pointer; color:#dc3545; font-size:16px;"
                       @click="eliminarFacturaDeModal(f.id)" title="Eliminar"></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button v-if="isAdministracion" type="button" class="btn btn-primary"
                    @click="mostrarModalFacturacion = false; abrirSubirFactura(filaFacturacion)">
              <i class="bi bi-upload" style="font-size:14px;"></i> Cargar factura
            </button>
            <button type="button" class="btn btn-secondary" @click="mostrarModalFacturacion = false">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Subir Factura -->
    <div class="modal" :class="{ 'show': mostrarModalSubirFactura }" id="mostrarModalSubirFactura">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Cargar Factura</h5>
            <button type="button" class="btn-close" @click="mostrarModalSubirFactura = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Monto</label>
              <select v-model="subirFacturaModoMonto" class="form-select mb-2">
                <option value="pendiente">Total pendiente — $ {{ formatMontoARS(subirFacturaData.montoPendiente) }}</option>
                <option value="otro">Otro monto</option>
              </select>
              <input v-if="subirFacturaModoMonto === 'otro'"
                     :value="subirFacturaMontoManual"
                     @input="onMontoManualInput"
                     type="text" inputmode="numeric" class="form-control"
                     placeholder="Ej: 125000">
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Archivo</label>
              <input type="file" class="form-control" ref="inputSubirFactura"
                     @change="subirFacturaData.archivo = $event.target.files[0]">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary"
                    :disabled="!subirFacturaData.archivo"
                    @click="confirmarSubirFactura">Guardar</button>
            <button type="button" class="btn btn-secondary" @click="mostrarModalSubirFactura = false">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Nota Rechazo Área -->
    <div class="modal" :class="{ 'show': mostrarModalVerRechazoArea }" id="mostrarModalVerRechazoArea">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#ffc107;">
            <h5 class="modal-title" style="color:#b8860b;">Nota de Rechazo — Responsable Área</h5>
            <button type="button" class="btn-close" @click="mostrarModalVerRechazoArea = false"></button>
          </div>
          <div class="modal-body">
            <p style="white-space:pre-line;">{{ cicloVerRechazoArea?.nota_rechazo_area }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="mostrarModalVerRechazoArea = false">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Rechazo ST -->
    <div class="modal" :class="{ 'show': mostrarModalRechazoST }" id="mostrarModalRechazoST">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#9c7cc7;">
            <h5 class="modal-title" style="color:#9c7cc7;">Rechazar Informe — Servicios Tecnológicos</h5>
            <button type="button" class="btn-close" @click="cerrarModalRechazoST"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted small mb-3">
              El informe volverá al paso seleccionado para su corrección.
            </p>
            <div class="mb-3">
              <label class="form-label fw-semibold">Enviar de vuelta a:</label>
              <div class="d-flex gap-3">
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoSTDestino" value="administracion"> &nbsp;Administración
                </label>
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoSTDestino" value="area"> &nbsp;Área
                </label>
              </div>
            </div>
            <div class="mb-2">
              <label class="form-label fw-semibold">Nota de corrección:</label>
              <textarea v-model="rechazoSTNota" class="form-control" rows="4"
                        placeholder="Describí los cambios necesarios..." style="border-color:#9c7cc7;"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger"
                    @click="confirmarRechazoST"
                    :disabled="!rechazoSTDestino || !rechazoSTNota.trim()">
              <i class="bi bi-x-circle"></i> Rechazar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRechazoST">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Nota Rechazo ST -->
    <div class="modal" :class="{ 'show': mostrarModalVerRechazoST }" id="mostrarModalVerRechazoST">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#9c7cc7;">
            <h5 class="modal-title" style="color:#9c7cc7;">Nota de Rechazo — Servicios Tecnológicos</h5>
            <button type="button" class="btn-close" @click="mostrarModalVerRechazoST = false"></button>
          </div>
          <div class="modal-body">
            <p style="white-space:pre-line;">{{ cicloVerRechazoST?.nota_rechazo_st }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="mostrarModalVerRechazoST = false">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Rechazo Dirección -->
    <div class="modal" :class="{ 'show': mostrarModalRechazoDireccion }" id="mostrarModalRechazoDireccion">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" style="color:#dc3545;">Rechazar Informe</h5>
            <button type="button" class="btn-close" @click="cerrarModalRechazoDireccion"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted small mb-3">El informe volverá al paso seleccionado para su corrección.</p>
            <div class="mb-3">
              <label class="form-label fw-semibold">Enviar de vuelta a:</label>
              <div class="d-flex gap-3">
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoDireccionDestino" value="st"> &nbsp;Servicios Tecnológicos
                </label>
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoDireccionDestino" value="administracion"> &nbsp;Administración
                </label>
                <label style="cursor:pointer;">
                  <input type="radio" v-model="rechazoDireccionDestino" value="area"> &nbsp;Área
                </label>
              </div>
            </div>
            <div class="mb-2">
              <label class="form-label fw-semibold">Nota de corrección:</label>
              <textarea v-model="rechazoDireccionNota" class="form-control" rows="4"
                        placeholder="Describí los cambios necesarios..." style="border-color:#dc3545;"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="confirmarRechazoDireccion"
                    :disabled="!rechazoDireccionDestino || !rechazoDireccionNota.trim()">
              <i class="bi bi-x-circle"></i> Rechazar
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarModalRechazoDireccion">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Nota Rechazo Dirección -->
    <div class="modal" :class="{ 'show': mostrarModalVerRechazo }" id="mostrarModalVerRechazo">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="border-bottom-color:#dc3545;">
            <h5 class="modal-title" style="color:#dc3545;">Nota de Rechazo — Dirección</h5>
            <button type="button" class="btn-close" @click="mostrarModalVerRechazo = false"></button>
          </div>
          <div class="modal-body">
            <p style="white-space:pre-line;">{{ cicloVerRechazo?.nota_rechazo_direccion }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="mostrarModalVerRechazo = false">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modales Archivo -->
    <!-- Modal Historial del circuito -->
    <div class="modal" :class="{ 'show': mostrarModalHistorial }" id="modalHistorial">
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-activity me-2"></i>Historial — Circuito #{{ historialCircuitoId }}
            </h5>
            <button type="button" class="btn-close" @click="cerrarModalHistorial"></button>
          </div>
          <div class="modal-body p-0">
            <div v-if="historialCargando" class="text-center py-4 text-muted">
              <div class="spinner-border spinner-border-sm me-2"></div>Cargando...
            </div>
            <div v-else-if="!historialEventos.length" class="text-center py-4 text-muted">
              Sin eventos registrados para este circuito.
            </div>
            <ul v-else class="historial-timeline list-unstyled mb-0 px-3 py-3">
              <li v-for="ev in historialEventos" :key="ev.id" class="historial-item">
                <div class="historial-dot"></div>
                <div class="historial-contenido">
                  <div class="historial-accion">{{ labelAccion(ev.accion) }}</div>
                  <div v-if="ev.descripcion" class="historial-desc text-muted small">{{ ev.descripcion }}</div>
                  <div class="historial-meta small text-muted mt-1">
                    <i class="bi bi-person me-1"></i>{{ ev.usuario_nombre }}
                    <span class="ms-2"><i class="bi bi-calendar3 me-1"></i>{{ formatHistorialFecha(ev.fecha) }}</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalHistorial">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'show': mostrarModalArchivar }" id="mostrarModalArchivar">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title"><i class="bi bi-archive-fill me-2"></i>Archivar circuito #{{ numeroCircuitoGlobal }}</h4>
            <button type="button" class="btn-close" @click="cerrarModalArchivar"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted mb-3">Seleccioná el motivo de archivo:</p>
            <div class="d-flex flex-column gap-2">
              <label v-for="opt in motivosArchivo" :key="opt.value" class="motivo-archivo-option" :class="{ selected: motivoArchivar === opt.value }">
                <input type="radio" :value="opt.value" v-model="motivoArchivar" class="me-2" />
                <span>{{ opt.label }}</span>
              </label>
            </div>
            <div v-if="motivoArchivar === 'otro'" class="mt-3">
              <label class="form-label text-muted small">Descripción <span class="text-danger">*</span></label>
              <textarea v-model="notaArchivar" class="form-control" rows="3" maxlength="500" placeholder="Describí el motivo..."></textarea>
            </div>
            <div v-else-if="motivoArchivar" class="mt-3">
              <label class="form-label text-muted small">Nota adicional (opcional)</label>
              <textarea v-model="notaArchivar" class="form-control" rows="2" maxlength="500" placeholder="Observaciones adicionales..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalArchivar">Cancelar</button>
            <button
              type="button"
              class="btn btn-danger"
              @click="enviarArchivar"
              :disabled="!motivoArchivar || (motivoArchivar === 'otro' && !notaArchivar.trim())"
            >
              <i class="bi bi-archive me-1"></i>Archivar
            </button>
          </div>
        </div>
      </div>
    </div>

   
    
</template>
  
<script>
  import { onMounted, onUnmounted, ref, computed, nextTick } from 'vue';
  import api from '@/api.js';
  import { AREAS_TEMATICAS } from '@/constants/areas.js';
  import AttachmentCell from './AttachmentCell.vue';
  import ISOHeader from '@/components/ISOHeader.vue';

  export default {
    components: { AttachmentCell, ISOHeader },
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
        if (restantes <= 5) return 'row-alerta';
        return '';
      };

      const plazoCriticidad = (dias) => {
        if (dias === null || dias === undefined || dias === '') return null;
        const d = Number(dias);
        if (isNaN(d)) return null;
        if (d <= 3) return 'plazo-urgente';
        if (d <= 5) return 'plazo-alerta';
        return null;
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
      // SS / Recepcion / OS: visibles solo para ST y Dirección (no administración)
      const isTecnologicoOrDireccion = ref(userRole === 'servicios_tecnologicos' || userRole === 'direccion');
      // Inter Area: visible para ST, Dirección, Área y Administración
      const isTecnologicoOrDireccionOrArea = ref(userRole === 'servicios_tecnologicos' || userRole === 'direccion' || userRole === 'area_jefe' || userRole === 'area_standard' || userRole === 'administracion');

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
      const emailFacturaDataServicio = ref();
      const emailInformeTecnicoDataServicio = ref();
      // Conceptos de Facturación
      const catalogoConceptos = ref([]);
      const conceptosDS = ref([]);
      const nroDataServicioAbierto = ref(null);
      const conceptoSeleccionadoDS = ref('');
      const guardandoConceptosDS = ref(false);
      const mensajeConceptoDS = ref('');
      const conceptosCatalogoDisponibles = computed(() =>
        catalogoConceptos.value.filter(c => !conceptosDS.value.some(x => x.id === c.id))
      );
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
        plazo_original: null,
        plazo_adicional: 0,
        cant_numLabs_original: null,
        labs_adicionales: 0,
        nuevoPres: '',
        presupuestosCompatibles: [],
        totalCalculado: 0,
      });

      const presupuestosDisponibles = computed(() => {
        const yaAgregados = new Set(editarDS.value.presupuestos_adicionales.map(p => p.nro_presupuesto));
        return (editarDS.value.presupuestosCompatibles || []).filter(p => !yaAgregados.has(p.nro_presupuesto));
      });

      const abrirEditarDataServicio = async (fila) => {
        const adicionalesOriginales = (fila.presupuestos_adicionales || []).map(p => p.nro_presupuesto);
        editarDS.value = {
          nro_dataServicio: fila.nro_dataServicio,
          nro_circuito: fila.nro_circuito,
          nro_presupuesto: fila.nro_presupuesto,
          presupuestos_adicionales: [...(fila.presupuestos_adicionales || [])],
          presupuestos_adicionales_originales: adicionalesOriginales,
          plazo_original: fila.plazo_estimado_ds,
          plazo_adicional: 0,
          cant_numLabs_original: fila.cant_numLabs,
          labs_adicionales: 0,
          nuevoPres: '',
          presupuestosCompatibles: [],
          totalCalculado: 0,
          tieneFacturas: !!(fila.adjuntos_factura && fila.adjuntos_factura.length > 0),
        };
        mostrarModalEditarDS.value = true;
        try {
          const res = await api.get(`/encurso/presupuestos_compatibles/${fila.nro_presupuesto}/`);
          editarDS.value.presupuestosCompatibles = res.data.presupuestos || [];
        } catch (e) {
          console.error('Error al cargar presupuestos compatibles:', e);
        }
      };

      const cerrarEditarDataServicio = () => { mostrarModalEditarDS.value = false; };

      const agregarPresupuestoAdicional = () => {
        const nro = editarDS.value.nuevoPres;
        if (!nro) return;
        const pres = editarDS.value.presupuestosCompatibles.find(p => p.nro_presupuesto === nro);
        if (pres && !editarDS.value.presupuestos_adicionales.find(p => p.nro_presupuesto === nro)) {
          editarDS.value.presupuestos_adicionales.push({ nro_presupuesto: nro, arancel_presupuesto: pres.arancel_presupuesto });
        }
        editarDS.value.nuevoPres = '';
      };

      const quitarPresupuestoAdicional = (nro) => {
        editarDS.value.presupuestos_adicionales = editarDS.value.presupuestos_adicionales.filter(p => p.nro_presupuesto !== nro);
      };

      const guardarEdicionDataServicio = async () => {
        // Si el usuario seleccionó un presupuesto del dropdown sin clickear "Agregar", agregarlo ahora
        if (editarDS.value.nuevoPres) {
          agregarPresupuestoAdicional();
        }
        const { nro_dataServicio, plazo_original, plazo_adicional, cant_numLabs_original, labs_adicionales, presupuestos_adicionales, presupuestos_adicionales_originales } = editarDS.value;
        const plazo_estimado = (plazo_original || 0) + (plazo_adicional || 0);
        const cant_numLabs = (cant_numLabs_original || 0) + (labs_adicionales || 0);
        // Solo enviar presupuestos realmente nuevos (no los ya vinculados)
        const originalesSet = new Set(presupuestos_adicionales_originales || []);
        const nuevosPresupuestos = presupuestos_adicionales.filter(p => !originalesSet.has(p.nro_presupuesto));
        try {
          await api.patch(`/encurso/editar_dataservicio/${nro_dataServicio}/`, {
            plazo_estimado,
            cant_numLabs,
          });
          for (const p of nuevosPresupuestos) {
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
          fetchData(); // sincronizar UI aunque haya error parcial
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Aprobar Labs Adicionales
      const mostrarModalAprobarLabs = ref(false);
      const aprobarLabs = ref({ nro_circuito: null, labs_adicionales_pendientes: 0, monto_adicional_pendiente: false });

      const abrirAprobarLabs = (fila) => {
        aprobarLabs.value = {
          nro_circuito: fila.nro_circuito,
          labs_adicionales_pendientes: fila.labs_adicionales_pendientes,
          monto_adicional_pendiente: fila.monto_adicional_pendiente,
        };
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
      const versionLegajo = ref('01');
      const configFormularioLegajo = ref({ nombre: '', codigo: '', version_actual: '', fecha_version_actual: '', revisiones: [] });
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
      const nuevoRangoOS = ref('');
      const plazoOS = ref();
      const solicitanteOS = ref();
      const servicioOS = ref();
      const muestrasOS = ref();
      const observacionesOS = ref();
      const mostrarModalCrearOrdenServicio = ref(false);
      const osReadOnly = ref(false);
      const osModificadaActual = ref(false);
      const osFilaActual = ref(null);
      const osCircuitoActual = ref(null);
      const versionOS = ref('01');
      const configFormularioOS = ref({ nombre: '', codigo: '', version_actual: '', fecha_version_actual: '', revisiones: [] });
      const mostrarModalOrdenServicio = ref(false);
      const mostrarModalPlazoOrdenServicio = ref(false);
      // Setup Ciclos de Informe
      const mostrarModalTipoCiclo = ref(false);
      // Setup Inter Area
      const serviciosDisponibles = ref([]);
      const serviciosSeleccionados = ref([]);
      const catalogoAranceles = ref([]);
      const busquedaArancel = ref('');
      const arancelAdicional = ref(null);
      const cantidadAdicional = ref(1);
      const arancelFiltrado = computed(() => {
        const q = busquedaArancel.value.trim().toLowerCase();
        if (!q) return [];
        return catalogoAranceles.value.filter(a =>
          a.servicio.toLowerCase().includes(q) || (a.norma && a.norma.toLowerCase().includes(q))
        ).slice(0, 8);
      });

      const inter_areaTematicaOptions = computed(() => {
        const todasOpciones = [
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
        ];
        return todasOpciones.filter(o => o.value !== userAreaTematica);
      });
      const nuevaSolicitudInterarea = ref({
        fecha_solicitudInterarea: new Date().toISOString().substring(0, 10),
        areaTematica_origen: '',
        inter_areaTematica: '',
        num_labs: '',
        genera_informe_parcial: null, // null = no seleccionado aún
        servicios_solicitudInterarea: [
          {
            nro_servicio: '',
            servicio: '',
            cant: 0,
          }
        ],
        nro_circuito: null,
      });
      const labsDisponiblesIA = ref([]);
      const labsSeleccionadosIA = computed(() => labsDisponiblesIA.value.filter(l => l.seleccionado));
      const labsPickerAbierto = ref(false);
      const erroresIA = ref({});

      // IAs ya abiertas esta sesión (persiste en sessionStorage)
      const iaVistoIds = ref(new Set(
        JSON.parse(sessionStorage.getItem('ia_vistas') || '[]')
      ));
      const marcarIAVista = (iaId) => {
        iaVistoIds.value.add(iaId);
        sessionStorage.setItem('ia_vistas', JSON.stringify([...iaVistoIds.value]));
      };
      const iaDebeParpadear = (ia) => {
        if (iaVistoIds.value.has(ia.id)) return false;
        // Inter-área: recibieron una solicitud de trabajo pendiente
        if (esInterAreaDeIA(ia)) return true;
        // Área principal: solo cuando la inter-área sometió algo que requiere su revisión
        // (NO cuando acaban de crear la solicitud — eso no es un evento entrante)
        if (esPrincipalDeIA(ia)) {
          const ciclo = ultimoCicloIA(ia);
          if (ia.estado_correc_informe === 'subido') return true;
          if (ciclo && ciclo.adjunto_informeArea && ciclo.registros_ensayo && ciclo.registros_ensayo.length) return true;
        }
        return false;
      };
      const labsPickerTriggerRef = ref(null);
      const labsPickerStyle = ref({});

      const abrirLabsPicker = () => {
        if (!labsPickerAbierto.value) {
          const rect = labsPickerTriggerRef.value?.getBoundingClientRect();
          if (rect) {
            const popupWidth = 280;
            const spaceBelow = window.innerHeight - rect.bottom - 8;
            const popupMaxHeight = Math.min(320, spaceBelow > 180 ? spaceBelow : window.innerHeight * 0.5);
            const top = spaceBelow > 180 ? rect.bottom + 4 : rect.top - popupMaxHeight - 4;
            const left = Math.min(rect.left, window.innerWidth - popupWidth - 8);
            labsPickerStyle.value = {
              position: 'fixed',
              top: top + 'px',
              left: left + 'px',
              width: popupWidth + 'px',
              maxHeight: popupMaxHeight + 'px',
              zIndex: 9000,
            };
          }
        }
        labsPickerAbierto.value = !labsPickerAbierto.value;
      };
      const nroSolicitudInterArea = ref();
      const fechaSolicitudInterArea = ref();
      const areaTematicaOrigen = ref();
      const interAreaSolicitudInterArea = ref();
      const muestrasSolicitudInterArea = ref();
      const numLabsSolicitudInterArea = ref();
      const observacionesSolicitudInterArea = ref();
      const servicioSolicitudInterArea = ref();
      
      const mostrarModalCrearSolicitudInterArea = ref(null);
      // mostrarModalSolicitudInterArea se declara más abajo junto a la función abrirSolicitudInterArea

      // Setup Formato Administracion
      const mostrarModalPDFpreliminar = ref(false);
      const urlPdf = ref('');
      const mostrarModalCorreccionesInformeServicio = ref(false);
      const correcciones = ref(null);

      // Setup Servicios Tecnologicos - Revision
      const popupSTId = ref(null);
      const popupAreaId = ref(null);
      const stReemplazadoIds = ref(new Set());
      const popupDirId = ref(null);
      const popupPDFAdminId = ref(null);
      const popupFormatoId = ref(null);
      const popupFacturaId = ref(null);
      const mostrarModalFacturacion = ref(false);
      const datosFacturacion = ref({});
      const filaFacturacion = ref(null);
      const mostrarModalSubirFactura = ref(false);
      const subirFacturaData = ref({ archivo: null, monto: null, nroLegajo: null, nroCircuito: null, montoPendiente: null });
      const subirFacturaModoMonto = ref('pendiente');
      const subirFacturaMontoManual = ref('');
      const mostrarModalCorreccionST = ref(false);
      const textoCorreccionST = ref('');
      const cicloParaCorreccionST = ref(null);
      const mostrarOpciones = ref(false);
      const mostrarModalVerCorrecciones = ref(false);
      const cicloVerCorrecciones = ref(null);
      const filaSeleccionada = ref(null);

      // Firma guardada del usuario
      const firmaUsuarioUrl = ref(null);
      const cargarFirmaUsuario = async () => {
        try {
          const res = await api.get('/auth/firma_usuario/');
          firmaUsuarioUrl.value = res.data.firma_url || null;
        } catch (e) { /* silenciar error de red */ }
      };

      // Setup Responsable del Area - Firma
      const mostrarModalAdvertirCorrecciones = ref(false);
      const correccionesNuevas = ref('');
      const mostrarModalFirmaResponsableArea = ref(false);
      const signatureCanvas = ref(null);
      const firmaHecha = ref(false);
      let _sigDrawing = false, _sigLastX = 0, _sigLastY = 0;

      const _sigGetPos = (clientX, clientY) => {
        const c = signatureCanvas.value;
        const r = c.getBoundingClientRect();
        return { x: (clientX - r.left) * c.width / r.width, y: (clientY - r.top) * c.height / r.height };
      };
      const _sigStroke = (x, y) => {
        const ctx = signatureCanvas.value.getContext('2d');
        ctx.beginPath(); ctx.moveTo(_sigLastX, _sigLastY); ctx.lineTo(x, y);
        ctx.strokeStyle = '#00008b'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.stroke();
        _sigLastX = x; _sigLastY = y; firmaHecha.value = true;
      };
      const startSignature = (e) => { _sigDrawing = true; const p = _sigGetPos(e.clientX, e.clientY); _sigLastX = p.x; _sigLastY = p.y; };
      const drawSignature = (e) => { if (!_sigDrawing) return; const p = _sigGetPos(e.clientX, e.clientY); _sigStroke(p.x, p.y); };
      const stopSignature = () => { _sigDrawing = false; };
      const startSignatureTouch = (e) => { _sigDrawing = true; const t = e.touches[0]; const p = _sigGetPos(t.clientX, t.clientY); _sigLastX = p.x; _sigLastY = p.y; };
      const drawSignatureTouch = (e) => { if (!_sigDrawing) return; const t = e.touches[0]; const p = _sigGetPos(t.clientX, t.clientY); _sigStroke(p.x, p.y); };
      const limpiarFirma = () => { const c = signatureCanvas.value; if (!c) return; c.getContext('2d').clearRect(0, 0, c.width, c.height); firmaHecha.value = false; };

      // Setup Rechazo Dirección
      const mostrarModalRechazoDireccion = ref(false);
      const mostrarModalVerRechazo = ref(false);
      const cicloVerRechazo = ref(null);
      const rechazoDireccionDestino = ref('st');
      const rechazoDireccionNota = ref('');

      // Setup Rechazo Área
      const mostrarModalRechazoArea = ref(false);
      const mostrarModalVerRechazoArea = ref(false);
      const cicloVerRechazoArea = ref(null);
      const rechazoAreaDestino = ref('st');
      const rechazoAreaNota = ref('');

      // Setup Rechazo ST
      const mostrarModalRechazoST = ref(false);
      const mostrarModalVerRechazoST = ref(false);
      const cicloVerRechazoST = ref(null);
      const rechazoSTDestino = ref('administracion');
      const rechazoSTNota = ref('');

      // Setup Direccion - Firma
      const mostrarModalFirmaDireccion = ref(false);
      const signatureCanvasDir = ref(null);
      const firmaHechaDir = ref(false);
      let _sigDirDrawing = false, _sigDirLastX = 0, _sigDirLastY = 0;

      const _sigDirGetPos = (clientX, clientY) => {
        const c = signatureCanvasDir.value;
        const r = c.getBoundingClientRect();
        return { x: (clientX - r.left) * c.width / r.width, y: (clientY - r.top) * c.height / r.height };
      };
      const _sigDirStroke = (x, y) => {
        const ctx = signatureCanvasDir.value.getContext('2d');
        ctx.beginPath(); ctx.moveTo(_sigDirLastX, _sigDirLastY); ctx.lineTo(x, y);
        ctx.strokeStyle = '#00008b'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.stroke();
        _sigDirLastX = x; _sigDirLastY = y; firmaHechaDir.value = true;
      };
      const startSignatureDir = (e) => { _sigDirDrawing = true; const p = _sigDirGetPos(e.clientX, e.clientY); _sigDirLastX = p.x; _sigDirLastY = p.y; };
      const drawSignatureDir = (e) => { if (!_sigDirDrawing) return; const p = _sigDirGetPos(e.clientX, e.clientY); _sigDirStroke(p.x, p.y); };
      const stopSignatureDir = () => { _sigDirDrawing = false; };
      const startSignatureDirTouch = (e) => { _sigDirDrawing = true; const t = e.touches[0]; const p = _sigDirGetPos(t.clientX, t.clientY); _sigDirLastX = p.x; _sigDirLastY = p.y; };
      const drawSignatureDirTouch = (e) => { if (!_sigDirDrawing) return; const t = e.touches[0]; const p = _sigDirGetPos(t.clientX, t.clientY); _sigDirStroke(p.x, p.y); };
      const limpiarFirmaDir = () => { const c = signatureCanvasDir.value; if (!c) return; c.getContext('2d').clearRect(0, 0, c.width, c.height); firmaHechaDir.value = false; };

      // Setup Archivar
      const mostrarModalArchivar = ref(false);


      //methods

      // ── Polling & notificaciones de actualización ──────────────────────────
      let pollInterval = null;
      let lastFingerprint = '';
      const hayActualizaciones = ref(false);
      const refreshCargando = ref(false);

      // Silenciar alertas de sonido (persiste en localStorage)
      const silenciado = ref(localStorage.getItem('notif_silenciado') === 'true');
      const toggleSilencio = () => {
        silenciado.value = !silenciado.value;
        localStorage.setItem('notif_silenciado', String(silenciado.value));
      };

      const playNotificationSound = () => {
        if (silenciado.value) return;
        try {
          const ctx = new (window.AudioContext || window.webkitAudioContext)();
          [0, 0.28].forEach(offset => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.value = 880;
            gain.gain.setValueAtTime(0.25, ctx.currentTime + offset);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + offset + 0.22);
            osc.start(ctx.currentTime + offset);
            osc.stop(ctx.currentTime + offset + 0.22);
          });
        } catch { /* Sin soporte de audio */ }
      };

      // Detecta si hay acciones pendientes para el rol actual en los datos crudos de la API
      const hasPendingForMyRole = (data) => {
        const rol = sessionStorage.getItem('role');
        const ciclos = data.ciclos || [];
        const solicitudes = data.solicitudes || [];
        const legajos = data.legajos || [];

        if (rol === 'servicios_tecnologicos') {
          const circuitosConOS = new Set((data.ordenes_servicio || []).map(o => o.nro_circuito));
          const necesitaOS = legajos.some(l => !circuitosConOS.has(l.nro_circuito));
          return necesitaOS || ciclos.some(c =>
            (c.adjunto_informeServicio && !c.revision_confirmada) ||
            (c.historial_correcciones || []).some(r => r.destinatario === 'st' && r.estado === 'pendiente')
          );
        }
        if (rol === 'administracion') {
          const circuitosConLegajo = new Set(legajos.map(l => l.nro_circuito));
          const sinLegajo = solicitudes.some(s => s.nro_circuito && !circuitosConLegajo.has(s.nro_circuito));
          const listaParaArchivar = ciclos.some(c => c.firma_direccion);
          const rechazoPendiente = ciclos.some(c =>
            (c.historial_correcciones || []).some(r => r.destinatario === 'administracion' && r.estado === 'pendiente')
          );
          return sinLegajo || listaParaArchivar || rechazoPendiente;
        }
        if (rol === 'area_jefe' || rol === 'area_standard') {
          return ciclos.some(c =>
            (c.revision_confirmada && !c.firma_responsable_area) ||
            (c.historial_correcciones || []).some(r => r.destinatario === 'area' && r.estado === 'pendiente')
          );
        }
        if (rol === 'direccion') {
          return ciclos.some(c => c.firma_responsable_area && !c.firma_direccion);
        }
        return false;
      };

      // Fingerprint por rol: área no incluye cambios de pago (no los ve), todos incluyen estado de OS
      const computeRoleFp = (data, rol) => {
        const circuits = (data.solicitudes || []).map(s => s.nro_circuito).sort().join(',');
        const ciclosState = (data.ciclos || [])
          .map(c => `${c.id}:${c.firma_direccion}:${c.firma_responsable_area}:${c.revision_confirmada}:${!!c.adjunto_informeArea}:${!!c.adjunto_informeServicio}`)
          .sort().join('|');
        const legajosState = (data.legajos || []).map(l => `${l.nro_legajo}:${l.pago}`).sort().join('|');
        const osState = (data.ordenes_servicio || []).map(o => `${o.nro_circuito}:${o.completo}`).sort().join('|');

        if (rol === 'area_jefe' || rol === 'area_standard') {
          return [circuits, ciclosState, osState].join('||');
        }
        return [circuits, ciclosState, legajosState, osState].join('||');
      };

      // Mantener compatibilidad con fetchData
      const computeFingerprint = (data) => computeRoleFp(data, sessionStorage.getItem('role'));

      const pollData = async () => {
        try {
          const response = await api.get('/encurso/obtener_todoencurso/');
          const rol = sessionStorage.getItem('role');
          const fp = computeRoleFp(response.data, rol);
          if (lastFingerprint && fp !== lastFingerprint) {
            lastFingerprint = fp;
            if (rol === 'administracion') {
              // Admin: banner y sonido solo cuando le toca actuar
              if (hasPendingForMyRole(response.data)) {
                hayActualizaciones.value = true;
                playNotificationSound();
              }
            } else {
              // ST, área, dirección: banner siempre que haya cambios visibles para su rol
              hayActualizaciones.value = true;
              if (hasPendingForMyRole(response.data)) {
                playNotificationSound();
              }
            }
          }
        } catch {
          // fallo silencioso en polling
        }
      };

      const aplicarActualizaciones = () => {
        hayActualizaciones.value = false;
        fetchData();
      };

      const manualRefresh = async () => {
        refreshCargando.value = true;
        hayActualizaciones.value = false;
        await new Promise(resolve => {
          fetchData();
          setTimeout(resolve, 600);
        });
        refreshCargando.value = false;
      };
      // ────────────────────────────────────────────────────────────────────────

      const fetchData = () => {
          api.get('/encurso/obtener_todoencurso/')
            .then(response => {
              const data = response.data;
              lastFingerprint = computeFingerprint(data);

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
                const solicitudesInterAreaFiltered = (data.solicitudes_inter_area || [])
                  .filter(s => s.nro_circuito === solicitud.nro_circuito)
                  .map(s => ({
                    id: s.nro_solicitudInterarea,
                    fecha: s.fecha_solicitudInterarea ? formatDate(s.fecha_solicitudInterarea) : '',
                    inter_areaTematica: formatAreaTematica(s.inter_areaTematica),
                    inter_areaTematica_raw: s.inter_areaTematica,
                    areaTematica_origen: s.areaTematica_origen,
                    muestras: s.muestras_solicitudIa,
                    num_labs: s.num_labs,
                    observaciones: s.observaciones,
                    genera_informe_parcial: s.genera_informe_parcial,
                    confirmado_ap: s.confirmado_ap,
                    tipo_rechazo_ap: s.tipo_rechazo_ap,
                    comentario_rechazo_ap: s.comentario_rechazo_ap,
                    estado_correc_informe: s.estado_correc_informe,
                    estado_correc_registros: s.estado_correc_registros,
                    tipo: s.tipo || 'parcial',
                    plazo: s.plazo || null,
                    ciclos: (s.ciclos || []).map(c => ({
                      id: c.id,
                      numero: c.numero,
                      adjunto_informeArea: c.adjunto_informeArea,
                      fecha_informeArea: c.fecha_informeArea,
                      registros_ensayo: c.registros_ensayo || [],
                      adjunto_informeServicio: c.adjunto_informeServicio,
                      firma_responsable_area: c.firma_responsable_area,
                      firma_responsable_ap: c.firma_responsable_ap,
                      adjunto_firmado_ap: c.adjunto_firmado_ap || null,
                      firma_direccion: c.firma_direccion,
                      nota_rechazo_st: c.nota_rechazo_st,
                      rechazo_st_destino: c.rechazo_st_destino,
                    })),
                    servicio_solicitado: s.servicio_solicitado || [],
                  }));
                // Arrays multi-adjunto
                const adjuntos_solicitud = (data.adjuntos_solicitud || [])
                  .filter(a => a.data_servicio === solicitud.nro_dataServicio)
                  .map(a => ({ id: a.id, archivo: a.archivo }));

                const adjuntos_factura = legajoCorrespondiente
                  ? (data.adjuntos_factura || [])
                    .filter(a => a.legajo === legajoCorrespondiente.nro_legajo)
                    .map(a => ({ id: a.id, archivo: a.archivo, monto: a.monto }))
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
                    historial_correcciones: c.historial_correcciones || [],
                    firma_responsable_area: c.firma_responsable_area,
                    adjunto_firmado_area: c.adjunto_firmado_area || null,
                    firma_direccion: c.firma_direccion,
                    adjunto_firmado_direccion: c.adjunto_firmado_direccion || null,
                    nota_rechazo_direccion: c.nota_rechazo_direccion || null,
                    rechazo_destino: c.rechazo_destino || null,
                    nota_rechazo_area: c.nota_rechazo_area || null,
                    rechazo_area_destino: c.rechazo_area_destino || null,
                    adjunto_informeServicio_pdf: c.adjunto_informeServicio_pdf || null,
                    pdf_confirmado_admin: c.pdf_confirmado_admin || false,
                    nota_rechazo_st: c.nota_rechazo_st || null,
                    rechazo_st_destino: c.rechazo_st_destino || null,
                  }));

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
                  total_arancel: solicitud.total_arancel || 0,
                  pendiente_factura: solicitud.pendiente_factura !== undefined ? solicitud.pendiente_factura : null,
                  // Legajo
                  nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo : '',
                  fecha_legajo: legajoCorrespondiente ? formatDate(legajoCorrespondiente.fecha_legajo) : '',
                  adjuntos_factura,
                  pago: legajoCorrespondiente ? legajoCorrespondiente.pago : null,
                  plazo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago : '',
                  legajo_completo: legajoCorrespondiente ? legajoCorrespondiente.completo : '',
                  labs_adicionales_pendientes: legajoCorrespondiente ? (legajoCorrespondiente.labs_adicionales_pendientes || 0) : 0,
                  monto_adicional_pendiente: legajoCorrespondiente ? !!legajoCorrespondiente.monto_adicional_pendiente : false,
                  rangos_laboratorios: legajoCorrespondiente ? (legajoCorrespondiente.rangos_laboratorios || '') : '',
                  // Recepcion
                  nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.nros_remitos : '',
                  estado_recepcion: recepcionCorrespondiente ? recepcionCorrespondiente.estado_recepcion : '',
                  plazo_muestras: recepcionCorrespondiente ? recepcionCorrespondiente.plazo_muestras : '',
                  // Orden de Servicio
                  nro_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.nro_ordenServicio : '',
                  fecha_ordenServicio: ordenCorrespondiente ? formatDate(ordenCorrespondiente.fecha_ordenServicio) : '',
                  plazo_estimado: solicitud.plazo_estimado,
                  ordenServicio_completo: ordenCorrespondiente ? ordenCorrespondiente.completo : '',
                  os_modificada: ordenCorrespondiente ? !!ordenCorrespondiente.modificada : false,
                  os_max_parciales: ordenCorrespondiente ? (ordenCorrespondiente.max_parciales ?? null) : null,
                  os_plazos_parciales: ordenCorrespondiente ? (ordenCorrespondiente.plazos_parciales || []) : [],
                  // Ciclos de Informe
                  ciclos,
                  firma_direccion: ultimoCiclo ? ultimoCiclo.firma_direccion : false,
                  nombre_solicitante: solicitud.nombre_solicitante,
                  // Solicitudes Inter Area (múltiples)
                  solicitudes_interarea: solicitudesInterAreaFiltered,
                  // Conceptos de Facturación
                  conceptos_facturacion: solicitud.conceptos_facturacion || [],
                };

                // Filtrar las filas según el área temática del usuario, excepto si es servicios_tecnologicos, administracion, o direccion
                if (userAreaTematica === 'Servicios Tecnologicos' ||
                    userAreaTematica === 'Administracion' ||
                    userAreaTematica === 'Direccion' ||
                    (fila.area_tematica === userAreaTematica && fila.nro_ordenServicio) ||
                    solicitudesInterAreaFiltered.some(ia => ia.inter_areaTematica === userAreaTematica)) {
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
      const userAreaTematicaFormatted = userAreaTematica ? formatAreaTematica(userAreaTematica) : '';

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
        popupSTId.value = null;
        popupAreaId.value = null;
        popupDirId.value = null;
        popupFormatoId.value = null;
        popupFacturaId.value = null;
        popupSTIAId.value = null;
        popupPDFAdminIAId.value = null;
        popupAreaIAId.value = null;
        popupAPIAId.value = null;
        popupDirIAId.value = null;
        popupConfirmIAId.value = null;
        popupCorreccionIAId.value = null;
        popupFormatoIAId.value = null;
      };

      const onFirmaActualizada = (e) => { firmaUsuarioUrl.value = e.detail.firma_url || null; };

      const fetchCatalogoConceptos = () => {
        api.get('/aranceles/conceptos/').then(res => { catalogoConceptos.value = res.data; }).catch(() => {});
      };

      onMounted(() => {
        fetchData();
        cargarFirmaUsuario();
        fetchCatalogoConceptos();
        document.addEventListener('click', closeAllPopups);
        document.addEventListener('att-cell-open', closeAllPopups);
        document.addEventListener('encurso-refresh', fetchData);
        window.addEventListener('firma-usuario-actualizada', onFirmaActualizada);
        pollInterval = setInterval(pollData, 60000);
      });

      onUnmounted(() => {
        document.removeEventListener('click', closeAllPopups);
        document.removeEventListener('att-cell-open', closeAllPopups);
        document.removeEventListener('encurso-refresh', fetchData);
        window.removeEventListener('firma-usuario-actualizada', onFirmaActualizada);
        clearInterval(pollInterval);
      });

      const triggerFileInput = () => {
      document.getElementById('fileInput').click();
      };

      // SOLICITUD DE SERVICIO

      // DS - Data Servicio
      const abrirDataServicio = (nroDS, fila) => {
          nroDataServicioAbierto.value = nroDS;
          conceptosDS.value = fila && fila.conceptos_facturacion ? [...fila.conceptos_facturacion] : [];
          conceptoSeleccionadoDS.value = '';
          api.get(`/encurso/obtener_dataservicio/${nroDS}/`)
              .then(response => {
                  const { nro_dataServicio, fecha_dataServicio, obra, cant_numLabs, plazo_estimado, muestras, nro_presupuesto, area_tematica, nombre_solicitante, arancel_presupuesto, observaciones, email_factura, email_informe_tecnico, conceptos_facturacion } = response.data;
                  nroDataServicio.value = nro_dataServicio;
                  fechaDataServicio.value = formatDate(fecha_dataServicio);
                  obraDataServicio.value = obra;
                  cantNumLabsDataServicio.value = cant_numLabs;
                  plazoEstimadoDataServicio.value = plazo_estimado;
                  muestrasDataServicio.value = muestras;
                  nroPresupuestoDataServicio.value = nro_presupuesto;
                  areaDataServicio.value = formatAreaTematica(area_tematica);
                  solicitanteDataServicio.value = nombre_solicitante;
                  arancelDataServicio.value = formatArancel(arancel_presupuesto);
                  observacionesDataServicio.value = observaciones;
                  emailFacturaDataServicio.value = email_factura;
                  emailInformeTecnicoDataServicio.value = email_informe_tecnico;
                  if (conceptos_facturacion) conceptosDS.value = conceptos_facturacion;
                  mostrarModalDataServicio.value = true;
              })
              .catch(error => {
                  console.error('Error al obtener los datos del legajo:', error);
              });
      };

      const agregarConceptoDS = () => {
        if (!conceptoSeleccionadoDS.value) return;
        conceptosDS.value.push(conceptoSeleccionadoDS.value);
        conceptoSeleccionadoDS.value = '';
      };

      const quitarConceptoDS = (c) => {
        conceptosDS.value = conceptosDS.value.filter(x => x.id !== c.id);
      };

      const guardarConceptosDS = async () => {
        if (!nroDataServicioAbierto.value) return;
        guardandoConceptosDS.value = true;
        mensajeConceptoDS.value = '';
        try {
          await api.patch(`/encurso/actualizar_conceptos_ds/${nroDataServicioAbierto.value}/`, {
            conceptos_facturacion: conceptosDS.value.map(c => c.id),
          });
          mensajeConceptoDS.value = 'ok';
          setTimeout(() => { mensajeConceptoDS.value = ''; }, 3000);
          fetchData();
        } catch (err) {
          console.error('Error guardando conceptos:', err);
          mensajeConceptoDS.value = 'error';
          setTimeout(() => { mensajeConceptoDS.value = ''; }, 4000);
        } finally {
          guardandoConceptosDS.value = false;
        }
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
      const abrirLegajo = async (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          const nro_circuito = numeroCircuitoGlobal.value;
          try {
              const [resLegajo, resConfig] = await Promise.all([
                api.get(`/encurso/obtener_legajo/${nro_circuito}/`),
                api.get('/encurso/config_formulario/legajo/'),
              ]);
              const { nro_legajo, fecha_legajo, rangos_laboratorios, nombre_solicitante, version_formulario } = resLegajo.data;
              nroLegajo.value = nro_legajo;
              fechaLegajo.value = fecha_legajo;
              rangosLaboratorios.value = rangos_laboratorios;
              nombreSolicitante.value = nombre_solicitante;
              añoLegajo.value = new Date(fecha_legajo).getFullYear();
              versionLegajo.value = version_formulario || '01';
              configFormularioLegajo.value = resConfig.data;
              mostrarModalLegajo.value = true;
          } catch (error) {
              console.error('Error al obtener los datos del legajo:', error);
          }
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
      const labelPago = (pago) => {
        const p = String(pago);
        if (p === '100') return '100%';
        if (p === 'no_arancelado') return 'No arancelado';
        if (p === 'pago_diferido') return 'Pago diferido';
        return '0%';
      };

      const labelPagoBadgeClass = (pago) => {
        const p = String(pago);
        if (p === '100' || p === 'no_arancelado') return 'badge bg-success';
        if (p === 'pago_diferido') return 'badge bg-warning text-dark';
        return 'badge bg-danger';
      };

      const pagoEsCompleto = (pago) => {
        const p = String(pago);
        return p === '100' || p === 'no_arancelado' || p === 'pago_diferido';
      };

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
        if (!adjunto) return;
        const s = String(adjunto);
        if (/^https?:\/\//i.test(s)) { window.open(s, '_blank'); return; }
        const cleanPath = s.replace(/^\/?(media\/)+/, '');
        window.open(window.location.origin + '/media/' + cleanPath, '_blank');
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

      const osMaxParciales = ref(null);
      const osPlazosArr = ref([]);

      const sincronizarPlazosOS = () => {
        const n = parseInt(osMaxParciales.value) || 0;
        const actual = osPlazosArr.value.slice(0, n);
        while (actual.length < n) actual.push(null);
        osPlazosArr.value = actual;
      };

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
          osMaxParciales.value = null;
          osPlazosArr.value = [];
        } catch (e) {
          console.error('Error al cargar preview OS:', e);
        }
        mostrarModalCrearOrdenServicio.value = true;
      };

      const cerrarModalCrearOrdenServicio = () => {
        mostrarModalCrearOrdenServicio.value = false;
        osReadOnly.value = false;
        osModificadaActual.value = false;
        osFilaActual.value = null;
        osCircuitoActual.value = null;
        nuevoRangoOS.value = '';
        osMaxParciales.value = null;
        osPlazosArr.value = [];
      };

      const aceptarOrdenServicio = () => {
        const nro_circuito = osCircuitoActual.value;
        const fila = osFilaActual.value;
        api.post(`/encurso/confirmar_lectura_os/${nro_circuito}/`)
          .then(() => { if (fila) fila.os_modificada = false; })
          .catch(() => {});
        cerrarModalCrearOrdenServicio();
      };
      
      const crearOrdenServicio = async () => {
          const nro_circuito = numeroCircuitoGlobal.value;
          try {
              await api.post(`/encurso/crear_ordenservicio/${nro_circuito}/`);
              if (osMaxParciales.value > 0) {
                try {
                  await api.patch(`/encurso/orden/${nro_circuito}/config_parciales/`, {
                    max_parciales: osMaxParciales.value,
                    plazos_parciales: osPlazosArr.value.map(v => v || 0),
                  });
                } catch (e) { console.error('Error guardando config parciales:', e); }
              }
              mostrarModalCrearOrdenServicio.value = false;
              fetchData();
              showSuccessAlert.value = true;
              setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
              console.error('Error al crear la orden de servicio:', error);
              mostrarModalCrearOrdenServicio.value = false;
              showErrorAlert.value = true;
              setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
      };

      // OS - Abrir Orden de Servicio
      const abrirOrdenServicio = async (fila) => {
          const nro_circuito = fila.nro_circuito;
          try {
              const [response, resConfig] = await Promise.all([
                api.get(`/encurso/obtener_orden_servicio/${nro_circuito}/`),
                api.get('/encurso/config_formulario/orden_servicio/'),
              ]);
              const { nro_ordenServicio, fecha_ordenServicio, area_tematica, nro_legajo, rangos_laboratorios, nuevo_rango_lab, plazo_estimado, nombre_solicitante, servicio_solicitado, muestras, observaciones, version_formulario, max_parciales, plazos_parciales } = response.data;
              nroOS.value = nro_ordenServicio;
              fechaOS.value = fecha_ordenServicio;
              areaOS.value = formatAreaTematica(area_tematica);
              legajoOS.value = nro_legajo;
              rangosOS.value = rangos_laboratorios;
              nuevoRangoOS.value = nuevo_rango_lab || '';
              plazoOS.value = plazo_estimado;
              solicitanteOS.value = nombre_solicitante;
              servicioOS.value = servicio_solicitado;
              muestrasOS.value = muestras;
              observacionesOS.value = observaciones;
              versionOS.value = version_formulario || '01';
              configFormularioOS.value = resConfig.data;
              osMaxParciales.value = max_parciales || null;
              osPlazosArr.value = [...(plazos_parciales || [])];
              osReadOnly.value = true;
              // Guardar si la OS está modificada: el área DEBE aceptar explícitamente
              osModificadaActual.value = !!(fila.os_modificada && (isAreaJefe.value || isAreaStandard.value));
              osFilaActual.value = fila;
              osCircuitoActual.value = nro_circuito;
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

      const plazoCiclo = (ciclo, fila) => {
        if (ciclo.tipo !== 'parcial') return null;
        const plazos = fila.os_plazos_parciales;
        if (!plazos || !plazos.length) return null;
        const parciales = fila.ciclos.filter(c => c.tipo === 'parcial');
        const idx = parciales.findIndex(c => c.id === ciclo.id);
        if (idx < 0 || idx >= plazos.length) return null;
        return plazos[idx] || null;
      };

      const guardarConfigParciales = async () => {
        const nro_circuito = osCircuitoActual.value;
        if (!nro_circuito) return;
        try {
          await api.patch(`/encurso/orden/${nro_circuito}/config_parciales/`, {
            max_parciales: osMaxParciales.value || null,
            plazos_parciales: (osPlazosArr.value || []).map(v => v || 0),
          });
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 2000);
        } catch (e) {
          console.error('Error guardando config parciales:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 4000);
        }
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
          && fila.ciclos[fila.ciclos.length - 1].tipo === 'parcial'
          && !fila.solicitudes_interarea.some(ia => ia.tipo === 'complementario');
      };

      const mostrarBotonAgregarIA = (fila) => {
        return isAreaJefe.value && fila.ordenServicio_completo === true &&
          fila.area_tematica === userAreaTematicaFormatted &&
          !fila.ciclos.some(c => c.tipo === 'complementario') &&
          !fila.solicitudes_interarea.some(ia => ia.tipo === 'complementario');
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
      const filaModalTipoCiclo = ref(null);

      const togglePopupInformeArea = (cicloId) => {
        const opening = popupInformeAreaId.value !== cicloId;
        popupInformeAreaId.value = opening ? cicloId : null;
        if (opening) {
          document.dispatchEvent(new Event('speed-dial-open'));
          popupSTId.value = null;
          popupAreaId.value = null;
          popupDirId.value = null;
        }
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
        filaModalTipoCiclo.value = fila || null;
        hayParcialesPrevios.value = fila
          ? fila.ciclos.some(c => c.tipo === 'parcial' && c.adjunto_informeArea)
          : false;
        mostrarModalTipoCiclo.value = true;
      };

      const reemplazarInformeAreaCiclo = async (event, ciclo) => {
        const archivo = event.target.files[0];
        if (!archivo) return;
        const formData = new FormData();
        formData.append('archivo', archivo);
        formData.append('tipo', ciclo.tipo);
        try {
          await api.post(`/encurso/subir_informe_area_ciclo/${ciclo.id}/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const seleccionarArchivoParaNuevoCiclo = (event, fila) => {
        const file = event.target.files[0];
        if (!file) return;
        archivoPendiente.value = file;
        cicloSeleccionado.value = null;
        filaParaNuevoCiclo.value = fila;
        filaModalTipoCiclo.value = fila;
        hayParcialesPrevios.value = fila.ciclos.some(c => c.tipo === 'parcial' && c.adjunto_informeArea);
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
        filaModalTipoCiclo.value = fila || null;
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
        filaModalTipoCiclo.value = null;
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

      const isServicioOSSeleccionado = (servicio) =>
        serviciosSeleccionados.value.some(s => s.nro_servicio === servicio.nro_servicio);

      const toggleServicioOS = (servicio, checked) => {
        if (checked) {
          serviciosSeleccionados.value.push({ ...servicio });
        } else {
          const idx = serviciosSeleccionados.value.findIndex(s => s.nro_servicio === servicio.nro_servicio);
          if (idx !== -1) serviciosSeleccionados.value.splice(idx, 1);
        }
      };

      const seleccionarArancel = (arancel) => {
        arancelAdicional.value = arancel;
        busquedaArancel.value = '';
        cantidadAdicional.value = 1;
      };

      const agregarArancel = () => {
        if (!arancelAdicional.value || cantidadAdicional.value < 1) return;
        serviciosSeleccionados.value.push({
          nro_servicio: arancelAdicional.value.nro_servicio,
          servicio: arancelAdicional.value.servicio,
          norma: arancelAdicional.value.norma || '',
          cant: cantidadAdicional.value,
        });
        arancelAdicional.value = null;
        busquedaArancel.value = '';
        cantidadAdicional.value = 1;
      };

      const quitarServicioSeleccionado = (index) => {
        serviciosSeleccionados.value.splice(index, 1);
      };

      const parsearRangosLab = (rangosStr, preseleccionar = false) => {
        if (!rangosStr) return [];
        const labs = [];
        const partes = rangosStr.split(',');
        for (const parte of partes) {
          const str = parte.trim();
          const match = str.match(/^(\d+)(?:-(\d+))?\/(\d+)$/);
          if (!match) continue;
          const desde = parseInt(match[1]);
          const hasta = match[2] ? parseInt(match[2]) : desde;
          const anio = match[3];
          for (let n = desde; n <= hasta; n++) {
            labs.push({ numero: n, anio, seleccionado: preseleccionar });
          }
        }
        return labs;
      };

      const filaParaCrearIA = ref(null);

      const abrirModalCrearSolicitudInterArea = async (fila) => {
        numeroCircuitoGlobal.value = fila.nro_circuito;
        filaParaCrearIA.value = fila;
        try {
          await obtenerServicios(numeroCircuitoGlobal.value);
          nuevaSolicitudInterarea.value.nro_circuito = fila.nro_circuito;
          nuevaSolicitudInterarea.value.areaTematica_origen = fila.area_tematica;
          mostrarModalCrearSolicitudInterArea.value = true;
          labsDisponiblesIA.value = parsearRangosLab(fila.rangos_laboratorios, false);
          labsPickerAbierto.value = false;
          if (!catalogoAranceles.value.length) {
            try {
              const res = await api.get('/aranceles/todos/');
              catalogoAranceles.value = Array.isArray(res.data) ? res.data : [];
            } catch (_) { /* sin acción */ }
          }
        } catch (error) {
          console.error('Error al obtener servicios:', error);
        }
      };

      const cerrarModalCrearSolicitudInterArea = () => {
        mostrarModalCrearSolicitudInterArea.value = false;
        filaParaCrearIA.value = null;
        serviciosDisponibles.value = [];
        serviciosSeleccionados.value = [];
        busquedaArancel.value = '';
        arancelAdicional.value = null;
        cantidadAdicional.value = 1;
        labsDisponiblesIA.value = [];
        labsPickerAbierto.value = false;
        erroresIA.value = {};
        nuevaSolicitudInterarea.value = {
          fecha_solicitudInterarea: new Date().toISOString().substring(0, 10),
          areaTematica_origen: '',
          inter_areaTematica: '',
          num_labs: '',
          genera_informe_parcial: null,
          tipo: null,
          servicios_solicitudInterarea: [{ nro_servicio: '', servicio: '', cant: 0 }],
          nro_circuito: null,
          plazo: null,
        };
      };

      const crearSolicitudInterArea = () => {
          erroresIA.value = {};
          const errs = {};

          if (!nuevaSolicitudInterarea.value.tipo) {
            errs.tipo = 'Seleccioná el tipo de inter-área.';
          }
          if (!nuevaSolicitudInterarea.value.inter_areaTematica) {
            errs.inter_areaTematica = 'Seleccioná el inter-área temática.';
          }
          if (!serviciosSeleccionados.value.length) {
            errs.servicios = 'Agregá al menos un servicio.';
          }
          if ((nuevaSolicitudInterarea.value.tipo === 'parcial' || nuevaSolicitudInterarea.value.tipo === 'complementario') && !labsSeleccionadosIA.value.length) {
            errs.num_labs = 'Seleccioná al menos un número de laboratorio.';
          }
          if (!nuevaSolicitudInterarea.value.muestras_solicitudIa?.trim()) {
            errs.muestras = 'Ingresá las muestras a entregar.';
          }
          if (!nuevaSolicitudInterarea.value.plazo || nuevaSolicitudInterarea.value.plazo < 1) {
            errs.plazo = 'Ingresá el plazo en días.';
          }

          if (Object.keys(errs).length) {
            erroresIA.value = errs;
            return;
          }

          nuevaSolicitudInterarea.value.servicios_solicitudInterarea = [];
          serviciosSeleccionados.value.forEach(servicio => {
            nuevaSolicitudInterarea.value.servicios_solicitudInterarea.push({
              nro_servicio: servicio.nro_servicio,
              servicio: servicio.servicio,
              cant: servicio.cant,
            });
          });

          if (labsSeleccionadosIA.value.length) {
            const anio = labsSeleccionadosIA.value[0].anio;
            const nums = labsSeleccionadosIA.value.map(l => l.numero).join(', ');
            nuevaSolicitudInterarea.value.num_labs = `${nums} / ${anio}`;
          }

          nuevaSolicitudInterarea.value.areaTematica_origen = desformatearAreaTematica(nuevaSolicitudInterarea.value.areaTematica_origen);

          api.post('/encurso/crear_solicitud_interarea/', nuevaSolicitudInterarea.value)
            .then(() => {
              cerrarModalCrearSolicitudInterArea();
              fetchData();
              showSuccessAlert.value = true;
              setTimeout(() => { showSuccessAlert.value = false; }, 3000);
            })
            .catch(error => {
              console.error('Error al crear la solicitud inter area:', error.response?.data);
              cerrarModalCrearSolicitudInterArea();
              showErrorAlert.value = true;
              setTimeout(() => { showErrorAlert.value = false; }, 5000);
            });
      };


      // Inter Area - Abrir detalle de una solicitud inter-área
      const solicitudIASeleccionada = ref(null);
      const mostrarModalSolicitudInterArea = ref(false);

      const abrirSolicitudInterArea = (ia) => {
        marcarIAVista(ia.id);
        nroSolicitudInterArea.value = ia.id;
        fechaSolicitudInterArea.value = ia.fecha;
        areaTematicaOrigen.value = formatAreaTematica(ia.areaTematica_origen);
        interAreaSolicitudInterArea.value = ia.inter_areaTematica;
        muestrasSolicitudInterArea.value = ia.muestras;
        numLabsSolicitudInterArea.value = ia.num_labs;
        observacionesSolicitudInterArea.value = ia.observaciones;
        servicioSolicitudInterArea.value = ia.servicio_solicitado || [];
        solicitudIASeleccionada.value = ia;
        mostrarModalSolicitudInterArea.value = true;
      };

      const cerrarModalSolicitudInterArea = () => {
        mostrarModalSolicitudInterArea.value = false;
        solicitudIASeleccionada.value = null;
      };

      // Inter Area — helpers de estado
      const ultimoCicloIA = (ia) => {
        if (!ia.ciclos || ia.ciclos.length === 0) return null;
        return ia.ciclos[ia.ciclos.length - 1];
      };

      const normalizeArea = (s) => s ? s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim() : '';

      const esPrincipalDeIA = (ia) => {
        return isAreaJefe.value && normalizeArea(ia.areaTematica_origen) === normalizeArea(userAreaTematica);
      };

      const esInterAreaDeIA = (ia) => {
        return (isAreaJefe.value || isAreaStandard.value) && normalizeArea(ia.inter_areaTematica_raw) === normalizeArea(userAreaTematica);
      };

      const esMiAreaEsteFila = (fila) => normalizeArea(fila.area_tematica) === normalizeArea(userAreaTematicaFormatted);

      // Usuario de área viendo fila de otra área (solo inter-área en esa fila)
      const esSoloInterAreaEnFila = (fila) => (isAreaJefe.value || isAreaStandard.value) && !esMiAreaEsteFila(fila);

      // Siempre true — se mantiene por compatibilidad pero ya no oculta nada
      const mostrarInformeAreaEnFila = () => true;

      // Inter Area — subir informe área por el inter-área (crea ciclo si no existe)
      const subirInformeAreaCicloIA = async (event, ia) => {
        const archivo = event.target.files[0];
        if (!archivo) return;
        let cicloId;
        const cicloExistente = ultimoCicloIA(ia);
        if (cicloExistente) {
          cicloId = cicloExistente.id;
        } else {
          try {
            const res = await api.post(`/encurso/ia/ciclo/crear/${ia.id}/`);
            cicloId = res.data.id;
          } catch (e) {
            console.error('Error al crear ciclo inter-área:', e);
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 3000);
            return;
          }
        }
        const formData = new FormData();
        formData.append('archivo', archivo);
        try {
          await api.post(`/encurso/ia/ciclo/${cicloId}/subir_informe_area/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al subir informe inter-área:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Inter Area — subir registro de ensayo por el inter-área
      const subirRegistroEnsayoCicloIA = async (event, cicloIA) => {
        const archivo = event.target.files[0];
        if (!archivo) return;
        const formData = new FormData();
        formData.append('archivo', archivo);
        try {
          await api.post(`/encurso/ia/ciclo/${cicloIA.id}/subir_registro_ensayo/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al subir registro de ensayo inter-área:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const eliminarRegistroEnsayoCicloIA = async (id) => {
        if (!confirm('¿Eliminar el registro de ensayo?')) return;
        try {
          await api.delete(`/encurso/ia/registro_ensayo/${id}/`);
          fetchData();
        } catch (e) { console.error('Error al eliminar registro ensayo IA:', e); }
      };

      // Inter Area — confirmación inicial por área principal
      const confirmarInterareaPrincipal = async (ia) => {
        try {
          await api.post(`/encurso/ia/solicitud/${ia.id}/confirmar_principal/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al confirmar inter-área:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Inter Area — confirmar correcciones post-rechazo (por separado)
      const confirmarCorreccionInformeAP = async (ia) => {
        try {
          await api.post(`/encurso/ia/solicitud/${ia.id}/confirmar_correc_informe/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al confirmar corrección de informe:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const confirmarCorreccionRegistrosAP = async (ia) => {
        try {
          await api.post(`/encurso/ia/solicitud/${ia.id}/confirmar_correc_registros/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al confirmar corrección de registros:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Inter Area — rechazo
      const mostrarModalRechazarIA = ref(false);
      const iaParaRechazar = ref(null);
      const tipoRechazoIA = ref('informe');
      const comentarioRechazoIA = ref('');

      const abrirModalRechazarIA = (ia) => {
        iaParaRechazar.value = ia;
        tipoRechazoIA.value = 'informe';
        comentarioRechazoIA.value = '';
        mostrarModalRechazarIA.value = true;
      };

      const cerrarModalRechazarIA = () => {
        mostrarModalRechazarIA.value = false;
        iaParaRechazar.value = null;
        comentarioRechazoIA.value = '';
      };

      const rechazarInterareaPrincipal = async () => {
        if (!comentarioRechazoIA.value.trim()) {
          alert('El comentario es obligatorio.');
          return;
        }
        try {
          await api.post(`/encurso/ia/solicitud/${iaParaRechazar.value.id}/rechazar_principal/`, {
            tipo: tipoRechazoIA.value,
            comentario: comentarioRechazoIA.value.trim(),
          });
          cerrarModalRechazarIA();
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al rechazar inter-área:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      // Inter Area — ver comentario de rechazo (tooltip expandido)
      const mostrarModalComentarioRechazo = ref(false);
      const comentarioRechazoVer = ref('');
      const tipoRechazoVer = ref('');

      const verComentarioRechazoIA = (ia) => {
        comentarioRechazoVer.value = ia.comentario_rechazo_ap || '';
        tipoRechazoVer.value = ia.tipo_rechazo_ap || '';
        mostrarModalComentarioRechazo.value = true;
      };

      const cerrarModalComentarioRechazo = () => {
        mostrarModalComentarioRechazo.value = false;
      };
      
      // Administracion - Generar PDF desde Word (LibreOffice server-side)
      const generandoPDFId = ref(null);
      const generarPDFServicioCiclo = async (ciclo) => {
        generandoPDFId.value = ciclo.id;
        try {
          await api.post(`/encurso/generar_pdf_servicio_ciclo/${ciclo.id}/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          const msg = error?.response?.data?.error || 'Error al generar PDF.';
          alert(msg);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        } finally {
          generandoPDFId.value = null;
        }
      };

      const confirmarTipoCambioAdmin = async (ciclo) => {
        try {
          await api.post(`/encurso/ciclo/${ciclo.id}/confirmar_tipo_cambio_admin/`);
          fetchData();
        } catch (error) {
          console.error('Error al confirmar cambio de tipo:', error);
        }
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
      const togglePopupST = (cicloId) => {
        const opening = popupSTId.value !== cicloId;
        popupSTId.value = opening ? cicloId : null;
        popupAreaId.value = null;
        popupDirId.value = null;
        popupPDFAdminId.value = null;
        if (opening) {
          document.dispatchEvent(new Event('speed-dial-open'));
          popupInformeAreaId.value = null;
        }
      };

      const togglePopupArea = (cicloId) => {
        const opening = popupAreaId.value !== cicloId;
        popupAreaId.value = opening ? cicloId : null;
        popupSTId.value = null;
        popupDirId.value = null;
        popupPDFAdminId.value = null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      const togglePopupDir = (cicloId) => {
        const opening = popupDirId.value !== cicloId;
        popupDirId.value = opening ? cicloId : null;
        popupSTId.value = null;
        popupAreaId.value = null;
        popupPDFAdminId.value = null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      const togglePopupFormato = (cicloId) => {
        const opening = popupFormatoId.value !== cicloId;
        popupFormatoId.value = opening ? cicloId : null;
        popupSTId.value = null;
        popupAreaId.value = null;
        popupDirId.value = null;
        popupPDFAdminId.value = null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      const togglePopupPDFAdmin = (cicloId) => {
        const opening = popupPDFAdminId.value !== cicloId;
        popupPDFAdminId.value = opening ? cicloId : null;
        popupSTId.value = null;
        popupAreaId.value = null;
        popupDirId.value = null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      // Factura - helpers
      const pendienteFactura = (fila) => {
        return fila.pendiente_factura !== undefined ? fila.pendiente_factura : null;
      };

      const formatMontoARS = (val) => {
        if (val === null || val === undefined || val === '') return '0';
        return new Intl.NumberFormat('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(Number(val));
      };

      const onMontoManualInput = (e) => {
        const digits = e.target.value.replace(/\D/g, '');
        const formatted = digits ? new Intl.NumberFormat('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(Number(digits)) : '';
        subirFacturaMontoManual.value = formatted;
        e.target.value = formatted;
      };

      // Factura - speed dial
      const togglePopupFactura = (nroDataServicio) => {
        const opening = popupFacturaId.value !== nroDataServicio;
        popupFacturaId.value = opening ? nroDataServicio : null;
        openDSPopup.value = null;
        openST02Popup.value = null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      const abrirDatosFacturacion = (fila) => {
        filaFacturacion.value = fila;
        api.get(`/encurso/datos_facturacion/${fila.nro_dataServicio}/`)
          .then(res => {
            datosFacturacion.value = res.data;
            mostrarModalFacturacion.value = true;
          })
          .catch(err => console.error('Error al obtener datos de facturación:', err));
      };

      const abrirSubirFactura = (fila) => {
        filaFacturacion.value = fila;
        const pendiente = datosFacturacion.value?.pendiente ?? fila.pendiente_factura ?? null;
        subirFacturaData.value = { archivo: null, monto: null, nroLegajo: fila.nro_legajo, nroCircuito: fila.nro_circuito, montoPendiente: pendiente };
        subirFacturaModoMonto.value = 'pendiente';
        subirFacturaMontoManual.value = '';
        mostrarModalSubirFactura.value = true;
      };

      const confirmarSubirFactura = () => {
        const { archivo, nroLegajo, nroCircuito, montoPendiente } = subirFacturaData.value;
        if (!archivo) return;
        let monto = null;
        if (subirFacturaModoMonto.value === 'pendiente') {
          monto = montoPendiente;
        } else {
          const raw = subirFacturaMontoManual.value.replace(/\./g, '').replace(',', '.');
          monto = raw ? parseFloat(raw) : null;
        }
        const formData = new FormData();
        formData.append('archivo', archivo);
        formData.append('nroLegajo', nroLegajo);
        formData.append('nroCircuito', nroCircuito);
        if (monto !== null && monto !== '') formData.append('monto', monto);
        api.post('/encurso/guardar_adjuntofactura/', formData)
          .then(() => {
            mostrarModalSubirFactura.value = false;
            subirFacturaData.value = { archivo: null, monto: null, nroLegajo: null, nroCircuito: null };
            fetchData();
            showSuccessAlert.value = true;
            setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          })
          .catch(err => {
            console.error('Error al guardar factura:', err);
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 3000);
          });
      };

      const eliminarFacturaDeModal = async (id) => {
        if (!confirm('¿Eliminar la factura?')) return;
        try {
          await api.delete(`/encurso/adjunto_factura/${id}/`);
          fetchData();
          // Refrescar los datos del modal
          if (filaFacturacion.value) {
            api.get(`/encurso/datos_facturacion/${filaFacturacion.value.nro_dataServicio}/`)
              .then(res => { datosFacturacion.value = res.data; });
          }
        } catch (e) { console.error('Error al eliminar factura:', e); }
      };

      const seleccionarArchivoSTCorregido = async (event, ciclo) => {
        const file = event.target.files[0];
        event.target.value = '';
        if (!file) return;
        popupSTId.value = null;
        const formData = new FormData();
        formData.append('archivo', file);
        try {
          await api.post(`/encurso/subir_informe_st_corregido/${ciclo.id}/`, formData);
          fetchData();
          const updatedReemplazados = new Set(stReemplazadoIds.value);
          updatedReemplazados.add(ciclo.id);
          stReemplazadoIds.value = updatedReemplazados;
          cicloParaCorreccionST.value = ciclo;
          textoCorreccionST.value = '';
          mostrarModalCorreccionST.value = true;
        } catch (error) {
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

      const registrarCorreccionST = async () => {
        const ciclo = cicloParaCorreccionST.value;
        if (!ciclo || !textoCorreccionST.value.trim()) return;
        try {
          await api.post(`/encurso/registrar_correccion_st/${ciclo.id}/`, {
            descripcion: textoCorreccionST.value.trim()
          });
          fetchData();
        } catch (error) {
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        } finally {
          mostrarModalCorreccionST.value = false;
          textoCorreccionST.value = '';
          cicloParaCorreccionST.value = null;
        }
      };

      const cerrarModalCorreccionST = () => {
        mostrarModalCorreccionST.value = false;
        textoCorreccionST.value = '';
        cicloParaCorreccionST.value = null;
      };

      const abrirModalVerCorrecciones = (ciclo) => {
        cicloVerCorrecciones.value = ciclo;
        mostrarModalVerCorrecciones.value = true;
      };

      const cerrarModalVerCorrecciones = () => {
        mostrarModalVerCorrecciones.value = false;
        cicloVerCorrecciones.value = null;
      };

      const confirmarRevisionST = async (ciclo) => {
        popupSTId.value = null;
        try {
          await api.put(`/encurso/confirmar_revision_ciclo/${ciclo.id}/`);
          fetchData();
          const updatedReemplazados = new Set(stReemplazadoIds.value);
          updatedReemplazados.delete(ciclo.id);
          stReemplazadoIds.value = updatedReemplazados;
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
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

      // IA pipeline state
      const popupSTIAId = ref(null);
      const popupPDFAdminIAId = ref(null);
      const popupAreaIAId = ref(null);
      const popupDirIAId = ref(null);
      const popupConfirmIAId = ref(null);
      const popupCorreccionIAId = ref(null);
      const popupFormatoIAId = ref(null);
      const generandoPDFIAId = ref(null);
      const cicloIAParaFirmaArea = ref(null);
      const cicloIAParaFirmaAP = ref(null);
      const cicloIAParaFirmaDireccion = ref(null);
      const cicloIsIA = ref(false);
      const popupAPIAId = ref(null);

      const togglePopupSTIA = (iaId) => { popupSTIAId.value = popupSTIAId.value === iaId ? null : iaId; };
      const togglePopupPDFAdminIA = (iaId) => { popupPDFAdminIAId.value = popupPDFAdminIAId.value === iaId ? null : iaId; };
      const togglePopupAreaIA = (iaId) => { popupAreaIAId.value = popupAreaIAId.value === iaId ? null : iaId; };
      const togglePopupAPIA = (iaId) => { popupAPIAId.value = popupAPIAId.value === iaId ? null : iaId; };
      const togglePopupDirIA = (iaId) => { popupDirIAId.value = popupDirIAId.value === iaId ? null : iaId; };
      const togglePopupConfirmIA = (iaId) => { popupConfirmIAId.value = popupConfirmIAId.value === iaId ? null : iaId; };
      const togglePopupCorreccionIA = (iaId) => { popupCorreccionIAId.value = popupCorreccionIAId.value === iaId ? null : iaId; };
      const togglePopupFormatoIA = (cicloIAId) => {
        const opening = popupFormatoIAId.value !== cicloIAId;
        popupFormatoIAId.value = opening ? cicloIAId : null;
        if (opening) document.dispatchEvent(new Event('speed-dial-open'));
      };

      const tipoIALabel = (tipo) => ({ parcial: 'Parcial', resultado: 'Resultado', complementario: 'Compl.' }[tipo] || 'Parcial');

      const mostrarModalTipoIA = ref(false);
      const iaParaCambioTipo = ref(null);
      const filaModalTipoIA = ref(null);

      const abrirModalTipoIA = (ia, fila) => {
        iaParaCambioTipo.value = ia;
        filaModalTipoIA.value = fila || null;
        mostrarModalTipoIA.value = true;
      };

      const confirmarCambioTipoIA = async (tipo) => {
        mostrarModalTipoIA.value = false;
        const ia = iaParaCambioTipo.value;
        iaParaCambioTipo.value = null;
        if (!ia) return;
        try {
          await api.patch(`/encurso/ia/solicitud/${ia.id}/cambiar_tipo/`, { tipo });
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (e) {
          console.error('Error al cambiar tipo IA:', e);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const cerrarModalTipoIA = () => {
        mostrarModalTipoIA.value = false;
        iaParaCambioTipo.value = null;
        filaModalTipoIA.value = null;
      };

      const subirInformeServicioCicloIA = async (event, cicloIA) => {
        const archivo = event.target.files[0];
        const formData = new FormData();
        formData.append('archivo', archivo);
        try {
          await api.post(`/encurso/ia/ciclo/${cicloIA.id}/subir_informe_servicio/`, formData);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 3000);
        }
      };

      const confirmarRevisionCicloIA = async (ia) => {
        const cicloIA = ultimoCicloIA(ia);
        if (!cicloIA) return;
        popupSTIAId.value = null;
        try {
          await api.post(`/encurso/ia/ciclo/${cicloIA.id}/confirmar_revision/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

      const generarPDFCicloIA = async (ia) => {
        const cicloIA = ultimoCicloIA(ia);
        if (!cicloIA) return;
        generandoPDFIAId.value = ia.id;
        popupPDFAdminIAId.value = null;
        try {
          await api.post(`/encurso/ia/ciclo/${cicloIA.id}/generar_pdf/`);
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          const msg = error?.response?.data?.error || 'Error al generar PDF.';
          alert(msg);
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        } finally {
          generandoPDFIAId.value = null;
        }
      };

      const abrirModalFirmaAreaCicloIA = (cicloIA) => {
        cicloIAParaFirmaArea.value = cicloIA;
        mostrarModalFirmaResponsableArea.value = true;
        nextTick(() => limpiarFirma());
      };

      const abrirModalFirmaAPCicloIA = (cicloIA) => {
        cicloIAParaFirmaAP.value = cicloIA;
        mostrarModalFirmaResponsableArea.value = true;
        nextTick(() => limpiarFirma());
      };

      const abrirModalFirmaDireccionCicloIA = (cicloIA) => {
        cicloIAParaFirmaDireccion.value = cicloIA;
        mostrarModalFirmaDireccion.value = true;
        nextTick(() => limpiarFirmaDir());
      };

      const abrirModalFirmaResponsableAreaCiclo = (ciclo) => {
        cicloSeleccionado.value = ciclo;
        mostrarModalFirmaResponsableArea.value = true;
        nextTick(() => limpiarFirma());
      };

      const cerrarModalFirmaResponsableArea = () => {
        mostrarModalFirmaResponsableArea.value = false;
      };

      const confirmarFirmaResponsableAreaCiclo = async () => {
        const isIAAP = !!cicloIAParaFirmaAP.value;
        const isIA = !!cicloIAParaFirmaArea.value;
        const obj = isIAAP ? cicloIAParaFirmaAP.value : (isIA ? cicloIAParaFirmaArea.value : cicloSeleccionado.value);
        if (!obj || (!firmaUsuarioUrl.value && !firmaHecha.value)) return;
        const payload = {};
        if (!firmaUsuarioUrl.value && firmaHecha.value) {
          payload.firma_imagen = signatureCanvas.value.toDataURL('image/png');
        }
        try {
          if (isIAAP) {
            await api.put(`/encurso/ia/ciclo/${obj.id}/confirmar_firma_ap/`, payload);
          } else if (isIA) {
            await api.post(`/encurso/ia/ciclo/${obj.id}/confirmar_firma_area/`, payload);
          } else {
            await api.put(`/encurso/confirmar_firma_responsable_area_ciclo/${obj.id}/`, payload);
          }
          mostrarModalFirmaResponsableArea.value = false;
          firmaHecha.value = false;
          cicloIAParaFirmaArea.value = null;
          cicloIAParaFirmaAP.value = null;
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
        nextTick(() => limpiarFirmaDir());
      };

      const cerrarModalFirmaDireccion = () => {
        mostrarModalFirmaDireccion.value = false;
      };

      const confirmarFirmaDireccionCiclo = async () => {
        const isIA = !!cicloIAParaFirmaDireccion.value;
        const obj = isIA ? cicloIAParaFirmaDireccion.value : cicloSeleccionado.value;
        if (!obj || (!firmaUsuarioUrl.value && !firmaHechaDir.value)) return;
        const payload = {};
        if (!firmaUsuarioUrl.value && firmaHechaDir.value) {
          payload.firma_imagen = signatureCanvasDir.value.toDataURL('image/png');
        }
        try {
          if (isIA) {
            await api.post(`/encurso/ia/ciclo/${obj.id}/confirmar_firma_direccion/`, payload);
          } else {
            await api.put(`/encurso/confirmar_firma_direccion_ciclo/${obj.id}/`, payload);
          }
          mostrarModalFirmaDireccion.value = false;
          firmaHechaDir.value = false;
          cicloIAParaFirmaDireccion.value = null;
          fetchData();
          showSuccessAlert.value = true;
          setTimeout(() => { showSuccessAlert.value = false; }, 3000);
        } catch (error) {
          mostrarModalFirmaDireccion.value = false;
          showErrorAlert.value = true;
          setTimeout(() => { showErrorAlert.value = false; }, 5000);
        }
      };

        // Rechazo Firma AP (Área Principal)
        const mostrarModalRechazoAPIA = ref(false);
        const rechazoAPIANota = ref('');
        const rechazoAPIADestino = ref('area');
        const cicloIAParaRechazoAP = ref(null);

        const abrirModalRechazoAPIA = (cicloIA) => {
          cicloIAParaRechazoAP.value = cicloIA;
          rechazoAPIADestino.value = 'area';
          rechazoAPIANota.value = '';
          mostrarModalRechazoAPIA.value = true;
        };
        const cerrarModalRechazoAPIA = () => {
          mostrarModalRechazoAPIA.value = false;
          cicloIAParaRechazoAP.value = null;
        };
        const confirmarRechazoAPIA = async () => {
          const ciclo = cicloIAParaRechazoAP.value;
          if (!ciclo) return;
          try {
            await api.put(`/encurso/ia/ciclo/${ciclo.id}/rechazar_firma_ap/`, {
              destino: rechazoAPIADestino.value,
              nota_rechazo: rechazoAPIANota.value,
            });
            mostrarModalRechazoAPIA.value = false;
            cicloIAParaRechazoAP.value = null;
            fetchData();
            showSuccessAlert.value = true;
            setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
            mostrarModalRechazoAPIA.value = false;
            cicloIAParaRechazoAP.value = null;
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
        };

        // Rechazo Dirección
        const abrirModalRechazoDireccion = (ciclo) => {
          cicloSeleccionado.value = ciclo;
          cicloIsIA.value = false;
          rechazoDireccionDestino.value = 'st';
          rechazoDireccionNota.value = '';
          mostrarModalRechazoDireccion.value = true;
        };
        const abrirModalRechazoDireccionIA = (cicloIA) => {
          cicloSeleccionado.value = cicloIA;
          cicloIsIA.value = true;
          rechazoDireccionDestino.value = 'st';
          rechazoDireccionNota.value = '';
          mostrarModalRechazoDireccion.value = true;
        };
        const cerrarModalRechazoDireccion = () => {
          mostrarModalRechazoDireccion.value = false;
          cicloIsIA.value = false;
        };
        const abrirModalVerRechazo = (ciclo) => {
          cicloVerRechazo.value = ciclo;
          mostrarModalVerRechazo.value = true;
        };
        const confirmarRechazoDireccion = async () => {
          const ciclo = cicloSeleccionado.value;
          if (!ciclo) return;
          try {
            const url = cicloIsIA.value
              ? `/encurso/ia/ciclo/${ciclo.id}/rechazar_firma_direccion/`
              : `/encurso/rechazar_firma_direccion_ciclo/${ciclo.id}/`;
            await api.put(url, {
              destino: rechazoDireccionDestino.value,
              nota_rechazo: rechazoDireccionNota.value,
            });
            mostrarModalRechazoDireccion.value = false;
            cicloIsIA.value = false;
            fetchData();
            showSuccessAlert.value = true;
            setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
            mostrarModalRechazoDireccion.value = false;
            cicloIsIA.value = false;
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
        };

        // Rechazo Área
        const abrirModalRechazoArea = (ciclo) => {
          cicloSeleccionado.value = ciclo;
          cicloIsIA.value = false;
          rechazoAreaDestino.value = 'st';
          rechazoAreaNota.value = '';
          mostrarModalRechazoArea.value = true;
        };
        const abrirModalRechazoAreaIA = (cicloIA) => {
          cicloSeleccionado.value = cicloIA;
          cicloIsIA.value = true;
          rechazoAreaDestino.value = 'st';
          rechazoAreaNota.value = '';
          mostrarModalRechazoArea.value = true;
        };
        const cerrarModalRechazoArea = () => {
          mostrarModalRechazoArea.value = false;
          cicloIsIA.value = false;
        };
        const abrirModalVerRechazoArea = (ciclo) => {
          cicloVerRechazoArea.value = ciclo;
          mostrarModalVerRechazoArea.value = true;
        };
        const confirmarRechazoArea = async () => {
          const ciclo = cicloSeleccionado.value;
          if (!ciclo) return;
          try {
            const url = cicloIsIA.value
              ? `/encurso/ia/ciclo/${ciclo.id}/rechazar_firma_area/`
              : `/encurso/rechazar_firma_area_ciclo/${ciclo.id}/`;
            await api.put(url, {
              destino: rechazoAreaDestino.value,
              nota_rechazo: rechazoAreaNota.value,
            });
            mostrarModalRechazoArea.value = false;
            cicloIsIA.value = false;
            fetchData();
            showSuccessAlert.value = true;
            setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
            mostrarModalRechazoArea.value = false;
            cicloIsIA.value = false;
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
        };

        // Rechazo ST
        const abrirModalRechazoST = (ciclo) => {
          cicloSeleccionado.value = ciclo;
          cicloIsIA.value = false;
          rechazoSTDestino.value = 'administracion';
          rechazoSTNota.value = '';
          mostrarModalRechazoST.value = true;
        };
        const abrirModalRechazoSTIA = (cicloIA) => {
          cicloSeleccionado.value = cicloIA;
          cicloIsIA.value = true;
          rechazoSTDestino.value = 'administracion';
          rechazoSTNota.value = '';
          mostrarModalRechazoST.value = true;
        };
        const cerrarModalRechazoST = () => {
          mostrarModalRechazoST.value = false;
          cicloIsIA.value = false;
        };
        const abrirModalVerRechazoST = (ciclo) => {
          cicloVerRechazoST.value = ciclo;
          mostrarModalVerRechazoST.value = true;
        };
        const confirmarRechazoST = async () => {
          const ciclo = cicloSeleccionado.value;
          if (!ciclo) return;
          try {
            const url = cicloIsIA.value
              ? `/encurso/ia/ciclo/${ciclo.id}/rechazar_revision_st/`
              : `/encurso/rechazar_revision_st_ciclo/${ciclo.id}/`;
            await api.put(url, {
              destino: rechazoSTDestino.value,
              nota: rechazoSTNota.value,
            });
            mostrarModalRechazoST.value = false;
            cicloIsIA.value = false;
            fetchData();
            showSuccessAlert.value = true;
            setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
            mostrarModalRechazoST.value = false;
            cicloIsIA.value = false;
            showErrorAlert.value = true;
            setTimeout(() => { showErrorAlert.value = false; }, 5000);
          }
        };

        // Historial del circuito
        const mostrarModalHistorial = ref(false);
        const historialCircuitoId = ref(null);
        const historialEventos = ref([]);
        const historialCargando = ref(false);

        const LABEL_ACCIONES = {
          crear_data_servicio:    'Solicitud de servicio creada',
          crear_legajo:           'Legajo creado',
          guardar_factura:        'Factura adjuntada',
          subir_informe_area:     'Informe de área subido',
          reemplazar_informe_area:'Informe de área reemplazado',
          subir_registros:        'Registro de ensayo adjuntado',
          crear_orden_servicio:   'Orden de servicio generada',
          subir_formato_institucional: 'Formato institucional subido',
          revision_st:            'Revisión ST confirmada',
          rechazar_revision_st:   'Revisión ST rechazada',
          firma_area:             'Firma de Área confirmada',
          rechazar_firma_area:    'Firma de Área rechazada',
          firma_direccion:        'Firma de Dirección confirmada',
          rechazar_firma_direccion:'Firma de Dirección rechazada',
          archivar_circuito:      'Circuito archivado',
        };

        const labelAccion = (accion) => LABEL_ACCIONES[accion] || accion;

        const formatHistorialFecha = (fechaStr) => {
          if (!fechaStr) return '';
          const d = new Date(fechaStr);
          return d.toLocaleString('es-AR', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit',
          });
        };

        const abrirModalHistorial = async (fila) => {
          historialCircuitoId.value = fila.nro_circuito;
          historialEventos.value = [];
          historialCargando.value = true;
          mostrarModalHistorial.value = true;
          try {
            const res = await api.get(`/encurso/historial_circuito/${fila.nro_circuito}/`);
            historialEventos.value = res.data;
          } catch (e) {
            console.error('Error al cargar historial:', e);
          } finally {
            historialCargando.value = false;
          }
        };

        const cerrarModalHistorial = () => {
          mostrarModalHistorial.value = false;
        };

        // Archivar
        const motivoArchivar = ref('');
        const notaArchivar = ref('');

        const motivosArchivo = [
          { value: 'exito',                label: 'Finalizado con éxito' },
          { value: 'falta_pago',           label: 'Empresa no abonó' },
          { value: 'vencimiento_muestras', label: 'Vencimiento del plazo de muestras' },
          { value: 'desistimiento',        label: 'Desistimiento del cliente' },
          { value: 'otro',                 label: 'Otro' },
        ];

        const alertasPlazos = computed(() => {
          const alertas = [];
          for (const fila of filas.value) {
            // Plazo de pago vencido → Administración
            if (isAdministracion.value && fila.plazo_pago !== '' && fila.plazo_pago !== null && Number(fila.plazo_pago) <= 0 && !pagoEsCompleto(fila.pago)) {
              alertas.push({
                key: `pago_${fila.nro_circuito}`,
                nro_circuito: fila.nro_circuito,
                mensaje: 'El plazo de pago venció y el pago no está completo.',
                motivo: 'falta_pago',
                tipo: 'pago',
              });
            }
            // Plazo de muestras vencido → ST
            if (isServiciosTecnologicos.value && fila.plazo_muestras !== '' && fila.plazo_muestras !== null && Number(fila.plazo_muestras) <= 0 && fila.estado_recepcion !== 'total') {
              alertas.push({
                key: `muestras_${fila.nro_circuito}`,
                nro_circuito: fila.nro_circuito,
                mensaje: 'El plazo de recepción de muestras venció.',
                motivo: 'vencimiento_muestras',
                tipo: 'muestras',
              });
            }
          }
          return alertas;
        });

        const abrirModalArchivar = (fila) => {
          numeroCircuitoGlobal.value = fila.nro_circuito;
          motivoArchivar.value = '';
          notaArchivar.value = '';
          mostrarModalArchivar.value = true;
        };

        const abrirModalArchivarConMotivo = (alerta) => {
          numeroCircuitoGlobal.value = alerta.nro_circuito;
          motivoArchivar.value = alerta.motivo;
          notaArchivar.value = '';
          mostrarModalArchivar.value = true;
        };

        const extenderPlazoPorAlerta = (alerta) => {
          const fila = filas.value.find(f => f.nro_circuito === alerta.nro_circuito);
          if (!fila) return;
          if (alerta.tipo === 'pago') abrirModalPlazoPago(fila);
          else if (alerta.tipo === 'muestras') abrirModalPlazoMuestras(fila);
        };

        const cerrarModalArchivar = () => {
          mostrarModalArchivar.value = false;
        };

        const enviarArchivar = async () => {
          if (!motivoArchivar.value) return;
          if (motivoArchivar.value === 'otro' && !notaArchivar.value.trim()) return;
          const nroCircuito = numeroCircuitoGlobal.value;
          try {
              await api.put(
                  `/encurso/archivar_circuito/${nroCircuito}/`,
                  { motivo_archivo: motivoArchivar.value, nota_archivo: notaArchivar.value }
              );
              mostrarModalArchivar.value = false;
              fetchData();
              showSuccessAlert.value = true;
              setTimeout(() => { showSuccessAlert.value = false; }, 3000);
          } catch (error) {
              console.error('Error al archivar:', error);
              mostrarModalArchivar.value = false;
              showErrorAlert.value = true;
              setTimeout(() => { showErrorAlert.value = false; }, 5000);
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
        const imprimirOS = () => { window.print(); };

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
        plazoCriticidad,
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
        isTecnologicoOrDireccion,
        isTecnologicoOrDireccionOrArea,
        userAreaTematica,
        userAreaTematicaFormatted,
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
        emailFacturaDataServicio,
        emailInformeTecnicoDataServicio,
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
        presupuestosDisponibles,
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
        versionLegajo,
        configFormularioLegajo,
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
        labelPago,
        labelPagoBadgeClass,
        pagoEsCompleto,
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
        nuevoRangoOS,
        plazoOS,
        solicitanteOS,
        servicioOS,
        muestrasOS,
        observacionesOS,
        versionOS,
        configFormularioOS,
        crearOrdenServicio,
        mostrarModalCrearOrdenServicio,
        osReadOnly,
        osModificadaActual,
        abrirModalCrearOrdenServicio,
        cerrarModalCrearOrdenServicio,
        aceptarOrdenServicio,
        abrirOrdenServicio,
        mostrarModalOrdenServicio,
        cerrarModalOrdenServicio,
        cambiarPlazoOrdenServicio,
        abrirModalPlazoOrdenServicio,
        cerrarModalPlazoOrdenServicio,
        mostrarModalPlazoOrdenServicio,
        osMaxParciales,
        osPlazosArr,
        sincronizarPlazosOS,
        guardarConfigParciales,
        plazoCiclo,
        // Ciclos de Informe
        mostrarModalTipoCiclo,
        mostrarClipParaNuevoParcial,
        mostrarBotonAgregarIA,
        puedeCrearNuevoCiclo,
        crearCiclo,
        popupInformeAreaId,
        hayParcialesPrevios, filaModalTipoCiclo,
        togglePopupInformeArea,
        eliminarInformeAreaCiclo,
        seleccionarArchivoInformeAreaCiclo,
        reemplazarInformeAreaCiclo,
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
        catalogoAranceles,
        busquedaArancel,
        arancelAdicional,
        cantidadAdicional,
        arancelFiltrado,
        isServicioOSSeleccionado,
        toggleServicioOS,
        seleccionarArancel,
        agregarArancel,
        quitarServicioSeleccionado,
        inter_areaTematicaOptions,
        nuevaSolicitudInterarea,
        obtenerServicios,
        abrirModalCrearSolicitudInterArea, filaParaCrearIA,
        cerrarModalCrearSolicitudInterArea,
        mostrarModalCrearSolicitudInterArea,
        crearSolicitudInterArea,
        labsDisponiblesIA,
        labsSeleccionadosIA,
        labsPickerAbierto,
        labsPickerTriggerRef,
        labsPickerStyle,
        abrirLabsPicker,
        erroresIA,
        iaDebeParpadear,
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
        solicitudIASeleccionada,
        // Helpers de estado inter-área
        ultimoCicloIA,
        esPrincipalDeIA,
        esInterAreaDeIA,
        esMiAreaEsteFila,
        esSoloInterAreaEnFila,
        mostrarInformeAreaEnFila,
        // Acciones inter-área
        subirInformeAreaCicloIA,
        subirRegistroEnsayoCicloIA,
        eliminarRegistroEnsayoCicloIA,
        // Acciones área principal
        confirmarInterareaPrincipal,
        confirmarCorreccionInformeAP,
        confirmarCorreccionRegistrosAP,
        // Rechazo
        mostrarModalRechazarIA,
        abrirModalRechazarIA,
        cerrarModalRechazarIA,
        rechazarInterareaPrincipal,
        tipoRechazoIA,
        comentarioRechazoIA,
        // Ver comentario de rechazo
        mostrarModalComentarioRechazo,
        cerrarModalComentarioRechazo,
        verComentarioRechazoIA,
        comentarioRechazoVer,
        tipoRechazoVer,
        eliminarAdjuntoInformeInterarea,
        // Administracion - Informe Servicio
        subirInformeServicioCiclo, confirmarTipoCambioAdmin,
        generarPDFServicioCiclo,
        generandoPDFId,
        abrirModalCorreccionesCiclo,
        cerrarModalCorreccionesInformeServicio,
        mostrarModalCorreccionesInformeServicio,
        correcciones,
        corregirCiclo,
        // Servicios Tecnologicos - Revision
        popupSTId,
        togglePopupST,
        popupAreaId,
        togglePopupArea,
        popupDirId,
        togglePopupDir,
        popupFormatoId,
        togglePopupFormato,
        popupPDFAdminId,
        togglePopupPDFAdmin,
        pendienteFactura,
        formatMontoARS,
        onMontoManualInput,
        subirFacturaModoMonto,
        subirFacturaMontoManual,
        popupFacturaId,
        togglePopupFactura,
        mostrarModalFacturacion,
        datosFacturacion,
        filaFacturacion,
        abrirDatosFacturacion,
        mostrarModalSubirFactura,
        subirFacturaData,
        abrirSubirFactura,
        confirmarSubirFactura,
        eliminarFacturaDeModal,
        seleccionarArchivoSTCorregido,
        registrarCorreccionST,
        cerrarModalCorreccionST,
        confirmarRevisionST,
        stReemplazadoIds,
        mostrarModalCorreccionST,
        textoCorreccionST,
        abrirModalVerCorrecciones,
        cerrarModalVerCorrecciones,
        mostrarModalVerCorrecciones,
        cicloVerCorrecciones,
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
        abrirModalFirmaAreaCicloIA,
        abrirModalFirmaAPCicloIA,
        abrirModalFirmaDireccionCicloIA,
        cicloIAParaFirmaArea,
        cicloIAParaFirmaAP,
        cicloIAParaFirmaDireccion,
        subirInformeServicioCicloIA,
        confirmarRevisionCicloIA,
        generarPDFCicloIA,
        popupSTIAId, popupPDFAdminIAId, popupAreaIAId, popupAPIAId, popupDirIAId,
        popupConfirmIAId, popupCorreccionIAId, popupFormatoIAId,
        togglePopupCorreccionIA,
        generandoPDFIAId,
        cicloIsIA,
        togglePopupSTIA, togglePopupPDFAdminIA, togglePopupAreaIA, togglePopupAPIA, togglePopupDirIA,
        togglePopupConfirmIA, togglePopupFormatoIA,
        tipoIALabel,
        mostrarModalTipoIA, abrirModalTipoIA, confirmarCambioTipoIA, cerrarModalTipoIA, filaModalTipoIA,
        cerrarModalFirmaResponsableArea,
        mostrarModalFirmaResponsableArea,
        confirmarFirmaResponsableAreaCiclo,
        firmaUsuarioUrl,
        signatureCanvas, firmaHecha,
        startSignature, drawSignature, stopSignature,
        startSignatureTouch, drawSignatureTouch, limpiarFirma,
        // Direccion - Firma
        abrirModalFirmaDireccionCiclo,
        cerrarModalFirmaDireccion,
        mostrarModalFirmaDireccion,
        confirmarFirmaDireccionCiclo,
        signatureCanvasDir, firmaHechaDir,
        startSignatureDir, drawSignatureDir, stopSignatureDir,
        startSignatureDirTouch, drawSignatureDirTouch, limpiarFirmaDir,
        // Rechazo Dirección
        mostrarModalRechazoDireccion, mostrarModalVerRechazo, cicloVerRechazo,
        rechazoDireccionDestino, rechazoDireccionNota,
        abrirModalRechazoDireccion, cerrarModalRechazoDireccion,
        abrirModalVerRechazo, confirmarRechazoDireccion,
        // Rechazo Área
        mostrarModalRechazoArea, mostrarModalVerRechazoArea, cicloVerRechazoArea,
        rechazoAreaDestino, rechazoAreaNota,
        abrirModalRechazoArea, cerrarModalRechazoArea,
        abrirModalVerRechazoArea, confirmarRechazoArea,
        // Rechazo ST
        mostrarModalRechazoST, mostrarModalVerRechazoST, cicloVerRechazoST,
        rechazoSTDestino, rechazoSTNota,
        abrirModalRechazoST, cerrarModalRechazoST,
        abrirModalVerRechazoST, confirmarRechazoST,
        abrirModalRechazoSTIA,
        // Rechazo Área IA
        abrirModalRechazoAreaIA,
        // Rechazo Firma AP (Área Principal)
        mostrarModalRechazoAPIA, rechazoAPIANota, rechazoAPIADestino,
        abrirModalRechazoAPIA, cerrarModalRechazoAPIA, confirmarRechazoAPIA,
        // Rechazo Dirección IA
        abrirModalRechazoDireccionIA,
        // Archivar
        abrirModalArchivar,
        cerrarModalArchivar,
        imprimirDataServicio,
        imprimirLegajo,
        imprimirOS,
        fechaLegajoFormateada,
        mostrarModalArchivar,
        enviarArchivar,
        motivoArchivar,
        notaArchivar,
        motivosArchivo,
        alertasPlazos,
        abrirModalArchivarConMotivo,
        extenderPlazoPorAlerta,
        mostrarModalHistorial,
        historialCircuitoId,
        historialEventos,
        historialCargando,
        abrirModalHistorial,
        cerrarModalHistorial,
        labelAccion,
        formatHistorialFecha,
        hayActualizaciones,
        refreshCargando,
        aplicarActualizaciones,
        manualRefresh,
        silenciado,
        toggleSilencio,
        // Conceptos de Facturación
        catalogoConceptos,
        conceptosDS,
        conceptoSeleccionadoDS,
        conceptosCatalogoDisponibles,
        guardandoConceptosDS,
        mensajeConceptoDS,
        agregarConceptoDS,
        quitarConceptoDS,
        guardarConceptosDS,
      };
    },
  };
</script>
  
<style scoped>

  /* Ocupa todo el alto disponible que le da el flex parent (EnCursoView) */
  .pt-inner {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  /* Contenedor de tabla: crece para llenar el espacio restante bajo los filtros */
  .table-scroll-wrapper {
    flex: 1;
    min-height: 0;
    overflow-x: auto;
    overflow-y: scroll; /* siempre visible para evitar layout shift al aparecer */
  }

  /* Headers pegados al tope al hacer scroll vertical */
  /* Usamos box-shadow INSET en lugar de border para evitar el bug border-collapse + sticky */
  .sticky-thead th {
    position: sticky;
    z-index: 20;
    background-color: #026290;
    border: none !important;
  }

  /* Fila 1: pegada al tope — separador inferior inset (no empuja fila 2) */
  .sticky-thead tr:first-child th {
    top: 0;
    height: 42px;
    z-index: 25;
    background-color: #026290;
    box-shadow: inset 0 -1px 0 rgba(255,255,255,0.15);
  }

  /* Fila 2: pegada debajo de fila 1 — todos los th tienen separador vertical sutil */
  .sticky-thead tr:nth-child(2) th {
    top: 42px;
    z-index: 20;
    background-color: #026290;
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.15), inset 0 -2px 0 #014f73;
  }

  /* Separador de sección (más prominente) en fila 1 */
  .sticky-thead tr:first-child th.add-border-right {
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.4), inset 0 -1px 0 rgba(255,255,255,0.15);
  }

  /* Separador de sección (más prominente) en fila 2 */
  .sticky-thead tr:nth-child(2) th.add-border-right {
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.4), inset 0 -2px 0 #014f73;
  }

  /* Agrega un borde vertical a la derecha de las subcolumnas en el cuerpo */
  .add-border-right {
    border-right: 1px solid #dee2e6;
  }

  .table tbody tr:nth-child(even) {
    background-color: #f0f6fa;
  }

  .table tbody tr:hover {
    background-color: #daeaf3;
  }

  /* Badge circular para plazos de pago y muestras */
  .plazo-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 30px;
    height: 30px;
    border-radius: 50%;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0 4px;
  }

  .plazo-badge.plazo-alerta {
    background: #fff3cd;
    color: #856404;
  }

  .plazo-badge.plazo-urgente {
    background: #f8d7da;
    color: #842029;
    animation: plazo-pulso 1.6s ease-out infinite;
  }

  @keyframes plazo-pulso {
    0%   { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.45); }
    60%  { box-shadow: 0 0 0 7px rgba(220, 53, 69, 0); }
    100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
  }

  /* Inter-area modal — OS checkboxes */
  .ia-os-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: 160px;
    overflow-y: auto;
    padding: 6px 8px;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    background: #fafafa;
  }
  .ia-os-item {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 2px 0;
    font-size: 0.83rem;
    margin: 0;
  }
  .ia-os-item input[type="checkbox"] { flex-shrink: 0; cursor: pointer; }
  .ia-os-label { line-height: 1.3; }

  /* Inter-area modal — arancel search */
  .ia-arancel-resultados {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    max-height: 160px;
    overflow-y: auto;
    background: white;
  }
  .ia-arancel-item {
    padding: 6px 10px;
    font-size: 0.82rem;
    cursor: pointer;
    border-bottom: 1px solid #f0f0f0;
  }
  .ia-arancel-item:last-child { border-bottom: none; }
  .ia-arancel-item:hover { background: #e8f4fd; }

  /* Inter-area modal — selected list */
  .ia-seleccionados-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .ia-seleccionado-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 8px;
    background: #e8f4fd;
    border-radius: 6px;
    font-size: 0.82rem;
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

  /* Fila de ciclo - altura fija para alinear iconos entre columnas */
  .ciclo-row {
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
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
    border: 1px solid #ccc;
    border-radius: 6px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    min-width: 180px;
    padding: 4px 0;
  }

  .attach-popup-row {
    display: flex;
    align-items: center;
    padding: 4px 8px;
    gap: 4px;
  }

  .attach-popup-label {
    flex: 1;
    font-size: 11px;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .ia-btn {
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

  .ia-btn:hover { background: #e8f4f8; }

  .ia-btn-del { color: #dc3545; }
  .ia-btn-del:hover { background: #fde8ea; }

  .attach-popup-corr-divider {
    height: 1px;
    background: #e8e8e8;
    margin: 2px 0;
  }
  .attach-popup-corr-item {
    display: flex;
    align-items: flex-start;
    padding: 3px 8px;
    gap: 4px;
  }

  /* Speed dial ST revisión */
  .st-sd-cell {
    position: relative;
    display: inline-flex;
    justify-content: center;
    align-items: center;
  }
  .st-sd-trigger {
    position: relative;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 1.5px solid #026290;
    background: white;
    color: #026290;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: background 0.15s, color 0.15s;
  }
  .st-sd-trigger:hover { background: #026290; color: white; }
  .st-sd-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #ffc107;
  }
  .st-sd-dial {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    z-index: 200;
  }
  .st-sd-opcion {
    position: absolute;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    border: 2px solid #026290;
    border-radius: 50%;
    color: #026290;
    cursor: pointer;
    transform: rotate(var(--rotation)) translate(62px) rotate(calc(-1 * var(--rotation)));
    transition: transform 0.25s ease, background-color 0.15s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  }
  .st-sd-opcion i { font-size: 14px; cursor: pointer; }
  .st-sd-opcion:hover {
    background-color: #026290;
    color: white;
    transform: rotate(var(--rotation)) translate(70px) rotate(calc(-1 * var(--rotation)));
  }
  .st-sd-opcion--ok { border-color: #198754; color: #198754; }
  .st-sd-opcion--ok:hover { background-color: #198754; color: white; }
  .st-sd-opcion--generando {
    opacity: 0.75;
    pointer-events: none;
    border-color: #dc3545 !important;
    color: #dc3545 !important;
  }
  @keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }
  .st-sd-opcion--warn { border-color: #ffc107; color: #b57a00; }
  .st-sd-opcion--warn:hover { background-color: #ffc107; color: white; }
  .st-sd-opcion--danger { border-color: #dc3545; color: #dc3545; }
  .st-sd-opcion--danger:hover { background-color: #dc3545; color: white; }
  .st-sd-badge--rechazo { background: #dc3545; }
  .st-sd-badge--rechazo-area { background: #ffc107; }
  .st-sd-badge--confirmar {
    background: #198754;
    animation: pulse-confirmar 1.4s ease-in-out infinite;
  }
  @keyframes pulse-confirmar {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(1.5); }
  }
  /* Texto "↑ Confirmar" bajo el trigger para ST */
  .st-confirmar-hint {
    position: absolute;
    top: calc(100% + 4px);
    left: 50%;
    transform: translateX(-50%);
    font-size: 9px;
    color: #198754;
    font-weight: 700;
    white-space: nowrap;
    pointer-events: none;
  }
  /* Texto "Pend. confirmación" bajo el reloj para no-ST */
  .st-pend-label {
    font-size: 9px;
    color: #6c757d;
    white-space: nowrap;
  }
  .st-nota-correcciones { font-size: 16px; color: #9c7cc7; cursor: pointer; }
  .st-nota-correcciones:hover { color: #7b5fa0; }
  .firma-canvas-wrapper {
    border: 2px solid #ced4da;
    border-radius: 6px;
    background: #fafafa;
    cursor: crosshair;
    overflow: hidden;
  }
  .firma-canvas-wrapper canvas {
    display: block;
    width: 100%;
    height: 160px;
    touch-action: none;
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

  .revision-history-wrapper {
    padding: 0 1rem 0.5rem;
  }

  .revision-history-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.72rem;
    margin-top: 12px;
  }

  .revision-history-table th,
  .revision-history-table td {
    border: 1px solid #aaa;
    padding: 3px 6px;
    text-align: left;
    vertical-align: middle;
  }

  .revision-history-table th {
    background-color: #e8f0f7 !important;
    color: #333 !important;
    font-weight: 600;
  }

  .revision-title {
    text-align: center !important;
    font-weight: 700;
    background-color: #cfe0f0 !important;
    color: #1a3a5c !important;
    padding: 4px !important;
    font-size: 0.75rem;
  }

  /* Inter-área: layout de fila por solicitud */
  .ia-row {
    flex-direction: column;
    align-items: center;
    gap: 1px;
    height: 50px;
    padding: 2px 0;
  }

  .ia-sp {
    height: 50px;
    visibility: hidden;
    display: flex;
  }

  .ia-area-label {
    color: #555;
    font-size: 0.72rem;
    word-break: break-word;
    overflow-wrap: break-word;
    line-height: 1.1;
  }

  .ia-estado {
    display: inline-flex;
    align-items: center;
    font-size: 1rem;
  }

  .ia-papelito {
    font-size: 1rem;
  }

  /* Animación de titilado para estados que requieren revisión */
  @keyframes ia-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .ia-blink i {
    animation: ia-pulse 1.2s ease-in-out infinite;
  }

  @keyframes ia-row-glow {
    0%, 100% { background-color: transparent; box-shadow: none; }
    50% { background-color: rgba(2, 98, 144, 0.13); box-shadow: 0 0 0 2px rgba(2, 98, 144, 0.18); }
  }
  .ia-row-pendiente {
    animation: ia-row-glow 1.6s ease-in-out infinite;
    border-radius: 5px;
  }

  @keyframes pago-pulse-anim {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.65; transform: scale(1.08); }
  }
  .pago-pulse {
    animation: pago-pulse-anim 1.2s ease-in-out infinite;
  }

  /* Botones de tipo de rechazo */
  .ia-tipo-btn {
    text-align: center;
    min-width: 90px;
  }

  .concepto-box {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    min-height: 42px;
  }

  .rango-lab-display {
    display: flex;
    align-items: baseline;
    gap: 6px;
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 10px 14px;
  }

  .rango-lab-num {
    font-size: 1.25rem;
    font-weight: 700;
    color: #026290;
    letter-spacing: 0.5px;
  }

  .rango-lab-anio {
    font-size: 0.95rem;
    color: #6c757d;
    font-weight: 500;
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
  border: 1.5px solid #026290;
  background: white;
  color: #026290;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  padding: 0;
  transition: background 0.15s, color 0.15s;
}
.ds-icon-btn:hover {
  background: #026290;
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

/* Botón de refresh manual */
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.spin-icon { animation: spin 0.7s linear infinite; }

/* Modal Historial — timeline */
.historial-timeline { position: relative; }
.historial-timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #dee2e6;
}
.historial-item {
  display: flex;
  gap: 14px;
  margin-bottom: 20px;
  position: relative;
}
.historial-dot {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #0d6efd;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #dee2e6;
  margin-top: 2px;
  z-index: 1;
}
.historial-contenido { flex: 1; }
.historial-accion { font-weight: 600; font-size: 0.9rem; }
.historial-desc { font-size: 0.82rem; margin-top: 2px; }
.historial-meta { font-size: 0.78rem; }

/* Modal Archivar — opciones de motivo */
.motivo-archivo-option {
  display: flex;
  align-items: center;
  padding: 10px 14px;
  border: 1.5px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.15s, background-color 0.15s;
  font-size: 0.9rem;
  user-select: none;
}
.motivo-archivo-option:hover {
  border-color: #adb5bd;
  background-color: #f8f9fa;
}
.motivo-archivo-option.selected {
  border-color: #dc3545;
  background-color: #fff5f5;
  font-weight: 500;
}
.motivo-archivo-option input[type="radio"] {
  accent-color: #dc3545;
}

/* Lab picker — grilla estilo almanaque */
.lab-cal-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 7px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  background: #fff;
  font-size: 0.85rem;
  cursor: pointer;
  color: #495057;
  text-align: left;
  gap: 8px;
  transition: border-color 0.12s;
}
.lab-cal-trigger:hover,
.lab-cal-trigger--open {
  border-color: #026290;
}
.lab-cal-overlay {
  position: fixed;
  inset: 0;
  z-index: 8999;
}
.lab-cal-popup {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
  padding: 12px 14px;
  overflow-y: auto;
}
.lab-cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #dee2e6;
}
.lab-cal-close {
  background: none;
  border: none;
  font-size: 0.8rem;
  cursor: pointer;
  color: #6c757d;
  padding: 2px 6px;
  border-radius: 4px;
  line-height: 1;
}
.lab-cal-close:hover {
  background: #f0f0f0;
  color: #212529;
}
.lab-cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
.lab-cal-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 500;
  cursor: pointer;
  user-select: none;
  color: #212529;
  transition: background 0.1s, color 0.1s;
  min-width: 0;
}
.lab-cal-cell:hover {
  background: #d4edf7;
  color: #026290;
}
.lab-cal-cell--selected {
  background: #026290;
  color: #fff;
}
.lab-cal-cell--selected:hover {
  background: #015070;
}
.lab-cal-footer {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #dee2e6;
  font-size: 0.8rem;
  color: #495057;
}
.lab-cal-confirm {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #dee2e6;
}
.lab-cal-trigger--error {
  border-color: #dc3545 !important;
}
.ia-error-msg {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 4px;
}
.ia-fieldset-disabled {
  opacity: 0.45;
  pointer-events: none;
}

/* ── Filter bar ─────────────────────────────────────────── */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 4px 8px;
  flex-wrap: wrap;
}
.filter-ctrl {
  height: 34px;
  padding: 0 28px 0 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.84rem;
  color: #495057;
  background-color: #fff;
  appearance: auto;
  cursor: pointer;
  outline: none;
}
.filter-ctrl:focus {
  border-color: #026290;
  box-shadow: 0 0 0 2px rgba(2, 98, 144, 0.15);
}
.filter-date-range {
  display: flex;
  align-items: center;
  height: 34px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  background: #fff;
  padding: 0 10px;
  gap: 7px;
}
.filter-date-range:focus-within {
  border-color: #026290;
  box-shadow: 0 0 0 2px rgba(2, 98, 144, 0.15);
}
.fdr-label {
  font-size: 0.78rem;
  color: #6c757d;
  white-space: nowrap;
  user-select: none;
}
.fdr-sep {
  width: 1px;
  height: 55%;
  background: #ced4da;
  flex-shrink: 0;
}
.fdr-input {
  border: none;
  outline: none;
  font-size: 0.83rem;
  color: #495057;
  background: transparent;
  height: 100%;
  padding: 0;
  min-width: 110px;
}
.filter-clear {
  height: 34px;
  padding: 0 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.83rem;
  background: #fff;
  color: #6c757d;
  cursor: pointer;
  white-space: nowrap;
}
.filter-clear:hover {
  background: #f8f9fa;
  color: #343a40;
  border-color: #adb5bd;
}
</style>
  