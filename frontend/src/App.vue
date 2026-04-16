<template>
  <router-view />
  <ToastNotification ref="toastRef" />
</template>

<script setup>
import { ref, provide } from 'vue'
import ToastNotification from './components/ToastNotification.vue'

const toastRef = ref(null)

// Global toast — any component can inject('toast') and call show()
provide('toast', {
  success: (msg) => toastRef.value?.show(msg, 'success'),
  error: (msg) => toastRef.value?.show(msg, 'error'),
  info: (msg) => toastRef.value?.show(msg, 'info'),
  warning: (msg) => toastRef.value?.show(msg, 'warning')
})
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #f0f0f0;
  background-color: #080c12;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #111;
}

::-webkit-scrollbar-thumb {
  background: #333;
}

::-webkit-scrollbar-thumb:hover {
  background: #444;
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}
</style>
