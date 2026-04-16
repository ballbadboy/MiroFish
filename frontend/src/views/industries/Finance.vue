<template>
  <div class="page-wrap">

    <!-- ── Navbar ─────────────────────────────────────── -->
    <nav class="navbar">
      <span class="nav-wordmark">ENDORA</span>

      <div class="nav-center">
        <span class="nav-subtitle">Finance &amp; Investment Intelligence</span>
      </div>

      <div class="nav-right">
        <a class="nav-back" @click.prevent="router.push('/')">← Back to Platform</a>
        <button class="btn-sim" @click="router.push('/new')">Start Market Simulation →</button>
      </div>
    </nav>

    <!-- ── Hero ───────────────────────────────────────── -->
    <section class="hero-section">
      <div class="hero-left">
        <div class="breadcrumb">Platform / Industries / Finance</div>

        <div class="industry-badge">◈ FINANCE &amp; INVESTMENT</div>

        <h1 class="hero-h1">Institutional-Grade Intelligence for Every Investor</h1>

        <p class="hero-sub">
          From sentiment analysis to market simulation — ENDORA models millions
          of investor agents to reveal hidden market dynamics before they
          materialize.
        </p>

        <div class="hero-stats-inline">
          <div class="inline-stat">
            <span class="inline-val">10M+</span>
            <span class="inline-lbl">Investor Agents</span>
          </div>
          <div class="inline-sep"></div>
          <div class="inline-stat">
            <span class="inline-val">Sub-$5</span>
            <span class="inline-lbl">Per Simulation</span>
          </div>
        </div>

        <button class="btn-cta-gold" @click="router.push('/new')">
          Run Market Simulation →
        </button>
      </div>

      <div class="hero-right">
        <div class="terminal-card">
          <div class="terminal-header">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
            <span class="terminal-title">◈ LIVE SIMULATION / SET_SENTIMENT_Q3_2025</span>
          </div>
          <div class="terminal-body">
            <div
              v-for="(line, i) in logLines"
              :key="i"
              class="log-line"
              :class="{ 'log-visible': i < visibleLogs }"
            >
              <span class="log-ts">{{ line.ts }}</span>
              <span class="log-msg" :class="line.cls">{{ line.msg }}</span>
            </div>
            <span v-if="visibleLogs >= logLines.length" class="cursor-blink">▌</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Use Cases ──────────────────────────────────── -->
    <section class="section sect-mid">
      <div class="sect-inner">
        <div class="sect-label">◈ USE CASES</div>
        <h2 class="sect-h2">Where ENDORA Transforms Finance</h2>

        <div class="cases-grid">
          <div class="case-card" v-for="c in useCases" :key="c.title">
            <div class="case-icon">{{ c.icon }}</div>
            <h3 class="case-title">{{ c.title }}</h3>
            <p class="case-desc">{{ c.desc }}</p>
            <div class="case-tag">{{ c.tag }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── How It Works ───────────────────────────────── -->
    <section class="section sect-dark">
      <div class="sect-inner">
        <div class="sect-label">◈ WORKFLOW</div>
        <h2 class="sect-h2">From Data to Decision in Minutes</h2>

        <div class="workflow-row">
          <div class="wf-step" v-for="(step, i) in workflowSteps" :key="step.label">
            <div class="wf-num">0{{ i + 1 }}</div>
            <div class="wf-label">{{ step.label }}</div>
            <p class="wf-desc">{{ step.desc }}</p>
            <div class="wf-connector" v-if="i < workflowSteps.length - 1" aria-hidden="true"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Metrics Strip ──────────────────────────────── -->
    <div class="metrics-strip">
      <div class="metrics-inner">
        <div class="metric-item" v-for="m in metrics" :key="m.label">
          <div class="metric-val">{{ m.val }}</div>
          <div class="metric-lbl">{{ m.label }}</div>
        </div>
      </div>
    </div>

    <!-- ── Compliance ─────────────────────────────────── -->
    <section class="section sect-mid compliance-section">
      <div class="sect-inner">
        <div class="compliance-box">
          <div class="compliance-text">
            <div class="sect-label" style="margin-bottom: 12px;">◈ COMPLIANCE &amp; SECURITY</div>
            <p class="compliance-body">
              ENDORA Finance operates on publicly available market data and de-identified
              behavioral models. No personal trading data is collected. SEC-compliant
              research framework. Not financial advice.
            </p>
          </div>
          <div class="compliance-badges">
            <div class="badge-item" v-for="b in complianceBadges" :key="b">
              <span class="badge-check">✓</span> {{ b }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────── -->
    <section class="section sect-dark cta-section">
      <div class="sect-inner cta-inner">
        <h2 class="cta-h2">Ready to simulate the market?</h2>
        <p class="cta-sub">Join hedge funds, fintechs, and individual investors already using ENDORA.</p>
        <button class="btn-cta-gold btn-cta-large" @click="router.push('/new')">
          Start Market Simulation →
        </button>
        <div class="cta-contact">
          Contact our Finance team:
          <a class="cta-email" href="mailto:finance@endora.ai">finance@endora.ai</a>
        </div>
      </div>
    </section>

    <!-- ── Footer ─────────────────────────────────────── -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-left">
          <span class="footer-wordmark">ENDORA</span>
          <span class="footer-copy">© 2025 Endora Intelligence. All rights reserved.</span>
        </div>
        <nav class="footer-nav" aria-label="Footer navigation">
          <a class="footer-link" @click.prevent="router.push('/')">Platform</a>
          <a class="footer-link" @click.prevent="router.push('/')">Industries</a>
          <a class="footer-link" href="mailto:hello@endora.ai">Contact</a>
        </nav>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Log animation ─────────────────────────────────────────
const visibleLogs = ref(0)
let logInterval = null

const logLines = [
  { ts: '[00:00:01]', msg: 'Initializing 1,247,891 investor agents...', cls: 'log-normal' },
  { ts: '[00:00:04]', msg: 'Loading SET100 historical data (24mo)...', cls: 'log-normal' },
  { ts: '[00:00:09]', msg: 'Injecting interest rate cut scenario...', cls: 'log-warn' },
  { ts: '[00:00:14]', msg: 'Sentiment shift detected: +12.3% bullish', cls: 'log-alert' },
  { ts: '[00:00:19]', msg: 'Predicted SET index: 1,847 ± 42 (conf: 83%)', cls: 'log-normal' },
  { ts: '[00:00:23]', msg: 'Recommended: overweight Energy, Banking sectors', cls: 'log-success' },
]

// ── Use Cases ─────────────────────────────────────────────
const useCases = [
  {
    icon: '◈',
    title: 'Investor Sentiment Modeling',
    desc: 'Simulate how millions of retail and institutional investors react to news, earnings, and policy changes. Predict sentiment shifts before price moves.',
    tag: 'RETAIL · INSTITUTIONAL',
  },
  {
    icon: '▣',
    title: 'Market Scenario Testing',
    desc: 'Run parallel simulations: bull case, bear case, black swan. Compare outcomes across thousands of portfolio configurations.',
    tag: 'PORTFOLIO · RISK MGMT',
  },
  {
    icon: '⬡',
    title: 'IPO & Listing Prediction',
    desc: 'Model investor appetite for new listings. Simulate subscription rates, day-one pricing, and secondary market behavior.',
    tag: 'EQUITY · CAPITAL MARKETS',
  },
  {
    icon: '◉',
    title: 'Crypto & DeFi Modeling',
    desc: 'Simulate on-chain behavior, whale movements, and liquidity dynamics across DEX and CEX platforms.',
    tag: 'CRYPTO · WEB3',
  },
  {
    icon: '◫',
    title: 'Macro Policy Impact',
    desc: 'Model how rate changes, fiscal policy, or geopolitical events ripple through investor populations and asset classes.',
    tag: 'MACRO · POLICY',
  },
  {
    icon: '⚕',
    title: 'Alternative Data Signals',
    desc: 'Combine satellite imagery, social sentiment, options flow, and supply chain data into agent behaviors for alpha generation.',
    tag: 'ALT DATA · QUANT',
  },
]

// ── Workflow ──────────────────────────────────────────────
const workflowSteps = [
  {
    label: 'INGEST',
    desc: 'Feed ENDORA market data, news feeds, earnings reports, or alternative data streams',
  },
  {
    label: 'MODEL',
    desc: 'ENDORA creates investor personas: retail traders, hedge funds, market makers, and institutional allocators',
  },
  {
    label: 'SIMULATE',
    desc: 'Run million-scale agent simulation of investor behavior under your target scenario',
  },
  {
    label: 'PREDICT',
    desc: 'Receive probabilistic market forecasts with confidence intervals and position recommendations',
  },
]

// ── Metrics ───────────────────────────────────────────────
const metrics = [
  { val: '1,247,891', label: 'avg agents per market sim' },
  { val: '83%',       label: 'avg prediction confidence' },
  { val: '< $4',      label: 'avg cost per simulation' },
  { val: '12.3%',     label: 'avg sentiment detection lead' },
]

// ── Compliance ────────────────────────────────────────────
const complianceBadges = [
  'SEC Compliant',
  'Public Data Only',
  'Not Financial Advice',
]

// ── Lifecycle ─────────────────────────────────────────────
onMounted(() => {
  logInterval = setInterval(() => {
    if (visibleLogs.value < logLines.length) {
      visibleLogs.value++
    } else {
      clearInterval(logInterval)
    }
  }, 1800)
})

onUnmounted(() => {
  if (logInterval) clearInterval(logInterval)
})
</script>

<style scoped>
.page-wrap {
  --bg: #080c12; --bg-mid: #0d1117;
  --border: rgba(255,255,255,0.07); --border-str: rgba(255,255,255,0.12);
  --accent: #6366f1; --accent-lt: #a5b4fc;
  --gold: #f59e0b; --gold-bg: rgba(245,158,11,0.08); --gold-border: rgba(245,158,11,0.25);
  --text: #f0f0f0; --muted: #888;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  font-family: var(--sans); min-height: 100vh;
}

/* Navbar */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  height: 64px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 48px;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  background: rgba(8,12,18,0.85);
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.nav-wordmark { font-family: var(--mono); font-weight: 800; font-size: 1.05rem; letter-spacing: 3px; color: #fff; user-select: none; flex-shrink: 0; }
.nav-center { flex: 1; display: flex; justify-content: center; }
.nav-subtitle { font-family: var(--mono); font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; }
.nav-right { display: flex; align-items: center; gap: 16px; flex-shrink: 0; }
.nav-back { font-size: 0.83rem; color: var(--muted); cursor: pointer; text-decoration: none; transition: color 0.2s; }
.nav-back:hover { color: var(--text); }
.btn-sim {
  background: var(--gold); color: #080c12; border: none;
  padding: 8px 20px; border-radius: 8px;
  font-family: var(--sans); font-size: 0.85rem; font-weight: 700;
  cursor: pointer; white-space: nowrap;
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 0 20px rgba(245,158,11,0.2);
}
.btn-sim:hover { opacity: 0.88; transform: translateY(-1px); box-shadow: 0 0 32px rgba(245,158,11,0.35); }

/* Hero */
.hero-section {
  min-height: 100vh; padding-top: 64px;
  display: grid; grid-template-columns: 1fr 1fr;
  align-items: center; gap: 64px;
  max-width: 1200px; margin: 0 auto; padding-left: 48px; padding-right: 48px;
}
.hero-left { display: flex; flex-direction: column; gap: 24px; }
.breadcrumb {
  font-family: var(--mono); font-size: 0.7rem; color: var(--muted);
  letter-spacing: 0.06em;
}
.industry-badge {
  align-self: flex-start;
  font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.15em;
  color: var(--gold); border: 1px solid var(--gold-border);
  border-radius: 4px; padding: 6px 14px; background: var(--gold-bg);
}
.hero-h1 {
  font-size: clamp(2.4rem, 4vw + 0.5rem, 4rem); line-height: 1.1;
  font-weight: 800; letter-spacing: -0.03em; color: #fff; margin: 0;
}
.hero-sub {
  font-size: 1.05rem; line-height: 1.75; color: var(--muted); margin: 0;
  max-width: 520px;
}
.hero-stats-inline {
  display: flex; align-items: center; gap: 0;
  border: 1px solid var(--gold-border); border-radius: 10px;
  background: rgba(245,158,11,0.04); align-self: flex-start; overflow: hidden;
}
.inline-stat { display: flex; flex-direction: column; padding: 12px 24px; gap: 2px; }
.inline-val { font-family: var(--mono); font-size: 1rem; font-weight: 700; color: var(--gold); }
.inline-lbl { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; }
.inline-sep { width: 1px; height: 36px; background: var(--gold-border); flex-shrink: 0; }

.btn-cta-gold {
  align-self: flex-start;
  background: var(--gold); color: #080c12; border: none;
  padding: 14px 32px; border-radius: 10px;
  font-family: var(--sans); font-size: 0.95rem; font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 32px rgba(245,158,11,0.3);
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
}
.btn-cta-gold:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 0 48px rgba(245,158,11,0.45); }

/* Terminal card */
.hero-right { display: flex; align-items: center; justify-content: center; }
.terminal-card {
  width: 100%; max-width: 520px;
  background: #0a0e15; border: 1px solid var(--gold-border);
  border-radius: 14px; overflow: hidden;
  box-shadow: 0 0 0 1px rgba(245,158,11,0.08), 0 0 48px rgba(245,158,11,0.12), 0 24px 64px rgba(0,0,0,0.6);
}
.terminal-header {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 16px; background: rgba(245,158,11,0.04);
  border-bottom: 1px solid var(--gold-border);
}
.terminal-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.dot-red    { background: #ef4444; }
.dot-yellow { background: #f97316; }
.dot-green  { background: #22c55e; }
.terminal-title {
  font-family: var(--mono); font-size: 0.68rem; color: #22c55e;
  letter-spacing: 0.08em; margin-left: 6px; flex: 1;
}
.terminal-body {
  padding: 20px 20px 24px;
  display: flex; flex-direction: column; gap: 10px;
  min-height: 220px;
}
.log-line {
  display: flex; gap: 10px; align-items: baseline;
  opacity: 0; transform: translateY(4px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.log-line.log-visible { opacity: 1; transform: translateY(0); }
.log-ts {
  font-family: var(--mono); font-size: 0.68rem;
  color: rgba(245,158,11,0.45); white-space: nowrap; flex-shrink: 0;
}
.log-msg { font-family: var(--mono); font-size: 0.73rem; line-height: 1.5; }
.log-normal  { color: #c0cce0; }
.log-warn    { color: #f97316; }
.log-alert   { color: #ef4444; font-weight: 700; }
.log-success { color: #22c55e; font-weight: 700; }
.cursor-blink {
  font-family: var(--mono); font-size: 0.85rem; color: var(--gold);
  animation: blink 1.1s step-end infinite; display: inline-block;
  margin-top: 4px;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* Sections */
.section { padding: 100px 0; }
.sect-dark { background: var(--bg); }
.sect-mid  { background: var(--bg-mid); }
.sect-inner { max-width: 1200px; margin: 0 auto; padding: 0 48px; }
.sect-label { font-family: var(--mono); font-size: 0.72rem; font-variant: small-caps; letter-spacing: 0.18em; color: var(--gold); margin-bottom: 16px; }
.sect-h2 { font-size: clamp(1.8rem, 3vw, 2.6rem); font-weight: 700; letter-spacing: -0.025em; margin: 0 0 48px; color: var(--text); }

/* Use Cases */
.cases-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
}
.case-card {
  background: var(--bg); border: 1px solid var(--border); border-radius: 14px;
  padding: 28px 24px; display: flex; flex-direction: column; gap: 10px;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.case-card:hover {
  border-color: var(--gold-border);
  box-shadow: 0 0 0 1px rgba(245,158,11,0.08), 0 16px 48px rgba(0,0,0,0.4);
  transform: translateY(-2px);
}
.case-icon { font-size: 1.5rem; line-height: 1; color: var(--gold); }
.case-title { font-size: 1rem; font-weight: 700; color: var(--text); margin: 0; }
.case-desc  { font-size: 0.85rem; color: var(--muted); line-height: 1.65; margin: 0; flex: 1; }
.case-tag {
  font-family: var(--mono); font-size: 0.62rem; color: var(--gold);
  letter-spacing: 0.08em; opacity: 0.7; margin-top: 4px;
}

/* Workflow */
.workflow-row {
  display: flex; position: relative; gap: 0;
}
.wf-step {
  flex: 1; position: relative; padding: 0 20px 0 0;
}
.wf-connector {
  position: absolute; top: 22px; left: 50%; right: -50%;
  height: 1px; border-top: 1px dashed rgba(245,158,11,0.3);
  z-index: 0; pointer-events: none;
}
.wf-num {
  font-family: var(--mono); font-size: 0.78rem; font-weight: 700;
  color: var(--gold); margin-bottom: 14px;
  display: inline-block; background: var(--bg); padding-right: 10px;
  position: relative; z-index: 1;
}
.wf-label { font-family: var(--mono); font-size: 0.85rem; font-weight: 700; color: var(--text); letter-spacing: 0.06em; margin-bottom: 10px; }
.wf-desc { font-size: 0.83rem; color: var(--muted); line-height: 1.65; margin: 0; }

/* Metrics Strip */
.metrics-strip {
  background: var(--bg-mid);
  border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  padding: 40px 48px;
}
.metrics-inner {
  max-width: 1200px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(4, 1fr);
}
.metric-item {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  border-right: 1px solid var(--border); padding: 0 32px;
}
.metric-item:first-child { padding-left: 0; }
.metric-item:last-child  { border-right: none; }
.metric-val { font-family: var(--mono); font-size: 1.6rem; font-weight: 700; color: var(--gold); }
.metric-lbl { font-size: 0.78rem; color: var(--muted); text-align: center; letter-spacing: 0.05em; }

/* Compliance */
.compliance-section { padding-top: 64px; padding-bottom: 64px; }
.compliance-box {
  border: 1px solid var(--gold-border); border-left: 3px solid var(--gold);
  border-radius: 12px; background: var(--gold-bg);
  padding: 36px 40px; display: flex; align-items: flex-start;
  justify-content: space-between; gap: 40px; flex-wrap: wrap;
}
.compliance-text { flex: 1; min-width: 260px; }
.compliance-body { font-size: 0.92rem; color: var(--muted); line-height: 1.75; margin: 0; }
.compliance-badges {
  display: flex; flex-direction: column; gap: 12px;
  justify-content: center; flex-shrink: 0;
}
.badge-item {
  font-family: var(--mono); font-size: 0.75rem;
  color: var(--gold); letter-spacing: 0.06em;
  display: flex; align-items: center; gap: 8px; white-space: nowrap;
}
.badge-check { color: #22c55e; font-size: 0.8rem; }

/* CTA */
.cta-section { border-top: 1px solid var(--border); }
.cta-inner {
  min-height: 360px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; gap: 0;
}
.cta-h2 {
  font-size: clamp(1.8rem, 3.5vw, 2.8rem); font-weight: 800;
  letter-spacing: -0.03em; color: var(--text); margin: 0 0 14px;
}
.cta-sub {
  font-size: 1rem; color: var(--muted); max-width: 480px;
  line-height: 1.7; margin: 0 0 36px;
}
.btn-cta-large {
  align-self: center;
  padding: 18px 44px; font-size: 1rem; border-radius: 12px;
  box-shadow: 0 0 40px rgba(245,158,11,0.35);
  margin-bottom: 24px;
}
.btn-cta-large:hover { box-shadow: 0 0 64px rgba(245,158,11,0.5); }
.cta-contact { font-family: var(--mono); font-size: 0.75rem; color: var(--muted); letter-spacing: 0.05em; }
.cta-email {
  color: var(--gold); text-decoration: none; margin-left: 6px;
  transition: opacity 0.2s;
}
.cta-email:hover { opacity: 0.75; }

/* Footer */
.footer { background: var(--bg-mid); border-top: 1px solid var(--border); padding: 32px 48px; }
.footer-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 16px;
}
.footer-left { display: flex; align-items: center; gap: 24px; }
.footer-wordmark {
  font-family: var(--mono); font-weight: 800; font-size: 0.9rem;
  letter-spacing: 3px; color: var(--text);
}
.footer-copy { font-size: 0.8rem; color: var(--muted); }
.footer-nav { display: flex; gap: 28px; }
.footer-link {
  font-size: 0.82rem; color: var(--muted); text-decoration: none;
  cursor: pointer; transition: color 0.2s;
}
.footer-link:hover { color: var(--text); }

/* Responsive */
@media (max-width: 1024px) {
  .navbar { padding: 0 24px; }
  .nav-center { display: none; }
  .hero-section {
    grid-template-columns: 1fr; padding-top: 96px; gap: 48px;
    padding-left: 24px; padding-right: 24px; min-height: auto; padding-bottom: 80px;
  }
  .hero-left { align-items: flex-start; }
  .hero-right { justify-content: flex-start; }
  .terminal-card { max-width: 100%; }
  .sect-inner { padding: 0 24px; }
  .cases-grid { grid-template-columns: 1fr 1fr; }
  .workflow-row { flex-direction: column; gap: 32px; }
  .wf-connector { display: none; }
  .metrics-inner { grid-template-columns: repeat(2, 1fr); gap: 24px; }
  .metric-item { border-right: none; padding: 0; }
  .metrics-strip { padding: 32px 24px; }
  .compliance-box { flex-direction: column; gap: 24px; }
}
@media (max-width: 640px) {
  .navbar { padding: 0 16px; }
  .nav-back { display: none; }
  .btn-sim { font-size: 0.78rem; padding: 7px 14px; }
  .hero-section { padding-left: 16px; padding-right: 16px; }
  .sect-inner { padding: 0 16px; }
  .cases-grid { grid-template-columns: 1fr; }
  .hero-stats-inline { flex-direction: column; border-radius: 10px; }
  .inline-sep { width: 100%; height: 1px; }
  .section { padding: 64px 0; }
  .compliance-section { padding-top: 48px; padding-bottom: 48px; }
  .compliance-box { padding: 24px 20px; }
  .metrics-inner { grid-template-columns: 1fr 1fr; }
  .footer { padding: 24px 16px; }
  .footer-inner { flex-direction: column; align-items: flex-start; }
  .footer-nav { flex-wrap: wrap; gap: 16px; }
  .cta-h2 { font-size: 1.8rem; }
}
</style>
