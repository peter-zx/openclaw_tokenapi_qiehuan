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
          @submit="handleSubmit"
          @save="handleSave"
        />

        <!-- 模型卡片列表 -->
        <div class="model-cards-section">
          <h3>已保存的模型</h3>
          <div v-if="modelCards.length === 0" class="empty-state">
            <el-empty description="暂无已保存的模型" />
          </div>
          <div v-else class="model-cards-grid">
            <ModelCard
              v-for="card in modelCards"
              :key="card.id"
              :model="card"
              @click="handleCardClick"
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
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

// 保存到通讯录（不重启服务）
const handleSave = async () => {
  if (!formData.providerId || !formData.baseUrl || !formData.apiKey || !formData.modelId) {
    ElMessage.warning('请填写所有必填字段')
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
  if (!formData.providerId || !formData.baseUrl || !formData.apiKey || !formData.modelId) {
    ElMessage.warning('请填写所有必填字段')
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

.model-cards-section h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 20px;
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
