import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { init as initAnalytics, trackPageView } from './utils/analytics'
import './styles/global.css'

const app = createApp(App)

app.use(router)
app.use(i18n)

initAnalytics({
  endpoint: import.meta.env.VITE_ANALYTICS_ENDPOINT,
  debug: import.meta.env.DEV
})

router.afterEach((to) => {
  trackPageView(to.fullPath, to.meta?.title)
})

app.mount('#app')
