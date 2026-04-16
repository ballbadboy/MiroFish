<template>
  <div class="main-view">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <div class="brand" @click="router.push('/')">ENDORA</div>
      </div>
      
      <div class="header-center">
        <div class="view-switcher">
          <button 
            v-for="mode in ['graph', 'split', 'workbench']" 
            :key="mode"
            class="switch-btn"
            :class="{ active: viewMode === mode }"
            @click="viewMode = mode"
          >
            {{ { graph: $t('main.layoutGraph'), split: $t('main.layoutSplit'), workbench: $t('main.layoutWorkbench') }[mode] }}
          </button>
        </div>
      </div>

      <div class="header-right">
        <LanguageSwitcher />
        <div class="step-divider"></div>
        <div class="workflow-step">
          <span class="step-num">Step 3/5</span>
          <span class="step-name">{{ $tm('main.stepNames')[2] }}</span>
        </div>
        <div class="step-divider"></div>
        <span class="status-indicator" :class="statusClass">
          <span class="dot"></span>
          {{ statusText }}
        </span>
        <div class="step-divider"></div>
        <button class="branch-btn" @click="showBranchCreator = true" title="Create what-if branches">
          ◈ Branch
        </button>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="content-area">
      <!-- Left Panel: Graph -->
      <div class="panel-wrapper left" :style="leftPanelStyle">
        <GraphPanel 
          :graphData="graphData"
          :loading="graphLoading"
          :currentPhase="3"
          :isSimulating="isSimulating"
          @refresh="refreshGraph"
          @toggle-maximize="toggleMaximize('graph')"
        />
      </div>

      <!-- Right Panel: Step3 开始模拟 -->
      <div class="panel-wrapper right" :style="rightPanelStyle">
        <Step3Simulation
          :simulationId="currentSimulationId"
          :maxRounds="maxRounds"
          :minutesPerRound="minutesPerRound"
          :projectData="projectData"
          :graphData="graphData"
          :systemLogs="systemLogs"
          @go-back="handleGoBack"
          @next-step="handleNextStep"
          @add-log="addLog"
          @update-status="updateStatus"
        />
      </div>
    </main>

    <!-- Scenario Branch Creator Modal -->
    <ScenarioBranchCreator
      :simulation-id="currentSimulationId"
      :visible="showBranchCreator"
      @close="showBranchCreator = false"
      @experiment-created="handleExperimentCreated"
    />

    <!-- Scenario Comparison Panel (slides in from right when active) -->
    <Transition name="slide-panel">
      <div v-if="comparisonData" class="comparison-overlay">
        <div class="comparison-drawer">
          <div class="drawer-header">
            <span class="drawer-title">◈ EXPERIMENT RESULTS</span>
            <button class="drawer-close" @click="comparisonData = null">×</button>
          </div>
          <ScenarioComparisonPanel :experiment-id="activeExperimentId" />
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GraphPanel from '../components/GraphPanel.vue'
import Step3Simulation from '../components/Step3Simulation.vue'
import ScenarioBranchCreator from '../components/ScenarioBranchCreator.vue'
import ScenarioComparisonPanel from '../components/ScenarioComparisonPanel.vue'
import { getProject, getGraphData } from '../api/graph'
import { getSimulation, getSimulationConfig, stopSimulation, closeSimulationEnv, getEnvStatus, compareBranchExperiment } from '../api/simulation'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

// Props
const props = defineProps({
  simulationId: String
})

// Layout State
const viewMode = ref('split')

// Data State
const currentSimulationId = ref(route.params.simulationId)
// 直接在初始化时从 query 参数获取 maxRounds，确保子组件能立即获取到值
const maxRounds = ref(route.query.maxRounds ? parseInt(route.query.maxRounds) : null)
const minutesPerRound = ref(30) // 默认每轮30分钟
const projectData = ref(null)
const graphData = ref(null)
const graphLoading = ref(false)
const systemLogs = ref([])
const currentStatus = ref('processing') // processing | completed | error

// Scenario Branching state
const showBranchCreator = ref(false)
const activeExperimentId = ref(null)
const comparisonData = ref(null)

