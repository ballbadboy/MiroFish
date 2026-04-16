<template>
  <div class="scenario-panel">

    <!-- ── Loading ── -->
    <div v-if="state === 'loading'" class="panel-loading">
      <div class="spinner"></div>
      <span>Fetching scenario comparison…</span>
    </div>

    <!-- ── Error ── -->
    <div v-else-if="state === 'error'" class="panel-error">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <span>{{ errorMsg }}</span>
    </div>

    <!-- ── Result ── -->
    <template v-else-if="state === 'done' && result">

      <!-- Header -->
      <div class="panel-header">
        <div class="panel-title">
          <span class="label-tag">SCENARIO COMPARISON</span>
          <span class="exp-id">{{ result.experiment_id }}</span>
        </div>
        <div class="panel-meta">
          <span class="meta-item">
            BASE:
            <strong class="mono">{{ result.base_simulation_id }}</strong>
          </span>
          <span class="meta-item" v-if="result.branches?.length">
            {{ result.branches.length }} BRANCHES
          </span>
          <span class="meta-item" v-if="result.divergence_round">
            DIVERGES AT
            <strong class="mono red">R{{ result.divergence_round }}</strong>
          </span>
        </div>
      </div>

      <!-- Winner Banner -->
      <div v-if="result.winner" class="winner-banner">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <span>
          <strong>{{ result.winner }}</strong> shows highest sentiment by final round
        </span>
      </div>

      <!-- Sentiment Chart -->
      <div class="chart-section">
        <div class="section-label">SENTIMENT TRAJECTORY</div>
        <SentimentChart
          :series="chartSeries"
          :divergence-round="result.divergence_round"
          :winner-name="result.winner"
          :height="220"
        />
      </div>

      <!-- Branch Cards -->
      <div class="branches-grid">
        <div
          v-for="branch in result.branches"
          :key="branch.branch_name"
          class="branch-card"
          :class="{
            'is-winner': result.winner && branch.branch_name === result.winner,
            'is-failed': branch.status === 'failed',
          }"
        >
          <!-- Card Header -->
          <div class="card-top">
            <div class="branch-name">
              <span class="branch-dot" :class="{ 'dot-winner': result.winner && branch.branch_name === result.winner }"></span>
              {{ branch.branch_name }}
            </div>
            <div class="card-badges">
              <span v-if="result.winner && branch.branch_name === result.winner" class="badge-winner">★ WINNER</span>
              <span class="status-badge" :class="`status-${branch.status}`">{{ branch.status?.toUpperCase() }}</span>
            </div>
          </div>

          <!-- Description -->
          <p class="branch-desc">{{ branch.branch_description }}</p>

          <!-- Stats row -->
          <div class="stat-row">
            <div class="stat-cell">
              <span class="stat-label">ROUNDS</span>
              <span class="stat-val mono">{{ branch.rounds_completed ?? '—' }}</span>
            </div>
            <div class="stat-cell">
              <span class="stat-label">ACTIONS</span>
              <span class="stat-val mono">{{ totalActions(branch) }}</span>
            </div>
            <div class="stat-cell">
              <span class="stat-label">FINAL SENTIMENT</span>
              <span class="stat-val mono" :class="sentimentClass(finalSentiment(branch))">
                {{ finalSentiment(branch) != null ? `${(finalSentiment(branch) * 100).toFixed(0)}%` : '—' }}
              </span>
            </div>
          </div>

          <!-- Action breakdown -->
          <div v-if="branch.action_counts && Object.keys(branch.action_counts).length" class="action-pills">
            <span
              v-for="(count, action) in branch.action_counts"
              :key="action"
              class="action-pill"
            >{{ action }} <strong>{{ count }}</strong></span>
          </div>

          <!-- Top posts preview -->
          <div v-if="branch.top_posts?.length" class="top-posts">
            <div class="top-posts-label">TOP POSTS</div>
            <div
              v-for="(post, idx) in branch.top_posts.slice(0, 2)"
              :key="idx"
              class="post-preview"
            >
              "{{ truncate(post, 100) }}"
            </div>
          </div>

          <!-- Error display -->
          <div v-if="branch.error" class="branch-error">
            ⚠ {{ branch.error }}
          </div>
        </div>
      </div>

      <!-- Summary text -->
      <div v-if="result.summary" class="summary-block">
        <div class="section-label">ANALYSIS SUMMARY</div>
        <p class="summary-text">{{ result.summary }}</p>
      </div>

    </template>

    <!-- ── Empty ── -->
    <div v-else-if="state === 'idle'" class="panel-empty">
      No experiment data available
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import SentimentChart from './SentimentChart.vue'
import { compareBranchExperiment } from '../api/simulation'

// ─── Props ────────────────────────────────────────────────────────────────────
const props = defineProps({
  /** Experiment ID to fetch and display */
  experimentId: { type: String, required: true },
  /** Sentiment divergence threshold (0–1) */
  divergenceThreshold: { type: Number, default: 0.15 },
})

// ─── State ────────────────────────────────────────────────────────────────────
const state    = ref('idle')   // idle | loading | done | error
const result   = ref(null)
const errorMsg = ref('')

// ─── Computed ─────────────────────────────────────────────────────────────────
/** Build multi-series data for SentimentChart */
const chartSeries = computed(() => {
  if (!result.value?.branches) return []
  return result.value.branches
    .filter(b => b.sentiment_per_round?.length)
    .map(b => ({
      name: b.branch_name,
      data: b.sentiment_per_round,
    }))
})

