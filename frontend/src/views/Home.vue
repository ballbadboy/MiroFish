<template>
  <div class="home-container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-brand">
        <span class="brand-miro">MIRO</span><span class="brand-fish">FISH</span>
      </div>
      <div class="nav-links">
        <LanguageSwitcher />
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          {{ $t('nav.visitGithub') }} <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="version-badge">
              <span class="badge-dot"></span>
              {{ $t('home.tagline') }} / {{ $t('home.version') }}
            </span>
          </div>

          <h1 class="main-title">
            {{ $t('home.heroTitle1') }}<br>
            <span class="gradient-text">{{ $t('home.heroTitle2') }}</span>
          </h1>

          <div class="hero-desc">
            <p>
              <i18n-t keypath="home.heroDesc" tag="span">
                <template #brand><span class="highlight-bold">{{ $t('home.heroDescBrand') }}</span></template>
                <template #agentScale><span class="highlight-orange">{{ $t('home.heroDescAgentScale') }}</span></template>
                <template #optimalSolution><span class="highlight-code">{{ $t('home.heroDescOptimalSolution') }}</span></template>
              </i18n-t>
            </p>
            <p class="slogan-text">
              {{ $t('home.slogan') }}<span class="blinking-cursor">_</span>
            </p>
          </div>

          <div class="decoration-square"></div>
        </div>

        <div class="hero-right">
          <div class="logo-container">
            <div class="logo-glow"></div>
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="MiroFish Logo" class="hero-logo" />
          </div>

          <button class="scroll-down-btn" @click="scrollToBottom">↓</button>
        </div>
      </section>

      <!-- Dashboard Section -->
      <section class="dashboard-section">
        <!-- Left Panel -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="online-dot"></span>
            <span class="online-label">ONLINE</span>
            <span class="status-sep">&nbsp;/&nbsp;</span>
            {{ $t('home.systemStatus') }}
          </div>

          <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
          <p class="section-desc">{{ $t('home.systemReadyDesc') }}</p>

          <!-- Metric cards -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
              <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
              <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
            </div>
          </div>

          <!-- Workflow steps -->
          <div class="steps-container">
            <div class="steps-header">
              <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <div class="step-indicator">
                  <div class="step-circle active">01</div>
                  <div class="step-line"></div>
                </div>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step01Title') }}</div>
                  <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <div class="step-indicator">
                  <div class="step-circle">02</div>
                  <div class="step-line"></div>
                </div>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step02Title') }}</div>
                  <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <div class="step-indicator">
                  <div class="step-circle">03</div>
                  <div class="step-line"></div>
                </div>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step03Title') }}</div>
                  <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <div class="step-indicator">
                  <div class="step-circle">04</div>
                  <div class="step-line"></div>
                </div>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step04Title') }}</div>
                  <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <div class="step-indicator">
                  <div class="step-circle">05</div>
                  <div class="step-line last"></div>
                </div>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step05Title') }}</div>
                  <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel: Console -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Console title bar -->
            <div class="console-titlebar">
              <div class="titlebar-dots">
                <span class="dot dot-red"></span>
                <span class="dot dot-yellow"></span>
                <span class="dot dot-green"></span>
              </div>
              <span class="titlebar-label">reality-seed.sh</span>
            </div>

            <!-- Upload section -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.realitySeed') }}</span>
                <span class="console-meta">{{ $t('home.supportedFormats') }}</span>
              </div>

              <div
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />

                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17 8 12 3 7 8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                  </div>
                  <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                  <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                </div>

                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Divider -->
            <div class="console-divider">
              <span>{{ $t('home.inputParams') }}</span>
            </div>

            <!-- Textarea section -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  :placeholder="$t('home.promptPlaceholder')"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">{{ $t('home.engineBadge') }}</div>
              </div>
            </div>

            <!-- Start button -->
            <div class="console-section btn-section">
              <button
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
                :class="{ 'is-active': canSubmit && !loading, 'is-loading': loading }"
              >
                <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                <span v-else>{{ $t('home.initializing') }}</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- History -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

const router = useRouter()

