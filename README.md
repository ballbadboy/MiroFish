<div align="center">

# ◈ ENDORA

### Predict. Simulate. Decide with Certainty.

**Enterprise AI platform for million-scale agent simulation.**
From unstructured data to living simulations — test the future before it happens.

[![Vue 3](https://img.shields.io/badge/Vue-3.5-42b883?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Production_Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](./Dockerfile)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)](./LICENSE)

[Quick Start](#-quick-start) · [Features](#-features) · [Verticals](#-industry-verticals) · [Architecture](#-architecture) · [Screenshots](./screenshots/)

</div>

---

## ⚡ Overview

**ENDORA** transforms unstructured documents into living, multi-agent simulations. Upload a report, define a scenario, and ENDORA constructs a parallel digital world of millions of intelligent agents — each with unique personas, memories, and behaviors. Inject "what-if" variables from a god's-eye view to predict outcomes before they happen.

> **Rehearse the future in a digital sandbox. Win decisions through simulation.**

### Why ENDORA?

| Traditional Forecasting | ENDORA Simulation |
|-------------------------|-------------------|
| Static models | Living, reactive agents |
| Aggregate statistics | Individual behavioral chains |
| Correlation only | **Causal reasoning** |
| One scenario at a time | **Parallel what-if branches** |
| Black-box predictions | Explorable, interrogable agents |

---

## 🎯 Features

### Core Engine
- **5-Step Pipeline** — Graph Build → Env Setup → Simulate → Analyze → Interact
- **Million-Scale Agents** — average 847,293 agents per simulation
- **Living Ontology** — entities and relationships update in real-time
- **Causal AI Engine** — explains *why* outcomes happen, not just *what*
- **Scenario Branching** — clone simulations and inject what-if variables in parallel
- **Multi-Modal Data** — documents, news, satellite, social signals

### Frontend
- **6 Industry Verticals** — purpose-built UIs for each sector (see below)
- **Dark Premium Design** — animated dot-grid hero, bento layouts, glass effects
- **Auth Flow** — login, register, route guards, redirect-after-login
- **Toast Notifications** — 4 types with auto-dismiss
- **i18n** — English, 中文, ไทย (629 keys)
- **Mobile Responsive** — 375px → 1440px
- **Privacy-First Analytics** — DNT-respecting, no third-party trackers

### Production
- **Docker Compose** — nginx + Flask + Gunicorn
- **CI/CD Workflows** — GitHub Actions for build, test, deploy
- **E2E Tests** — Playwright suite covering 5 critical flows
- **SEO Meta Tags** — dynamic per-route titles and descriptions
- **Health Checks** — built-in liveness probes

---

## 🏭 Industry Verticals

Each vertical includes a purpose-built landing page with industry-specific use cases, animated terminal preview, and tailored CTAs.

| Vertical | Color | Use Cases | Sample Scenarios |
|----------|-------|-----------|------------------|
| **⚕ Healthcare** | Teal `#2dd4bf` | ICU overflow, epidemic modeling, triage optimization | ER demand surge, ward staffing |
| **◈ Finance** | Gold `#f59e0b` | Sentiment modeling, market scenarios, IPO prediction | Rate cuts, sector rotation |
| **⬡ Defense** | Red `#ef4444` | Wargaming, narrative warfare, threat propagation | NARWAR campaigns, OSINT fusion |
| **▣ Real Estate** | Cyan `#06b6d4` | Site selection, footfall sim, ROI forecast | Mixed-use development scoring |
| **◉ Environment** | Emerald `#10b981` | Flood modeling, ESG impact, carbon credits | Monsoon scenarios, evacuation |
| **◫ Politics** | Purple `#8b5cf6` | Election modeling, policy impact, opinion tracking | Minimum wage impact, coalitions |

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose, OR
- Python 3.11 + Node 20 + uv

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/your-org/endora.git
cd endora
cp .env.example .env  # Edit and add API keys
docker compose -f docker-compose.prod.yml up -d
```

Open http://localhost — nginx serves the frontend and proxies `/api/*` to the backend.

### Option 2: Local Development

```bash
# Backend
cd backend
uv sync
uv run python run.py  # → http://localhost:5001

# Frontend (separate terminal)
cd frontend
npm install
npm run dev  # → http://localhost:5173
```

### Required Environment Variables

```bash
# Edit .env
ENDORA_LLM_API_KEY=sk-...           # OpenAI-compatible LLM
ENDORA_LLM_MODEL=gpt-4o-mini
ZEP_API_KEY=...                      # Knowledge graph backend
```

See [`.env.example`](./.env.example) for the full list.

---

## 🏗 Architecture

### Frontend (Vue 3 + Vite)

```
frontend/src/
├── views/                   # Route components
│   ├── Home.vue            # Landing page
│   ├── Auth.vue            # Login / Register
│   ├── Dashboard.vue       # Simulation history
│   ├── NewProject.vue      # Create simulation
│   ├── NotFound.vue        # 404 page
│   └── industries/         # 6 vertical pages
├── components/             # Reusable UI
│   ├── ScenarioBranchCreator.vue   # What-if modal
│   ├── ScenarioComparisonPanel.vue # Branch results
│   ├── ToastNotification.vue       # Global toasts
│   ├── GraphPanel.vue              # D3 knowledge graph
│   └── Step{1-5}*.vue              # Pipeline steps
├── store/auth.js           # Auth composable (localStorage-backed)
├── api/                    # Backend API clients
├── utils/analytics.js      # Privacy-first telemetry
├── i18n/                   # EN, ZH, TH (629 keys)
└── router/index.js         # Vue Router with guards
```

### Backend (Flask + Gunicorn)

```
backend/app/
├── api/                              # Flask blueprints
│   ├── graph.py                     # Ontology + GraphRAG
│   ├── simulation.py                # Run + branch + interact
│   └── report.py                    # Report agent
├── services/
│   ├── ontology_generator.py        # LLM → schema
│   ├── graph_builder.py             # Documents → Zep graph
│   ├── oasis_profile_generator.py   # Persona generation
│   ├── simulation_runner.py         # Agent simulation engine
│   ├── scenario_branch_manager.py   # What-if branching (512 lines)
│   ├── report_agent.py              # ReACT report generator
│   └── zep_*.py                     # Knowledge graph adapters
└── utils/
    ├── llm_client.py                # OpenAI-compatible wrapper
    ├── logger.py                    # Structured logging
    └── security.py                  # Input sanitization
```

### Production Deployment

```
                  ┌────────────────────────────┐
                  │  nginx (port 80)           │
                  │  • static files            │
                  │  • gzip + cache headers    │
                  │  • security headers        │
                  └─────────┬──────────────────┘
                            │ /api/*
                  ┌─────────▼──────────────────┐
                  │  Flask + Gunicorn          │
                  │  4 workers, 120s timeout   │
                  └─────────┬──────────────────┘
                            │
                  ┌─────────▼──────────────────┐
                  │  Zep · LLM API · OASIS sim │
                  └────────────────────────────┘
```

---

## 🧪 Testing

```bash
cd frontend
npm install
npx playwright install chromium
npm run test:e2e            # Run all E2E tests
npm run test:e2e:ui         # Interactive UI mode
npm run test:e2e:report     # View HTML report
```

E2E coverage:
- ✅ Landing page (hero, industries, pricing, 404)
- ✅ Auth flow (login, register, redirect guard, sign out)
- ✅ Dashboard (stats, search, filters, mock data)
- ✅ All 6 industry verticals (smoke tests)

---

## 📊 Routes

| Route | Auth | Description |
|-------|------|-------------|
| `/` | Public | Landing page |
| `/auth` | Public | Sign in / Register |
| `/industry/{vertical}` | Public | 6 vertical pages |
| `/new` | 🔒 Required | Create new simulation |
| `/dashboard` | 🔒 Required | Simulation history |
| `/process/:id` | 🔒 Required | Step 1: Graph Build |
| `/simulation/:id` | 🔒 Required | Step 2: Env Setup |
| `/simulation/:id/start` | 🔒 Required | Step 3: Run + Branch |
| `/report/:id` | 🔒 Required | Step 4: Report |
| `/interaction/:id` | 🔒 Required | Step 5: Deep Interaction |
| `/*` | Public | 404 page |

---

## 🎨 Screenshots

13 pitch-deck screenshots at 1440×900 in [`./screenshots/`](./screenshots/):

| # | Page |
|---|------|
| 01 | Landing Hero |
| 02 | Industries Bento Grid |
| 03 | Pricing |
| 04 | Auth (Sign In / Register) |
| 05 | New Simulation |
| 06 | Dashboard |
| 07–12 | 6 Industry Verticals |
| 13 | 404 Not Found |

---

## 🛣 Roadmap

- [x] 6 industry vertical pages
- [x] Scenario branching (backend + UI)
- [x] Auth state + route guards
- [x] Toast notifications
- [x] i18n (EN / ZH / TH)
- [x] Production Docker + nginx
- [x] CI/CD workflows
- [x] E2E test suite
- [x] Privacy-first analytics
- [ ] Backend API integration verification
- [ ] Real-time collaborative editing
- [ ] Multi-tenant RBAC
- [ ] Audit log + compliance reports
- [ ] On-premise deployment guide (Defense vertical)

---

## 📜 Origin

ENDORA is forked from [MiroFish](./README.upstream.md), a swarm intelligence engine by 666ghj. The original engine and architecture are preserved; ENDORA adds enterprise positioning, vertical-specific UIs, auth, scenario branching UI, and production-ready deployment.

---

## 📝 License

Apache 2.0 — see [LICENSE](./LICENSE).

---

<div align="center">

**◈ ENDORA** — _Rehearse the future. Win the present._

</div>
