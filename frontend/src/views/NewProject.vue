<template>
  <div class="new-project-page">

    <!-- Navbar -->
    <nav class="navbar" aria-label="Main navigation">
      <span class="nav-wordmark">ENDORA</span>
      <router-link to="/" class="nav-back">
        <span class="back-arrow">←</span> Back
      </router-link>
    </nav>

    <!-- Main layout -->
    <main class="main-grid">

      <!-- ── Left column: Form ─────────────────────────────── -->
      <div class="form-col">
        <!-- Page header -->
        <header class="page-header">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <router-link to="/" class="crumb-link">Home</router-link>
            <span class="crumb-sep">/</span>
            <span class="crumb-current">New Simulation</span>
          </nav>
          <h1 class="page-title">New Simulation</h1>
          <p class="page-sub">Configure your intelligence simulation in three steps.</p>
        </header>

        <!-- Step 1: Industry -->
        <section class="form-section" aria-labelledby="step1-label">
          <div class="step-label" id="step1-label">◈ 01 / SELECT INDUSTRY</div>
          <div class="industry-grid" role="radiogroup" aria-label="Industry selection">
            <button
              v-for="ind in industries"
              :key="ind.key"
              class="industry-pill"
              :class="{ selected: selectedIndustry === ind.key }"
              role="radio"
              :aria-checked="selectedIndustry === ind.key"
              @click="selectIndustry(ind.key)"
            >
              <span class="pill-icon" aria-hidden="true">{{ ind.icon }}</span>
              <span class="pill-label">{{ ind.label }}</span>
            </button>
          </div>
        </section>

        <!-- Step 2: Upload -->
        <section class="form-section" aria-labelledby="step2-label">
          <div class="step-label" id="step2-label">◈ 02 / UPLOAD DOCUMENTS</div>
          <div
            class="drop-zone"
            :class="{ 'drag-over': isDragOver }"
            role="button"
            tabindex="0"
            aria-label="Drop files here or click to browse"
            @click="triggerFileInput"
            @keydown.enter.prevent="triggerFileInput"
            @keydown.space.prevent="triggerFileInput"
            @dragover.prevent="onDragOver"
            @dragleave.prevent="onDragLeave"
            @drop.prevent="onDrop"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.md,.txt,.docx"
              class="file-input-hidden"
              aria-hidden="true"
              tabindex="-1"
              @change="onFileInput"
            />
            <span class="drop-icon" aria-hidden="true">◈</span>
            <span class="drop-main">Drop files here</span>
            <span class="drop-types">PDF, MD, TXT, DOCX supported</span>
            <span class="drop-or">or click to browse</span>
          </div>

          <!-- File chips -->
          <div v-if="uploadedFiles.length > 0" class="file-chips" aria-label="Uploaded files">
            <div
              v-for="(file, index) in uploadedFiles"
              :key="index"
              class="file-chip"
            >
              <span class="chip-name">{{ file.name }}</span>
              <span class="chip-size">{{ formatSize(file.size) }}</span>
              <button
                class="chip-remove"
                :aria-label="`Remove ${file.name}`"
                @click="removeFile(index)"
              >×</button>
            </div>
          </div>
        </section>

        <!-- Step 3: Prompt -->
        <section class="form-section" aria-labelledby="step3-label">
          <div class="step-label" id="step3-label">◈ 03 / SIMULATION PROMPT</div>
          <div class="textarea-wrap">
            <textarea
              v-model="prompt"
              class="prompt-textarea"
              rows="5"
              placeholder='// Describe your prediction goal in natural language. E.g. "Simulate how patients respond to a new triage protocol over 30 days"'
              aria-label="Simulation prompt"
              maxlength="2000"
            ></textarea>
            <span class="char-counter" aria-live="polite">{{ prompt.length }} / 2000</span>
          </div>
        </section>

        <!-- Submit -->
        <div class="submit-wrap">
          <button
            class="submit-btn"
            :class="{ loading: isLoading, disabled: !canSubmit }"
            :disabled="!canSubmit || isLoading"
            aria-label="Initialize simulation"
            @click="handleSubmit"
          >
            <span v-if="isLoading" class="btn-spinner" aria-hidden="true"></span>
            <span v-if="isLoading">Initializing...</span>
            <span v-else>◈ Initialize Simulation</span>
          </button>
          <p v-if="submitError" class="submit-error" role="alert">{{ submitError }}</p>
        </div>
      </div>

      <!-- ── Right column: Preview card ───────────────────── -->
      <aside class="preview-col" aria-label="Simulation preview">
        <div class="preview-card">
          <div class="preview-header">SIMULATION PREVIEW</div>

          <dl class="preview-fields">
            <div class="preview-row">
              <dt class="preview-key">Industry</dt>
              <dd class="preview-val" :class="{ empty: !selectedIndustry }">
                {{ selectedIndustryLabel }}
              </dd>
            </div>
            <div class="preview-row">
              <dt class="preview-key">Documents</dt>
              <dd class="preview-val" :class="{ empty: uploadedFiles.length === 0 }">
                {{ uploadedFiles.length === 0 ? '0 files' : `${uploadedFiles.length} file${uploadedFiles.length > 1 ? 's' : ''}` }}
              </dd>
            </div>
            <div class="preview-row">
              <dt class="preview-key">Prompt</dt>
              <dd class="preview-val prompt-preview" :class="{ empty: !prompt.trim() }">
                {{ promptPreview }}
              </dd>
            </div>
            <div class="preview-divider" aria-hidden="true"></div>
            <div class="preview-row">
              <dt class="preview-key">Estimated cost</dt>
              <dd class="preview-val cost-val">~$0.50–$5.00</dd>
            </div>
            <div class="preview-row">
              <dt class="preview-key">Est. duration</dt>
              <dd class="preview-val cost-val">2–10 min</dd>
            </div>
          </dl>
        </div>

        <!-- Tips -->
        <div class="tips-box" aria-label="Tips">
          <div class="tips-header">Tips</div>
          <ul class="tips-list">
            <li class="tip-item">💡 More documents = richer agent personas</li>
            <li class="tip-item">💡 Specific prompts yield more actionable insights</li>
            <li class="tip-item">💡 Finance simulations work best with 6–12 month data</li>
          </ul>
        </div>
      </aside>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { generateOntology } from '../api/graph'

