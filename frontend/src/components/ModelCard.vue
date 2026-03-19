<template>
  <el-card
    class="model-card"
    :class="{ 'is-current': model.isCurrent }"
    @click="$emit('click', model)"
    shadow="hover"
  >
    <div class="card-content">
      <div class="model-id">{{ model.modelId }}</div>
      <div class="provider-name">{{ getProviderName(model.providerId) }}</div>
      <div v-if="model.isCurrent" class="current-badge">使用中</div>
    </div>
  </el-card>
</template>

<script setup>
import { PRESET_PROVIDERS } from '../stores/provider'

defineProps({
  model: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const getProviderName = (providerId) => {
  for (const provider of Object.values(PRESET_PROVIDERS)) {
    if (provider.providerId === providerId) {
      return provider.name
    }
  }
  return providerId
}
</script>

<style scoped>
.model-card {
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid #dcdfe6;
}

.model-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.model-card.is-current {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9eb 0%, #e1f3d8 100%);
}

.card-content {
  position: relative;
  padding: 10px;
}

.model-id {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
  word-break: break-all;
}

.provider-name {
  font-size: 12px;
  color: #909399;
}

.current-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: #67c23a;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
}
</style>
