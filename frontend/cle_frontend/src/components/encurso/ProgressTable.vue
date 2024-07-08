<template>
     <div class="alert alert-success" role="alert" v-if="showSuccessAlert">
      ¡Éxito! Se ha creado correctamente.
    </div>
    <div class="alert alert-danger" role="alert" v-if="showErrorAlert">
      ¡Error! Ha ocurrido un problema al guardar. Por favor, inténtalo de nuevo.
    </div>

    <div>
      <table class="table">
        <thead>
          <tr>
            <th colspan="6" class="add-border-right">Solicitud de Servicio</th>
            <th colspan="6" class="add-border-right">Legajo</th>
            <th colspan="3" class="add-border-right">Recepcion</th>
            <th colspan="3" class="add-border-right">Orden de Servicio</th>
            <th colspan="3" class="add-border-right">Informe de Area</th>
            <th colspan="4" class="add-border-right">Inter Area</th>
            <th colspan="1" class="add-border-right">Informe Area</th>
            <th colspan="1" class="add-border-right">Administracion</th>
            <th colspan="1" class="add-border-right">Servicios Tecnologicos</th>
            <th colspan="1" class="add-border-right">Responsable Area</th>
            <th colspan="1" class="add-border-right">Direccion</th>
            <th colspan="1">Archivo</th>
          </tr>
          <tr>
            <!-- Subcolumnas de Solicitud de Servicio -->
            <th>N°</th>
            <th>Fecha</th>
            <th>Area Tematica</th>
            <th>ST-01 Presupuesto</th>
            <th>Data Servicio</th>
            <th class="add-border-right">ST-02 Solicitud</th>
            <!-- Subcolumnas de Legajo -->
            <th>N°</th>
            <th>Fecha</th>
            <th>Legajo</th>
            <th>Factura</th>
            <th>Pago</th>
            <th class="add-border-right">Plazo</th>
            <!-- Subcolumnas de Recepcion -->
            <th>ST-03 Recepcion</th>
            <th>Muestras</th>
            <th class="add-border-right">Plazo</th>
            <!-- Subcolumnas de Orden de Servicio -->
            <th>Fecha</th>
            <th>ST-05 Orden</th>
            <th class="add-border-right">Plazo</th>
            <!-- Subcolumnas de Informe de Area -->
            <th>Fecha</th>
            <th>Solicitante</th>
            <th class="add-border-right">Informe Area</th>
            <!-- Subcolumnas de Inter Area -->
            <th>Fecha</th>
            <th>Solicitud</th>
            <th>Inter-Area</th>
            <th class="add-border-right">Informe</th>
            <!-- Subcolumnas de Informe Area -->
            <th class="add-border-right">Estado</th>
            <!-- Subcolumnas de Administracion -->
            <th class="add-border-right">Formato</th>
            <!-- Subcolumnas de Servicios Tecnologicos -->
            <th class="add-border-right">Revision</th>
            <!-- Subcolumnas de Responsable Area -->
            <th class="add-border-right">Firma</th>
            <!-- Subcolumnas de Direccion -->
            <th class="add-border-right">Firma</th>
            <!-- Subcolumnas de Archivo -->
            <th class="add-border-right">Archivar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(fila, index) in filas" :key="index">
            <!-- N° Solicitud de Servicio -->
            <td>{{ fila.nro_dataServicio }}</td>
            <!-- Fecha Solicitud -->
            <td class="fecha-columna">{{ fila.fecha_dataServicio }}</td>
            <!-- Area Tematica -->
            <td>{{ fila.area_tematica }}</td>
            <!-- ST-01 Presupuesto -->
            <td>{{ fila.nro_presupuesto }}</td>
            <!-- Data Servicio -->
            <td><i class="bi bi-file-earmark-check-fill text-success"  style="cursor: pointer;" @click="abrirDataServicio(fila.nro_dataServicio)"></i></td>
            <!-- ST-02 Solicitud -->
            <td class="add-border-right">
              <!-- Verificar si adjunto_solicitud está vacío -->
              <template v-if="fila.adjunto_solicitudServicio === null">
                <!-- Si no hay adjunto, mostrar el botón de cargar archivo -->
                <div class="custom-file">
                  <label class="custom-file-label"  style="cursor: pointer;" :for="'fileInputAdjuntoSolicitud-' + index">
                    <i class="bi bi-paperclip"></i>
                  </label>
                  <input :id="'fileInputAdjuntoSolicitud-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoSolicitud($event, fila.nro_dataServicio)">
                </div>
              </template>
              <template v-else>
                <i class="bi bi-file-earmark-text" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_solicitudServicio)"></i>
              </template>
            </td>
            <!-- N° Legajo -->
            <td>{{ fila.nro_legajo }}</td>
            <!-- Fecha Legajo -->
            <td class="fecha-columna">{{ fila.fecha_legajo }}</td>
            <!-- Archivo Legajo -->
            <td>
              <template v-if="fila.dataServicio_completo && !fila.nro_legajo">
                  <i class="bi bi-plus-square"  style="cursor: pointer;" @click="obtenerRangoLab(fila.nro_circuito)"></i>
              </template>
              <template v-else-if="fila.dataServicio_completo && fila.nro_legajo">
                  <i class="bi bi-file-earmark-check-fill text-success"  style="cursor: pointer;" @click="abrirLegajo(fila.nro_circuito)"></i>
              </template>
              <template v-else>
                
              </template>
            </td>
            <!-- Factura -->
            <td>
              <template v-if="fila.nro_legajo && !fila.adjunto_factura">
                  <!-- Si nro_legajo está completo y adjunto_factura está vacío, mostrar el botón de cargar archivo -->
                  <div class="custom-file">
                      <!-- El icono de Bootstrap es clicleable y activa el input de tipo file -->
                      <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoFactura-' + index">
                          <i class="bi bi-paperclip"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputAdjuntoFactura-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoFactura($event, fila.nro_legajo, fila.nro_circuito)">
                  </div>
              </template>
              <template v-else-if="fila.nro_legajo && fila.adjunto_factura">
                  <!-- Si nro_legajo está completo y adjunto_factura está completo, mostrar el icono del archivo -->
                  <i class="bi bi-file-earmark-text" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_factura)"></i>
              </template>
              <template v-else>
                  <!-- Si nro_legajo está vacío, entonces adjunto_factura también debe estar vacío -->
              </template>
            </td>
            <!-- Pago -->
            <td>
                <div v-if="fila.pago !== undefined && fila.pago !== null">
                    <!-- Mostrar el valor de fila.pago -->
                    <span v-if="fila.pago === 0" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">0%</span>
                    <span v-else-if="fila.pago === 50" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">50%</span>
                    <span v-else-if="fila.pago === 100" @click="abrirModalPagoLegajo(fila)" style="cursor: pointer;">100%</span>
                </div>
            </td>
            <!-- Plazo Pago -->
            <td class="add-border-right">
              <span @click="abrirModalPlazoPago(fila)" style="cursor: pointer;">
                {{ fila.plazo_pago }}
              </span>
            </td>

            <!-- Recepcion -->

            <!-- ST-03 Recepcion -->
            <td>
              <template v-if="(fila.nros_remitos === null) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <i class="bi bi-plus-square" style="cursor: pointer;" @click="abrirModalRemito(fila)"></i>
              </template>
              <template v-if="(fila.remitos !== null) && (fila.estado_recepcion == 'parcial' || fila.estado_recepcion == 'total')">
                {{ fila.nros_remitos }}
              </template>
            </td>
            <!-- Muestras -->
            <td>
              <div>
                <span v-if="(fila.pago == 50 ||fila.pago == 100) && (fila.estado_recepcion !== undefined && fila.estado_recepcion !== null)">
                    <!-- Mostrar el valor de fila.estado_recepcion -->
                    <span v-if="fila.estado_recepcion === 'sin_llegar'" class="no-wrap-column" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Sin Llegar</span>
                    <span v-else-if="fila.estado_recepcion === 'parcial'" @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Parcial</span>
                    <span v-else-if="fila.estado_recepcion === 'total'"  @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">Total</span>
                </span>
                <span v-else @click="abrirModalEstadoMuestras(fila)" style="cursor: pointer;">&nbsp;</span>
              </div>
            </td>
            <!-- Plazo Recepcion -->
            <td class="add-border-right">
              <div>
                <span v-if="fila.legajo_completo" @click="abrirModalPlazoMuestras(fila)" style="cursor: pointer;">
                  {{ fila.plazo_muestras }}
                </span>
                <span v-else>
                  <!-- Este span estará vacío -->
                </span>
              </div>
            </td>

            <!-- Orden de Servicio -->

            <!-- Fecha Orden -->
            <td>{{ fila.fecha_ordenServicio }}</td>
            <!-- ST-05 Orden -->
            <td>
              <template v-if="(fila.ordenServicio_completo  === '' || fila.ordenServicio_completo === false ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <i class="bi bi-plus-square" style="cursor: pointer;" @click="abrirModalCrearOrdenServicio(fila)"></i>
              </template>
              <template v-if="(fila.ordenServicio_completo  === true ) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total')">
                <i class="bi bi-file-check"  style="cursor: pointer;" @click="abrirOrdenServicio(fila)"></i>
              </template>
            </td>
            <!-- Plazo Orden -->
            <td class="add-border-right">
              <template v-if="(fila.estado_recepcion == 'parcial' || fila.estado_recepcion == 'total')">
                <span @click="abrirOrdenServicio(fila)" style="cursor: pointer;">
                {{ fila.plazo_estimado }}
              </span>
              </template>
              <template v-else>
                
              </template>
            </td>

            <!-- Informe de Area -->

            <!-- Fecha Informe -->
            <td>{{ fila.fecha_informeArea }}</td>
            <!-- Solicitante -->
            <td>{{ fila.nombre_solicitante }}</td>
            <!-- Informe Area -->
            <td class="add-border-right">
              <template v-if="fila.adjunto_informeArea === null">
                  <!-- Si fia.completo está completo, mostrar el botón de cargar archivo -->
                  <div class="custom-file">
                      <!-- El icono de Bootstrap es clicleable y activa el input de tipo file -->
                      <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeArea-' + index">
                          <i class="bi bi-paperclip"></i>
                      </label>
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <input :id="'fileInputAdjuntoInformeArea-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeArea($event, fila.nro_circuito)">
                  </div>
              </template>
              <template v-else-if="fila.adjunto_informeArea">
                {{console.log('tendria que figurar el icono del archivo adjunto')}}
                  <!-- Si adjunto_informeArea está completo, mostrar el icono del archivo -->
                  <i class="bi bi-file-earmark-text" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_informeArea)"></i>
              </template>
              <template v-else>
                  <!-- Si nro_legajo está vacío, entonces adjunto_factura también debe estar vacío -->
              </template>
            </td>

            <!-- Inter Area -->

            <!-- Fecha inter area -->
            <td>{{ fila.fecha_solicitudInterarea }}</td>
            <!-- Solicitud inter area -->
            <td>
              <!-- <template v-if="fila.completo = true"> -->
                  <!-- Si fia.completo está completo, mostrar el botón de cargar archivo -->
                  <!-- <div class="custom-file"> -->
                      <!-- El icono de Bootstrap es clicleable y activa el input de tipo file -->
                      <!-- <label class="custom-file-label" style="cursor: pointer;" :for="'fileInputAdjuntoInformeArea-' + index"> -->
                          <!-- <i class="bi bi-paperclip"></i> -->
                      <!-- </label> -->
                      <!-- El input de tipo file está oculto visualmente pero se activa al hacer clic en el icono -->
                      <!-- <input :id="'fileInputAdjuntoInformeArea-' + index" style="opacity:0; height:0; width:0;" type="file" class="custom-file-input" @change="cargarAdjuntoInformeArea($event, fila.nro_informeArea)"> -->
                  <!-- </div> -->
              <!-- </template> -->
              <!-- <template v-else-if="fila.adjunto_informeArea"> -->
                  <!-- Si adjunto_informeArea está completo, mostrar el icono del archivo -->
                  <!-- <i class="bi bi-file-earmark-text" style="cursor: pointer;" @click="abrirArchivo(fila.adjunto_informeArea)"></i> -->
              <!-- </template> -->
              <!-- <template v-else> -->
                  <!-- Si nro_legajo está vacío, entonces adjunto_factura también debe estar vacío -->
              <!-- </template> -->
              <i class="bi bi-plus-square"></i>
              <!-- <i class="bi bi-file-check"></i> -->
            </td>

            <!-- Nombre inter area -->
            <td>{{ fila.inter_areaTematica }}</td>
            <!-- Informe inter area -->
            <td class="add-border-right"><i class="bi bi-paperclip"></i></td>

            <!-- Informe Area -->

            <!-- Estado informe -->
            <td class="add-border-right">{{ fila.estado_informeArea }}</td>

            <!-- Formato -->
            <td class="add-border-right"><i class="bi bi-paperclip"></i></td>
            <!-- Revision -->
            <td class="add-border-right">{{ fila.revision }}</td>
            <!-- Responsable Area -->
            <td class="add-border-right">{{ fila.firma_area }}</td>
            <!-- Direccion -->
            <td class="add-border-right">{{ fila.firma_direccion }}</td>
            <!-- Archivo -->
            <td>
              <button @click="enviarArchivar" class="btn btn-link"><i class="bi bi-archive-fill"></i></button>
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
              <h1 class="modal-title fs-5 fw-bold">Servicio N° {{ nroDataServicio }}</h1>
              <div class="mb-3">
                  <label for="fechaDataServicio" class="form-label text-left">Fecha:</label>
                  <input v-model="fechaDataServicio" type="date" readonly class="form-control" id="fechaDataServicio" name="fechaDataServicio" required />
              </div>

              <div class="mb-3">
                <label for="obraDataServicio" class="form-label text-left">Obra:</label>
                <input v-model="obraDataServicio" type="text" class="form-control" id="obraDataServicio" name="obraDataServicio" readonly required />
              </div>
              
              <div class="mb-3">
                <label for="cantNumLabsDataServicio" class="form-label text-left">Cantidad Num Laboratorios:</label>
                <input v-model="cantNumLabsDataServicio" type="text" class="form-control" id="cantNumLabsDataServicio" name="cantNumLabsDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="plazoEstimadoDataServicio" class="form-label text-left">Plazo Estimado:</label>
                <input v-model="plazoEstimadoDataServicio" type="text" class="form-control" id="plazoEstimadoDataServicio" name="plazoEstimadoDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="muestrasDataServicio" class="form-label text-left">Muestras:</label>
                <input v-model="muestrasDataServicio" type="text" class="form-control" id="muestrasDataServicio" name="muestrasDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="nroPresupuestoDataServicio" class="form-label text-left">N° Presupuesto:</label>
                <input v-model="nroPresupuestoDataServicio" type="text" class="form-control" id="nroPresupuestoDataServicio" name="nroPresupuestoDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="areaDataServicio" class="form-label text-left">Area Tematica:</label>
                <input v-model="areaDataServicio" type="text" class="form-control" id="areaDataServicio" name="areaDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="solicitanteDataServicio" class="form-label text-left">Solicitante:</label>
                <input v-model="solicitanteDataServicio" type="text" class="form-control" id="solicitanteDataServicio" name="solicitanteDataServicio" readonly required />
              </div>

              <div class="mb-3">
                <label for="arancelDataServicio" class="form-label text-left">Arancel:</label>
                <input v-model="arancelDataServicio" type="text" class="form-control" id="arancelDataServicio" name="arancelDataServicio" readonly required />
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
              <label for="plazoMuestras">Ingrese Nuevo Numero de Remito:</label>
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
      <div class="modal-dialog">
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


   
    