const router = useRouter()

// ── State ─────────────────────────────────────────────────
const selectedIndustry = ref(null)
const uploadedFiles    = ref([])
const prompt           = ref('')
const isLoading        = ref(false)
const submitError      = ref(null)
const isDragOver       = ref(false)
const fileInput        = ref(null)

// ── Data ──────────────────────────────────────────────────
const industries = [
  { key: 'healthcare',  icon: '⚕', label: 'Healthcare'  },
  { key: 'finance',     icon: '◈', label: 'Finance'     },
  { key: 'defense',     icon: '⬡', label: 'Defense'     },
  { key: 'real-estate', icon: '▣', label: 'Real Estate' },
  { key: 'environment', icon: '◉', label: 'Environment' },
  { key: 'politics',    icon: '◫', label: 'Politics'    },
]

// ── Computed ──────────────────────────────────────────────
const canSubmit = computed(() =>
  selectedIndustry.value !== null && prompt.value.trim().length > 10
)

const selectedIndustryLabel = computed(() => {
  if (!selectedIndustry.value) return '—'
  return industries.find(i => i.key === selectedIndustry.value)?.label ?? '—'
})

const promptPreview = computed(() => {
  const trimmed = prompt.value.trim()
  if (!trimmed) return '—'
  return trimmed.length > 80 ? trimmed.slice(0, 80) + '…' : trimmed
})