// ─── Helpers ──────────────────────────────────────────────────────────────────
const totalActions = (branch) => {
  if (!branch.action_counts) return '—'
  return Object.values(branch.action_counts).reduce((a, b) => a + b, 0)
}

const finalSentiment = (branch) => {
  const arr = branch.sentiment_per_round
  if (!arr?.length) return null
  return arr.at(-1)
}

const sentimentClass = (val) => {
  if (val == null) return ''
  if (val >= 0.6) return 'val-positive'
  if (val <= 0.4) return 'val-negative'
  return 'val-neutral'
}

const truncate = (str, max) =>
  str?.length > max ? str.slice(0, max) + '…' : str

// ─── Data fetch ───────────────────────────────────────────────────────────────
async function fetchComparison() {
  if (!props.experimentId) return
  state.value = 'loading'
  errorMsg.value = ''

  try {
    const res = await compareBranchExperiment(props.experimentId, props.divergenceThreshold)
    if (res?.data) {
      result.value = res.data
      state.value  = 'done'
    } else {
      throw new Error(res?.error || 'Empty response')
    }
  } catch (err) {
    errorMsg.value = err?.response?.data?.error || err.message || 'Failed to load comparison'
    state.value    = 'error'
  }
}

watch(() => props.experimentId, fetchComparison)
onMounted(fetchComparison)
</script>

<style scoped>
.scenario-panel {
  font-family: 'Space Grotesk', system-ui, sans-serif;
  color: #f0f0f0;
  background: #0d1117;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 4px;
  overflow: hidden;
}

/* ── Loading / Error / Empty ── */
.panel-loading,
.panel-error,
.panel-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 48px 24px;
  font-size: 13px;
  color: #a0a0b0;
}

.panel-error { color: #ef4444; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.07);
  border-top-color: #f0f0f0;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Header ── */
.panel-header {
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 8px;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label-tag {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-family: 'JetBrains Mono', monospace;
  color: #a0a0b0;
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.3);
  padding: 3px 7px;
  border-radius: 2px;
}

.exp-id {
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  color: #a0a0b0;
}

.panel-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  color: #a0a0b0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.meta-item strong { color: #f0f0f0; }
.meta-item strong.red { color: #ef4444; }
.mono { font-family: 'JetBrains Mono', monospace; }

/* ── Winner Banner ── */
.winner-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
}

.winner-banner strong { font-weight: 700; }

/* ── Chart Section ── */
.chart-section {
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.section-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  color: #666;
  margin-bottom: 10px;
}

/* ── Branch Cards Grid ── */
.branches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.branch-card {
  padding: 16px 20px;
  border-right: 1px solid rgba(255, 255, 255, 0.07);
  transition: background 0.2s;
}

.branch-card:last-child { border-right: none; }

.branch-card.is-winner {
  background: rgba(255, 255, 255, 0.03);
}

.branch-card.is-failed {
  opacity: 0.6;
}

/* Card Top */
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.branch-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #f0f0f0;
}

.branch-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  flex-shrink: 0;
}

.branch-dot.dot-winner { background: #6366f1; }

.card-badges {
  display: flex;
  gap: 6px;
  align-items: center;
  flex-shrink: 0;
}

.badge-winner {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff;
  padding: 2px 6px;
  border-radius: 2px;
}

.status-badge {
  font-size: 9px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 2px;
  letter-spacing: 0.05em;
}

.status-completed  { background: rgba(34, 197, 94, 0.12); color: #22c55e; }
.status-running    { background: rgba(249, 115, 22, 0.12); color: #f97316; }
.status-failed     { background: rgba(239, 68, 68, 0.12); color: #ef4444; }
.status-pending    { background: rgba(255, 255, 255, 0.05); color: #a0a0b0; }

/* Branch description */
.branch-desc {
  font-size: 12px;
  color: #a0a0b0;
  line-height: 1.5;
  margin-bottom: 12px;
}

/* Stat row */
.stat-row {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.stat-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #666;
  font-family: 'JetBrains Mono', monospace;
}

.stat-val {
  font-size: 13px;
  font-weight: 600;
  color: #f0f0f0;
}

.val-positive { color: #22c55e; }
.val-negative { color: #ef4444; }
.val-neutral  { color: #a0a0b0; }

/* Action pills */
.action-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 10px;
}

.action-pill {
  font-size: 9px;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.3);
  padding: 2px 6px;
  border-radius: 2px;
  letter-spacing: 0.03em;
}

.action-pill strong { color: #f0f0f0; }

/* Top posts */
.top-posts { margin-bottom: 8px; }
.top-posts-label {
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  color: #666;
  margin-bottom: 6px;
}

.post-preview {
  font-size: 11px;
  color: #a0a0b0;
  line-height: 1.45;
  font-style: italic;
  padding: 4px 8px;
  border-left: 2px solid rgba(255, 255, 255, 0.07);
  margin-bottom: 4px;
}

/* Branch error */
.branch-error {
  font-size: 11px;
  color: #ef4444;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 8px;
}

/* ── Summary ── */
.summary-block {
  padding: 16px 20px;
}

.summary-text {
  font-size: 13px;
  color: #a0a0b0;
  line-height: 1.65;
  max-width: 720px;
}
</style>