</template>
  
<script>
  import { onMounted, ref} from 'vue';
  import axios from 'axios';

  export default {
    components: {
    },
    setup() {
      
      const filas = ref([]);
      
      const nuevoLegajo = ref({
        fecha_legajo: new Date().toISOString().substring(0, 10), // Obtener la fecha actual en formato "YYYY-MM-DD",
        rangos_laboratorios: '',
        pago: 0,
        plazo_pago: 30,
        nuevo_ultimo_numero: '',
        nro_circuito: null,
      });
      console.log('PRIMER NUEVO LEGAJO', nuevoLegajo)

      const nuevoRecepcion = ref ({
        nros_remitos: '',
        estado_recepcion: '',
        plazo_muestras: 30,
      })

      const nroLegajo = ref();
      const fechaLegajo = ref();
      const rangosLaboratorios = ref();
      const nombreSolicitante = ref();
      const añoLegajo = ref();

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
       
      const mostrarModalCrearLegajo = ref(false);
      const mostrarModalDataServicio = ref(false);
      const mostrarModalLegajo = ref(false);
      const showSuccessAlert = ref(false);
      const showErrorAlert = ref(false);
      const mostrarModalPagoLegajo = ref(false);
      const mostrarModalPlazoPago = ref(false);
      const mostrarModalRemito = ref(false);
      const mostrarModalEstadoMuestras = ref(false);
      const mostrarModalPlazoMuestras = ref(false);
      // const estadoMuestrasNuevo = ref(null);
      const numeroCircuitoParaRecepcion = ref(null);
      
      const mostrarModalCrearOrdenServicio = ref(false);
      const mostrarModalOrdenServicio = ref(false);
      
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

      //methods

      const fetchData = () => {
        axios.get('api/encurso/obtener_todoencurso/')
          .then(response => {
            const data = response.data;
            console.log('DATA:', data)
            console.log('NRO DATA SERVICIO', data.solicitudes[0].nro_dataServicio)
            
            // Iterar sobre las solicitudes
            data.solicitudes.forEach(solicitud => {
              // Buscar los objetos correspondientes
              const legajoCorrespondiente = data.legajos.find(legajo => legajo.nro_circuito === solicitud.nro_circuito);
              const recepcionCorrespondiente = data.recepciones.find(recepciones => recepciones.nro_circuito === solicitud.nro_circuito);
              const ordenCorrespondiente = data.ordenes_servicio.find(ordenes_servicio => ordenes_servicio === solicitud.nro_circuito);
              const informeAreaCorrespondiente = data.informes_area.find(informes_area => informes_area === solicitud.nro_circuito);

              // Construir la fila de la tabla combinando datos de solicitudes, legajos, recepciones, etc.
              const fila = {
                nro_dataServicio: solicitud.nro_dataServicio,
                fecha_dataServicio: solicitud.fecha_dataServicio,
                area_tematica: solicitud.area_tematica,
                nro_presupuesto: solicitud.nro_presupuesto,
                adjunto_solicitudServicio: solicitud.adjunto_solicitudServicio,
                nro_circuito: solicitud.nro_circuito,
                dataServicio_completo: solicitud.completo,
                nro_legajo: legajoCorrespondiente ? legajoCorrespondiente.nro_legajo: '',
                fecha_legajo: legajoCorrespondiente ? legajoCorrespondiente.fecha_legajo: '',
                adjunto_factura: legajoCorrespondiente ? legajoCorrespondiente.adjunto_factura: '',
                pago: legajoCorrespondiente ? legajoCorrespondiente.pago: '',
                plazo_pago: legajoCorrespondiente ? legajoCorrespondiente.plazo_pago: '',
                legajo_completo: legajoCorrespondiente ? legajoCorrespondiente.completo: '',
                nros_remitos: recepcionCorrespondiente ? recepcionCorrespondiente.nros_remitos: '',
                estado_recepcion: recepcionCorrespondiente ? recepcionCorrespondiente.estado_recepcion: '',
                plazo_muestras: recepcionCorrespondiente ? recepcionCorrespondiente.plazo_muestras: '',
                fecha_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.fecha_ordenServicio: '',
                plazo_estimado: solicitud.plazo_estimado,
                nro_ordenServicio: ordenCorrespondiente ? ordenCorrespondiente.nro_ordenServicio: '',
                ordenServicio_completo: ordenCorrespondiente ? ordenCorrespondiente.completo: '',
                fecha_informeArea: informeAreaCorrespondiente ? informeAreaCorrespondiente.fecha_informeArea: '',
                nombre_solicitante: solicitud.nombre_solicitante,
              };
                console.log('fechaaaaaaaa:', fila.fecha_ordenServicio)
                console.log('data prueba', fila)


              filas.value.push(fila);
            });
          })
          .catch(error => {
            console.error('Error al obtener datos:', error);
          });
      };

      // Función para formatear el campo area_tematica
      const formatAreaTematica = (areaTematica) => {
        return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
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

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroDataServicio.value = nro_dataServicio;
                  fechaDataServicio.value = fecha_dataServicio;
                  obraDataServicio.value = obra;
                  cantNumLabsDataServicio.value = cant_numLabs;
                  plazoEstimadoDataServicio.value = plazo_estimado;
                  muestrasDataServicio.value = muestras;
                  nroPresupuestoDataServicio.value = nro_presupuesto;
                  areaDataServicio.value = formatAreaTematica(area_tematica);
                  solicitanteDataServicio.value = nombre_solicitante ;
                  arancelDataServicio.value = formatArancel(arancel_presupuesto);
                  observacionesDataServicio.value = observaciones ;

                  // Mostrar el modal para mostrar los detalles del legajo
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
      const abrirLegajo = (nro_circuito) => {
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
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        // console.log('Pago Legajo en abrirModalPagoLegajo',fila.pago)
        // console.log('Numero Circuito en abrirModalPagoLegajo',numeroCircuitoParaRecepcion.value)
        mostrarModalPagoLegajo.value = true;
      };

      const cerrarModalPagoLegajo = () => {
        mostrarModalPagoLegajo.value = false;
      };

      const guardarPagoLegajo = async (pagoLegajoNuevo) => {
        // console.log('numero Circuito en guardarPagoLegajo', numeroCircuitoParaRecepcion.value)
        // console.log('pagoLegajoNuevo en guardarPagoLegajo', pagoLegajoNuevo)
        const nro_circuito = numeroCircuitoParaRecepcion.value;
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
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        console.log('Plazo de Pago actual en abrirModalPlazoPago',fila.plazo_pago)
        console.log('Numero Circuito en abrirModalPlazoPago',numeroCircuitoParaRecepcion.value)
        mostrarModalPlazoPago.value = true;
      };

      const cerrarModalPlazoPago = () => {
        mostrarModalPlazoPago.value = false;
      };

      const cambiarPlazoPago = async (plazoPagoNuevo) => {
        const nro_circuito = numeroCircuitoParaRecepcion.value;
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
        const urlCompleta = 'http://localhost:8000' + adjunto;
        window.open(urlCompleta, '_blank');
      };

      const formatArancel = (arancel) => {
          // Verificar si arancel es numérico
          if (!isNaN(arancel)) {
              // Si es numérico, formatearlo con el signo $ y separación de miles
              return '$ ' + arancel.toLocaleString(); // Utilizamos toLocaleString() para la separación de miles
          } else {
              // Si no es numérico, devolver el valor sin formato
              return arancel;
          }
      };


      // RECEPCION

      // Recepcion - ST03 - Recepcion (Remitos)
      const abrirModalRemito = (fila) => {
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        // console.log('Plazo Muestras actual en abrirModalPlazoMuestras',fila.plazo_muestras)
        // console.log('Numero Circuito en abrirModalPlazoMuestras',numeroCircuitoParaRecepcion.value)
        mostrarModalRemito.value = true;
      };

      const cerrarModalRemito = () => {
        mostrarModalRemito.value = false;
      };

      const cambiarRemito = async (remitoNuevo) => {
        // console.log('Numero Circuito en cambiarRemito', numeroCircuitoParaRecepcion.value)
        // console.log('remitoNuevo en cambiarRemito', remitoNuevo)
        const nro_circuito = numeroCircuitoParaRecepcion.value;
        try {
          // Realizar la petición para actualizar el numero de remito en la base de datos
          const response = await axios.put(`/api/encurso/cambiar_remito/${nro_circuito}/`, {
            nros_remitos: remitoNuevo
          });

          // Verificar si la actualización fue exitosa
          if (response.status === 200) {
            console.log('Numero de Remito actualizado correctamente:', remitoNuevo);
            mostrarModalRemito.value = false;  // Cerrar el modal
            showSuccessAlert.value = true;
            
            setTimeout(() => {
                  showSuccessAlert.value = false;
                }, 3000);

          } else {
            mostrarModalRemito.value = false;
            console.error('Error al actualizar el numero de Remito:', response.statusText);
            showErrorAlert.value = true;
            setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
          }
        } catch (error) {
          mostrarModalRemito.value = false;
          console.error('Error al cambiar el numero de Remito:', error);
          showErrorAlert.value = true;
          setTimeout(() => {
            showErrorAlert.value = false;
          }, 5000);
        }
      };

      // Recepcion - Estado Muestras
      const abrirModalEstadoMuestras = (fila) => {
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        // console.log('Estado Recepcion en abrirModalEstadoMuestras',fila.estado_recepcion)
        // console.log('Numero Circuito en abrirModalEstadoMuestras',numeroCircuitoParaRecepcion.value)
        mostrarModalEstadoMuestras.value = true;
      };

      const cerrarModalEstadoMuestras = () => {
        mostrarModalEstadoMuestras.value = false;
      };

      const guardarEstadoMuestras = async (estadoMuestrasNuevo) => {
        // console.log('numero Circuito en guardarEstadoMuestras', numeroCircuitoParaRecepcion.value)
        // console.log('estadoMuestrasNuevo en guardarEstadoMuestras', estadoMuestrasNuevo)
        const nro_circuito = numeroCircuitoParaRecepcion.value;
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
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        // console.log('Plazo Muestras actual en abrirModalPlazoMuestras',fila.plazo_muestras)
        // console.log('Numero Circuito en abrirModalPlazoMuestras',numeroCircuitoParaRecepcion.value)
        mostrarModalPlazoMuestras.value = true;
      };

      const cerrarModalPlazoMuestras = () => {
        mostrarModalPlazoMuestras.value = false;
      };

      const cambiarPlazoMuestras = async (plazoMuestrasNuevo) => {
        // console.log('Numero Circuito en cambiarPlazoMuestras', numeroCircuitoParaRecepcion.value)
        // console.log('plazoMuestrasNuevo en cambiarPlazoMuestras', plazoMuestrasNuevo)
        const nro_circuito = numeroCircuitoParaRecepcion.value;
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

      // OS - Fecha

      // OS - Archivo
      // const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];  
      // console.log('VARIABLE CRSTOKEN=', csrfToken)

      // Función watch para monitorear cambios en fila.pago y fila.estado_recepcion
      // watch(filas, (nuevasFilas) => {
      //   nuevasFilas.forEach((fila) => {
      //     if ((fila.pago === 50 || fila.pago === 100) && (fila.estado_recepcion === 'parcial' || fila.estado_recepcion === 'total') && (fila.fecha_ordenServicio === 'null')) {
      
      const abrirModalCrearOrdenServicio = (fila) => {
        numeroCircuitoParaRecepcion.value = fila.nro_circuito;
        // console.log('Estado Recepcion en abrirModalEstadoMuestras',fila.estado_recepcion)
        // console.log('Numero Circuito en abrirModalEstadoMuestras',numeroCircuitoParaRecepcion.value)
        mostrarModalCrearOrdenServicio.value = true;
      };

      const cerrarModalCrearOrdenServicio = () => {
        mostrarModalCrearOrdenServicio.value = false;
      };
      
      const crearOrdenServicio = async () => {
          const nro_circuito = numeroCircuitoParaRecepcion.value;
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


      const abrirOrdenServicio = (nro_circuito) => {
          axios.get(`api/encurso/obtener_orden_servicio/${nro_circuito}/`)
              .then(response => {
                  // Obtener los datos del legajo de la respuesta
                  const { nro_ordenServicio, fecha_ordenServicio, area_tematica, nro_legajo, rangos_laboratorios, plazo_estimado, nombre_solicitante,servicio_solicitado, muestras, observaciones } = response.data;

                  // Asignar los datos del legajo a variables en el contexto del componente
                  nroOS.value = nro_ordenServicio;
                  fechaOS.value = fecha_ordenServicio;
                  areaOS.value = area_tematica;
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
        console.log('CERRAR MODAL') 
        mostrarModalOrdenServicio.value = false;
      };

      // OS - Plazo

      // INFORME AREA

      // Informe Area - Adjunto
      const cargarAdjuntoInformeArea = (event, nro_circuito) => {
          const archivoSeleccionado = event.target.files[0]; // Obtener el archivo seleccionado
          const formData = new FormData();
          formData.append('archivo', archivoSeleccionado);
          formData.append('nroCircuito', nro_circuito); // Agregar el número de circuito

          // Realizar una petición POST al servidor para guardar el archivo
          axios.post('api/encurso/guardar_adjunto_informearea/', formData)
              .then(response => {
                  console.log('Archivo guardado exitosamente:', response.data);
              })
              .catch(error => {
                  console.error('Error al guardar el archivo:', error);
              });
      };

      return {
        filas,
        nuevoLegajo,
        nuevoRecepcion,
        triggerFileInput,
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
        cargarAdjuntoSolicitud,
        cargarAdjuntoFactura,
        abrirArchivo,
        obtenerRangoLab,
        abrirLegajo,
        nroLegajo,
        fechaLegajo,
        rangosLaboratorios,
        nombreSolicitante,
        añoLegajo,
        mostrarModalCrearLegajo,
        mostrarModalDataServicio,
        mostrarModalLegajo,
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
        showSuccessAlert,
        showErrorAlert,
        // formatAreaTematica,
        formatArancel,
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
        mostrarModalCrearOrdenServicio,
        abrirModalCrearOrdenServicio,
        cerrarModalCrearOrdenServicio,
        abrirOrdenServicio,
        mostrarModalOrdenServicio,
        cerrarModalOrdenServicio,
        cargarAdjuntoInformeArea,
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
        validarNumeroEntero,
        crearOrdenServicio,
      };
    },
  };
</script>
  
<style scoped>

  .table th,
  .table td {
      padding: 15px;
      vertical-align: middle;
  }

  /* Agrega un borde vertical a la derecha de las subcolumnas específicas */
  .add-border-right {
      border-right: 1px solid gainsboro; /* Establece el borde derecho */
  }

  .fecha-columna {
        white-space: nowrap; /* Evita que el contenido de la columna se divida en múltiples líneas */
        overflow: hidden; /* Oculta el contenido excedente */
        text-overflow: ellipsis; /* Agrega puntos suspensivos (...) al final del texto que no se muestra */
  }

  .bi {
        font-size: 24px; /* Aquí puedes ajustar el tamaño según tu preferencia */
  }

  .radio-options input[type="radio"] {
    display: inline-block;
    margin-right: 5px;
  }

  .radio-options label {
    font-size: 10px;
  }

  /* .modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
  } */
  
  /* .modal.show {
    display: flex;
    align-items: center;
    justify-content: center;
  } */

  .menu {
    position: absolute;
    z-index: 1;
    background-color: #fff;
    border: 1px solid #ced4da;
    padding: 5px;
    margin-top: -50px;
    border-radius: 5px;
  }
  .menu select {
    width: auto;
    padding: 6px 25px;
    font-size: 14px;
  }
  
  .btn-group {
    display: inline-block; /* Para mostrar los botones en línea */
  }

  /* .modal-footer {
  display: flex;
  justify-content: space-between;
  } */

  .radio-options {
    text-align: left;
  }

  .radio-options input[type="radio"] {
    display: inline-block;
    margin-right: 10px; /* Aumenta el espacio entre las opciones */
  }

  .radio-options label {
    font-size: 12px; /* Ajusta el tamaño de la letra */
  }

  /* .modal-content {
    text-align: center;
  } */

  .modal-footer .btn {
    width: 45%; /* Establece el ancho de los botones */
  }

  .no-wrap-column {
    white-space: nowrap;
  }
</style>
  