<template>
  <div class="ds-wrap">

    <!-- Navbar -->
    <nav class="navbar" aria-label="Main navigation">
      <span class="nav-wordmark" @click="router.push('/')">ENDORA</span>
      <span class="nav-center-label">DATA SOURCES</span>
      <div class="nav-right">
        <button
          class="btn-ghost"
          :class="{ refreshing: isRefreshing }"
          aria-label="Refresh connectors"
          @click="loadAll"
        >
          <span class="refresh-icon" aria-hidden="true">↻</span>
          <span>Refresh</span>
        </button>
        <router-link to="/dashboard" class="nav-back">
          <span class="back-arrow">←</span> Back to Dashboard
        </router-link>
      </div>
    </nav>

    <!-- Main -->
    <main class="ds-main">

      <!-- Page header -->
      <header class="page-header">
        <h1 class="page-title">Data Connectors</h1>
        <p class="page-sub">Manage live data sources powering your simulations.</p>
      </header>

      <!-- Stats strip -->
      <div class="stats-row">
        <div class="stat-card" v-for="s in stats" :key="s.label">
          <span class="stat-number">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- Filter pills -->
      <div class="filter-bar" role="tablist" aria-label="Filter by vertical">
        <button
          v-for="f in filters"
          :key="f.value"
          class="pill"
          :class="{ 'pill-active': activeFilter === f.value }"
          role="tab"
          :aria-selected="activeFilter === f.value"
          @click="activeFilter = f.value"
        >{{ f.label }}</button>
      </div>

      <!-- Loading skeletons -->
      <div v-if="loading" class="card-grid">
        <div class="skeleton-card" v-for="n in 6" :key="n">
          <div class="skel-icon"></div>
          <div class="skel-line skel-w70"></div>
          <div class="skel-line skel-w40"></div>
          <div class="skel-line skel-w90"></div>
          <div class="skel-line skel-w60"></div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredConnectors.length === 0" class="empty-state">
        <div class="empty-icon" aria-hidden="true">◇</div>
        <p class="empty-title">No connectors in this vertical</p>
        <p class="empty-sub">Try selecting a different filter above.</p>
      </div>

      <!-- Connector cards -->
      <div v-else class="card-grid">
        <article
          v-for="c in filteredConnectors"
          :key="c.name"
          class="connector-card"
        >
          <div class="card-top">
            <span
              class="vert-icon"
              :style="{ color: getVerticalMeta(c.vertical).color }"
              aria-hidden="true"
            >{{ getVerticalMeta(c.vertical).icon }}</span>
            <span
              class="vert-badge"
              :style="{
                color: getVerticalMeta(c.vertical).color,
                background: getVerticalBg(c.vertical),
                borderColor: getVerticalBorder(c.vertical),
              }"
            >{{ formatVertical(c.vertical) }}</span>
          </div>

          <h3 class="connector-name">{{ c.name }}</h3>

          <p class="connector-desc">{{ c.description || 'No description provided.' }}</p>

          <div class="meta-row">
            <span class="src-badge">{{ (c.source_type || 'API').toUpperCase() }}</span>
            <span class="auth-state" :class="getAuthState(c).cls">
              <span class="auth-dot" aria-hidden="true"></span>
              {{ getAuthState(c).label }}
            </span>
          </div>

          <div class="card-actions">
            <button
              class="btn-fetch"
              :disabled="fetchingMap[c.name]"
              @click="testFetch(c)"
            >
              <span v-if="fetchingMap[c.name]" class="btn-spinner" aria-hidden="true"></span>
              <span v-if="fetchingMap[c.name]">Fetching…</span>
              <span v-else>Test Fetch</span>
            </button>
          </div>
        </article>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { listConnectors, healthCheckAll, fetchConnector } from '../api/connectors'

const router = useRouter()
const toast  = inject('toast', null)

// ── State ───────────────────────────────────────────
const connectors    = ref([])
const healthMap     = ref({})
const loading       = ref(true)
const isRefreshing  = ref(false)
const activeFilter  = ref('all')
const fetchingMap   = reactive({})

