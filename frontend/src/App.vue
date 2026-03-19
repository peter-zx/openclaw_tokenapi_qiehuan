<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>OpenClaw 模型切换工具</h1>
        <div class="current-model">
          当前模型: <strong>{{ currentModel }}</strong>
        </div>
      </el-header>

      <el-main>
        <!-- 提供商选择 -->
        <ProviderSelect
          :selected-provider="providerStore.state.selectedProvider"
          @select="handleSelectProvider"
          @select-custom="handleSelectCustom"
        />

        <!-- 配置表单 -->
        <ConfigForm
          :form-data="formData"
          :is-custom="providerStore.state.isCustomProvider"
          :saving="saving"
          :applying="applying"
          :show-batch-import="showBatchImport"
          @submit="handleSubmit"
          @save="handleSave"
          @open-apikey="handleOpenApiKeyDialog"
          @open-batch-import="showBatchImport = true"
        />

        <!-- 模型卡片列表 -->
        <div class="model-cards-section">
          <div class="cards-header">
            <h3>已保存的模型 ({{ filteredCards.length }})</h3>
            <div class="filter-buttons">
              <el-button
                v-for="(p, key) in providerOptions"
                :key="key"
                :type="filterProvider === key ? 'primary' : 'default'"
                size="small"
                @click="filterProvider = filterProvider === key ? '' : key"
              >
                {{ p.name }}
              </el-button>
            </div>
          </div>

          <div v-if="filteredCards.length === 0" class="empty-state">
            <el-empty :description="filterProvider ? '该提供商下暂无模型' : '暂无已保存的模型'" />
          </div>
          <div v-else class="model-cards-grid">
            <ModelCard
              v-for="card in filteredCards"
              :key="card.id"
              :model="card"
              @click="handleCardClick"
              @delete="handleDeleteCard"
            />
          </div>
        </div>
      </el-main>

      <el-footer>
        <el-button @click="handleRefresh" :loading="refreshing">
          刷新状态
        </el-button>
        <el-button @click="handleRestart" :loading="restarting" type="warning">
          重启服务
        </el-button>
      </el-footer>
    </el-container>

    <!-- API Key 弹窗 -->
    <el-dialog v-model="showApiKeyDialog" title="设置 API Key" width="400px">
      <el-form label-position="top">
        <el-form-item :label="currentProviderName">
          <el-input
            v-model="apiKeyInput"
            type="password"
            placeholder="请输入 API Key"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showApiKeyDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveApiKey">保存</el-button>
      </template>
    </el-dialog>

    <!-- 批量导入弹窗 -->
    <el-dialog v-model="showBatchImport" title="批量导入模型" width="500px">
      <div style="margin-bottom: 15px; color: #909399;">
        当前提供商：{{ currentProviderName }}（批量导入将使用此提供商的配置）
      </div>
      <el-tabs v-model="batchImportTab">
        <el-tab-pane label="在线输入" name="input">
          <el-input
            type="textarea"
            v-model="batchInputText"
            :rows="8"
            placeholder="每行一个模型ID，例如：&#10;deepseek-v3&#10;gpt-4o&#10;doubao-seed-1.5"
          />
          <div style="margin-top: 10px; color: #909399; font-size: 12px;">
            每行一个模型ID，支持任意字符
          </div>
        </el-tab-pane>
        <el-tab-pane label="文件导入" name="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            accept=".txt"
            :on-change="handleFileChange"
          >
            <template #trigger>
              <el-button>选择 TXT 文件</el-button>
            </template>
            <template #tip>
              <div style="margin-top: 10px; color: #909399; font-size: 12px;">
                每行一个模型ID
              </div>
            </template>
          </el-upload>
        </el-tab-pane>
        <el-tab-pane label="下载模板" name="template">
          <el-button @click="downloadTemplate">下载模板文件</el-button>
          <div style="margin-top: 15px; color: #606266; font-size: 13px;">
            模板格式：每行一个模型ID<br/>
            # 开头的为注释行<br/>
            例如：<br/>
            <code style="background: #f5f7fa; padding: 5px; display: block; margin-top: 5px;">