// 表单数据
const formData = ref({
  simulationRequirement: ''
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// 文件输入引用
const fileInput = ref(null)

// 计算属性:是否可以提交
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // 存储待上传的数据
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    
    // 立即跳转到Process页面（使用特殊标识表示新建项目）
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* ── Design tokens ─────────────────────────────────── */
:root {
  --bg:             #080c12;
  --bg-card:        rgba(255,255,255,0.04);
  --bg-card-hover:  rgba(255,255,255,0.07);
  --border:         rgba(255,255,255,0.08);
  --border-strong:  rgba(255,255,255,0.15);
  --text:           #f0f0f0;
  --text-2:         #a1a1aa;
  --text-3:         #52525b;
  --accent:         #6366f1;
  --accent-glow:    rgba(99,102,241,0.3);
  --cta:            #f97316;
  --cta-glow:       rgba(249,115,22,0.25);
  --success:        #22c55e;
  --mono:           'JetBrains Mono', monospace;
  --sans:           'Inter', 'Space Grotesk', system-ui, sans-serif;
}

/* ── Base ──────────────────────────────────────────── */
.home-container {
  min-height: 100vh;
  background: var(--bg);
  font-family: var(--sans);
  color: var(--text);
}

/* ── Navbar ────────────────────────────────────────── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  height: 60px;
  background: rgba(8,12,18,0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 48px;
}

.nav-brand {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 1.15rem;
  letter-spacing: 0.5px;
}

.brand-miro {
  color: #fff;
}

.brand-fish {
  color: var(--accent);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.github-link {
  color: var(--text-2);
  text-decoration: none;
  font-family: var(--mono);
  font-size: 0.82rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s;
}

.github-link:hover {
  color: var(--text);
}

.arrow {
  font-size: 0.9rem;
}

/* ── Main content ──────────────────────────────────── */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 72px 48px 80px;
}

/* ── Hero ──────────────────────────────────────────── */
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 96px;
  gap: 48px;
}

.hero-left {
  flex: 1;
  min-width: 0;
}

/* Badge */
.tag-row {
  margin-bottom: 28px;
}

.version-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px;
  border: 1px solid rgba(99,102,241,0.4);
  border-radius: 999px;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--accent);
  letter-spacing: 0.5px;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  flex-shrink: 0;
}

/* Title */
.main-title {
  font-size: 5rem;
  line-height: 1.1;
  font-weight: 800;
  margin: 0 0 36px 0;
  letter-spacing: -0.04em;
  color: var(--text);
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

/* Description */
.hero-desc {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-2);
  max-width: 600px;
  margin-bottom: 40px;
}

.hero-desc p {
  margin-bottom: 1.2rem;
}

.highlight-bold {
  color: var(--text);
  font-weight: 700;
}

.highlight-orange {
  color: var(--cta);
  font-weight: 700;
  font-family: var(--mono);
}

.highlight-code {
  background: rgba(99,102,241,0.12);
  padding: 2px 7px;
  border-radius: 4px;
  font-family: var(--mono);
  font-size: 0.88em;
  color: #a5b4fc;
  font-weight: 600;
}

.slogan-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.02em;
  border-left: 3px solid var(--accent);
  padding-left: 14px;
  margin-top: 16px;
}

.blinking-cursor {
  color: var(--accent);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 14px;
  height: 14px;
  background: var(--cta);
  margin-top: 28px;
}

/* Hero right */
.hero-right {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.logo-container {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.logo-glow {
  position: absolute;
  inset: 10%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
  pointer-events: none;
  filter: blur(24px);
}

.hero-logo {
  max-width: 460px;
  width: 100%;
  position: relative;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  background: #f8f8f8;
  padding: 6px;
  box-shadow:
    0 0 0 1px rgba(99,102,241,0.15),
    0 20px 60px rgba(0,0,0,0.5),
    0 0 80px rgba(99,102,241,0.1);
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border-strong);
  border-radius: 8px;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--accent);
  font-size: 1.1rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--accent);
  background: rgba(99,102,241,0.1);
}

/* ── Dashboard two-column ──────────────────────────── */
.dashboard-section {
  display: flex;
  gap: 48px;
  border-top: 1px solid var(--border);
  padding-top: 64px;
  align-items: flex-start;
}

/* ── Left panel ────────────────────────────────────── */
.left-panel {
  flex: 0.85;
  display: flex;
  flex-direction: column;
}

.panel-header {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--text-3);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 22px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.online-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 6px var(--success);
  flex-shrink: 0;
}

.online-label {
  color: var(--success);
  font-weight: 700;
}

.status-sep {
  color: var(--text-3);
}

.section-title {
  font-size: 2rem;
  font-weight: 400;
  margin: 0 0 12px 0;
  color: var(--text);
  letter-spacing: -0.02em;
}

.section-desc {
  color: var(--text-2);
  margin-bottom: 28px;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Metric cards */
.metrics-row {
  display: flex;
  gap: 16px;
  margin-bottom: 28px;
}

.metric-card {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 22px;
  transition: background 0.2s, border-color 0.2s;
}

.metric-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}

.metric-value {
  font-family: var(--mono);
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 4px;
  color: var(--accent);
}

.metric-label {
  font-size: 0.8rem;
  color: var(--text-3);
  line-height: 1.4;
}

/* Steps */
.steps-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 28px 24px;
}

.steps-header {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--text-3);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.diamond-icon {
  color: var(--accent);
}