// ── Static config ───────────────────────────────────
const filters = [
  { label: 'All',         value: 'all'         },
  { label: 'Healthcare',  value: 'healthcare'  },
  { label: 'Finance',     value: 'finance'     },
  { label: 'Defense',     value: 'defense'     },
  { label: 'Real Estate', value: 'real-estate' },
  { label: 'Environment', value: 'environment' },
  { label: 'Politics',    value: 'politics'    },
  { label: 'General',     value: 'general'     },
]

const verticalMeta = {
  healthcare:    { icon: '⚕', color: '#2dd4bf' },
  finance:       { icon: '◈', color: '#f59e0b' },
  defense:       { icon: '⬡', color: '#ef4444' },
  'real-estate': { icon: '▣', color: '#06b6d4' },
  environment:   { icon: '◉', color: '#10b981' },
  politics:      { icon: '◫', color: '#8b5cf6' },
  general:       { icon: '◇', color: '#a5b4fc' },
}

const DEFAULT_META = { icon: '◇', color: '#a5b4fc' }

// ── Computed ────────────────────────────────────────
const filteredConnectors = computed(() => {
  if (activeFilter.value === 'all') return connectors.value
  return connectors.value.filter(c => (c.vertical || 'general') === activeFilter.value)
})

const stats = computed(() => {
  const total = connectors.value.length
  const active = connectors.value.filter(c => healthMap.value[c.name]?.ok === true).length
  const verticals = new Set(connectors.value.map(c => c.vertical || 'general')).size
  return [
    { value: String(total),     label: 'Total Connectors'  },
    { value: String(active),    label: 'Active'            },
    { value: String(verticals), label: 'Verticals Covered' },
    { value: '—',               label: 'Last Sync'         },
  ]
})

// ── Helpers ─────────────────────────────────────────
const getVerticalMeta = (v) => verticalMeta[v] ?? DEFAULT_META

const getVerticalBg = (v) => {
  const color = getVerticalMeta(v).color
  return `${color}14`
}

const getVerticalBorder = (v) => {
  const color = getVerticalMeta(v).color
  return `${color}40`
}

