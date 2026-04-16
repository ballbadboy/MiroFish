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
    component: Home
  },
  {
    path: '/new',
    name: 'NewProject',
    component: NewProject
  },
  {
    path: '/industry/healthcare',
    name: 'Healthcare',
    component: Healthcare
  },
  {
    path: '/industry/finance',
    name: 'Finance',
    component: Finance
  },
  {
    path: '/industry/defense',
    name: 'Defense',
    component: Defense
  },
  {
    path: '/industry/real-estate',
    name: 'RealEstate',
    component: RealEstate
  },
  {
    path: '/industry/environment',
    name: 'Environment',
    component: Environment
  },
  {
    path: '/industry/politics',
    name: 'Politics',
    component: Politics
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
