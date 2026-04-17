<template>
  <div class="dash-wrap">

    <!-- Navbar -->
    <nav class="navbar">
      <span class="nav-wordmark" @click="router.push('/')" style="cursor:pointer">ENDORA</span>
      <div class="nav-center">
        <span class="nav-center-label">DASHBOARD</span>
        <router-link to="/data-sources" class="nav-link">Data Sources</router-link>
      </div>
      <button class="btn-new" @click="router.push('/new')">+ New Simulation</button>
    </nav>

    <!-- Main -->
    <main class="dash-main">

      <!-- Stats bar -->
      <div class="stats-row">
        <div class="stat-card" v-for="s in stats" :key="s.label">
          <span class="stat-number">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- Search & Filter -->
      <div class="filter-bar">
        <div class="search-wrap">
          <span class="search-icon" aria-hidden="true">&#x1F50D;</span>
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Search simulations..."
          />
        </div>
        <div class="filter-pills">
          <button
            v-for="f in filters"
            :key="f.value"
            class="pill"
            :class="{ 'pill-active': activeFilter === f.value }"
            @click="activeFilter = f.value"
          >{{ f.label }}</button>
        </div>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="card-list">
        <div class="skeleton-card" v-for="n in 3" :key="n">
          <div class="skel-dot"></div>
          <div class="skel-body">
            <div class="skel-line skel-w60"></div>
            <div class="skel-line skel-w90"></div>
            <div class="skel-line skel-w40"></div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredSimulations.length === 0" class="empty-state">
        <div class="empty-icon" aria-hidden="true">&#x25C8;</div>
        <p class="empty-title">No simulations yet</p>
        <p class="empty-sub">Start your first simulation to see it here.</p>
        <button class="btn-new" @click="router.push('/new')">Create Simulation &rarr;</button>
      </div>

      <!-- Simulation list -->
      <div v-else class="card-list">
        <div
          v-for="sim in filteredSimulations"
          :key="sim.id"
          class="sim-card"
        >
          <!-- Status dot -->
          <span
            class="status-dot"
            :class="'dot-' + sim.status"
            :title="sim.status"
          ></span>

          <!-- Main info -->
          <div class="sim-info">
            <div class="sim-row-1">
              <span class="sim-name">{{ sim.project_name }}</span>
              <span class="industry-badge" :style="{ background: getIndustryColor(sim.industry) }">{{ sim.industry }}</span>
            </div>
            <p class="sim-prompt">{{ truncate(sim.prompt, 100) }}</p>
            <div class="sim-meta">
              <span>Created: {{ formatDate(sim.created_at) }}</span>
              <span class="meta-sep">&middot;</span>
              <span>Duration: {{ sim.duration }}</span>
              <span class="meta-sep">&middot;</span>
              <span>Agents: {{ sim.agents }}</span>
              <span class="meta-sep">&middot;</span>
              <span>Rounds: {{ sim.rounds }}</span>
            </div>
          </div>

          <!-- Right section -->
          <div class="sim-actions">
            <span class="status-badge" :class="'badge-' + sim.status">
              {{ sim.status.toUpperCase() }}
            </span>
            <button
              v-if="sim.status === 'completed'"
              class="btn-action"
              @click="router.push('/report/' + sim.report_id)"
            >View Report &rarr;</button>
            <button
              v-else-if="sim.status === 'running'"
              class="btn-action"
              @click="router.push('/simulation/' + sim.id + '/start')"
            >Continue &rarr;</button>
            <button
              v-else-if="sim.status === 'failed'"
              class="btn-action btn-retry"
              @click="router.push('/new')"
            >Retry</button>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSimulationHistory } from '../api/simulation'

const router = useRouter()

const simulations = ref([])
const loading = ref(true)
const searchQuery = ref('')
const activeFilter = ref('all')

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Running', value: 'running' },
  { label: 'Completed', value: 'completed' },
  { label: 'Failed', value: 'failed' },
]

const mockData = [
  { id: 'sim-001', project_name: 'ICU Overflow Prediction', industry: 'Healthcare', status: 'completed', prompt: 'Simulate ICU capacity overflow under seasonal flu surge with varying hospital bed availability and staff rotation models across regional networks.', created_at: '2025-06-15T10:30:00Z', duration: '8 min', agents: '847,293', rounds: 15, report_id: 'rpt-001' },
  { id: 'sim-002', project_name: 'SET100 Sentiment Q3', industry: 'Finance', status: 'running', prompt: 'Model investor sentiment shift after interest rate announcement with multi-agent behavioral simulation across retail and institutional segments.', created_at: '2025-06-16T14:20:00Z', duration: '\u2014', agents: '1,247,891', rounds: 8, report_id: null },
  { id: 'sim-003', project_name: 'SCS Narrative Warfare', industry: 'Defense', status: 'completed', prompt: 'Simulate narrative warfare campaign in South China Sea region with information operations, media propagation, and public opinion modeling.', created_at: '2025-06-14T09:00:00Z', duration: '12 min', agents: '2,100,000', rounds: 20, report_id: 'rpt-003' },
  { id: 'sim-004', project_name: 'Bangkok Land Analysis', industry: 'Real Estate', status: 'failed', prompt: 'Identify optimal land parcels for mixed-use development in Sukhumvit corridor with footfall simulation and demand forecasting models.', created_at: '2025-06-13T16:45:00Z', duration: '3 min', agents: '500,000', rounds: 5, report_id: null },
  { id: 'sim-005', project_name: 'Carbon Credit Forecast', industry: 'Environment', status: 'completed', prompt: 'Forecast carbon credit pricing dynamics under new EU regulations with multi-stakeholder agent interactions and policy scenario branching.', created_at: '2025-06-12T08:00:00Z', duration: '6 min', agents: '750,000', rounds: 12, report_id: 'rpt-005' },
]

