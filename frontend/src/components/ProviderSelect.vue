<template>
  <div class="provider-select">
    <h3>选择提供商</h3>
    <div class="preset-buttons">
      <el-button
        v-for="(provider, key) in providers"
        :key="key"
        :type="selectedProvider === key ? 'primary' : 'default'"
        @click="$emit('select', key)"
        size="large"
      >
        {{ provider.name }}
      </el-button>
    </div>
    <el-button
      type="success"
      :type="selectedProvider === 'custom' ? 'success' : 'default'"
      @click="$emit('select-custom')"
      size="large"
      style="margin-top: 10px;"
    >
      + 添加新提供商
    </el-button>
  </div>
</template>

<script setup>
import { PRESET_PROVIDERS } from '../stores/provider'

defineProps({
  selectedProvider: {
    type: String,
    default: null
  }
})

defineEmits(['select', 'select-custom'])

const providers = PRESET_PROVIDERS
</script>

<style scoped>
.provider-select {
  margin-bottom: 20px;
}

.provider-select h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.preset-buttons .el-button {
  min-width: 100px;
}
</style>
