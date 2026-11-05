<template>
  <div class="iso-header-wrapper">
    <table class="iso-header-table">
      <tbody>
        <tr>
          <td rowspan="2" class="iso-logo-cell">
            <img :src="logoLemit" alt="LEMIT" class="iso-logo-img" />
          </td>
          <td class="iso-nombre-cell">{{ config.nombre }}</td>
          <td rowspan="2" class="iso-meta-cell">
            <div><strong>Código:</strong> {{ config.codigo }}</div>
            <div><strong>Versión:</strong> {{ versionDoc }}</div>
            <div><strong>Fecha:</strong> {{ fechaVersion }}</div>
          </td>
        </tr>
        <tr>
          <td class="iso-codigo-cell">{{ config.codigo }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { computed } from 'vue';
import logoLemit from '@/assets/logo_lemit_modal.png';

export default {
  name: 'ISOHeader',
  props: {
    config: {
      type: Object,
      default: () => ({ nombre: '', codigo: '', version_actual: '', fecha_version_actual: '', revisiones: [] }),
    },
    versionDoc: {
      type: String,
      default: '',
    },
  },
  setup(props) {
    const fechaVersion = computed(() => {
      if (!props.config || !props.config.revisiones || !props.versionDoc) {
        return props.config?.fecha_version_actual || '';
      }
      const rev = props.config.revisiones.find(r => r.version === props.versionDoc);
      return rev ? rev.fecha : (props.config.fecha_version_actual || '');
    });
    return { logoLemit, fechaVersion };
  },
};
</script>

<style scoped>
.iso-header-wrapper {
  margin-bottom: 8px;
}

.iso-header-table {
  width: 100%;
  border-collapse: collapse;
  border: 1.5px solid #333;
  font-size: 0.75rem;
}

.iso-header-table td {
  border: 1px solid #555;
  padding: 4px 8px;
  vertical-align: middle;
  text-align: left;
}

.iso-logo-cell {
  width: 100px;
  text-align: center !important;
  padding: 4px !important;
}

.iso-logo-img {
  width: 90px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.iso-nombre-cell {
  text-align: center !important;
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.3px;
}

.iso-codigo-cell {
  text-align: center !important;
  font-size: 0.72rem;
  color: #444;
}

.iso-meta-cell {
  width: 155px;
  font-size: 0.72rem;
  line-height: 1.6;
}

@media print {
  .iso-logo-img {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }
}
</style>
