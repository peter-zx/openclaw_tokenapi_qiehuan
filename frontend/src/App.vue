<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-left">
          <img :src="qrcodeImage" alt="QR Code" class="header-qrcode">
          <div class="header-info">
            <div class="header-author">@aigc散修竹相左边</div>
            <div class="header-slogan">你我的时间都很宝贵，只分享验证可行的前沿技术</div>
          </div>
        </div>
        <div class="header-center">
          <h1>OpenClaw</h1>
          <h2>模型切换工具</h2>
        </div>
        <div class="header-right">
          <div class="current-model">当前模型: <strong>{{ currentModel }}</strong></div>
        </div>
      </el-header>

      <el-main>
        <!-- 左侧：操作区 -->
        <div class="main-layout">
          <div class="left-panel">
            <!-- 提供商选择 -->
            <div class="provider-section">
              <div class="section-title">
                选择服务商
                <span class="section-tip">（点击名称选择，点击齿轮图标配置）</span>
              </div>
              <div class="provider-buttons">
                <div
                  v-for="(preset, key) in PRESET_PROVIDERS"
                  :key="key"
                  class="provider-btn-item"
                >
                  <el-button
                    :type="selectedProvider === key ? 'primary' : 'default'"
                    @click="handleSelectProvider(key)"
                    size="large"
                    class="provider-name-btn"
                  >
                    {{ preset.name }}
                  </el-button>
                  <el-button
                    size="small"
                    @click="openProviderConfig(key)"
                    :icon="Setting"
                    circle
                    class="provider-config-btn"
                  />
                </div>
              </div>
              <div class="provider-buttons custom-row">
                <div class="provider-btn-item">
                  <el-button
                    :type="selectedProvider === 'custom' ? 'primary' : 'default'"
                    @click="handleSelectCustom"
                    size="large"
                    class="provider-name-btn"
                  >
                    自定义
                  </el-button>
                  <el-button
                    v-if="selectedProvider === 'custom'"
                    size="small"
                    @click="openProviderConfig('custom')"
                    :icon="Setting"
                    circle
                    class="provider-config-btn"
                  />
                </div>
              </div>

              <!-- 模型ID输入框 -->
              <div class="model-input-section" v-if="selectedProvider">
                <div class="selected-provider-info">
                  已选择: <strong>{{ currentProviderName }}</strong>
                  <span v-if="isProviderConfigured()" class="config-hint">（已配置）</span>
                  <span v-else class="config-hint warning">（未配置，请点击齿轮按钮）</span>
                </div>
                <el-input
                  v-model="modelIdInput"
                  placeholder="输入模型ID，例如: deepseek-v3"
                  size="large"
                  @keyup.enter="handleSave"
                >
                  <template #append>
                    <el-button @click="handleOpenBatchImport" :icon="DocumentAdd" />
                  </template>
                </el-input>

                <div class="button-group">
                  <el-button
                    type="success"
                    @click="handleSave"
                    :loading="saving"
                    size="large"
                    :disabled="!canSave"
                  >
                    {{ saving ? '保存中...' : '保存到通讯录' }}
                  </el-button>
                  <el-button
                    type="primary"
                    @click="handleSubmit"
                    :loading="applying"
                    size="large"
                    :disabled="!canSave"
                  >
                    {{ applying ? '应用中...' : '保存并应用' }}
                  </el-button>
                </div>

                <div v-if="saving" class="loading-tip">正在保存到通讯录...</div>
                <div v-if="applying" class="loading-tip applying">正在保存并应用配置...</div>
              </div>
            </div>

            <!-- 运维指令 -->
            <div class="restart-guide">
              <div class="section-title">OpenClaw 运维指令</div>
              <div class="guide-steps">
                <p><strong>重启服务步骤（应用模型修改）：</strong></p>
                <div class="step">1. 按 <kbd>Win</kbd> + <kbd>R</kbd></div>
                <div class="step">2. 输入 <code>powershell</code></div>
                <div class="step">3. 右键选择 <strong>"以管理员身份运行"</strong></div>
                <div class="step">4. 复制以下命令粘贴执行：</div>
                <div class="code-wrapper">
                  <div class="code-block">Get-Process | Where-Object { $_.Name -like "*openclaw*" } | Stop-Process -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 5; openclaw gateway</div>
                  <button class="code-copy-btn" @click="copyRestartCmd">复制</button>
                </div>
              </div>
              <div class="guide-steps">
                <p><strong>服务管理：</strong></p>
                <div class="code-wrapper"><div class="code-block">openclaw gateway</div><button class="code-copy-btn" @click="copyCode('openclaw gateway')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw gateway --port 18789</div><button class="code-copy-btn" @click="copyCode('openclaw gateway --port 18789')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw gateway stop</div><button class="code-copy-btn" @click="copyCode('openclaw gateway stop')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw gateway restart</div><button class="code-copy-btn" @click="copyCode('openclaw gateway restart')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw health</div><button class="code-copy-btn" @click="copyCode('openclaw health')">复制</button></div>
              </div>
              <div class="guide-steps">
                <p><strong>配置管理：</strong></p>
                <div class="code-wrapper"><div class="code-block">openclaw configure</div><button class="code-copy-btn" @click="copyCode('openclaw configure')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw config</div><button class="code-copy-btn" @click="copyCode('openclaw config')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw version</div><button class="code-copy-btn" @click="copyCode('openclaw version')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw update</div><button class="code-copy-btn" @click="copyCode('openclaw update')">复制</button></div>
              </div>
              <div class="guide-steps">
                <p><strong>日志与诊断：</strong></p>
                <div class="code-wrapper"><div class="code-block">openclaw logs --tail 100</div><button class="code-copy-btn" @click="copyCode('openclaw logs --tail 100')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw doctor</div><button class="code-copy-btn" @click="copyCode('openclaw doctor')">复制</button></div>
                <div class="code-wrapper"><div class="code-block">openclaw clean</div><button class="code-copy-btn" @click="copyCode('openclaw clean')">复制</button></div>
              </div>
            </div>
          </div>

          <!-- 右侧：卡片列表 -->
          <div class="right-panel">
            <div class="cards-header">
              <h3>已保存的模型 ({{ filteredCards.length }})</h3>
              <div class="filter-buttons">
                <el-button
                  size="small"
                  :type="filterProvider === '' ? 'primary' : 'default'"
                  @click="filterProvider = ''"
                >全部</el-button>
                <el-button
                  v-for="(preset, key) in PRESET_PROVIDERS"
                  :key="key"
                  size="small"
                  :type="filterProvider === key ? 'primary' : 'default'"
                  @click="filterProvider = filterProvider === key ? '' : key"
                >
                  {{ preset.name }}
                </el-button>
              </div>
            </div>

            <div v-if="filteredCards.length === 0" class="empty-state">
              <el-empty :description="filterProvider ? '该服务商下暂无模型' : '暂无已保存的模型'" />
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
        </div>
      </el-main>

      <el-footer class="app-footer">
        <div class="footer-content">
          <span>@aigc散修竹相左边</span>
          <span class="separator">|</span>
          <span>v1.0.0</span>
          <span class="separator">|</span>
          <span>2026-03-19</span>
        </div>
      </el-footer>
    </el-container>

    <!-- 提供商配置弹窗 -->
    <el-dialog v-model="showProviderConfig" :title="`配置 ${currentConfigProviderName}`" width="450px">
      <el-form label-position="top">
        <el-form-item label="Provider ID">
          <el-input v-model="providerConfigForm.providerId" placeholder="请输入提供商ID" />
        </el-form-item>
        <el-form-item label="Base URL">
          <el-input v-model="providerConfigForm.baseUrl" placeholder="请输入Base URL" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="providerConfigForm.apiKey" type="password" placeholder="请输入API Key" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showProviderConfig = false">取消</el-button>
        <el-button type="primary" @click="handleSaveProviderConfig">保存配置</el-button>
      </template>
    </el-dialog>

    <!-- 批量导入弹窗 -->
    <el-dialog v-model="showBatchImport" title="批量导入模型" width="500px">
      <div style="margin-bottom: 15px; color: #909399;">
        当前提供商：{{ currentProviderName }}
      </div>
      <el-tabs v-model="batchImportTab">
        <el-tab-pane label="在线输入" name="input">
          <el-input type="textarea" v-model="batchInputText" :rows="8" placeholder="每行一个模型ID" />
        </el-tab-pane>
        <el-tab-pane label="文件导入" name="file">
          <el-upload ref="uploadRef" :auto-upload="false" :limit="1" accept=".txt" :on-change="handleFileChange">
            <template #trigger>
              <el-button>选择 TXT 文件</el-button>
            </template>
          </el-upload>
        </el-tab-pane>
        <el-tab-pane label="下载模板" name="template">
          <el-button @click="downloadTemplate">下载模板文件</el-button>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <el-button @click="showBatchImport = false">取消</el-button>
        <el-button type="primary" @click="handleBatchImport" :loading="batchImporting">确认导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Setting, DocumentAdd } from '@element-plus/icons-vue'
