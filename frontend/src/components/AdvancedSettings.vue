<template>
  <el-dialog
    v-model="visible"
    title="高级设置"
    width="680px"
    @update:model-value="$emit('update:visible', false)"
  >
    <div class="settings-content" v-loading="loading">
      <template v-if="!loading">
        <div class="section">
          <div class="section-header">
            <div class="section-icon">⚡</div>
            <div class="section-title-wrap">
              <div class="section-title">执行环境</div>
              <div class="section-desc">控制命令执行的环境与权限级别</div>
            </div>
          </div>
          <div class="setting-row">
            <div class="setting-item">
              <div class="setting-label">执行主机 <span class="label-key">tools.exec.host</span></div>
              <el-radio-group v-model="form.execHost" class="setting-radios">
                <el-radio value="sandbox">sandbox</el-radio>
                <el-radio value="gateway">gateway</el-radio>
                <el-radio value="node">node</el-radio>
              </el-radio-group>
              <div class="setting-tip">sandbox：沙箱隔离 &nbsp;|&nbsp; gateway：在网关执行（推荐）&nbsp;|&nbsp; node：在节点执行</div>
            </div>
          </div>
          <div class="setting-row">
            <div class="setting-item">
              <div class="setting-label">工具配置 <span class="label-key">tools.profile</span></div>
              <el-radio-group v-model="form.toolsProfile" class="setting-radios">
                <el-radio value="full">full</el-radio>
                <el-radio value="coding">coding</el-radio>
                <el-radio value="minimal">minimal</el-radio>
              </el-radio-group>
              <div class="setting-tip">full：完整权限 &nbsp;|&nbsp; coding：仅编码 &nbsp;|&nbsp; minimal：最小权限</div>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="section-header">
            <div class="section-icon">🛡️</div>
            <div class="section-title-wrap">
              <div class="section-title">安全策略</div>
              <div class="section-desc">沙箱隔离与历史压缩的安全策略</div>
            </div>
          </div>
          <div class="setting-row">
            <div class="setting-item">
              <div class="setting-label">沙箱模式 <span class="label-key">agents.defaults.sandbox.mode</span></div>
              <el-radio-group v-model="form.sandboxMode" class="setting-radios">
                <el-radio value="off">off（关闭沙箱）</el-radio>
                <el-radio value="default">default</el-radio>
                <el-radio value="safeguard">safeguard（推荐）</el-radio>
                <el-radio value="non-main">non-main</el-radio>
                <el-radio value="all">all</el-radio>
              </el-radio-group>
              <div class="setting-tip">off：关闭沙箱 &nbsp;|&nbsp; default：默认 &nbsp;|&nbsp; safeguard：安全保护 &nbsp;|&nbsp; non-main：非主线程 &nbsp;|&nbsp; all：全部隔离</div>
            </div>
          </div>
          <div class="setting-row">
            <div class="setting-item">
              <div class="setting-label">压缩模式 <span class="label-key">agents.defaults.compaction.mode</span></div>
              <el-radio-group v-model="form.compactionMode" class="setting-radios">
                <el-radio value="default">default</el-radio>
                <el-radio value="safeguard">safeguard</el-radio>
              </el-radio-group>
              <div class="setting-tip">default：默认压缩 &nbsp;|&nbsp; safeguard：安全压缩（推荐）</div>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="section-header">
            <div class="section-icon">💬</div>
            <div class="section-title-wrap">
              <div class="section-title">会话管理</div>
              <div class="section-desc">私聊会话的作用域控制</div>
            </div>
          </div>
          <div class="setting-row">
            <div class="setting-item">
              <div class="setting-label">会话范围 <span class="label-key">session.dmScope</span></div>
              <el-radio-group v-model="form.dmScope" class="setting-radios">
                <el-radio value="per-channel-peer">per-channel-peer</el-radio>
                <el-radio value="global">global</el-radio>
              </el-radio-group>
              <div class="setting-tip">per-channel-peer：按频道隔离 &nbsp;|&nbsp; global：全局共享</div>
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
  execHost: 'gateway',
  sandboxMode: 'off',
  compactionMode: 'safeguard',
  toolsProfile: 'full',
  dmScope: 'per-channel-peer'
})

const defaults = {
  execHost: 'gateway',
  sandboxMode: 'off',
  compactionMode: 'safeguard',
  toolsProfile: 'full',
  dmScope: 'per-channel-peer'
}

watch(() => props.modelValue, async (val) => {
  visible.value = val
  if (val) {
    await loadSettings()
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const loadSettings = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`${API_BASE}/settings`)
    const data = resp.data
    form.value = {
      execHost: data.execHost || defaults.execHost,
      sandboxMode: data.sandboxMode || defaults.sandboxMode,
      compactionMode: data.compactionMode || defaults.compactionMode,
      toolsProfile: data.toolsProfile || defaults.toolsProfile,
      dmScope: data.dmScope || defaults.dmScope
    }
  } catch (e) {
    ElMessage.warning('加载高级设置失败，使用默认值')
    Object.assign(form.value, defaults)
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
.settings-content {
  padding: 0 8px;
}

.section {
  background: #f8faff;
  border: 1px solid #e8efff;
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 16px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #dde6ff;
}

.section-icon {
  font-size: 26px;
  line-height: 1;
}

.section-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  letter-spacing: 1px;
}

.section-desc {
  font-size: 12px;
  color: #8891a8;
}

.setting-row {
  margin-bottom: 18px;
}
.setting-row:last-child {
  margin-bottom: 0;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-label {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.label-key {
  font-size: 11px;
  font-weight: 400;
  color: #909399;
  background: #edf0f7;
  padding: 1px 6px;
  border-radius: 4px;
  margin-left: 8px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.setting-radios {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 6px;
}

.setting-radios :deep(.el-radio) {
  margin-right: 0;
  padding: 6px 16px;
  border: 1.5px solid #dcdfe6;
  border-radius: 6px;
  font-size: 13px;
  transition: all 0.2s;
  background: white;
}

.setting-radios :deep(.el-radio:hover) {
  border-color: #409eff;
  color: #409eff;
}

.setting-radios :deep(.el-radio.is-checked) {
  border-color: #409eff;
  background: #ecf5ff;
  color: #409eff;
}

.setting-radios :deep(.el-radio__label) {
  font-size: 13px;
  padding-left: 6px;
}

.setting-tip {
  font-size: 12px;
  color: #a0aab8;
  line-height: 1.5;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
