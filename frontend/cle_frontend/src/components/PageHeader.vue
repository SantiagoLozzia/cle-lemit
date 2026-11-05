<template>
  <div class="page-header">
    <div class="page-header-icon">
      <i :class="icon"></i>
    </div>
    <div class="page-header-text">
      <h1 class="page-header-title">{{ title }}</h1>
      <span v-if="subtitle !== undefined" class="page-header-subtitle">{{ subtitle }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title:    { type: String, required: true },
    subtitle: { type: String, default: undefined },
    icon:     { type: String, default: 'bi bi-table' },
  },
};
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: #fff;
  border-left: 4px solid #026290;
  border-radius: 6px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-bottom: 16px;
}

.page-header-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #026290;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
}

.page-header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.page-header-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a2332;
  margin: 0;
  line-height: 1.2;
}

.page-header-subtitle {
  font-size: 0.78rem;
  color: #6c757d;
  line-height: 1;
}
</style>