const formatVertical = (v) => {
  if (!v) return 'General'
  return v
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

const getAuthState = (c) => {
  const h = healthMap.value[c.name]
  if (h?.ok === true) return { cls: 'auth-ok',      label: 'Connected'     }
  if (c.requires_auth && h && !h.auth_present) return { cls: 'auth-warn', label: 'Auth required' }
  if (h && h.ok === false) return { cls: 'auth-err', label: 'Error' }
  return { cls: 'auth-warn', label: 'Unknown' }
}

const showToast = (type, message) => {
  if (toast?.[type]) {
    toast[type](message)
  } else if (typeof toast === 'function') {
    toast({ type, message })
  } else {
    console.log(`[${type}] ${message}`)
  }
}

// ── Actions ─────────────────────────────────────────
const loadAll = async () => {
  if (isRefreshing.value) return
  isRefreshing.value = true
  if (connectors.value.length === 0) loading.value = true

  try {
    const [listRes, healthRes] = await Promise.all([
      listConnectors(),
      healthCheckAll(),
    ])
    const list = listRes?.data ?? []
    const health = healthRes?.data ?? {}
    connectors.value = Array.isArray(list) ? [...list] : []
    healthMap.value  = { ...health }
  } catch (e) {
    showToast('error', e?.message || 'Failed to load connectors')
    connectors.value = []
    healthMap.value  = {}
  } finally {
    loading.value = false
    isRefreshing.value = false
  }
}

const testFetch = async (c) => {
  if (fetchingMap[c.name]) return
  fetchingMap[c.name] = true
  try {
    const res = await fetchConnector(c.name, {})
    const count = res?.data?.count ?? 0
    showToast('success', `Fetched ${count} document${count === 1 ? '' : 's'} from ${c.name}`)
  } catch (e) {
    const msg = e?.response?.data?.error || e?.message || 'Fetch failed'
    showToast('error', `${c.name}: ${msg}`)
  } finally {
    fetchingMap[c.name] = false
  }
}

onMounted(loadAll)
</script>

<style scoped>
.ds-wrap {
  --bg: #080c12;
  --bg-mid: #0d1117;
  --border: rgba(255,255,255,0.07);
  --border-str: rgba(255,255,255,0.12);
  --accent: #6366f1;
  --accent-lt: #a5b4fc;
  --green: #22c55e;
  --orange: #f97316;
  --red: #ef4444;
  --text: #f0f0f0;
  --muted: #888;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  font-family: var(--sans); min-height: 100vh;
}

/* ── Navbar ─────────────────────────────── */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  height: 64px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 48px;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  background: rgba(8,12,18,0.85);
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.nav-wordmark {
  font-family: var(--mono); font-weight: 800;
  font-size: 1.05rem; letter-spacing: 3px; color: #fff;
  cursor: pointer; user-select: none;
  transition: opacity 0.2s;
}
.nav-wordmark:hover { opacity: 0.75; }
.nav-center-label {
  font-family: var(--mono); font-size: 0.72rem;
  font-variant: small-caps; letter-spacing: 0.18em;
  color: var(--muted);
}
.nav-right { display: flex; align-items: center; gap: 16px; }
.btn-ghost {
  display: inline-flex; align-items: center; gap: 6px;
  background: transparent; color: var(--muted);
  border: 1px solid var(--border-str); border-radius: 8px;
  padding: 6px 14px; font-family: var(--sans);
  font-size: 0.82rem; cursor: pointer;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
.btn-ghost:hover { color: var(--text); border-color: rgba(99,102,241,0.4); background: rgba(99,102,241,0.06); }
.refresh-icon { display: inline-block; font-size: 0.95rem; line-height: 1; }
.btn-ghost.refreshing .refresh-icon { animation: spin 0.9s linear infinite; }
.nav-back {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.85rem; color: var(--muted);
  text-decoration: none; transition: color 0.2s;
}
.nav-back:hover { color: var(--text); }
.back-arrow { font-size: 1rem; }

/* ── Main ───────────────────────────────── */
.ds-main {
  max-width: 1200px; margin: 0 auto;
  padding: 100px 48px 64px;
}

.page-header { margin-bottom: 32px; }
.page-title {
  font-size: clamp(2rem, 3vw + 0.5rem, 2.6rem);
  font-weight: 800; letter-spacing: -0.03em;
  color: #fff; margin: 0 0 10px;
}
.page-sub { font-size: 1rem; color: var(--muted); line-height: 1.6; margin: 0; }

/* ── Stats ──────────────────────────────── */
.stats-row {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 16px; margin-bottom: 32px;
}
.stat-card {
  background: var(--bg-mid); border: 1px solid var(--border);
  border-radius: 14px; padding: 22px 20px;
  display: flex; flex-direction: column; gap: 6px;
}
.stat-number {
  font-family: var(--mono); font-size: 1.7rem;
  font-weight: 700; color: var(--accent-lt);
}
.stat-label {
  font-size: 0.76rem; color: var(--muted);
  letter-spacing: 0.04em;
}

/* ── Filter pills ───────────────────────── */
.filter-bar {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin-bottom: 28px;
}
.pill {
  background: transparent; color: var(--muted);
  border: 1px solid var(--border-str); border-radius: 20px;
  padding: 6px 16px; font-size: 0.8rem; font-family: var(--sans);
  cursor: pointer; transition: all 0.2s;
}
.pill:hover { color: var(--text); border-color: rgba(255,255,255,0.2); }
.pill-active {
  background: var(--accent); color: #fff;
  border-color: var(--accent);
}

/* ── Card grid ──────────────────────────── */
.card-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.connector-card {
  display: flex; flex-direction: column; gap: 12px;
  padding: 20px;
  background: var(--bg-mid);
  border: 1px solid var(--border);
  border-radius: 14px;
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
  position: relative; overflow: hidden;
}
.connector-card::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at top right, rgba(99,102,241,0.06), transparent 60%);
  pointer-events: none; opacity: 0;
  transition: opacity 0.25s;
}
.connector-card:hover {
  border-color: rgba(99,102,241,0.35);
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.35);
}
.connector-card:hover::before { opacity: 1; }