# 阿里云模型<br/>
deepseek-v3<br/>
qwen-plus<br/>
# 火山引擎模型<br/>
doubao-seed-1.5
            </code>
          </div>
        </el-tab-pane>
      </el-tabs>

      <template #footer>
        <el-button @click="showBatchImport = false">取消</el-button>
        <el-button type="primary" @click="handleBatchImport" :loading="batchImporting">
          确认导入
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { useProviderStore, PRESET_PROVIDERS } from './stores/provider'
import ProviderSelect from './components/ProviderSelect.vue'
import ModelCard from './components/ModelCard.vue'
import ConfigForm from './components/ConfigForm.vue'

const API_BASE = 'http://127.0.0.1:9131/api'

const providerStore = useProviderStore()

const formData = reactive({
  providerId: '',
  baseUrl: '',
  apiKey: '',
  modelId: ''
})

const currentModel = ref('未设置')
const modelCards = ref([])
const saving = ref(false)
const applying = ref(false)
const refreshing = ref(false)
const restarting = ref(false)

// 筛选
const filterProvider = ref('')
const showBatchImport = ref(false)
const batchImportTab = ref('input')
const batchInputText = ref('')
const batchImporting = ref(false)
const uploadRef = ref(null)
const selectedFile = ref(null)

// API Key 弹窗
const showApiKeyDialog = ref(false)
const apiKeyInput = ref('')
const currentProviderKey = ref('')

// 提供商选项
const providerOptions = PRESET_PROVIDERS

// 当前提供商名称
const currentProviderName = computed(() => {
  if (!formData.providerId) return '请先选择提供商'
  const preset = Object.values(PRESET_PROVIDERS).find(p => p.providerId === formData.providerId)
  return preset ? preset.name : formData.providerId
})

// 过滤后的卡片
const filteredCards = computed(() => {
  if (!filterProvider.value) return modelCards.value
  return modelCards.value.filter(card => {
    const key = Object.keys(PRESET_PROVIDERS).find(k => PRESET_PROVIDERS[k].providerId === card.providerId)
    return key === filterProvider.value
  })
})

// 加载配置
const loadConfig = async () => {
  try {
    const response = await axios.get(`${API_BASE}/config`)
    currentModel.value = response.data.currentModel
    modelCards.value = response.data.modelCards
  } catch (error) {
    ElMessage.error('加载配置失败: ' + error.message)
  }
}

// 选择预设提供商
const handleSelectProvider = (key) => {
  const preset = PRESET_PROVIDERS[key]
  if (preset) {
    providerStore.selectPreset(key)
    formData.providerId = preset.providerId
    formData.baseUrl = preset.baseUrl
    formData.modelId = ''
    formData.apiKey = ''
  }
}

// 选择自定义提供商
const handleSelectCustom = () => {
  providerStore.selectCustom()
  formData.providerId = ''
  formData.baseUrl = ''
  formData.apiKey = ''
  formData.modelId = ''
}

// 打开 API Key 弹窗
const handleOpenApiKeyDialog = () => {
  currentProviderKey.value = formData.providerId
  apiKeyInput.value = formData.apiKey || ''
  showApiKeyDialog.value = true
}

