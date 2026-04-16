<template>
  <div class="auth-wrap">

    <!-- ── Left: Branding Panel ──────────────────────── -->
    <aside class="brand-panel">
      <router-link to="/" class="brand-wordmark">ENDORA</router-link>

      <div class="brand-center">
        <span class="brand-icon">&#x25C8;</span>
        <h1 class="brand-h1">Predict the Future</h1>
        <p class="brand-sub">
          Access ENDORA's intelligence platform to simulate, analyze,
          and decide with certainty.
        </p>

        <ul class="brand-features">
          <li>&#x25C8; Million-scale agent simulations</li>
          <li>&#x25C8; 6 industry verticals</li>
          <li>&#x25C8; Real-time causal AI engine</li>
        </ul>
      </div>

      <span class="brand-copy">&copy; 2025 Endora Intelligence</span>
    </aside>

    <!-- ── Right: Form Panel ─────────────────────────── -->
    <main class="form-panel">
      <div class="form-card">

        <!-- Tab switcher -->
        <div class="tab-bar">
          <button
            :class="['tab-btn', { active: activeTab === 'login' }]"
            @click="switchTab('login')"
          >Sign In</button>
          <button
            :class="['tab-btn', { active: activeTab === 'register' }]"
            @click="switchTab('register')"
          >Create Account</button>
        </div>

        <!-- Error banner -->
        <div v-if="error" class="error-banner">{{ error }}</div>

        <!-- Login form -->
        <form
          v-if="activeTab === 'login'"
          class="auth-form"
          @submit.prevent="handleLogin"
        >
          <label class="field-label">Email</label>
          <input
            v-model="loginForm.email"
            type="email"
            class="field-input"
            placeholder="you@company.com"
            required
          />

          <label class="field-label">Password</label>
          <input
            v-model="loginForm.password"
            type="password"
            class="field-input"
            placeholder="********"
            required
          />

          <a href="#" class="forgot-link">Forgot password?</a>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Signing in...' : 'Sign In \u2192' }}
          </button>

          <div class="divider"><span>or continue with</span></div>

          <div class="social-row">
            <button type="button" class="btn-social">
              <span class="social-icon">G</span> Google
            </button>
            <button type="button" class="btn-social">
              <span class="social-icon">&#x2687;</span> GitHub
            </button>
          </div>

          <p class="switch-text">
            Don't have an account?
            <a href="#" class="switch-link" @click.prevent="switchTab('register')">Create one &rarr;</a>
          </p>
        </form>

        <!-- Register form -->
        <form
          v-if="activeTab === 'register'"
          class="auth-form"
          @submit.prevent="handleRegister"
        >
          <label class="field-label">Full Name</label>
          <input
            v-model="registerForm.name"
            type="text"
            class="field-input"
            placeholder="Jane Doe"
            required
          />

          <label class="field-label">Work Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            class="field-input"
            placeholder="you@company.com"
            required
          />

          <label class="field-label">Company / Organization</label>
          <input
            v-model="registerForm.company"
            type="text"
            class="field-input"
            placeholder="Acme Inc."
            required
          />

          <label class="field-label">Password</label>
          <input
            v-model="registerForm.password"
            type="password"
            class="field-input"
            placeholder="********"
            required
          />

          <label class="field-label">Confirm Password</label>
          <input
            v-model="registerForm.confirmPassword"
            type="password"
            class="field-input"
            placeholder="********"
            required
          />

          <label class="field-label">Industry</label>
          <select v-model="registerForm.industry" class="field-input field-select" required>
            <option value="" disabled>Select your industry</option>
            <option>Healthcare</option>
            <option>Finance</option>
            <option>Defense</option>
            <option>Real Estate</option>
            <option>Environment</option>
            <option>Politics</option>
            <option>Other</option>
          </select>

          <label class="checkbox-row">
            <input v-model="registerForm.agreeTerms" type="checkbox" class="checkbox-input" />
            <span class="checkbox-custom"></span>
            <span class="checkbox-label">
              I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
            </span>
          </label>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Creating account...' : 'Create Account \u2192' }}
          </button>

          <p class="switch-text">
            Already have an account?
            <a href="#" class="switch-link" @click.prevent="switchTab('login')">Sign in &rarr;</a>
          </p>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../store/auth'

const router = useRouter()
const route = useRoute()
const { login } = useAuth()
const toast = inject('toast')
const redirectTo = route.query.redirect || '/dashboard'

const activeTab = ref('login')
const loading = ref(false)
const error = ref(null)

const loginForm = ref({ email: '', password: '' })
const registerForm = ref({
  name: '',
  email: '',
  company: '',
  password: '',
  confirmPassword: '',
  industry: '',
  agreeTerms: false,
})

function switchTab(tab) {
  activeTab.value = tab
  error.value = null
}

