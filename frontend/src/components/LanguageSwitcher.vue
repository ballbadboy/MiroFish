<template>
  <div class="language-switcher" ref="switcherRef">
    <button class="switcher-trigger" @click="toggleDropdown">
      {{ currentLabel }}
      <span class="caret">{{ open ? '▲' : '▼' }}</span>
    </button>
    <ul v-if="open" class="switcher-dropdown">
      <li
        v-for="loc in availableLocales"
        :key="loc.key"
        class="switcher-option"
        :class="{ active: loc.key === locale }"
        @click="switchLocale(loc.key)"
      >
        {{ loc.label }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { availableLocales } from '@/i18n/index.js'

const { locale } = useI18n()
const open = ref(false)
const switcherRef = ref(null)

const currentLabel = computed(() => {
  const found = availableLocales.find(l => l.key === locale.value)
  return found ? found.label : locale.value
})

const toggleDropdown = () => {
  open.value = !open.value
}

const switchLocale = (key) => {
  locale.value = key
  localStorage.setItem('locale', key)
  document.documentElement.lang = key
  open.value = false
}

const onClickOutside = (e) => {
  if (switcherRef.value && !switcherRef.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', onClickOutside)
  document.documentElement.lang = locale.value
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.language-switcher {
  position: relative;
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
}

.switcher-trigger {
  background: transparent;
  color: #a0a0b0;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 4px;
  transition: border-color 0.2s, color 0.2s;
  letter-spacing: 0.5px;
}

.switcher-trigger:hover {
  border-color: rgba(255,255,255,0.25);
  color: #f0f0f0;
}

.caret {
  font-size: 0.55rem;
  opacity: 0.6;
}

.switcher-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 6px;
  background: #111827;
  border: 1px solid rgba(255,255,255,0.1);
  list-style: none;
  padding: 4px 0;
  min-width: 100%;
  z-index: 1000;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  backdrop-filter: blur(12px);
}

.switcher-option {
  padding: 6px 14px;
  font-size: 0.75rem;
  color: #a0a0b0;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s, color 0.15s;
  letter-spacing: 0.5px;
}

.switcher-option:hover {
  background: rgba(255,255,255,0.06);
  color: #f0f0f0;
}

.switcher-option.active {
  color: #a5b4fc;
  background: rgba(99,102,241,0.1);
}
</style>
