<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
        @click="dismiss(toast.id)"
      >
        <span class="toast-icon">{{ iconMap[toast.type] }}</span>
        <span class="toast-msg">{{ toast.message }}</span>
        <button class="toast-close" @click.stop="dismiss(toast.id)">&times;</button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

const iconMap = {
  success: '✓',
  error: '✗',
  info: '◈',
  warning: '⚠'
}

function show(message, type = 'info', duration = 4000) {
  const id = nextId++
  toasts.value = [...toasts.value, { id, message, type }]
  if (duration > 0) {
    setTimeout(() => dismiss(id), duration)
  }
}

function dismiss(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

defineExpose({ show, dismiss })
</script>

<style scoped>
.toast-container {
  position: fixed; top: 80px; right: 24px; z-index: 9999;
  display: flex; flex-direction: column; gap: 10px;
  pointer-events: none;
}
.toast {
  pointer-events: auto; cursor: pointer;
  display: flex; align-items: center; gap: 10px;
  padding: 12px 20px; border-radius: 10px;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 0.88rem; color: #f0f0f0;
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  min-width: 280px; max-width: 420px;
}
.toast-success { background: rgba(34,197,94,0.15); border-color: rgba(34,197,94,0.3); }
.toast-error   { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.3); }
.toast-info    { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.3); }
.toast-warning { background: rgba(249,115,22,0.15); border-color: rgba(249,115,22,0.3); }
.toast-icon {
  font-size: 1rem; flex-shrink: 0;
}
.toast-success .toast-icon { color: #22c55e; }
.toast-error .toast-icon   { color: #ef4444; }
.toast-info .toast-icon    { color: #6366f1; }
.toast-warning .toast-icon { color: #f97316; }
.toast-msg { flex: 1; line-height: 1.4; }
.toast-close {
  background: none; border: none; color: rgba(255,255,255,0.4);
  font-size: 1.2rem; cursor: pointer; padding: 0 0 0 8px;
  transition: color 0.2s;
}
.toast-close:hover { color: #fff; }

/* Transitions */
.toast-enter-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.toast-leave-active { transition: all 0.25s ease-in; }
.toast-enter-from { opacity: 0; transform: translateX(40px) scale(0.95); }
.toast-leave-to   { opacity: 0; transform: translateX(40px) scale(0.95); }
</style>