// ── Methods ───────────────────────────────────────────────
const selectIndustry = (key) => {
  selectedIndustry.value = key
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const onFileInput = (event) => {
  const files = Array.from(event.target.files ?? [])
  pushFiles(files)
  event.target.value = ''
}

const onDragOver = () => {
  isDragOver.value = true
}

const onDragLeave = () => {
  isDragOver.value = false
}

const onDrop = (event) => {
  isDragOver.value = false
  const files = Array.from(event.dataTransfer?.files ?? [])
  pushFiles(files)
}

const pushFiles = (files) => {
  const allowed = ['.pdf', '.md', '.txt', '.docx']
  const filtered = files.filter(f => allowed.some(ext => f.name.toLowerCase().endsWith(ext)))
  uploadedFiles.value = [...uploadedFiles.value, ...filtered]
}

const removeFile = (index) => {
  uploadedFiles.value = uploadedFiles.value.filter((_, i) => i !== index)
}

const formatSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const handleSubmit = async () => {
  if (!canSubmit.value) return
  isLoading.value  = true
  submitError.value = null

  try {
    const formData = new FormData()
    formData.append('simulation_requirement', prompt.value)
    formData.append('project_name', `${selectedIndustryLabel.value} Simulation`)
    uploadedFiles.value.forEach(f => formData.append('files', f))

    const res = await generateOntology(formData)

    if (res.success && res.data?.project_id) {
      router.push({ name: 'Process', params: { projectId: res.data.project_id } })
    } else {
      submitError.value = res.error || 'Failed to initialize simulation'
    }
  } catch (e) {
    submitError.value = e.message || 'An unexpected error occurred'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ── Tokens ─── */
.new-project-page {
  --bg: #080c12; --bg-panel: #0d1117;
  --border: rgba(255,255,255,0.07); --border-str: rgba(255,255,255,0.12);
  --accent: #6366f1; --accent-lt: #a5b4fc;
  --orange: #f97316; --green: #22c55e; --red: #ef4444;
  --text: #f0f0f0; --muted: #888;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  font-family: var(--sans); min-height: 100vh;
}

/* ── Navbar ─── */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  height: 64px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 48px;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  background: rgba(8,12,18,0.88);
  border-bottom: 1px solid var(--border);
}

.nav-wordmark {
  font-family: var(--mono);
  font-weight: 800; font-size: 1.05rem;
  letter-spacing: 3px; color: #fff; user-select: none;
}

.nav-back {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.85rem; color: var(--muted);
  text-decoration: none;
  transition: color 0.2s;
}
.nav-back:hover { color: var(--text); }
.back-arrow { font-size: 1rem; }

/* ── Main grid ─── */
.main-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 100px 48px 80px;
}

/* ── Page header ─── */
.page-header { margin-bottom: 48px; }.breadcrumb { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font-family: var(--mono); font-size: 0.75rem; }
.crumb-link { color: var(--muted); text-decoration: none; transition: color 0.2s; }
.crumb-link:hover { color: var(--text); }
.crumb-sep { color: var(--border-str); }
.crumb-current { color: var(--text); }
.page-title { font-size: clamp(2rem, 3vw + 0.5rem, 2.8rem); font-weight: 800; letter-spacing: -0.03em; color: #fff; margin: 0 0 12px; }
.page-sub { font-size: 1rem; color: var(--muted); line-height: 1.7; margin: 0; }

/* ── Form sections ─── */
.form-section { margin-bottom: 40px; }
.step-label { font-family: var(--mono); font-size: 0.7rem; font-variant: small-caps; letter-spacing: 0.18em; color: var(--accent); margin-bottom: 16px; }

/* ── Industry pills ─── */
.industry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.industry-pill {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px;
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--muted);
  font-family: var(--sans); font-size: 0.88rem; font-weight: 500;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s, background 0.2s, box-shadow 0.2s;
  text-align: left;
}
.industry-pill:hover {
  border-color: rgba(99,102,241,0.45);
  color: var(--text);
  background: rgba(99,102,241,0.04);
}
.industry-pill.selected {
  border-color: var(--accent);
  color: var(--accent-lt);
  background: rgba(99,102,241,0.08);
  box-shadow: 0 0 0 1px rgba(99,102,241,0.25), 0 0 16px rgba(99,102,241,0.12);
}

.pill-icon { font-size: 1.1rem; line-height: 1; flex-shrink: 0; }
.pill-label { line-height: 1.2; }

/* ── Drop zone ─── */
.drop-zone {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 6px;
  padding: 40px 24px;
  border: 1.5px dashed rgba(99,102,241,0.3);
  border-radius: 12px;
  background: transparent;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  text-align: center;
}
.drop-zone:hover,
.drop-zone:focus-visible,
.drop-zone.drag-over {
  background: rgba(99,102,241,0.05);
  border-color: rgba(99,102,241,0.55);
  outline: none;
}

.file-input-hidden { display: none; }

.drop-icon {
  font-size: 1.5rem; color: var(--accent);
  margin-bottom: 6px; line-height: 1;
}
.drop-main  { font-size: 0.95rem; font-weight: 600; color: var(--text); }
.drop-types { font-family: var(--mono); font-size: 0.72rem; color: var(--muted); }
.drop-or    { font-size: 0.82rem; color: var(--muted); }

/* ── File chips ─── */
.file-chips {
  display: flex; flex-wrap: wrap;
  gap: 8px; margin-top: 12px;
}

.file-chip {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 12px;
  background: rgba(99,102,241,0.08);
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 6px;
  font-size: 0.8rem;
  max-width: 280px;
}
.chip-name {
  font-family: var(--mono); color: var(--text);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  max-width: 160px;
}
.chip-size { color: var(--muted); white-space: nowrap; }
.chip-remove {
  background: none; border: none;
  color: var(--muted); font-size: 1rem;
  line-height: 1; cursor: pointer; padding: 0 2px;
  flex-shrink: 0;
  transition: color 0.15s;
}
.chip-remove:hover { color: var(--red); }

/* ── Textarea ─── */
.textarea-wrap { position: relative; }

.prompt-textarea {
  width: 100%; box-sizing: border-box;
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  font-family: var(--mono); font-size: 0.85rem;
  line-height: 1.7; padding: 16px;
  resize: vertical; min-height: 120px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.prompt-textarea::placeholder { color: var(--muted); opacity: 0.7; }
.prompt-textarea:focus {
  outline: none;
  border-color: rgba(99,102,241,0.5);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.08);
}

.char-counter { position: absolute; bottom: 12px; right: 14px; font-family: var(--mono); font-size: 0.7rem; color: var(--muted); pointer-events: none; }

/* ── Submit ─── */
.submit-wrap { margin-top: 8px; }

.submit-btn {
  width: 100%;
  display: flex; align-items: center; justify-content: center; gap: 10px;
  padding: 16px 32px;
  background: var(--accent); color: #fff; border: none;
  border-radius: 10px;
  font-family: var(--sans); font-size: 1rem; font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 32px rgba(99,102,241,0.3);
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
}
.submit-btn:hover:not(.disabled):not(.loading) {
  opacity: 0.9; transform: translateY(-2px);
  box-shadow: 0 0 48px rgba(99,102,241,0.45);
}
.submit-btn.disabled {
  background: rgba(99,102,241,0.3);
  color: rgba(255,255,255,0.4);
  cursor: not-allowed;
  box-shadow: none;
}
.submit-btn.loading { cursor: wait; opacity: 0.85; }

.btn-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.25);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

