<template>
  <div class="page-wrap">

    <!-- ── Navbar ─────────────────────────────────────── -->
    <nav class="navbar">
      <span class="nav-wordmark">ENDORA</span>

      <div class="nav-center">
        <a class="nav-link" @click.prevent="scrollTo('hero')">Platform</a>
        <a class="nav-link" @click.prevent="scrollTo('industries')">Industries</a>
        <a class="nav-link" @click.prevent="scrollTo('how-it-works')">How It Works</a>
        <a class="nav-link" @click.prevent="scrollTo('pricing')">Pricing</a>
      </div>

      <div class="nav-right">
        <LanguageSwitcher />
        <button class="btn-demo" @click="scrollTo('cta')">Request Demo</button>
      </div>
    </nav>

    <!-- ── Hero ───────────────────────────────────────── -->
    <section id="hero" class="hero-section">
      <canvas ref="heroCanvas" class="hero-canvas" aria-hidden="true"></canvas>

      <div class="hero-content">
        <div class="hero-badge">◈ ENTERPRISE AI INTELLIGENCE PLATFORM</div>

        <h1 class="hero-h1">
          <span class="h1-white">Predict. Simulate.</span><br>
          <span class="h1-gradient">Decide with Certainty.</span>
        </h1>

        <p class="hero-sub">
          From unstructured data to living simulations. ENDORA builds a parallel world of agents —
          so you can test the future before it happens.
        </p>

        <div class="hero-ctas">
          <a href="/new" class="btn-primary" @click.prevent="router.push('/new')">
            Start Simulation <span class="btn-arrow">→</span>
          </a>
          <button class="btn-ghost">Watch Demo</button>
        </div>

        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-val">10M+</span>
            <span class="stat-lbl">Agents</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat-item">
            <span class="stat-val">6</span>
            <span class="stat-lbl">Industries</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat-item">
            <span class="stat-val">Real-time</span>
            <span class="stat-lbl">Prediction</span>
          </div>
        </div>
      </div>

      <div class="hero-chevron" aria-hidden="true">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </div>
    </section>

    <!-- ── Ticker ──────────────────────────────────────── -->
    <div class="ticker-wrap" aria-hidden="true">
      <div class="ticker-track">
        <span class="ticker-text">HEALTHCARE · FINANCE · DEFENSE · REAL ESTATE · ENVIRONMENT · POLITICS · RETAIL · SUPPLY CHAIN · ENERGY · MEDIA · </span>
        <span class="ticker-text">HEALTHCARE · FINANCE · DEFENSE · REAL ESTATE · ENVIRONMENT · POLITICS · RETAIL · SUPPLY CHAIN · ENERGY · MEDIA · </span>
      </div>
    </div>

    <!-- ── Industries ─────────────────────────────────── -->
    <section id="industries" class="section sect-dark">
      <div class="sect-inner">
        <div class="sect-label">◈ INDUSTRIES</div>
        <h2 class="sect-h2">Intelligence for Every Sector</h2>
        <p class="sect-desc">Domain-tuned agent simulations purpose-built for the complexity of each vertical.</p>

        <div class="bento-grid">
          <!-- Card 1: Healthcare – top-left tall -->
          <div class="bento-card card-tall">
            <div class="card-icon">⚕</div>
            <div class="card-tag">HOSPITALS · CLINICS · PHARMA</div>
            <h3 class="card-title">Healthcare &amp; Medical</h3>
            <p class="card-desc">Simulate patient flows, predict disease spread, optimize hospital operations. From ER triage to epidemic modeling.</p>
          </div>

          <!-- Card 2: Finance – primary, spans 2 cols -->
          <div class="bento-card card-primary card-wide">
            <div class="card-primary-badge">PRIMARY VERTICAL</div>
            <div class="card-icon">◈</div>
            <div class="card-tag">B2C · WEALTH MGMT · FINTECH</div>
            <h3 class="card-title">Finance &amp; Investment</h3>
            <p class="card-desc">Model investor sentiment, simulate market scenarios, give individuals institutional-grade intelligence.</p>
          </div>

          <!-- Card 3: Defense -->
          <div class="bento-card">
            <div class="card-icon">⬡</div>
            <div class="card-tag">INTEL · OSINT · WARGAMING</div>
            <h3 class="card-title">Defense &amp; Security</h3>
            <p class="card-desc">Wargame scenarios before deployment. Simulate narrative warfare, threat propagation, and strategic outcomes.</p>
          </div>

          <!-- Card 4: Real Estate – wide bottom -->
          <div class="bento-card card-wide">
            <div class="card-icon">▣</div>
            <div class="card-tag">DEVELOPERS · BANKS · URBAN PLANNING</div>
            <h3 class="card-title">Real Estate &amp; Urban</h3>
            <p class="card-desc">Identify optimal land parcels, simulate footfall, forecast demand before breaking ground.</p>
          </div>

          <!-- Card 5: Environment -->
          <div class="bento-card">
            <div class="card-icon">◉</div>
            <div class="card-tag">ESG · INSURANCE · GOVERNMENT</div>
            <h3 class="card-title">Environment &amp; Climate</h3>
            <p class="card-desc">Model climate impact, simulate community response to ESG policy, forecast carbon credit dynamics.</p>
          </div>

          <!-- Card 6: Political -->
          <div class="bento-card">
            <div class="card-icon">◫</div>
            <div class="card-tag">GOV · THINK TANKS · CAMPAIGNS</div>
            <h3 class="card-title">Political &amp; Policy</h3>
            <p class="card-desc">Simulate policy outcomes, model public sentiment shifts, predict election dynamics.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── How It Works ───────────────────────────────── -->
    <section id="how-it-works" class="section sect-mid">
      <div class="sect-inner">
        <div class="sect-label">◈ PLATFORM</div>
        <h2 class="sect-h2">Five Steps to Omniscience</h2>
        <p class="sect-desc">A fully automated intelligence pipeline — from raw data to living simulation.</p>

        <div class="timeline">
          <div class="timeline-step" v-for="step in steps" :key="step.num">
            <div class="ts-connector" aria-hidden="true"></div>
            <div class="ts-node">
              <div class="ts-num">{{ step.num }}</div>
              <h4 class="ts-title">{{ step.title }}</h4>
              <p class="ts-desc">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Capabilities ───────────────────────────────── -->
    <section id="platform" class="section sect-dark">
      <div class="sect-inner">
        <div class="sect-label">◈ CAPABILITIES</div>
        <h2 class="sect-h2">What Lives Inside ENDORA</h2>

        <div class="cap-grid">
          <div class="cap-card" v-for="cap in capabilities" :key="cap.title">
            <div class="cap-icon">{{ cap.icon }}</div>
            <h4 class="cap-title">{{ cap.title }}</h4>
            <p class="cap-desc">{{ cap.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Stats Bar ──────────────────────────────────── -->
    <div class="stats-bar">
      <div class="stats-inner">
        <div class="bar-stat" v-for="s in barStats" :key="s.label">
          <div class="bar-val">{{ s.val }}</div>
          <div class="bar-lbl">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <!-- ── Pricing ──────────────────────────────────── -->
    <section id="pricing" class="section sect-mid">
      <div class="sect-inner">
        <div class="sect-label">◈ PRICING</div>
        <h2 class="sect-h2">Intelligence at Every Scale</h2>
        <p class="sect-desc">Start free. Scale as your predictions do.</p>

        <div class="pricing-grid">
          <!-- Starter -->
          <div class="pricing-card">
            <div class="plan-tier">STARTER</div>
            <div class="plan-price"><span class="price-val">Free</span></div>
            <div class="plan-desc">For researchers and individual analysts exploring simulation.</div>
            <ul class="plan-features">
              <li><span class="feat-check">✓</span> 3 simulations / month</li>
              <li><span class="feat-check">✓</span> Up to 10,000 agents</li>
              <li><span class="feat-check">✓</span> Healthcare &amp; Finance verticals</li>
              <li><span class="feat-check">✓</span> PDF / TXT upload</li>
              <li><span class="feat-muted">—</span> Custom personas</li>
              <li><span class="feat-muted">—</span> API access</li>
            </ul>
            <button class="plan-btn plan-btn-ghost" @click="router.push('/new')">Get Started Free</button>
          </div>

          <!-- Pro (highlighted) -->
          <div class="pricing-card pricing-card-pro">
            <div class="plan-badge">MOST POPULAR</div>
            <div class="plan-tier">PRO</div>
            <div class="plan-price">
              <span class="price-val">$299</span>
              <span class="price-period">/ month</span>
            </div>
            <div class="plan-desc">For teams running recurring simulations across multiple verticals.</div>
            <ul class="plan-features">
              <li><span class="feat-check">✓</span> 30 simulations / month</li>
              <li><span class="feat-check">✓</span> Up to 1,000,000 agents</li>
              <li><span class="feat-check">✓</span> All 6 industry verticals</li>
              <li><span class="feat-check">✓</span> Custom persona injection</li>
              <li><span class="feat-check">✓</span> Scenario branching</li>
              <li><span class="feat-muted">—</span> Dedicated support</li>
            </ul>
            <button class="plan-btn plan-btn-primary" @click="scrollTo('cta')">Start Pro Trial →</button>
          </div>

          <!-- Enterprise -->
          <div class="pricing-card">
            <div class="plan-tier">ENTERPRISE</div>
            <div class="plan-price"><span class="price-val">Custom</span></div>
            <div class="plan-desc">For hospitals, governments, financial institutions, and defense contractors.</div>
            <ul class="plan-features">
              <li><span class="feat-check">✓</span> Unlimited simulations</li>
              <li><span class="feat-check">✓</span> 10M+ agents per run</li>
              <li><span class="feat-check">✓</span> On-premise deployment</li>
              <li><span class="feat-check">✓</span> Custom LLM fine-tuning</li>
              <li><span class="feat-check">✓</span> SLA &amp; dedicated infra</li>
              <li><span class="feat-check">✓</span> 24/7 priority support</li>
            </ul>
            <button class="plan-btn plan-btn-ghost" @click="scrollTo('cta')">Contact Sales →</button>
          </div>
        </div>

        <div class="pricing-note">
          All plans include: end-to-end encryption · GDPR compliant · SOC 2 Type II (in progress)
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────── -->
    <section id="cta" class="section sect-dark cta-section">
      <div class="sect-inner cta-inner">
        <h2 class="cta-h2">Ready to predict the future?</h2>
        <p class="cta-sub">Join enterprises already using ENDORA to simulate outcomes before they happen.</p>
        <button class="btn-cta-big">Request Early Access <span class="btn-arrow">→</span></button>
        <div class="cta-meta">Enterprise · Research · Government · Available Q3 2025</div>
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
          <a class="footer-link" @click.prevent="scrollTo('platform')">Platform</a>
          <a class="footer-link" @click.prevent="scrollTo('industries')">Industries</a>
          <a class="footer-link" href="mailto:hello@endora.ai">Contact</a>
        </nav>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

const router = useRouter()
const heroCanvas = ref(null)

let rafId = null
let resizeObserver = null

// ── Data ──────────────────────────────────────────────────
const steps = [
  { num: '01', title: 'INGEST',      desc: 'Upload any document, report, or data feed' },
  { num: '02', title: 'ONTOLOGIZE',  desc: 'ENDORA extracts entities, relationships, personas automatically' },
  { num: '03', title: 'SIMULATE',    desc: 'Million-scale agent simulation runs in parallel' },
  { num: '04', title: 'ANALYZE',     desc: 'Report agent synthesizes findings with causal reasoning' },
  { num: '05', title: 'INTERACT',    desc: 'Chat with any simulated agent or the intelligence layer' },
]

const capabilities = [
  { icon: '⬡', title: 'Living Ontology',      desc: 'Entities, relationships, and beliefs update in real-time as the simulation evolves. Never a static snapshot.' },
  { icon: '◈', title: 'Causal AI Engine',     desc: 'Not just correlation. ENDORA models cause-and-effect chains to tell you WHY outcomes happen.' },
  { icon: '◉', title: 'Human-in-the-Loop',    desc: 'Inject variables mid-simulation. Test counter-factuals. Steer outcomes from the god\'s-eye view.' },
  { icon: '▣', title: 'Multi-Modal Data',     desc: 'Ingest documents, news feeds, satellite data, financial streams, and social signals simultaneously.' },
]

const barStats = [
  { val: '10,000,000+', label: 'agents per simulation' },
  { val: '< $5',        label: 'avg cost per simulation' },
  { val: '6',           label: 'industry verticals' },
  { val: '5-step',      label: 'automated pipeline' },
]

// ── Navigation ────────────────────────────────────────────
const scrollTo = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// ── Canvas dot-grid pulse animation ──────────────────────
const initCanvas = () => {
  const canvas = heroCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  const DOT_SPACING = 36
  const DOT_RADIUS  = 1.4
  const BASE_ALPHA  = 0.12
  const PULSE_MAX   = 0.45
  const PULSE_SPEED = 0.0008
  const PULSE_SPREAD = 0.38

  let w = 0
  let h = 0
  let t = 0

  const resize = () => {
    const rect = canvas.parentElement.getBoundingClientRect()
    w = canvas.width  = rect.width
    h = canvas.height = rect.height
  }

  const draw = (ts) => {
    t = ts * PULSE_SPEED
    ctx.clearRect(0, 0, w, h)

    const cx = w / 2
    const cy = h / 2
    const maxDist = Math.sqrt(cx * cx + cy * cy)

    const cols = Math.ceil(w / DOT_SPACING) + 1
    const rows = Math.ceil(h / DOT_SPACING) + 1

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = c * DOT_SPACING
        const y = r * DOT_SPACING
        const dx = x - cx
        const dy = y - cy
        const dist = Math.sqrt(dx * dx + dy * dy)
        const norm = dist / maxDist

        // radial wave emanating from center
        const wave = Math.sin(t * 6 - norm * Math.PI * 2 * PULSE_SPREAD)
        const pulse = (wave + 1) / 2  // 0..1
        const alpha = BASE_ALPHA + pulse * (PULSE_MAX - BASE_ALPHA)

        ctx.beginPath()
        ctx.arc(x, y, DOT_RADIUS, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(99,102,241,${alpha.toFixed(3)})`
        ctx.fill()
      }
    }

    rafId = requestAnimationFrame(draw)
  }

  resize()
  rafId = requestAnimationFrame(draw)

  resizeObserver = new ResizeObserver(resize)
  resizeObserver.observe(canvas.parentElement)
}

onMounted(() => {
  initCanvas()
})

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
  if (resizeObserver) resizeObserver.disconnect()
})
</script>

<style scoped>
.page-wrap {
  --bg: #080c12; --bg-mid: #0d1117;
  --border: rgba(255,255,255,0.07); --border-str: rgba(255,255,255,0.12);
  --accent: #6366f1; --accent-lt: #a5b4fc;
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
.nav-wordmark { font-family: var(--mono); font-weight: 800; font-size: 1.05rem; letter-spacing: 3px; color: #fff; user-select: none; }
.nav-center { display: flex; gap: 36px; }
.nav-link { font-size: 0.85rem; color: var(--muted); cursor: pointer; transition: color 0.2s; text-decoration: none; }
.nav-link:hover { color: var(--text); }
.nav-right { display: flex; align-items: center; gap: 16px; }
.btn-demo {
  background: var(--accent); color: #fff; border: none;
  padding: 8px 20px; border-radius: 8px;
  font-family: var(--sans); font-size: 0.85rem; font-weight: 600;
  cursor: pointer; transition: opacity 0.2s, transform 0.2s;
}
.btn-demo:hover { opacity: 0.88; transform: translateY(-1px); }

/* Hero */
.hero-section {
  position: relative; width: 100%; height: 100vh; min-height: 640px;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; overflow: hidden; background: var(--bg);
}
.hero-canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; pointer-events: none; }
.hero-content {
  position: relative; z-index: 2; display: flex; flex-direction: column;
  align-items: center; text-align: center; padding: 0 24px; max-width: 860px;
}
.hero-badge {
  font-family: var(--mono); font-size: 0.72rem; font-variant: small-caps;
  letter-spacing: 0.15em; color: var(--accent); margin-bottom: 28px;
  padding: 6px 16px; border: 1px solid rgba(99,102,241,0.35);
  border-radius: 4px; background: rgba(99,102,241,0.06);
}
.hero-h1 { font-size: clamp(3.2rem, 5vw + 1rem, 6rem); line-height: 1.08; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 28px; }
.h1-white { color: #fff; }
.h1-gradient {
  background: linear-gradient(135deg, #6366f1 0%, #a5b4fc 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; display: inline-block;
}
.hero-sub { font-size: 1.1rem; line-height: 1.7; color: var(--muted); max-width: 620px; margin: 0 0 40px; }
.hero-ctas { display: flex; gap: 16px; margin-bottom: 52px; flex-wrap: wrap; justify-content: center; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--accent); color: #fff; padding: 14px 32px;
  border-radius: 10px; font-weight: 700; font-size: 0.95rem;
  text-decoration: none; cursor: pointer;
  box-shadow: 0 0 32px rgba(99,102,241,0.35);
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
}
.btn-primary:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 0 48px rgba(99,102,241,0.5); }
.btn-ghost {
  background: transparent; color: var(--text); border: 1px solid var(--border-str);
  padding: 14px 32px; border-radius: 10px; font-family: var(--sans);
  font-size: 0.95rem; font-weight: 600; cursor: pointer;
  backdrop-filter: blur(8px); transition: border-color 0.2s, background 0.2s;
}
.btn-ghost:hover { border-color: rgba(255,255,255,0.3); background: rgba(255,255,255,0.05); }
.btn-arrow { font-size: 1.05rem; }
.hero-stats {
  display: flex; align-items: center;
  border: 1px solid var(--border-str); border-radius: 10px;
  background: rgba(13,17,23,0.7); backdrop-filter: blur(12px); overflow: hidden;
}
.stat-item { display: flex; flex-direction: column; align-items: center; padding: 14px 32px; gap: 3px; }
.stat-val { font-family: var(--mono); font-size: 1rem; font-weight: 700; color: var(--text); white-space: nowrap; }
.stat-lbl { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; }
.stat-sep { width: 1px; height: 40px; background: var(--border-str); flex-shrink: 0; }
.hero-chevron {
  position: absolute; bottom: 28px; left: 50%; transform: translateX(-50%);
  color: var(--muted); opacity: 0.5; z-index: 2;
  animation: chevron-bounce 2s ease-in-out infinite;
}
@keyframes chevron-bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%       { transform: translateX(-50%) translateY(8px); }
}

/* Ticker */
.ticker-wrap {
  width: 100%; height: 48px; background: var(--bg-mid); overflow: hidden;
  border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  display: flex; align-items: center;
}
.ticker-track { display: flex; white-space: nowrap; animation: ticker-scroll 40s linear infinite; }
.ticker-text { font-family: var(--mono); font-size: 0.72rem; font-variant: small-caps; letter-spacing: 0.12em; color: var(--accent); opacity: 0.6; }
@keyframes ticker-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }

/* Sections */
.section { padding: 100px 0; }
.sect-dark { background: var(--bg); }
.sect-mid  { background: var(--bg-mid); }
.sect-inner { max-width: 1200px; margin: 0 auto; padding: 0 48px; }
.sect-label { font-family: var(--mono); font-size: 0.72rem; font-variant: small-caps; letter-spacing: 0.18em; color: var(--accent); margin-bottom: 16px; }
.sect-h2 { font-size: clamp(1.8rem, 3vw, 2.6rem); font-weight: 700; letter-spacing: -0.025em; margin: 0 0 12px; color: var(--text); }
.sect-desc { font-size: 1rem; color: var(--muted); max-width: 580px; line-height: 1.7; margin: 0 0 56px; }

/* Bento grid */
.bento-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.card-tall { grid-row: 1 / 3; }
.card-wide { grid-column: span 2; }
.bento-card {
  background: var(--bg-mid); border: 1px solid var(--border); border-radius: 14px;
  padding: 32px 28px; display: flex; flex-direction: column; gap: 10px;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
  position: relative; overflow: hidden;
}
.bento-card:hover { border-color: rgba(99,102,241,0.35); box-shadow: 0 0 0 1px rgba(99,102,241,0.1), 0 16px 48px rgba(0,0,0,0.4); transform: translateY(-2px); }
.card-primary { border-color: rgba(99,102,241,0.5); box-shadow: 0 0 0 1px rgba(99,102,241,0.15), 0 0 40px rgba(99,102,241,0.12); }
.card-primary-badge {
  font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.12em;
  color: var(--accent-lt); background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.3); border-radius: 4px;
  padding: 3px 10px; align-self: flex-start; margin-bottom: 4px;
}
.card-icon { font-size: 1.6rem; line-height: 1; color: var(--accent-lt); }
.card-tag  { font-family: var(--mono); font-size: 0.65rem; color: var(--muted); letter-spacing: 0.08em; }
.card-title { font-size: 1.1rem; font-weight: 700; color: var(--text); margin: 0; }
.card-desc  { font-size: 0.88rem; color: var(--muted); line-height: 1.65; margin: 0; }

/* Timeline */
.timeline { display: flex; position: relative; }
.timeline-step { flex: 1; position: relative; padding-top: 20px; }
.ts-connector { position: absolute; top: 20px; left: 50%; right: -50%; height: 1px; border-top: 1px dashed rgba(99,102,241,0.3); z-index: 0; }
.timeline-step:last-child .ts-connector { display: none; }
.ts-node { position: relative; z-index: 1; padding: 0 16px 0 0; }
.ts-num { font-family: var(--mono); font-size: 0.8rem; font-weight: 700; color: var(--accent); margin-bottom: 12px; display: inline-block; background: var(--bg-mid); padding-right: 10px; }
.ts-title { font-family: var(--mono); font-size: 0.85rem; font-weight: 700; color: var(--text); letter-spacing: 0.05em; margin: 0 0 8px; }
.ts-desc  { font-size: 0.83rem; color: var(--muted); line-height: 1.6; margin: 0; }

/* Capabilities */
.cap-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.cap-card {
  background: var(--bg-mid); border: 1px solid var(--border); border-radius: 14px;
  padding: 32px 28px; transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.cap-card:hover { border-color: rgba(99,102,241,0.35); box-shadow: 0 0 0 1px rgba(99,102,241,0.1), 0 12px 40px rgba(0,0,0,0.35); transform: translateY(-2px); }
.cap-icon  { font-size: 1.4rem; color: var(--accent-lt); margin-bottom: 14px; }
.cap-title { font-size: 1.05rem; font-weight: 700; color: var(--text); margin: 0 0 10px; }
.cap-desc  { font-size: 0.88rem; color: var(--muted); line-height: 1.65; margin: 0; }

/* Stats bar */
.stats-bar { background: var(--bg-mid); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 40px 48px; }
.stats-inner { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); }
.bar-stat { display: flex; flex-direction: column; align-items: center; gap: 6px; border-right: 1px solid var(--border); padding: 0 32px; }
.bar-stat:first-child { padding-left: 0; }
.bar-stat:last-child  { border-right: none; }
.bar-val { font-family: var(--mono); font-size: 1.6rem; font-weight: 700; color: var(--accent-lt); }
.bar-lbl { font-size: 0.78rem; color: var(--muted); text-align: center; letter-spacing: 0.05em; }

/* CTA */
.cta-section { border-top: 1px solid var(--border); }
.cta-inner { min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.cta-h2  { font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 800; letter-spacing: -0.03em; color: var(--text); margin: 0 0 16px; }
.cta-sub { font-size: 1.05rem; color: var(--muted); max-width: 520px; line-height: 1.7; margin: 0 0 40px; }
.btn-cta-big {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--accent); color: #fff; border: none;
  padding: 18px 44px; border-radius: 12px; font-family: var(--sans);
  font-size: 1rem; font-weight: 700; cursor: pointer; margin-bottom: 24px;
  box-shadow: 0 0 40px rgba(99,102,241,0.4);
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
}
.btn-cta-big:hover { opacity: 0.88; transform: translateY(-3px); box-shadow: 0 0 64px rgba(99,102,241,0.55); }
.cta-meta { font-family: var(--mono); font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; opacity: 0.7; }

/* Footer */
.footer { background: var(--bg-mid); border-top: 1px solid var(--border); padding: 32px 48px; }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
.footer-left { display: flex; align-items: center; gap: 24px; }
.footer-wordmark { font-family: var(--mono); font-weight: 800; font-size: 0.9rem; letter-spacing: 3px; color: var(--text); }
.footer-copy { font-size: 0.8rem; color: var(--muted); }
.footer-nav { display: flex; gap: 28px; }
.footer-link { font-size: 0.82rem; color: var(--muted); text-decoration: none; cursor: pointer; transition: color 0.2s; }
.footer-link:hover { color: var(--text); }

/* Pricing */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  align-items: start;
}
.pricing-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 36px 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.pricing-card:hover { border-color: rgba(99,102,241,0.3); transform: translateY(-2px); }
.pricing-card-pro {
  border-color: rgba(99,102,241,0.5);
  background: rgba(99,102,241,0.04);
  box-shadow: 0 0 0 1px rgba(99,102,241,0.15), 0 0 48px rgba(99,102,241,0.1);
}
.plan-badge {
  font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.12em;
  color: var(--accent-lt); background: rgba(99,102,241,0.15);
  border: 1px solid rgba(99,102,241,0.3); border-radius: 4px;
  padding: 3px 10px; align-self: flex-start;
}
.plan-tier { font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.18em; color: var(--muted); }
.plan-price { display: flex; align-items: baseline; gap: 6px; }
.price-val { font-size: 2.4rem; font-weight: 800; color: var(--text); letter-spacing: -0.03em; }
.price-period { font-size: 0.88rem; color: var(--muted); }
.plan-desc { font-size: 0.88rem; color: var(--muted); line-height: 1.65; }
.plan-features { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.plan-features li { display: flex; align-items: center; gap: 10px; font-size: 0.88rem; color: var(--text); }
.feat-check { color: var(--accent-lt); font-size: 0.8rem; flex-shrink: 0; }
.feat-muted { color: #333; flex-shrink: 0; }
.plan-features li:has(.feat-muted) { color: var(--muted); opacity: 0.5; }
.plan-btn {
  width: 100%; padding: 12px 20px; border-radius: 8px; font-family: var(--sans);
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s; margin-top: 8px;
}
.plan-btn-primary {
  background: var(--accent); color: #fff; border: none;
  box-shadow: 0 0 24px rgba(99,102,241,0.35);
}
.plan-btn-primary:hover { opacity: 0.88; transform: translateY(-1px); box-shadow: 0 0 36px rgba(99,102,241,0.5); }
.plan-btn-ghost {
  background: transparent; color: var(--text);
  border: 1px solid var(--border-str);
}
.plan-btn-ghost:hover { border-color: rgba(255,255,255,0.3); background: rgba(255,255,255,0.04); }
.pricing-note {
  text-align: center; margin-top: 40px;
  font-family: var(--mono); font-size: 0.72rem;
  color: var(--muted); letter-spacing: 0.05em; opacity: 0.6;
}

/* Responsive */
@media (max-width: 1024px) {
  .navbar, .sect-inner { padding: 0 24px; }
  .nav-center { display: none; }
  .bento-grid { grid-template-columns: 1fr 1fr; }
  .card-tall { grid-row: auto; }
  .card-wide { grid-column: span 2; }
  .timeline { flex-direction: column; gap: 32px; }
  .ts-connector { display: none; }
  .stats-inner { grid-template-columns: repeat(2, 1fr); gap: 24px; }
  .bar-stat { border-right: none; padding: 0; }
  .pricing-grid { grid-template-columns: 1fr; max-width: 480px; margin: 0 auto; }
}
@media (max-width: 640px) {
  .hero-stats { flex-direction: column; border: none; background: transparent; }
  .stat-sep { display: none; }
  .bento-grid, .cap-grid { grid-template-columns: 1fr; }
  .card-wide { grid-column: span 1; }
  .stats-inner { grid-template-columns: 1fr 1fr; }
  .footer-inner { flex-direction: column; align-items: flex-start; }
  .stats-bar { padding: 32px 24px; }
}
</style>