import axios from 'axios'
import { PRESET_PROVIDERS } from './stores/provider'
import ModelCard from './components/ModelCard.vue'
const qrcodeImage = '/qrcode.jpg'

const API_BASE = 'http://127.0.0.1:9131/api'

const selectedProvider = ref('')
const modelIdInput = ref('')
const currentModel = ref('未设置')
const modelCards = ref([])
const saving = ref(false)
const applying = ref(false)

// 批量导入
const showBatchImport = ref(false)
const batchImportTab = ref('input')
const batchInputText = ref('')
const batchImporting = ref(false)
const uploadRef = ref(null)
const selectedFile = ref(null)

// 卡片筛选
const filterProvider = ref('')

// 提供商配置弹窗
const showProviderConfig = ref(false)
const currentConfigProviderKey = ref('')
const providerConfigForm = reactive({ providerId: '', baseUrl: '', apiKey: '' })

const PROVIDER_CONFIG_KEY = 'openclaw_provider_configs'

const getAllStoredConfigs = () => {
  try { return JSON.parse(localStorage.getItem(PROVIDER_CONFIG_KEY) || '{}') } catch { return {} }
}

const getStoredProviderConfig = (key) => {
  const configs = getAllStoredConfigs()
  if (key === 'custom') return configs['custom'] || { providerId: '', baseUrl: '', apiKey: '' }
  const preset = PRESET_PROVIDERS[key]
  if (!preset) return { providerId: '', baseUrl: '', apiKey: '' }
  return { providerId: preset.providerId, baseUrl: preset.baseUrl, apiKey: configs[key]?.apiKey || '' }
}