.card-top {
  display: flex; align-items: center; justify-content: space-between;
  gap: 10px;
}
.vert-icon {
  font-size: 1.4rem; line-height: 1;
}
.vert-badge {
  font-family: var(--mono); font-size: 0.62rem;
  letter-spacing: 0.08em; font-weight: 600;
  padding: 3px 10px; border-radius: 4px;
  border: 1px solid; white-space: nowrap;
  text-transform: uppercase;
}

.connector-name {
  font-family: var(--mono); font-size: 1.05rem; font-weight: 700;
  color: var(--text); margin: 0;
  letter-spacing: -0.01em;
  word-break: break-word;
}

.connector-desc {
  font-size: 0.82rem; color: var(--muted);
  line-height: 1.5; margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.46em;
}

.meta-row {
  display: flex; align-items: center; justify-content: space-between;
  gap: 8px; flex-wrap: wrap;
  padding-top: 6px;
  border-top: 1px solid var(--border);
}
.src-badge {
  font-family: var(--mono); font-size: 0.62rem;
  letter-spacing: 0.1em; font-weight: 600;
  padding: 3px 8px; border-radius: 4px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  color: var(--muted);
}
.auth-state {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 0.74rem; font-family: var(--mono);
  white-space: nowrap;
}
.auth-dot {
  width: 8px; height: 8px; border-radius: 50%;
  display: inline-block;
}
.auth-ok { color: var(--green); }
.auth-ok .auth-dot { background: var(--green); box-shadow: 0 0 6px rgba(34,197,94,0.6); }
.auth-warn { color: var(--orange); }
.auth-warn .auth-dot { background: var(--orange); }
.auth-err { color: var(--red); }
.auth-err .auth-dot { background: var(--red); }

.card-actions { display: flex; }
.btn-fetch {
  flex: 1;
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 8px 14px;
  background: transparent; color: var(--accent-lt);
  border: 1px solid rgba(99,102,241,0.3); border-radius: 8px;
  font-family: var(--sans); font-size: 0.82rem; font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.btn-fetch:hover:not(:disabled) {
  background: rgba(99,102,241,0.1);
  border-color: var(--accent);
  color: #fff;
}
.btn-fetch:disabled { cursor: wait; opacity: 0.7; }

.btn-spinner {
  width: 12px; height: 12px;
  border: 2px solid rgba(165,180,252,0.25);
  border-top-color: var(--accent-lt);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Empty state ────────────────────────── */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; padding: 80px 20px;
}
.empty-icon { font-size: 2.4rem; color: var(--accent); opacity: 0.5; margin-bottom: 16px; }
.empty-title { font-size: 1.2rem; font-weight: 700; color: var(--text); margin: 0 0 6px; }
.empty-sub { font-size: 0.9rem; color: var(--muted); margin: 0; }

/* ── Skeleton cards ─────────────────────── */
.skeleton-card {
  display: flex; flex-direction: column; gap: 12px;
  padding: 20px; background: var(--bg-mid);
  border: 1px solid var(--border); border-radius: 14px;
}
.skel-icon {
  width: 28px; height: 28px; border-radius: 6px;
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
  background-size: 400% 100%;
  animation: shimmer 1.6s ease-in-out infinite;
}
.skel-line {
  height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
  background-size: 400% 100%;
  animation: shimmer 1.6s ease-in-out infinite;
}
.skel-w40 { width: 40%; }
.skel-w60 { width: 60%; }
.skel-w70 { width: 70%; }
.skel-w90 { width: 90%; }
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── Responsive ─────────────────────────── */
@media (max-width: 1024px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .navbar { padding: 0 20px; }
  .nav-center-label { display: none; }
  .ds-main { padding: 100px 20px 48px; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .card-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .nav-right { gap: 8px; }
  .btn-ghost span:not(.refresh-icon) { display: none; }
}
</style>
