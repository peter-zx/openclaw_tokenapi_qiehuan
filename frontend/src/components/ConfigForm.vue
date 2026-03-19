<template>
  <el-form :model="formData" label-position="top" class="config-form">
    <el-form-item label="Provider ID">
      <el-input
        v-model="formData.providerId"
        placeholder="请输入提供商ID"
        :disabled="!isCustom"
      />
    </el-form-item>

    <el-form-item label="Base URL">
      <el-input
        v-model="formData.baseUrl"
        placeholder="请输入Base URL"
      />
    </el-form-item>

    <el-form-item label="API Key">
      <div class="api-key-row">
        <el-input
          v-model="formData.apiKey"
          type="password"
          placeholder="请输入API Key（可留空，后续单独设置）"
          show-password
        />
        <el-button @click="$emit('open-apikey')" style="margin-left: 8px;">
          设置
        </el-button>
      </div>
    </el-form-item>

    <el-form-item label="模型ID">
      <div class="model-id-row">
        <el-input
          v-model="formData.modelId"
          placeholder="请输入模型ID，例如: deepseek-v3"
        />
        <el-button @click="$emit('open-batch-import')" style="margin-left: 8px;">
          批量导入
        </el-button>
      </div>
    </el-form-item>

    <div class="button-group">
      <el-button
        type="success"
        @click="$emit('save')"
        :loading="saving"
        size="large"
      >
        {{ saving ? '保存中...' : '保存到通讯录' }}
      </el-button>
      <el-button
        type="primary"
        @click="$emit('submit')"
        :loading="applying"
        size="large"
      >
        {{ applying ? '应用中...' : '保存并应用' }}
      </el-button>
    </div>

    <div v-if="saving" class="loading-tip">
      正在保存到通讯录，请稍候...
    </div>
    <div v-if="applying" class="loading-tip applying">
      正在保存配置、重启Gateway服务，请稍候...
    </div>
  </el-form>
</template>

<script setup>
defineProps({
  formData: {
    type: Object,
    required: true
  },
  isCustom: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  applying: {
    type: Boolean,
    default: false
  }
})

defineEmits(['submit', 'save', 'open-apikey', 'open-batch-import'])
</script>

<style scoped>
.config-form {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-top: 20px;
}

.api-key-row {
  display: flex;
  width: 100%;
}

.api-key-row .el-input {
  flex: 1;
}

.model-id-row {
  display: flex;
  width: 100%;
}

.model-id-row .el-input {
  flex: 1;
}

.button-group {
  display: flex;
  gap: 12px;
}

.button-group .el-button {
  flex: 1;
}

.loading-tip {
  margin-top: 12px;
  text-align: center;
  color: #909399;
  font-size: 14px;
  animation: pulse 1.5s infinite;
}

.loading-tip.applying {
  color: #e6a23c;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
