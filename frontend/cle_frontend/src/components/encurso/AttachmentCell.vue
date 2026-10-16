<template>
  <!-- Sin archivos -->
  <template v-if="!files || files.length === 0">
    <div v-if="canUpload" class="att-empty">
      <label :for="inputId" style="cursor:pointer;"><i :class="emptyIcon"></i></label>
      <input :id="inputId" style="display:none;" type="file" @change="onUpload">
    </div>
    <i v-else class="bi bi-stopwatch"></i>
  </template>

  <!-- Con archivos -->
  <div v-else class="att-cell" :class="{ 'is-open': isOpen }" @click.stop>
    <button class="att-trigger" @click="toggle" :title="files.length + ' archivo(s)'">
      <i :class="isOpen ? 'bi bi-x' : fileIcon"></i>
      <span v-if="!isOpen && files.length > 1" class="att-badge">{{ files.length }}</span>
    </button>

    <div v-if="isOpen" class="att-popup">
      <div v-for="f in files" :key="f.id" class="att-file-row">
        <span class="att-file-name" :title="shortName(f.archivo)">{{ shortName(f.archivo) }}</span>
        <button class="att-btn att-btn-view" @click="viewFile(f.archivo)" title="Ver">
          <i class="bi bi-eye"></i>
        </button>
        <button v-if="canDelete" class="att-btn att-btn-del" @click="onDelete(f.id)" title="Eliminar">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <div v-if="canUpload" class="att-add-row">
        <label :for="inputId + '-add'" class="att-add-btn">
          <i class="bi bi-plus-circle"></i> Agregar
        </label>
        <input :id="inputId + '-add'" style="display:none;" type="file" @change="onUpload">
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
export default {
  name: 'AttachmentCell',
  props: {
    files:     { type: Array, default: () => [] },
    canUpload: { type: Boolean, default: false },
    canDelete: { type: Boolean, default: false },
    inputId:   { type: String, required: true },
    fileIcon:  { type: String, default: 'bi bi-file-earmark-word' },
    emptyIcon: { type: String, default: 'bi bi-paperclip' },
  },
  emits: ['upload', 'delete'],
  setup(props, { emit }) {
    const isOpen = ref(false);
    const instanceId = Symbol();

    const close = () => { isOpen.value = false; };

    const closeOthersHandler = (e) => {
      if (e.detail !== instanceId) isOpen.value = false;
    };

    const toggle = () => {
      if (!isOpen.value) {
        document.dispatchEvent(new CustomEvent('att-cell-open', { detail: instanceId }));
      }
      isOpen.value = !isOpen.value;
    };

    const shortName = (archivo) => {
      const name = archivo ? archivo.split('/').pop() : '';
      return name.length > 28 ? name.slice(0, 25) + '...' : name;
    };
    const viewFile = (archivo) => {
      window.open(window.location.origin + '/media/' + archivo, '_blank');
    };
    const onUpload = (e) => { emit('upload', e); close(); };
    const onDelete = (id) => { emit('delete', id); close(); };
    onMounted(() => {
      document.addEventListener('click', close);
      document.addEventListener('att-cell-open', closeOthersHandler);
    });
    onUnmounted(() => {
      document.removeEventListener('click', close);
      document.removeEventListener('att-cell-open', closeOthersHandler);
    });
    return { isOpen, toggle, shortName, viewFile, onUpload, onDelete };
  }
};
</script>

<style scoped>
.att-empty { display: inline-block; }

.att-cell {
  position: relative;
  display: inline-block;
}

.att-trigger {
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
  font-size: 13px;
  padding: 0;
  transition: background 0.15s, color 0.15s;
}

.att-cell.is-open .att-trigger {
  background: #026290;
  color: white;
}

.att-badge {
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

.att-popup {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.18);
  min-width: 210px;
  z-index: 200;
  padding: 4px 0;
}

.att-file-row {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  gap: 4px;
  border-bottom: 1px solid #f0f0f0;
}

.att-file-row:last-of-type { border-bottom: none; }

.att-file-name {
  flex: 1;
  font-size: 11px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
}

.att-btn {
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

.att-btn:hover { background: #e8f4f8; }

.att-btn-del { color: #dc3545; }
.att-btn-del:hover { background: #fde8ea; }

.att-add-row {
  display: flex;
  align-items: center;
  padding: 6px 8px 4px;
  border-top: 1px solid #e8e8e8;
}

.att-add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #026290;
  cursor: pointer;
  font-weight: 500;
}

.att-add-btn:hover { text-decoration: underline; }
</style>