const saveProviderConfigToStorage = (key, config) => {
  const configs = getAllStoredConfigs()
  configs[key] = {
    ...config,
    providerId: config.providerId || PRESET_PROVIDERS[key]?.providerId || '',
    baseUrl: config.baseUrl || PRESET_PROVIDERS[key]?.baseUrl || ''
  }
  localStorage.setItem(PROVIDER_CONFIG_KEY, JSON.stringify(configs))
}

const currentProviderName = computed(() => {
  if (!selectedProvider.value) return ''
  if (selectedProvider.value === 'custom') return getStoredProviderConfig('custom').providerId || '自定义'
  return PRESET_PROVIDERS[selectedProvider.value]?.name || '未知'
})

const currentConfigProviderName = computed(() => {
  if (!currentConfigProviderKey.value) return ''
  if (currentConfigProviderKey.value === 'custom') return '自定义提供商'
  return PRESET_PROVIDERS[currentConfigProviderKey.value]?.name || '未知'
})

const canSave = computed(() => {
  if (!selectedProvider.value || !modelIdInput.value) return false
  return isProviderConfigured()
})

const isProviderConfigured = () => {
  const config = getStoredProviderConfig(selectedProvider.value)
  return !!(config.baseUrl && config.providerId && config.apiKey)
}

// 过滤后的卡片
const filteredCards = computed(() => {
  if (!filterProvider.value) return modelCards.value
  return modelCards.value.filter(card => {
    const key = Object.keys(PRESET_PROVIDERS).find(k => PRESET_PROVIDERS[k].providerId === card.providerId)
    return key === filterProvider.value
  })
})

const handleSelectProvider = (key) => { selectedProvider.value = key; modelIdInput.value = '' }
const handleSelectCustom = () => { selectedProvider.value = 'custom'; modelIdInput.value = '' }

const openProviderConfig = (key) => {
  currentConfigProviderKey.value = key
  const stored = getStoredProviderConfig(key)
  providerConfigForm.providerId = stored.providerId
  providerConfigForm.baseUrl = stored.baseUrl
  providerConfigForm.apiKey = stored.apiKey
  showProviderConfig.value = true
}

const handleSaveProviderConfig = () => {
  if (!providerConfigForm.providerId || !providerConfigForm.baseUrl) {
    ElMessage.warning('请填写完整的Provider ID和Base URL')
    return
  }
  saveProviderConfigToStorage(currentConfigProviderKey.value, {
    providerId: providerConfigForm.providerId,
    baseUrl: providerConfigForm.baseUrl,
    apiKey: providerConfigForm.apiKey
  })
  showProviderConfig.value = false
  ElMessage.success('提供商配置已保存')
}

const loadConfig = async () => {
  try {
    const response = await axios.get(`${API_BASE}/config`)
    currentModel.value = response.data.currentModel
    modelCards.value = response.data.modelCards
  } catch (error) { ElMessage.error('加载配置失败: ' + error.message) }
}

