<template>
  <div class="notfound-wrap">
    <div class="notfound-content">
      <div class="glitch-icon">◈</div>
      <h1 class="nf-code">404</h1>
      <p class="nf-title">Simulation Not Found</p>
      <p class="nf-desc">The page you're looking for doesn't exist in this timeline.</p>
      <div class="nf-actions">
        <button class="btn-primary" @click="$router.push('/')">
          ← Back to ENDORA
        </button>
        <button class="btn-ghost" @click="$router.push('/dashboard')">
          Dashboard
        </button>
      </div>
      <div class="nf-path">
        <span class="path-label">Requested:</span>
        <code class="path-code">{{ $route.fullPath }}</code>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notfound-wrap {
  min-height: 100vh; background: #080c12; color: #f0f0f0;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Space Grotesk', system-ui, sans-serif;
}
.notfound-content {
  text-align: center; max-width: 480px; padding: 24px;
}
.glitch-icon {
  font-size: 3rem; color: #6366f1; margin-bottom: 16px;
  animation: pulse-icon 2s ease-in-out infinite;
}
@keyframes pulse-icon {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.1); }
}
.nf-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(5rem, 12vw, 8rem); font-weight: 800;
  letter-spacing: -0.04em; margin: 0;
  background: linear-gradient(135deg, #6366f1 0%, #a5b4fc 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nf-title {
  font-size: 1.3rem; font-weight: 700; margin: 8px 0 12px; color: #f0f0f0;
}
.nf-desc {
  font-size: 0.95rem; color: #888; line-height: 1.6; margin: 0 0 32px;
}
.nf-actions {
  display: flex; gap: 12px; justify-content: center; margin-bottom: 40px;
}
.btn-primary {
  background: #6366f1; color: #fff; border: none;
  padding: 12px 28px; border-radius: 8px; font-weight: 600;
  font-size: 0.9rem; cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}
.btn-primary:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-ghost {
  background: transparent; color: #888;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 12px 28px; border-radius: 8px;
  font-size: 0.9rem; cursor: pointer;
  transition: all 0.2s;
}
.btn-ghost:hover { color: #f0f0f0; border-color: rgba(255,255,255,0.3); }
.nf-path {
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.path-label {
  font-size: 0.75rem; color: #666; font-family: 'JetBrains Mono', monospace;
}
.path-code {
  font-size: 0.75rem; color: #a5b4fc;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(99,102,241,0.08); padding: 4px 10px;
  border-radius: 4px; border: 1px solid rgba(99,102,241,0.2);
}
</style>
