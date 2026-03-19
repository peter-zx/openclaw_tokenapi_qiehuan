import { reactive } from 'vue'

// 预设提供商配置
export const PRESET_PROVIDERS = {
  'ali': {
    name: '阿里云',
    baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    providerId: 'ali-dashscope'
  },
  'volcengine': {
    name: '火山方舟',
    baseUrl: 'https://ark.cn-beijing.volces.com/api/v3',
    providerId: 'volcengine-ark'
  },
  'kimi': {
    name: 'Kimi',
    baseUrl: 'https://api.moonshot.cn/v1',
    providerId: 'kimi-moonshot'
  },
  'deepseek': {
    name: 'DeepSeek',
    baseUrl: 'https://api.deepseek.com',
    providerId: 'deepseek-api'
  },
  'openai': {
    name: 'OpenAI',
    baseUrl: 'https://api.openai.com/v1',
    providerId: 'openai-official'
  }
}

// 提供商状态管理
export const useProviderStore = () => {
  const state = reactive({
    selectedProvider: null,
    baseUrl: '',
    apiKey: '',
    modelId: '',
    isCustomProvider: false
  })

  // 选择预设提供商
  const selectPreset = (key) => {
    const preset = PRESET_PROVIDERS[key]
    if (preset) {
      state.selectedProvider = key
      state.baseUrl = preset.baseUrl
      state.providerId = preset.providerId
      state.isCustomProvider = false
    }
  }

  // 选择自定义提供商
  const selectCustom = () => {
    state.selectedProvider = 'custom'
    state.isCustomProvider = true
    state.baseUrl = ''
    state.providerId = ''
  }

  // 重置表单
  const resetForm = () => {
    state.selectedProvider = null
    state.baseUrl = ''
    state.apiKey = ''
    state.modelId = ''
    state.isCustomProvider = false
  }

  return {
    state,
    PRESET_PROVIDERS,
    selectPreset,
    selectCustom,
    resetForm
  }
}