.workflow-list {
  display: flex;
  flex-direction: column;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mono);
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--text-3);
  flex-shrink: 0;
}

.step-circle.active {
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(99,102,241,0.12);
  box-shadow: 0 0 10px rgba(99,102,241,0.2);
}

.step-line {
  width: 1px;
  height: 28px;
  background: var(--border);
  margin: 4px 0;
}

.step-line.last {
  display: none;
}

.step-info {
  flex: 1;
  padding-bottom: 12px;
}

.step-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 3px;
  color: var(--text);
}

.step-desc {
  font-size: 0.8rem;
  color: var(--text-2);
  line-height: 1.5;
}

/* ── Right panel: Console ──────────────────────────── */
.right-panel {
  flex: 1.15;
}

.console-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0,0,0,0.4);
}

/* Title bar */
.console-titlebar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--border);
}

.titlebar-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
}

.dot-red    { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green  { background: #28c840; }

.titlebar-label {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--text-3);
  margin-left: 4px;
}

.console-section {
  padding: 20px 24px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-family: var(--mono);
  font-size: 0.72rem;
}

.console-label {
  color: var(--text-2);
  font-weight: 600;
}

.console-meta {
  color: var(--text-3);
}

/* Upload zone */
.upload-zone {
  background: rgba(0,0,0,0.3);
  border: 1.5px dashed var(--border-strong);
  border-radius: 10px;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.25s, background 0.25s, box-shadow 0.25s;
  overflow-y: auto;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover,
.upload-zone.drag-over {
  border-color: var(--accent);
  background: rgba(99,102,241,0.06);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.upload-placeholder {
  text-align: center;
  padding: 20px;
}

.upload-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  border: 1px solid rgba(99,102,241,0.3);
  background: rgba(99,102,241,0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  color: var(--accent);
}

.upload-title {
  font-weight: 500;
  font-size: 0.88rem;
  margin-bottom: 4px;
  color: var(--text-2);
}

.upload-hint {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--text-3);
}

.file-list {
  width: 100%;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 7px 12px;
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-2);
}

.file-name {
  flex: 1;
  margin: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--text-3);
  padding: 0 2px;
  line-height: 1;
  transition: color 0.15s;
}

.remove-btn:hover {
  color: var(--text);
}

/* Divider */
.console-divider {
  display: flex;
  align-items: center;
  margin: 4px 0;
  padding: 0 24px;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.console-divider span {
  padding: 0 14px;
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-3);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

/* Textarea */
.input-wrapper {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(0,0,0,0.25);
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 16px 18px 36px;
  font-family: var(--mono);
  font-size: 0.85rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 130px;
  color: var(--text);
  caret-color: var(--accent);
}

.code-input::placeholder {
  color: var(--text-3);
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 14px;
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-3);
  pointer-events: none;
}

/* Start engine button */
.start-engine-btn {
  width: 100%;
  height: 60px;
  background: rgba(255,255,255,0.06);
  color: var(--text-3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0 24px;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: not-allowed;
  transition: all 0.3s ease;
  letter-spacing: 0.06em;
  position: relative;
  overflow: hidden;
}

.start-engine-btn.is-active {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border-color: transparent;
  cursor: pointer;
  box-shadow: 0 0 0 0 rgba(99,102,241,0);
  animation: pulse-glow 2.4s ease-in-out infinite;
}

.start-engine-btn.is-active:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(99,102,241,0.45);
}

.start-engine-btn.is-active:active {
  transform: translateY(0);
}

.start-engine-btn.is-loading {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border-color: transparent;
  cursor: wait;
  opacity: 0.75;
}

.btn-arrow {
  font-size: 1.1rem;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.4); }
  50%       { box-shadow: 0 0 0 8px rgba(99,102,241,0); }
}

/* ── Responsive ────────────────────────────────────── */
@media (max-width: 1024px) {
  .navbar {
    padding: 0 24px;
  }

  .main-content {
    padding: 48px 24px 60px;
  }

  .hero-section {
    flex-direction: column;
    margin-bottom: 64px;
  }

  .main-title {
    font-size: 3.2rem;
  }

  .hero-right {
    align-items: flex-start;
  }

  .hero-logo {
    max-width: 280px;
  }

  .dashboard-section {
    flex-direction: column;
    gap: 40px;
  }

  .metrics-row {
    flex-direction: column;
  }
}
</style>

<style>
/* English locale adjustments (unscoped to target html[lang]) */
html[lang="en"] .main-title {
  font-size: 3.8rem;
  letter-spacing: -0.03em;
}

html[lang="en"] .hero-desc {
  text-align: left;
  letter-spacing: 0;
}

html[lang="en"] .slogan-text {
  letter-spacing: 0;
}
</style>
