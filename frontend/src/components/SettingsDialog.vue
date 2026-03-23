<template>
  <el-dialog
    :model-value="visible"
    :title="`配置 ${providerName}`"
    width="500px"
    @update:model-value="$emit('update:visible', false)"
  >
    <el-form :model="form" label-width="120px">
      <el-form-item label="Provider ID" required>
        <el-input v-model="form.providerId" placeholder="请输入提供商ID" />
      </el-form-item>

      <el-form-item label="Base URL" required>
        <el-input v-model="form.baseUrl" placeholder="请输入Base URL" />
      </el-form-item>

      <el-form-item label="API Key" required>
        <el-input
          v-model="form.apiKey"
          type="password"
          placeholder="请输入API Key"
          show-password
        />
      </el-form-item>

      <el-divider />

      <el-form-item label="contextWindow">
        <el-input-number
          v-model="form.contextWindow"
          :min="1000"
          :max="128000"
          :step="1000"
          placeholder="默认值: 64000"
        />
        <span class="form-tip">范围: 1000 - 128000（上下文窗口）</span>
      </el-form-item>

      <el-form-item label="maxTokens">
        <el-input-number
          v-model="form.maxTokens"
          :min="100"
          :max="32000"
          :step="100"
          placeholder="默认值: 8000"
        />
        <span class="form-tip">范围: 100 - 32000（最大输出长度）</span>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="handleSave">保存配置</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: Boolean,
  providerKey: String,
  config: Object
})

const emit = defineEmits(['update:visible', 'save'])

const form = ref({
  providerId: '',
  baseUrl: '',
  apiKey: '',
  contextWindow: 64000,
  maxTokens: 8000
})

const providerName = ref('')

watch(() => props.visible, (newVal) => {
  if (newVal && props.config) {
    form.value = {
      providerId: props.config.providerId || '',
      baseUrl: props.config.baseUrl || '',
      apiKey: props.config.apiKey || '',
      contextWindow: props.config.contextWindow || 64000,
      maxTokens: props.config.maxTokens || 8000
    }
  }
})

watch(() => props.providerKey, (newVal) => {
  const names = {
    'ali': '阿里云',
    'volcengine': '火山引擎',
    'kimi': 'Kimi',
    'deepseek': 'DeepSeek',
    'openai': 'OpenAI',
    'minimax': 'MiniMax',
    'custom': '自定义'
  }
  providerName.value = names[newVal] || '未知'
})

const handleClose = () => {
  emit('update:visible', false)
}

const handleSave = () => {
  if (!form.value.providerId || !form.value.baseUrl || !form.value.apiKey) {
    ElMessage.warning('请填写完整的配置信息')
    return
  }
  emit('save', { ...form.value })
  handleClose()
  ElMessage.success('配置已保存')
}
</script>

<style scoped>
.form-tip {
  font-size: 12px;
  color: #909399;
  margin-left: 8px;
}

.el-divider {
  margin: 20px 0;
}
</style>
