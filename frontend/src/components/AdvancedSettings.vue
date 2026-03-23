<template>
  <el-dialog
    v-model="visible"
    title="高级设置"
    width="1100px"
    @update:model-value="$emit('update:visible', false)"
  >
    <div class="settings-content" v-loading="loading">
      <template v-if="!loading">
        <div class="settings-grid">

          <div class="setting-card card-full">
            <div class="card-header">
              <span class="card-icon">🔧</span>
              <div class="card-titles">
                <div class="card-title">工具权限配置</div>
                <div class="card-desc">控制 AI 可调用的工具能力</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-row">
                <div class="field-group">
                  <div class="field-label">权限级别</div>
                  <el-radio-group v-model="form.toolsProfile" class="radio-pills">
                    <el-radio value="full">full 全开</el-radio>
                    <el-radio value="coding">coding 编码</el-radio>
                    <el-radio value="minimal">minimal 最小</el-radio>
                  </el-radio-group>
                </div>
              </div>
              <div class="field-divider"></div>
              <div class="field-row gap-40">
                <div class="field-group">
                  <div class="field-label">允许的工具</div>
                  <div class="checkbox-grid">
                    <el-checkbox v-model="form.allowExec">exec 执行命令</el-checkbox>
                    <el-checkbox v-model="form.allowBrowser">browser 浏览器</el-checkbox>
                    <el-checkbox v-model="form.allowWebSearch">web_search 搜索</el-checkbox>
                    <el-checkbox v-model="form.allowWebFetch">web_fetch 抓取网页</el-checkbox>
                  </div>
                </div>
                <div class="field-group">
                  <div class="field-label">禁止的操作</div>
                  <div class="checkbox-grid">
                    <el-checkbox v-model="form.denyElevated">exec:elevated 提权操作</el-checkbox>
                    <el-checkbox v-model="form.denyShell">exec:shell 交互式shell</el-checkbox>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <span class="card-icon">⚡</span>
              <div class="card-titles">
                <div class="card-title">执行环境</div>
                <div class="card-desc">命令在何处执行</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-group">
                <div class="field-label">执行主机</div>
                <el-radio-group v-model="form.execHost" class="radio-pills-v">
                  <el-radio value="gateway">gateway 网关执行</el-radio>
                  <el-radio value="sandbox">sandbox 沙箱执行</el-radio>
                  <el-radio value="node">node 节点执行</el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <span class="card-icon">🔓</span>
              <div class="card-titles">
                <div class="card-title">权限策略</div>
                <div class="card-desc">云主机推荐完全开放</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-group">
                <div class="field-label">权限询问</div>
                <el-radio-group v-model="form.execAsk" class="radio-pills-v">
                  <el-radio value="off">off 不询问，直接执行</el-radio>
                  <el-radio value="on-miss">on-miss 未匹配时询问</el-radio>
                  <el-radio value="always">always 始终询问</el-radio>
                </el-radio-group>
              </div>
              <div class="field-group">
                <div class="field-label">安全模式</div>
                <el-radio-group v-model="form.execSecurity" class="radio-pills-v">
                  <el-radio value="full">full 无限制，完全开放</el-radio>
                  <el-radio value="allowlist">allowlist 白名单制</el-radio>
                  <el-radio value="deny">deny 拒绝所有</el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <span class="card-icon">🛡️</span>
              <div class="card-titles">
                <div class="card-title">沙箱与压缩</div>
                <div class="card-desc">安全隔离与历史压缩策略</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-group">
                <div class="field-label">沙箱模式</div>
                <el-radio-group v-model="form.sandboxMode" class="radio-pills-v">
                  <el-radio value="off">off 关闭沙箱</el-radio>
                  <el-radio value="safeguard">safeguard 安全保护</el-radio>
                  <el-radio value="default">default 默认</el-radio>
                  <el-radio value="non-main">non-main 非主线程</el-radio>
                  <el-radio value="all">all 全部隔离</el-radio>
                </el-radio-group>
              </div>
              <div class="field-group">
                <div class="field-label">压缩模式</div>
                <el-radio-group v-model="form.compactionMode" class="radio-pills-v">
                  <el-radio value="safeguard">safeguard 安全压缩</el-radio>
                  <el-radio value="default">default 默认压缩</el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <span class="card-icon">💬</span>
              <div class="card-titles">
                <div class="card-title">会话管理</div>
                <div class="card-desc">私聊会话作用域</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-group">
                <div class="field-label">会话范围</div>
                <el-radio-group v-model="form.dmScope" class="radio-pills-v">
                  <el-radio value="per-channel-peer">per-channel-peer 按频道隔离</el-radio>
                  <el-radio value="global">global 全局共享</el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <span class="card-icon">🌐</span>
              <div class="card-titles">
                <div class="card-title">网络工具</div>
                <div class="card-desc">搜索与网页抓取配置</div>
              </div>
            </div>
            <div class="card-body">
              <div class="field-group">
                <div class="field-label">搜索引擎</div>
                <el-radio-group v-model="form.webSearchProvider" class="radio-pills-v">
                  <el-radio value="brave">brave</el-radio>
                  <el-radio value="google">google</el-radio>
                  <el-radio value="duckduckgo">duckduckgo</el-radio>
                </el-radio-group>
              </div>
              <div class="field-group">
                <div class="field-label">网页抓取</div>
                <el-switch v-model="form.webFetchEnabled" active-text="开启" inactive-text="关闭" />
              </div>
            </div>
          </div>

        </div>
      </template>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false" size="large">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving" size="large">保存设置</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:9131/api'

