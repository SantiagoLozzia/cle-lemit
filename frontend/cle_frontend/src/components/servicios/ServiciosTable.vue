<template>
    <div>
      <h2>Tabla de Servicios</h2>
      <table>
        <thead>
          <tr>
            <th>Columna 1</th>
            <th>Columna 2</th>
            <!-- Agrega más encabezados de columna según sea necesario -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="(arancel, index) in aranceles" :key="index">
            <td>{{ arancel.columna1 }}</td>
            <td>{{ arancel.columna2 }}</td>
            <!-- Agrega más celdas según sea necesario -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        aranceles: [
          { columna1: 'Valor1', columna2: 'ValorA' },
          { columna1: 'Valor2', columna2: 'ValorB' },
          // Agrega más objetos según sea necesario
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* Agrega estilos CSS según sea necesario */
  </style>
  