.submit-error { margin-top: 12px; font-size: 0.85rem; color: var(--red); background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25); border-radius: 6px; padding: 10px 14px; }

/* ── Preview card ─── */
.preview-col {
  position: sticky; top: 80px;
  align-self: start;
  display: flex; flex-direction: column; gap: 16px;
}

.preview-card {
  background: var(--bg-panel);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 0 0 1px rgba(99,102,241,0.08), 0 12px 40px rgba(0,0,0,0.4);
}

.preview-header {
  font-family: var(--mono);
  font-size: 0.68rem; font-variant: small-caps;
  letter-spacing: 0.2em; color: var(--accent-lt);
  padding: 14px 20px;
  background: rgba(99,102,241,0.06);
  border-bottom: 1px solid rgba(99,102,241,0.15);
}

.preview-fields { margin: 0; padding: 20px; display: flex; flex-direction: column; gap: 0; }

.preview-row {
  display: flex; justify-content: space-between; align-items: flex-start;
  gap: 16px; padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.preview-row:last-child { border-bottom: none; }

.preview-key {
  font-family: var(--mono); font-size: 0.75rem;
  color: var(--muted); white-space: nowrap; flex-shrink: 0;
}
.preview-val {
  font-size: 0.85rem; color: var(--text);
  text-align: right; word-break: break-word; max-width: 60%;
}
.preview-val.empty { color: var(--muted); }
.preview-val.prompt-preview {
  font-size: 0.78rem; font-family: var(--mono);
  line-height: 1.5; max-width: 65%;
}
.preview-val.cost-val { color: var(--accent-lt); font-family: var(--mono); }

.preview-divider { height: 1px; background: var(--border); margin: 4px 0; }

/* ── Tips ─── */
.tips-box {
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 12px; overflow: hidden;
}
.tips-header {
  font-family: var(--mono); font-size: 0.68rem;
  font-variant: small-caps; letter-spacing: 0.15em;
  color: var(--muted);
  padding: 10px 16px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--border);
}
.tips-list {
  list-style: none; margin: 0; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 10px;
}
.tip-item { font-size: 0.82rem; color: var(--muted); line-height: 1.5; }

/* ── Responsive ─── */
@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
    padding: 88px 24px 60px;
    gap: 32px;
  }
  .preview-col { position: static; }
  .navbar { padding: 0 24px; }
}
@media (max-width: 640px) {
  .industry-grid { grid-template-columns: repeat(2, 1fr); }
  .main-grid { padding: 80px 16px 48px; }
}
@media (max-width: 480px) {
  .navbar { padding: 0 16px; }
  .industry-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .industry-pill { padding: 12px 10px; font-size: 0.82rem; }
  .submit-btn { font-size: 0.9rem; padding: 14px 20px; }
  .form-section { padding: 20px; }
}
</style>