// --- Computed Layout Styles ---
const leftPanelStyle = computed(() => {
  if (viewMode.value === 'graph') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'workbench') return { width: '0%', opacity: 0, transform: 'translateX(-20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

const rightPanelStyle = computed(() => {
  if (viewMode.value === 'workbench') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'graph') return { width: '0%', opacity: 0, transform: 'translateX(20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

// --- Status Computed ---
const statusClass = computed(() => {
  return currentStatus.value
})

const statusText = computed(() => {
  if (currentStatus.value === 'error') return 'Error'
  if (currentStatus.value === 'completed') return 'Completed'
  return 'Running'
})

const isSimulating = computed(() => currentStatus.value === 'processing')

// --- Helpers ---
const addLog = (msg) => {
  const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }) + '.' + new Date().getMilliseconds().toString().padStart(3, '0')
  systemLogs.value.push({ time, msg })
  if (systemLogs.value.length > 200) {
    systemLogs.value.shift()
  }
}

const updateStatus = (status) => {
  currentStatus.value = status
}

// --- Layout Methods ---
const toggleMaximize = (target) => {
  if (viewMode.value === target) {
    viewMode.value = 'split'
  } else {
    viewMode.value = target
  }
}

const handleGoBack = async () => {
  // 在返回 Step 2 之前，先关闭正在运行的模拟
  addLog(t('log.preparingGoBack'))
  
  // 停止轮询
  stopGraphRefresh()
  
  try {
    // 先尝试优雅关闭模拟环境
    const envStatusRes = await getEnvStatus({ simulation_id: currentSimulationId.value })
    
    if (envStatusRes.success && envStatusRes.data?.env_alive) {
      addLog(t('log.closingSimEnv'))
      try {
        await closeSimulationEnv({ 
          simulation_id: currentSimulationId.value,
          timeout: 10
        })
        addLog(t('log.simEnvClosed'))
      } catch (closeErr) {
        addLog(t('log.closeSimEnvFailed'))
        try {
          await stopSimulation({ simulation_id: currentSimulationId.value })
          addLog(t('log.simForceStopSuccess'))
        } catch (stopErr) {
          addLog(t('log.forceStopFailed', { error: stopErr.message }))
        }
      }
    } else {
      // 环境未运行，检查是否需要停止进程
      if (isSimulating.value) {
        addLog(t('log.stoppingSimProcess'))
        try {
          await stopSimulation({ simulation_id: currentSimulationId.value })
          addLog(t('log.simStopped'))
        } catch (err) {
          addLog(t('log.stopSimFailed', { error: err.message }))
        }
      }
    }
  } catch (err) {
    addLog(t('log.checkStatusFailed', { error: err.message }))
  }
  
  // 返回到 Step 2 (环境搭建)
  router.push({ name: 'Simulation', params: { simulationId: currentSimulationId.value } })
}

const handleNextStep = () => {
  // Step3Simulation 组件会直接处理报告生成和路由跳转
  // 这个方法仅作为备用
  addLog(t('log.enterStep4'))
}

// --- Data Logic ---
const loadSimulationData = async () => {
  try {
    addLog(t('log.loadingSimData', { id: currentSimulationId.value }))
    
    // 获取 simulation 信息
    const simRes = await getSimulation(currentSimulationId.value)
    if (simRes.success && simRes.data) {
      const simData = simRes.data
      
      // 获取 simulation config 以获取 minutes_per_round
      try {
        const configRes = await getSimulationConfig(currentSimulationId.value)
        if (configRes.success && configRes.data?.time_config?.minutes_per_round) {
          minutesPerRound.value = configRes.data.time_config.minutes_per_round
          addLog(t('log.timeConfig', { minutes: minutesPerRound.value }))
        }
      } catch (configErr) {
        addLog(t('log.timeConfigFetchFailed', { minutes: minutesPerRound.value }))
      }
      
      // 获取 project 信息
      if (simData.project_id) {
        const projRes = await getProject(simData.project_id)
        if (projRes.success && projRes.data) {
          projectData.value = projRes.data
          addLog(t('log.projectLoadSuccess', { id: projRes.data.project_id }))
          
          // 获取 graph 数据
          if (projRes.data.graph_id) {
            await loadGraph(projRes.data.graph_id)
          }
        }
      }
    } else {
      addLog(t('log.loadSimDataFailed', { error: simRes.error || t('common.unknownError') }))
    }
  } catch (err) {
    addLog(t('log.loadException', { error: err.message }))
  }
}

const loadGraph = async (graphId) => {
  // 当正在模拟时，自动刷新不显示全屏 loading，以免闪烁
  // 手动刷新或初始加载时显示 loading
  if (!isSimulating.value) {
    graphLoading.value = true
  }
  
  try {
    const res = await getGraphData(graphId)
    if (res.success) {
      graphData.value = res.data
      if (!isSimulating.value) {
        addLog(t('log.graphDataLoadSuccess'))
      }
    }
  } catch (err) {
    addLog(t('log.graphLoadFailed', { error: err.message }))
  } finally {
    graphLoading.value = false
  }
}

const refreshGraph = () => {
  if (projectData.value?.graph_id) {
    loadGraph(projectData.value.graph_id)
  }
}

// --- Auto Refresh Logic ---
let graphRefreshTimer = null

const startGraphRefresh = () => {
  if (graphRefreshTimer) return
  addLog(t('log.graphRealtimeRefreshStart'))
  // 立即刷新一次，然后每30秒刷新
  graphRefreshTimer = setInterval(refreshGraph, 30000)
}

const stopGraphRefresh = () => {
  if (graphRefreshTimer) {
    clearInterval(graphRefreshTimer)
    graphRefreshTimer = null
    addLog(t('log.graphRealtimeRefreshStop'))
  }
}

// ── Scenario Branching ─────────────────────────────────────────────
const handleExperimentCreated = ({ experimentId, manifest }) => {
  activeExperimentId.value = experimentId
  comparisonData.value = manifest
  showBranchCreator.value = false
  addLog(`◈ Branch experiment created: ${experimentId} (${manifest.branches?.length || 0} branches)`)
}

watch(isSimulating, (newValue) => {
  if (newValue) {
    startGraphRefresh()
  } else {
    stopGraphRefresh()
  }
}, { immediate: true })

onMounted(() => {
  addLog(t('log.simRunViewInit'))
  
  // 记录 maxRounds 配置（值已在初始化时从 query 参数获取）
  if (maxRounds.value) {
    addLog(t('log.customRounds', { rounds: maxRounds.value }))
  }
  
  loadSimulationData()
})

onUnmounted(() => {
  stopGraphRefresh()
})
</script>

<style scoped>
.main-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #080c12;
  overflow: hidden;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: #f0f0f0;
}

/* Header */
.app-header {
  height: 60px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(8,12,18,0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  z-index: 100;
  position: relative;
}

.header-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  font-size: 18px;
  letter-spacing: 2px;
  cursor: pointer;
  color: #fff;
}

.view-switcher {
  display: flex;
  background: rgba(255,255,255,0.05);
  padding: 4px;
  border-radius: 8px;
  gap: 2px;
  border: 1px solid rgba(255,255,255,0.07);
}

.switch-btn {
  border: none;
  background: transparent;
  padding: 5px 14px;
  font-size: 11px;
  font-weight: 600;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.switch-btn:hover {
  color: #a0a0b0;
  background: rgba(255,255,255,0.04);
}

.switch-btn.active {
  background: rgba(99,102,241,0.18);
  color: #a5b4fc;
  border: 1px solid rgba(99,102,241,0.3);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  color: #666;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #6366f1;
}

.step-name {
  font-weight: 600;
  color: #c0c0d0;
}

.step-divider {
  width: 1px;
  height: 14px;
  background-color: rgba(255,255,255,0.1);
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #444;
  flex-shrink: 0;
}

.status-indicator.processing .dot {
  background: #f97316;
  animation: pulse 1.2s ease-in-out infinite;
  box-shadow: 0 0 6px rgba(249,115,22,0.6);
}
.status-indicator.completed .dot {
  background: #22c55e;
  box-shadow: 0 0 6px rgba(34,197,94,0.5);
}
.status-indicator.error .dot {
  background: #ef4444;
  box-shadow: 0 0 6px rgba(239,68,68,0.5);
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}

/* Content */
.content-area {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
}

.panel-wrapper {
  height: 100%;
  overflow: hidden;
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease, transform 0.3s ease;
  will-change: width, opacity, transform;
}

.panel-wrapper.left {
  border-right: 1px solid rgba(255,255,255,0.06);
}

/* Branch button */
.branch-btn {
  background: rgba(99,102,241,0.12); color: #a5b4fc;
  border: 1px solid rgba(99,102,241,0.3); border-radius: 6px;
  padding: 4px 14px; font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem; cursor: pointer; transition: all 0.2s;
  letter-spacing: 0.05em;
}
.branch-btn:hover {
  background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.5);
}

/* Comparison drawer overlay */
.comparison-overlay {
  position: fixed; inset: 0; z-index: 900;
  background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);
  display: flex; justify-content: flex-end;
}
.comparison-drawer {
  width: 560px; max-width: 90vw; height: 100vh;
  background: #0d1117; border-left: 1px solid rgba(255,255,255,0.08);
  overflow-y: auto; padding: 24px;
}
.drawer-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.drawer-title {
  font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
  letter-spacing: 0.12em; color: #a5b4fc; font-variant: small-caps;
}
.drawer-close {
  background: none; border: none; color: #888; font-size: 1.4rem;
  cursor: pointer; transition: color 0.2s;
}
.drawer-close:hover { color: #f0f0f0; }

/* Slide panel transition */
.slide-panel-enter-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-panel-leave-active { transition: all 0.25s ease-in; }
.slide-panel-enter-from .comparison-drawer { transform: translateX(100%); }
.slide-panel-leave-to .comparison-drawer { transform: translateX(100%); }
.slide-panel-enter-from, .slide-panel-leave-to { opacity: 0; }
</style>

