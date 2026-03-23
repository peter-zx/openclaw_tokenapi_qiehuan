<template>
  <el-dialog
    v-model="visible"
    title="高级设置"
    width="520px"
    @update:model-value="$emit('update:visible', false)"
  >
    <div class="settings-content">
      <div v-if="loading" class="loading">加载中...</div>
      <template v-else>
        <div class="setting-group">
          <div class="setting-label">执行主机 (tools.exec.host)</div>
          <el-radio-group v-model="form.execHost">
            <el-radio value="sandbox">sandbox</el-radio>
            <el-radio value="gateway">gateway</el-radio>
            <el-radio value="node">node</el-radio>
          </el-radio-group>
          <div class="setting-tip">控制命令执行的环境，推荐 gateway</div>
        </div>

        <div class="setting-group">
          <div class="setting-label">沙箱模式 (agents.defaults.sandbox.mode)</div>
          <el-radio-group v-model="form.sandboxMode">
            <el-radio value="default">default</el-radio>
            <el-radio value="safeguard">safeguard</el-radio>
            <el-radio value="non-main">non-main</el-radio>
            <el-radio value="all">all</el-radio>
          </el-radio-group>
          <div class="setting-tip">控制哪些操作走沙箱隔离</div>
        </div>

        <div class="setting-group">
          <div class="setting-label">压缩模式 (agents.defaults.compaction.mode)</div>
          <el-radio-group v-model="form.compactionMode">
            <el-radio value="default">default</el-radio>
            <el-radio value="safeguard">safeguard</el-radio>
          </el-radio-group>
          <div class="setting-tip">历史记录压缩策略</div>
        </div>

        <div class="setting-group">
          <div class="setting-label">工具配置 (tools.profile)</div>
          <el-radio-group v-model="form.toolsProfile">
            <el-radio value="full">full</el-radio>
            <el-radio value="coding">coding</el-radio>
            <el-radio value="minimal">minimal</el-radio>
          </el-radio-group>
          <div class="setting-tip">工具调用权限级别</div>
        </div>

        <div class="setting-group">
          <div class="setting-label">会话范围 (session.dmScope)</div>
          <el-radio-group v-model="form.dmScope">
            <el-radio value="per-channel-peer">per-channel-peer</el-radio>
            <el-radio value="global">global</el-radio>
          </el-radio-group>
          <div class="setting-tip">私聊会话的作用域</div>
        </div>
      </template>
    </div>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="handleSave" :disabled="loading">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:9131/api'

const props = defineProps({
  modelValue: Boolean
})
const emit = defineEmits(['update:modelValue', 'saved'])

const visible = ref(false)
const loading = ref(false)

const form = ref({
  execHost: 'gateway',
  sandboxMode: 'safeguard',
  compactionMode: 'safeguard',
  toolsProfile: 'full',
  dmScope: 'per-channel-peer'
})

const defaults = {
  execHost: 'gateway',
  sandboxMode: 'safeguard',
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
  } catch {
    Object.assign(form.value, defaults)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  loading.value = true
  try {
    await axios.put(`${API_BASE}/settings`, form.value)
    visible.value = false
    emit('saved')
  } catch (e) {
    console.error('保存失败', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.settings-content { padding: 10px 0; }
.loading { text-align: center; color: #909399; padding: 30px; }
.setting-group { margin-bottom: 24px; }
.setting-label { font-size: 14px; font-weight: 600; color: #303133; margin-bottom: 10px; }
.setting-tip { font-size: 12px; color: #909399; margin-top: 6px; }
.el-radio-group { display: flex; flex-direction: column; gap: 8px; }
</style>