function handleLogin() {
  error.value = null
  loading.value = true
  setTimeout(() => {
    login({ email: loginForm.value.email })
    loading.value = false
    toast?.success('Welcome back to ENDORA')
    router.push(redirectTo)
  }, 1500)
}

function handleRegister() {
  error.value = null

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  if (!registerForm.value.agreeTerms) {
    error.value = 'Please agree to terms'
    return
  }

  loading.value = true
  setTimeout(() => {
    login({
      name: registerForm.value.name,
      email: registerForm.value.email,
      company: registerForm.value.company,
      industry: registerForm.value.industry
    })
    loading.value = false
    toast?.success('Account created — welcome to ENDORA')
    router.push(redirectTo)
  }, 1500)
}
</script>

<style scoped>
/* ── Tokens ─────────────────────────────────────────── */
.auth-wrap {
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

  display: flex;
  height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  overflow: hidden;
}

/* ── Left: Branding ─────────────────────────────────── */
.brand-panel {
  width: 50%;
  background: var(--bg-mid);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 40px 56px;
  border-right: 1px solid var(--border);
  overflow: hidden;
}

.brand-wordmark {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 1.05rem;
  letter-spacing: 3px;
  color: #fff;
  text-decoration: none;
  user-select: none;
}

.brand-center {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 420px;
}

.brand-icon {
  font-size: 64px;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 24px;
}

.brand-h1 {
  font-size: 32px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  margin: 0 0 16px;
}

.brand-sub {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--muted);
  margin: 0 0 32px;
}

.brand-features {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.brand-features li {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  color: var(--accent-lt);
  opacity: 0.85;
}

.brand-copy {
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--muted);
  letter-spacing: 0.06em;
  opacity: 0.5;
}

/* ── Right: Form ────────────────────────────────────── */
.form-panel {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
  overflow-y: auto;
}

.form-card {
  width: 100%;
  max-width: 400px;
}

/* Tabs */
.tab-bar {
  display: flex;
  gap: 4px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab-btn {
  flex: 1;
  padding: 10px 0;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-family: var(--sans);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.tab-btn.active {
  background: var(--accent);
  color: #fff;
}

/* Error */
.error-banner {
  background: rgba(239,68,68,0.12);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  font-size: 0.82rem;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 20px;
}

/* Form fields */
.auth-form {
  display: flex;
  flex-direction: column;
}

.field-label {
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.field-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  margin-bottom: 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: var(--text);
  font-family: var(--sans);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.field-input::placeholder {
  font-family: var(--mono);
  color: rgba(255,255,255,0.2);
  font-size: 0.82rem;
}

.field-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.18);
}

.field-select {
  appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23888' stroke-width='1.5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.field-select option {
  background: #0d1117;
  color: var(--text);
}

/* Forgot link */
.forgot-link {
  align-self: flex-end;
  font-size: 0.78rem;
  color: var(--muted);
  text-decoration: none;
  margin: -8px 0 20px;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: var(--accent-lt);
}

/* Submit */
.btn-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 48px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-family: var(--sans);
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 32px rgba(99,102,241,0.25);
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
  margin-bottom: 24px;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 0 48px rgba(99,102,241,0.45);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Spinner */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
  color: var(--muted);
  font-size: 0.72rem;
  letter-spacing: 0.06em;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-str);
}

/* Social buttons */
.social-row {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
}

.btn-social {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  background: transparent;
  border: 1px solid var(--border-str);
  border-radius: 10px;
  color: var(--text);
  font-family: var(--sans);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  backdrop-filter: blur(8px);
  transition: border-color 0.2s, background 0.2s;
}

.btn-social:hover {
  border-color: rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.05);
}

.social-icon {
  font-weight: 800;
  font-size: 1rem;
}

/* Switch text */
.switch-text {
  text-align: center;
  font-size: 0.82rem;
  color: var(--muted);
  margin: 0;
}

.switch-link {
  color: var(--accent-lt);
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}

.switch-link:hover {
  opacity: 0.8;
}

/* Checkbox */
.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 20px;
  cursor: pointer;
  position: relative;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-custom {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 4px;
  background: rgba(255,255,255,0.04);
  margin-top: 1px;
  transition: background 0.2s, border-color 0.2s;
  position: relative;
}

.checkbox-input:checked + .checkbox-custom {
  background: var(--accent);
  border-color: var(--accent);
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 5px;
  height: 9px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-label {
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.5;
}

.checkbox-label a {
  color: var(--accent-lt);
  text-decoration: none;
}

.checkbox-label a:hover {
  text-decoration: underline;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 860px) {
  .auth-wrap {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
    overflow: auto;
  }

  .brand-panel {
    width: 100%;
    padding: 32px 24px;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .brand-center {
    display: none;
  }

  .brand-copy {
    display: none;
  }

  .form-panel {
    width: 100%;
    padding: 32px 20px 48px;
  }
}
</style>