const handleSave = async () => {
  if (!canSave.value || !modelIdInput.value) { ElMessage.warning('请选择提供商并填写模型ID'); return }
  saving.value = true
  try {
    const config = getStoredProviderConfig(selectedProvider.value)
    const response = await axios.post(`${API_BASE}/save`, {
      providerId: config.providerId, baseUrl: config.baseUrl, apiKey: config.apiKey, modelId: modelIdInput.value
    })
    ElMessage.success(response.data.message)
    modelIdInput.value = ''
    await loadConfig()
  } catch (error) { ElMessage.error('保存失败: ' + (error.response?.data?.detail || error.message)) }
  finally { saving.value = false }
}

const handleSubmit = async () => {
  if (!canSave.value || !modelIdInput.value) { ElMessage.warning('请选择提供商并填写模型ID'); return }
  applying.value = true
  try {
    const config = getStoredProviderConfig(selectedProvider.value)
    const response = await axios.post(`${API_BASE}/switch`, {
      providerId: config.providerId, baseUrl: config.baseUrl, apiKey: config.apiKey, modelId: modelIdInput.value
    })
    ElMessage.success({ message: '模型已切换，正在重启服务，请等待 8 秒...', duration: 5000 })
    modelIdInput.value = ''
    await loadConfig()
  } catch (error) { ElMessage.error('切换失败: ' + (error.response?.data?.detail || error.message)) }
  finally { applying.value = false }
}

const handleCardClick = async (card) => {
  applying.value = true
  try {
    // 从localStorage获取API Key
    const storedConfig = getStoredProviderConfigByProviderId(card.providerId)
    const apiKey = storedConfig?.apiKey || ''

    const response = await axios.post(`${API_BASE}/switch`, {
      providerId: card.providerId, baseUrl: card.baseUrl, apiKey: apiKey, modelId: card.modelId
    })
    ElMessage.success({ message: '模型已切换，正在重启服务，请等待 8 秒...', duration: 5000 })
    await loadConfig()
  } catch (error) { ElMessage.error('切换失败: ' + (error.response?.data?.detail || error.message)) }
  finally { applying.value = false }
}

// 根据providerId获取存储的配置
const getStoredProviderConfigByProviderId = (providerId) => {
  const configs = getAllStoredConfigs()
  for (const key of Object.keys(configs)) {
    if (configs[key].providerId === providerId) {
      return configs[key]
    }
  }
  return null
}