// 保存 API Key
const handleSaveApiKey = async () => {
  if (!currentProviderKey.value) {
    ElMessage.warning('请先选择提供商')
    return
  }

  try {
    await axios.post(`${API_BASE}/provider/apikey`, {
      providerId: currentProviderKey.value,
      apiKey: apiKeyInput.value
    })
    formData.apiKey = apiKeyInput.value
    showApiKeyDialog.value = false
    ElMessage.success('API Key 已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 保存到通讯录（不重启服务）
const handleSave = async () => {
  if (!formData.providerId || !formData.baseUrl || !formData.modelId) {
    ElMessage.warning('请填写必填字段：提供商/URL/模型ID')
    return
  }

  saving.value = true
  try {
    const response = await axios.post(`${API_BASE}/save`, formData)
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

// 提交配置（保存并应用）
const handleSubmit = async () => {
  if (!formData.providerId || !formData.baseUrl || !formData.modelId) {
    ElMessage.warning('请填写必填字段：提供商/URL/模型ID')
    return
  }

  applying.value = true
  try {
    const response = await axios.post(`${API_BASE}/switch`, formData)
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) {
    ElMessage.error('切换模型失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    applying.value = false
  }
}

// 点击模型卡片（切换并应用）
const handleCardClick = async (card) => {
  const confirmText = `确认切换到模型: ${card.modelId}？`
  if (!confirm(confirmText)) {
    return
  }

  applying.value = true
  try {
    const response = await axios.post(`${API_BASE}/switch`, {
      providerId: card.providerId,
      baseUrl: card.baseUrl,
      apiKey: card.apiKey,
      modelId: card.modelId
    })
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) {
    ElMessage.error('切换模型失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    applying.value = false
  }
}

// 删除卡片
const handleDeleteCard = async (card) => {
  try {
    await ElMessageBox.confirm(
      `确定删除模型 "${card.modelId}" 吗？`,
      '确认删除',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )

    const response = await axios.post(`${API_BASE}/delete`, {
      providerId: card.providerId,
      modelId: card.modelId
    })
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// 刷新状态
const handleRefresh = async () => {
  refreshing.value = true
  try {
    await loadConfig()
    ElMessage.success('刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败: ' + error.message)
  } finally {
    refreshing.value = false
  }
}

// 重启服务
const handleRestart = async () => {
  if (!confirm('确认重启服务？')) {
    return
  }

  restarting.value = true
  try {
    const response = await axios.post(`${API_BASE}/gateway/control`, {
      action: 'restart'
    })
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) {
    ElMessage.error('重启失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    restarting.value = false
  }
}

// 下载模板
const downloadTemplate = () => {
  const template = `# OpenClaw 模型批量导入模板
# 每行一个模型ID，# 开头的行为注释
# 请删除所有注释行后导入，或直接填写模型ID

# 阿里云
deepseek-v3
qwen-plus

# 火山引擎
doubao-seed-1.5

# Kimi
moonshot-v1-8k

# DeepSeek
deepseek-chat

# OpenAI
gpt-4o
`
  const blob = new Blob([template], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'model_import_template.txt'
  a.click()
  URL.revokeObjectURL(url)
}

// 文件选择
const handleFileChange = (file) => {
  selectedFile.value = file.raw
}

// 批量导入
const handleBatchImport = async () => {
  let modelIds = []

  if (batchImportTab.value === 'input') {
    modelIds = batchInputText.value.split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'))
  } else if (batchImportTab.value === 'file') {
    if (!selectedFile.value) {
      ElMessage.warning('请先选择文件')
      return
    }
    const reader = new FileReader()
    modelIds = await new Promise((resolve) => {
      reader.onload = (e) => {
        const text = e.target.result
        const ids = text.split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'))
        resolve(ids)
      }
      reader.readAsText(selectedFile.value)
    })
  }

  if (modelIds.length === 0) {
    ElMessage.warning('未检测到有效模型ID')
    return
  }

  if (!formData.providerId || !formData.baseUrl) {
    ElMessage.warning('请先选择提供商')
    return
  }

  batchImporting.value = true
  let successCount = 0
  let failCount = 0

  for (const modelId of modelIds) {
    try {
      await axios.post(`${API_BASE}/save`, {
        providerId: formData.providerId,
        baseUrl: formData.baseUrl,
        apiKey: formData.apiKey,
        modelId: modelId
      })
      successCount++
    } catch {
      failCount++
    }
  }

  batchImporting.value = false
  showBatchImport.value = false
  batchInputText.value = ''
  selectedFile.value = null

  ElMessage.success(`导入完成：成功 ${successCount}，失败 ${failCount}`)
  await loadConfig()
}

onMounted(() => {
  loadConfig()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-header h1 {
  font-size: 24px;
  font-weight: 600;
}

.current-model {
  font-size: 14px;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
}

.current-model strong {
  color: #fff;
  margin-left: 5px;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.model-cards-section {
  margin-top: 40px;
}

.cards-header {
  margin-bottom: 20px;
}

.cards-header h3 {
  font-size: 18px;
  color: #303133;
  margin: 0 0 15px 0;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.model-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.el-footer {
  background-color: white;
  border-top: 1px solid #dcdfe6;
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}
</style>
