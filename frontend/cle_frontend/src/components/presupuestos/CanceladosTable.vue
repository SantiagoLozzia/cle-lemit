<template>
    <div class="cancelados-container">
      <div class="title-container">
        <h2>Presupuestos Cancelados</h2>
      </div>
  
      <div class="table-container">
        <table class="table presupuestos-table">
          <thead>
            <tr>
              <th>Nro</th>
              <th>Fecha</th>
              <th>Solicitante</th>
              <th>Area Tematica</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(presupuesto, index) in presupuestos" :key="index">
              <td>{{ presupuesto.nro_presupuesto }}</td>
              <td>{{ presupuesto.fecha }}</td>
              <td>{{ presupuesto.nombre_solicitante }}</td>
              <td>{{ presupuesto.area_tematica }}</td>
              <td>{{ presupuesto.estado_presupuesto }}</td>
              <td>
                <div class="acciones">
                  <button @click="mostrarMenu(index)" class="btn btn-link"><i class="bi bi-arrow-right-square"></i></button>
                  <!-- Menú desplegable para cambiar el estado -->
                  <div v-if="presupuesto.mostrarMenu" class="menu">
                    <select v-model="presupuesto.nuevoEstado" class="form-select">
                        <option value="en_espera">En Espera</option>
                        <option value="rechazado">Rechazado</option>
                        <option value="modificado">Modificado</option>
                        <option value="actualizado">Actualizado</option>
                    </select>
                    <button @click="cambiarEstado(presupuesto)" class="btn btn-primary">Guardar</button>
                    <button @click="cerrarMenu(index)" class="btn btn-danger">✖</button> 
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
        const presupuestos = ref([]);
  
        const fetchPresupuestos = async () => {
            try {
            const response = await axios.get('http://localhost:8000/api/presupuestos/cancelados/');
            // Formatear los datos antes de asignarlos a presupuestos.value
            presupuestos.value = response.data.map(presupuesto => ({
                ...presupuesto,
                area_tematica: formatAreaTematica(presupuesto.area_tematica),
                estado_presupuesto: formatEstadoPresupuesto(presupuesto.estado_presupuesto),
                mostrarMenu: false, // Agregar propiedad para controlar la visibilidad del menú
                nuevoEstado: '' // Nuevo estado seleccionado
            }));
            } catch (error) {
            console.error('Error al obtener presupuestos:', error);
            }
        };
  
        // Función para formatear el campo area_tematica
        const formatAreaTematica = (areaTematica) => {
            return areaTematica.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        };
  
        // Función para formatear el campo estado_presupuesto
        const formatEstadoPresupuesto = (estadoPresupuesto) => {
            return estadoPresupuesto.replace(/_/g, ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        };
  
        // Función para mostrar u ocultar el menú desplegable
        const mostrarMenu = (index) => {
            presupuestos.value.forEach((presupuesto, i) => {
            if (i === index) {
                presupuesto.mostrarMenu = !presupuesto.mostrarMenu;
            } else {
                presupuesto.mostrarMenu = false;
            }
            });
        };
  
        const cerrarMenu = (index) => {
            presupuestos.value[index].mostrarMenu = false;
            // Restablecer el nuevo estado seleccionado
            presupuestos.value[index].nuevoEstado = '';
        };
  
        const cambiarEstado = async (presupuesto) => {
            try {
                // Realizar la petición para actualizar el estado del presupuesto en la base de datos
                const response = await axios.put(`http://localhost:8000/api/presupuestos/actualizar_estado/${presupuesto.nro_presupuesto}/`, {
                estado_presupuesto: presupuesto.nuevoEstado
                });
        
                // Verificar si la actualización fue exitosa
                if (response.status === 200) {
                console.log('Estado del presupuesto actualizado correctamente:', presupuesto.nuevoEstado);
                // Recargar la página para reflejar los cambios actualizados
                location.reload();
                } else {
                console.error('Error al actualizar el estado del presupuesto:', response.statusText);
                }
            } catch (error) {
                console.error('Error al cambiar el estado del presupuesto:', error);
            }
        };
  
        onMounted(fetchPresupuestos); // Utilizamos onMounted para llamar a fetchPresupuestos en la creación del componente
    
        return { 
          presupuestos, 
          mostrarMenu, 
          cambiarEstado, 
          cerrarMenu 
        }; 
    }
  };
  </script>
  
  <style scoped>
  .title-container {
    position: relative;
    top: 50px;
  }
  .table-container {
    margin-top: 80px;
  }
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
  .acciones {
    position: relative;
  }
  </style>
  