const filteredSimulations = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return simulations.value.filter((sim) => {
    const matchFilter = activeFilter.value === 'all' || sim.status === activeFilter.value
    const matchSearch =
      !q ||
      sim.project_name.toLowerCase().includes(q) ||
      sim.prompt.toLowerCase().includes(q)
    return matchFilter && matchSearch
  })
})

const stats = computed(() => {
  const total = simulations.value.length
  const active = simulations.value.filter((s) => s.status === 'running').length
  return [
    { value: String(total), label: 'Total Simulations' },
    { value: String(active), label: 'Active Now' },
    { value: '847,293', label: 'Avg. Agents' },
    { value: '94.2%', label: 'Success Rate' },
  ]
})

const formatDate = (iso) => {
  const d = new Date(iso)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const truncate = (str, len) => {
  if (!str) return ''
  return str.length > len ? str.slice(0, len) + '...' : str
}

const industryColors = {
  Healthcare: 'rgba(34,197,94,0.15)',
  Finance: 'rgba(99,102,241,0.18)',
  Defense: 'rgba(239,68,68,0.15)',
  'Real Estate': 'rgba(249,115,22,0.15)',
  Environment: 'rgba(16,185,129,0.15)',
}

const getIndustryColor = (industry) => industryColors[industry] ?? 'rgba(255,255,255,0.06)'

onMounted(async () => {
  try {
    const res = await getSimulationHistory()
    const list = res?.data?.data ?? res?.data ?? []
    simulations.value = Array.isArray(list) ? list : []
    if (simulations.value.length === 0) {
      simulations.value = mockData
    }
  } catch {
    simulations.value = mockData
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dash-wrap {
  --bg: #080c12;
  --bg-mid: #0d1117;
  --border: rgba(255,255,255,0.06);
  --border-str: rgba(255,255,255,0.12);
  --accent: #6366f1;
  --accent-lt: #a5b4fc;
  --text: #f0f0f0;
  --muted: #888;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  min-height: 100vh;
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
  user-select: none;
}
.nav-center {
  display: flex; align-items: center; gap: 20px;
}
.nav-center-label {
  font-family: var(--mono); font-size: 0.72rem;
  font-variant: small-caps; letter-spacing: 0.18em;
  color: var(--muted);
}
.nav-link {
  font-family: var(--sans); font-size: 0.82rem;
  color: var(--muted); text-decoration: none;
  padding: 6px 12px; border-radius: 8px;
  border: 1px solid transparent;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
.nav-link:hover {
  color: var(--text);
  border-color: rgba(99,102,241,0.3);
  background: rgba(99,102,241,0.06);
}
.nav-link.router-link-active {
  color: var(--accent-lt);
  border-color: rgba(99,102,241,0.4);
}
.btn-new {
  background: var(--accent); color: #fff; border: none;
  padding: 8px 20px; border-radius: 8px;
  font-family: var(--sans); font-size: 0.85rem; font-weight: 600;
  cursor: pointer; transition: opacity 0.2s, transform 0.2s;
}
.btn-new:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── Main ───────────────────────────────── */
.dash-main {
  max-width: 1200px; margin: 0 auto;
  padding: 100px 48px 64px;
}

/* ── Stats row ──────────────────────────── */
.stats-row {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 16px; margin-bottom: 32px;
}
.stat-card {
  background: var(--bg-mid); border: 1px solid var(--border);
  border-radius: 14px; padding: 24px 20px;
  display: flex; flex-direction: column; gap: 6px;
}
.stat-number {
  font-family: var(--mono); font-size: 1.8rem;
  font-weight: 700; color: var(--accent-lt);
}
.stat-label {
  font-size: 0.78rem; color: var(--muted);
  letter-spacing: 0.04em;
}

/* ── Filter bar ─────────────────────────── */
.filter-bar {
  display: flex; align-items: center;
  justify-content: space-between; gap: 16px;
  margin-bottom: 24px; flex-wrap: wrap;
}
.search-wrap {
  position: relative; flex: 1; min-width: 200px; max-width: 400px;
}
.search-icon {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  font-size: 0.85rem; pointer-events: none; opacity: 0.5;
}
.search-input {
  width: 100%; padding: 10px 14px 10px 40px;
  background: var(--bg-mid); border: 1px solid var(--border-str);
  border-radius: 10px; color: var(--text);
  font-family: var(--mono); font-size: 0.85rem;
  outline: none; transition: border-color 0.2s;
}
.search-input::placeholder { color: var(--muted); opacity: 0.6; }
.search-input:focus { border-color: var(--accent); }
.filter-pills { display: flex; gap: 8px; }
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

/* ── Card list ──────────────────────────── */
.card-list {
  display: flex; flex-direction: column; gap: 12px;
}

/* ── Simulation card ────────────────────── */
.sim-card {
  display: flex; align-items: center; gap: 20px;
  padding: 20px; background: var(--bg-mid);
  border: 1px solid var(--border); border-radius: 14px;
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.sim-card:hover {
  border-color: rgba(99,102,241,0.35);
  transform: translateY(-1px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Status dot */
.status-dot {
  width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0;
}
.dot-running { background: #f97316; animation: pulse-dot 1.6s ease-in-out infinite; }
.dot-completed { background: #22c55e; }
.dot-failed { background: #ef4444; }
.dot-pending { background: #666; }
@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(249,115,22,0.5); }
  50% { opacity: 0.6; box-shadow: 0 0 0 6px rgba(249,115,22,0); }
}

/* Sim info */
.sim-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.sim-row-1 { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.sim-name { font-weight: 700; font-size: 1rem; color: var(--text); }
.industry-badge {
  font-family: var(--mono); font-size: 0.65rem;
  letter-spacing: 0.06em; padding: 2px 10px;
  border-radius: 4px; color: var(--text); white-space: nowrap;
}
.sim-prompt {
  font-size: 0.85rem; color: var(--muted); line-height: 1.5;
  margin: 0; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis;
}
.sim-meta {
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
  font-family: var(--mono); font-size: 0.72rem; color: var(--muted);
}
.meta-sep { opacity: 0.4; }

/* Right actions */
.sim-actions {
  display: flex; flex-direction: column; align-items: flex-end;
  gap: 10px; flex-shrink: 0;
}
.status-badge {
  font-family: var(--mono); font-size: 0.65rem;
  letter-spacing: 0.1em; padding: 4px 12px;
  border-radius: 20px; white-space: nowrap;
}
.badge-running { background: rgba(249,115,22,0.15); color: #f97316; }
.badge-completed { background: rgba(34,197,94,0.15); color: #22c55e; }
.badge-failed { background: rgba(239,68,68,0.15); color: #ef4444; }
.badge-pending { background: rgba(102,102,102,0.15); color: #888; }
.btn-action {
  background: transparent; color: var(--accent-lt);
  border: 1px solid rgba(99,102,241,0.3); border-radius: 8px;
  padding: 6px 16px; font-size: 0.8rem; font-family: var(--sans);
  font-weight: 600; cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.btn-action:hover { background: rgba(99,102,241,0.1); border-color: var(--accent); }
.btn-retry { color: #ef4444; border-color: rgba(239,68,68,0.3); }
.btn-retry:hover { background: rgba(239,68,68,0.1); border-color: #ef4444; }

/* ── Empty state ────────────────────────── */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; padding: 80px 20px;
}
.empty-icon { font-size: 2.4rem; color: var(--accent); opacity: 0.5; margin-bottom: 16px; }
.empty-title { font-size: 1.2rem; font-weight: 700; color: var(--text); margin: 0 0 8px; }
.empty-sub { font-size: 0.9rem; color: var(--muted); margin: 0 0 28px; }

/* ── Skeleton cards ─────────────────────── */
.skeleton-card {
  display: flex; align-items: center; gap: 20px;
  padding: 20px; background: var(--bg-mid);
  border: 1px solid var(--border); border-radius: 14px;
}
.skel-dot {
  width: 12px; height: 12px; border-radius: 50%;
  background: rgba(255,255,255,0.06); flex-shrink: 0;
}
.skel-body { flex: 1; display: flex; flex-direction: column; gap: 10px; }
.skel-line {
  height: 14px; border-radius: 6px;
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
  background-size: 400% 100%;
  animation: shimmer 1.6s ease-in-out infinite;
}
.skel-w60 { width: 60%; }
.skel-w90 { width: 90%; }
.skel-w40 { width: 40%; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── Responsive ─────────────────────────── */
@media (max-width: 768px) {
  .navbar { padding: 0 20px; }
  .dash-main { padding: 100px 20px 48px; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .sim-card { flex-direction: column; align-items: flex-start; }
  .sim-actions { flex-direction: row; align-items: center; width: 100%; }
  .sim-meta .meta-sep:nth-child(n+6) { display: none; }
  .sim-meta span:nth-child(n+5) { display: none; }
  .filter-bar { flex-direction: column; align-items: stretch; }
  .search-wrap { max-width: none; }
  .filter-pills { flex-wrap: wrap; }
}
</style>