const copyCode = async (code) => {
  try {
    await navigator.clipboard.writeText(code)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}

const copyRestartCmd = async () => {
  await copyCode('Get-Process | Where-Object { $_.Name -like "*openclaw*" } | Stop-Process -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 5; openclaw gateway')
}

const handleDeleteCard = async (card) => {
  try {
    await ElMessageBox.confirm(`确定删除模型 "${card.modelId}" 吗？`, '确认删除', { type: 'warning' })
    const response = await axios.post(`${API_BASE}/delete`, { providerId: card.providerId, modelId: card.modelId })
    ElMessage.success(response.data.message)
    await loadConfig()
  } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') }
}

const handleOpenBatchImport = () => {
  if (!selectedProvider.value) { ElMessage.warning('请先选择提供商'); return }
  showBatchImport.value = true
}

const downloadTemplate = () => {
  const blob = new Blob([`# 模型ID列表\ndeepseek-v3\ngpt-4o\nqwen-plus`], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = 'model_import_template.txt'; a.click()
  URL.revokeObjectURL(url)
}

const handleFileChange = (file) => { selectedFile.value = file.raw }

const handleBatchImport = async () => {
  let modelIds = []
  if (batchImportTab.value === 'input') {
    modelIds = batchInputText.value.split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'))
  } else if (batchImportTab.value === 'file') {
    if (!selectedFile.value) { ElMessage.warning('请先选择文件'); return }
    modelIds = await new Promise((resolve) => {
      const reader = new FileReader()
      reader.onload = (e) => resolve(e.target.result.split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#')))
      reader.readAsText(selectedFile.value)
    })
  }
  if (modelIds.length === 0) { ElMessage.warning('未检测到有效模型ID'); return }
  if (!canSave.value) { ElMessage.warning('请先选择并配置提供商'); return }
  batchImporting.value = true
  const config = getStoredProviderConfig(selectedProvider.value)
  let successCount = 0, failCount = 0
  for (const modelId of modelIds) {
    try {
      await axios.post(`${API_BASE}/save`, { providerId: config.providerId, baseUrl: config.baseUrl, apiKey: config.apiKey, modelId })
      successCount++
    } catch { failCount++ }
  }
  batchImporting.value = false
  showBatchImport.value = false
  batchInputText.value = ''
  ElMessage.success(`导入完成：成功 ${successCount}，失败 ${failCount}`)
  await loadConfig()
}

onMounted(() => { loadConfig() })
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f5f7fa; }
#app { min-height: 100vh; }

.el-header { background: linear-gradient(135deg, #409eff 0%, #3078d8 100%) !important; color: white !important; padding: 15px 40px !important; min-height: 150px !important; height: auto !important; display: flex !important; justify-content: space-between !important; align-items: center !important; flex-shrink: 0 !important; }
.header-left { display: flex; align-items: flex-start; gap: 15px; flex: 1; margin: 15px 0 15px 0; }
.header-qrcode { width: 90px; height: 90px; border-radius: 8px; object-fit: cover; border: 2px solid rgba(255,255,255,0.3); }
.header-info { display: flex; flex-direction: column; gap: 5px; }
.header-author { font-size: 14px; font-weight: 600; }
.header-slogan { font-size: 12px; opacity: 0.85; }
.header-center { flex: 1; text-align: center; display: flex; flex-direction: column; justify-content: center; }
.header-center h1 { font-size: 36px; font-weight: 800; margin: 0 0 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); letter-spacing: 3px; }
.header-center h2 { font-size: 18px; font-weight: 400; margin: 0; opacity: 0.9; letter-spacing: 5px; }
.header-right { flex: 1; display: flex; justify-content: flex-end; }
.current-model { font-size: 14px; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; }
.current-model strong { color: #fff; margin-left: 5px; }

.el-main { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
.el-footer { background: #f5f7fa; padding: 15px; text-align: center; color: #909399; font-size: 13px; }
.footer-content { display: flex; justify-content: center; align-items: center; gap: 10px; }
.separator { color: #dcdfe6; }

.main-layout { display: flex; gap: 30px; }
.left-panel { flex: 0 0 420px; }
.right-panel { flex: 1; min-width: 0; }

.section-title { font-size: 16px; font-weight: 600; color: #303133; margin-bottom: 15px; }
.section-tip { font-size: 12px; font-weight: normal; color: #909399; margin-left: 10px; }

.provider-section { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.provider-buttons { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px; justify-content: flex-start; }
.provider-btn-item { display: flex; align-items: center; gap: 8px; }
.provider-name-btn { min-width: 100px; }
.provider-config-btn { flex-shrink: 0; }
.custom-row { border-top: 1px dashed #e4e7ed; padding-top: 15px; margin-top: 5px; }

.model-input-section { }
.selected-provider-info { margin-bottom: 15px; font-size: 14px; color: #606266; }
.selected-provider-info strong { color: #409eff; }
.config-hint { margin-left: 10px; font-size: 12px; }
.config-hint.warning { color: #e6a23c; }

.button-group { display: flex; gap: 12px; margin-top: 15px; }
.button-group .el-button { flex: 1; }

.loading-tip { margin-top: 12px; text-align: center; color: #909399; font-size: 14px; animation: pulse 1.5s infinite; }
.loading-tip.applying { color: #67c23a; font-weight: bold; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* 重启服务说明 */
.restart-guide { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.guide-steps { margin-bottom: 15px; }
.guide-steps:last-child { margin-bottom: 0; }
.guide-steps p { margin-bottom: 8px; color: #303133; font-size: 14px; }
.step { margin-bottom: 6px; color: #606266; font-size: 13px; }
kbd { background: #f5f7fa; border: 1px solid #dcdfe6; border-radius: 4px; padding: 2px 6px; font-size: 12px; }
code { background: #f5f7fa; padding: 2px 8px; border-radius: 4px; color: #409eff; }
.code-wrapper { position: relative; margin-top: 8px; }
.code-block { background: #283142; color: #67c23a; padding: 10px 40px 10px 15px; border-radius: 6px; font-family: monospace; font-size: 12px; white-space: pre-wrap; word-break: break-all; overflow: hidden; max-height: 48px; }
.code-copy-btn { position: absolute; top: 4px; right: 4px; background: rgba(255,255,255,0.1); border: none; color: #67c23a; cursor: pointer; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
.code-copy-btn:hover { background: rgba(255,255,255,0.2); }
.step-tip { color: #e6a23c; font-size: 12px; margin-top: 8px; font-weight: 500; padding-left: 10px; }
.step.tip { color: #e6a23c; font-size: 12px; margin-top: 10px; font-weight: 500; }

/* 卡片 */
.cards-header { margin-bottom: 20px; }
.cards-header h3 { font-size: 18px; color: #303133; margin-bottom: 15px; }
.filter-buttons { display: flex; flex-wrap: wrap; gap: 8px; }
.empty-state { text-align: center; padding: 40px 0; }
.model-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
</style>
