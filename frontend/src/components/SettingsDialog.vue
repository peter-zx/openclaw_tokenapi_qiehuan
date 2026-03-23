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
      <el-button type="primary" @click="handleSave" :disabled="!form.providerId || !form.baseUrl || !form.apiKey">保存配置</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const PRESET_MAP = {
  'ali': { name: '阿里云', baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1', providerId: 'ali-dashscope' },
  'volcengine': { name: '火山引擎', baseUrl: 'https://ark.cn-beijing.volces.com/api/v3', providerId: 'volcengine-ark' },
  'kimi': { name: 'Kimi', baseUrl: 'https://api.moonshot.cn/v1', providerId: 'kimi-moonshot' },
  'deepseek': { name: 'DeepSeek', baseUrl: 'https://api.deepseek.com', providerId: 'deepseek-api' },
  'openai': { name: 'OpenAI', baseUrl: 'https://api.openai.com/v1', providerId: 'openai-official' },
  'minimax': { name: 'MiniMax', baseUrl: 'https://api.minimax.chat/v1', providerId: 'minimax' },
}

const API_BASE = 'http://127.0.0.1:9131/api'

const props = defineProps({
  visible: Boolean,
  providerKey: String,
  storedConfig: Object
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
const loading = ref(false)

watch(() => props.visible, async (newVal) => {
  if (!newVal) return

  const preset = PRESET_MAP[props.providerKey]
  const stored = props.storedConfig || {}

  let backendConfig = null
  if (preset) {
    try {
      loading.value = true
      const resp = await axios.get(`${API_BASE}/provider/${preset.providerId}`)
      backendConfig = resp.data
    } catch {
    } finally {
      loading.value = false
    }
  }

  if (preset) {
    form.value = {
      providerId: backendConfig?.providerId || stored.providerId || preset.providerId,
      baseUrl: backendConfig?.baseUrl || stored.baseUrl || preset.baseUrl,
      apiKey: backendConfig?.apiKey || stored.apiKey || '',
      contextWindow: backendConfig?.contextWindow || stored.contextWindow || 64000,
      maxTokens: backendConfig?.maxTokens || stored.maxTokens || 8000
    }
  } else {
    form.value = {
      providerId: stored.providerId || '',
      baseUrl: stored.baseUrl || '',
      apiKey: stored.apiKey || '',
      contextWindow: stored.contextWindow || 64000,
      maxTokens: stored.maxTokens || 8000
    }
  }
})

watch(() => props.providerKey, (newVal) => {
  if (PRESET_MAP[newVal]) {
    providerName.value = PRESET_MAP[newVal].name
  } else {
    providerName.value = newVal === 'custom' ? '自定义' : (newVal || '未知')
  }
}, { immediate: true })

const handleSave = () => {
  if (!form.value.providerId || !form.value.baseUrl || !form.value.apiKey) {
    ElMessage.warning('请填写完整的配置信息')
    return
  }
  emit('save', { ...form.value })
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
