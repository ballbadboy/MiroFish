import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NewProject from '../views/NewProject.vue'
import Healthcare from '../views/industries/Healthcare.vue'
import Finance from '../views/industries/Finance.vue'
import Defense from '../views/industries/Defense.vue'
import RealEstate from '../views/industries/RealEstate.vue'
import Environment from '../views/industries/Environment.vue'
import Politics from '../views/industries/Politics.vue'
import Process from '../views/MainView.vue'
import SimulationView from '../views/SimulationView.vue'
import SimulationRunView from '../views/SimulationRunView.vue'
import ReportView from '../views/ReportView.vue'
import InteractionView from '../views/InteractionView.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'ENDORA — Predict. Simulate. Decide.',
      description: 'Enterprise AI platform for million-scale agent simulation across healthcare, finance, defense, and more.'
    }
  },
  {
    path: '/new',
    name: 'NewProject',
    component: NewProject,
    meta: {
      title: 'New Simulation — ENDORA',
      description: 'Configure and launch a new AI agent simulation.'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: 'Dashboard — ENDORA',
      description: 'View your simulation history, track active runs, and access reports.'
    }
  },
  {
    path: '/industry/healthcare',
    name: 'Healthcare',
    component: Healthcare,
    meta: {
      title: 'Healthcare Intelligence — ENDORA',
      description: 'Simulate patient flows, predict disease spread, optimize hospital operations.'
    }
  },
  {
    path: '/industry/finance',
    name: 'Finance',
    component: Finance,
    meta: {
      title: 'Finance Intelligence — ENDORA',
      description: 'Model investor sentiment, simulate market scenarios, institutional-grade AI.'
    }
  },
  {
    path: '/industry/defense',
    name: 'Defense',
    component: Defense,
    meta: {
      title: 'Defense Intelligence — ENDORA',
      description: 'Wargame scenarios, simulate narrative warfare, assess strategic threats.'
    }
  },
  {
    path: '/industry/real-estate',
    name: 'RealEstate',
    component: RealEstate,
    meta: {
      title: 'Real Estate Intelligence — ENDORA',
      description: 'Find optimal sites, simulate footfall, forecast urban development ROI.'
    }
  },
  {
    path: '/industry/environment',
    name: 'Environment',
    component: Environment,
    meta: {
      title: 'Climate Intelligence — ENDORA',
      description: 'Model climate impact, simulate community response, forecast ESG outcomes.'
    }
  },
  {
    path: '/industry/politics',
    name: 'Politics',
    component: Politics,
    meta: {
      title: 'Policy Intelligence — ENDORA',
      description: 'Simulate policy outcomes, model public opinion, predict election dynamics.'
    }
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true,
    meta: {
      title: 'Graph Build — ENDORA',
      description: 'Step 1: Knowledge graph construction and entity extraction.'
    }
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true,
    meta: {
      title: 'Env Setup — ENDORA',
      description: 'Step 2: Environment setup and agent configuration.'
    }
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true,
    meta: {
      title: 'Simulation — ENDORA',
      description: 'Step 3: Running agent simulation.'
    }
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true,
    meta: {
      title: 'Report — ENDORA',
      description: 'Step 4: Simulation report and analysis.'
    }
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true,
    meta: {
      title: 'Interaction — ENDORA',
      description: 'Step 5: Deep interaction with simulated agents.'
    }
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../views/Auth.vue'),
    meta: {
      title: 'Sign In — ENDORA',
      description: 'Sign in or create an ENDORA account.'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.afterEach((to) => {
  document.title = to.meta.title || 'ENDORA'
})

export default router
