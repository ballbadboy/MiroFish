import { ref, computed } from 'vue'

// ── Reactive auth state (persisted in localStorage) ──
const user = ref(JSON.parse(localStorage.getItem('endora_user') || 'null'))

const isLoggedIn = computed(() => !!user.value)
const userName = computed(() => user.value?.name || '')
const userEmail = computed(() => user.value?.email || '')

function login(userData) {
  const profile = {
    name: userData.name || userData.email.split('@')[0],
    email: userData.email,
    company: userData.company || '',
    industry: userData.industry || '',
    loggedInAt: new Date().toISOString()
  }
  user.value = profile
  localStorage.setItem('endora_user', JSON.stringify(profile))
}

function logout() {
  user.value = null
  localStorage.removeItem('endora_user')
}

export function useAuth() {
  return { user, isLoggedIn, userName, userEmail, login, logout }
}