const props = defineProps({
  modelValue: Boolean
})
const emit = defineEmits(['update:modelValue', 'saved'])

const visible = ref(false)
const loading = ref(false)
const saving = ref(false)

const form = ref({
  toolsProfile: 'full',
  allowExec: true,
  allowBrowser: true,
  allowWebSearch: true,
  allowWebFetch: true,
  denyElevated: false,
  denyShell: false,
  execHost: 'gateway',
  execAsk: 'off',
  execSecurity: 'full',
  sandboxMode: 'off',
  compactionMode: 'safeguard',
  dmScope: 'per-channel-peer',
  webSearchProvider: 'brave',
  webFetchEnabled: true,
})

const defaults = { ...form.value }

watch(() => props.modelValue, async (val) => {
  visible.value = val
  if (val) await loadSettings()
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const loadSettings = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`${API_BASE}/settings`)
    const d = resp.data
    form.value = {
      toolsProfile: d.toolsProfile ?? defaults.toolsProfile,
      allowExec: d.allowExec ?? true,
      allowBrowser: d.allowBrowser ?? true,
      allowWebSearch: d.allowWebSearch ?? true,
      allowWebFetch: d.allowWebFetch ?? true,
      denyElevated: d.denyElevated ?? false,
      denyShell: d.denyShell ?? false,
      execHost: d.execHost ?? defaults.execHost,
      execAsk: d.execAsk ?? defaults.execAsk,
      execSecurity: d.execSecurity ?? defaults.execSecurity,
      sandboxMode: d.sandboxMode ?? defaults.sandboxMode,
      compactionMode: d.compactionMode ?? defaults.compactionMode,
      dmScope: d.dmScope ?? defaults.dmScope,
      webSearchProvider: d.webSearchProvider ?? defaults.webSearchProvider,
      webFetchEnabled: d.webFetchEnabled ?? true,
    }
  } catch (e) {
    ElMessage.warning('加载高级设置失败，使用默认值')
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    const resp = await axios.put(`${API_BASE}/settings`, form.value)
    ElMessage.success(resp.data.message || '保存成功')
    visible.value = false
    emit('saved')
  } catch (e) {
    ElMessage.error('保存失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.settings-content { padding: 0; }

.settings-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.card-full {
  grid-column: 1 / -1;
}

.setting-card {
  background: white;
  border: 1.5px solid #e4e8f4;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: linear-gradient(135deg, #f5f7ff 0%, #eef1fa 100%);
  border-bottom: 1px solid #dde3f5;
}

.card-icon { font-size: 22px; line-height: 1; }

.card-titles { display: flex; flex-direction: column; gap: 1px; }
.card-title { font-size: 14px; font-weight: 700; color: #1a1a2e; }
.card-desc { font-size: 11px; color: #8891a8; }

.card-body {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field-group { display: flex; flex-direction: column; gap: 8px; }

.field-row { display: flex; gap: 24px; }
.gap-40 { gap: 40px; }

.field-divider { height: 1px; background: #eef1f8; margin: 2px 0; }

.field-label { font-size: 12px; font-weight: 600; color: #5a6a85; letter-spacing: 0.5px; }

.radio-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.radio-pills-v { display: flex; flex-direction: column; gap: 6px; }

.radio-pills :deep(.el-radio),
.radio-pills-v :deep(.el-radio) {
  margin-right: 0;
  padding: 5px 14px;
  border: 1.5px solid #d8dff0;
  border-radius: 6px;
  font-size: 13px;
  background: white;
  transition: all 0.2s;
}

.radio-pills :deep(.el-radio:hover),
.radio-pills-v :deep(.el-radio:hover) {
  border-color: #409eff;
  color: #409eff;
}

.radio-pills :deep(.el-radio.is-checked),
.radio-pills-v :deep(.el-radio.is-checked) {
  border-color: #409eff;
  background: #ecf5ff;
  color: #409eff;
  font-weight: 600;
}

.radio-pills :deep(.el-radio__label),
.radio-pills-v :deep(.el-radio__label) { font-size: 13px; padding-left: 6px; }

.checkbox-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

:deep(.el-checkbox) { font-size: 13px; }
:deep(.el-switch) { --el-switch-on-color: #409eff; }

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
