<template>
  <Transition name="overlay">
    <div v-if="visible" class="branch-overlay" @mousedown.self="$emit('close')">
      <div class="branch-modal">

        <!-- Header -->
        <div class="modal-header">
          <div>
            <span class="label-tag">&#9672; SCENARIO BRANCHING</span>
            <p class="header-sub">
              Create what-if experiments from simulation
              <span class="mono">{{ simulationId }}</span>
            </p>
          </div>
          <button class="close-btn" @click="$emit('close')">&times;</button>
        </div>

        <!-- Scrollable content -->
        <div class="modal-body">

          <!-- Base info card -->
          <div class="base-card">
            <span class="base-label">BASE SIMULATION:</span>
            <span class="mono">{{ simulationId }}</span>
            <p class="base-note">
              The base simulation will be cloned for each branch. No re-generation cost.
            </p>
          </div>

          <!-- Error banner -->
          <div v-if="error" class="error-banner">&#9888; {{ error }}</div>

          <!-- Branch list -->
          <TransitionGroup name="branch" tag="div" class="branch-list">
            <div
              v-for="(branch, idx) in branches"
              :key="branch._key"
              class="branch-card"
            >
              <div class="card-head">
                <span class="branch-badge">BRANCH {{ String(idx + 1).padStart(2, '0') }}</span>
                <button
                  v-if="branches.length > 2"
                  class="remove-btn"
                  @click="removeBranch(idx)"
                >&times;</button>
              </div>

              <label class="field-label">Branch Name</label>
              <input
                v-model="branch.name"
                class="field-input"
                type="text"
                placeholder='e.g. "Price +10%"'
              />

              <label class="field-label">Description</label>
              <textarea
                v-model="branch.description"
                class="field-input field-textarea"
                rows="2"
                placeholder="Describe this scenario variant..."
              ></textarea>

              <div class="injection-divider">INJECTION</div>

              <label class="field-label">Narrative Direction</label>
              <input
                v-model="branch.narrative"
                class="field-input"
                type="text"
                placeholder='e.g. "Strong public backlash"'
              />

              <label class="field-label">Initial Post</label>
              <textarea
                v-model="branch.initialPost"
                class="field-input field-textarea"
                rows="2"
                placeholder='e.g. "We are raising prices by 10%"'
              ></textarea>

              <label class="field-label">Poster Type</label>
              <select v-model="branch.posterType" class="field-input">
                <option value="Official">Official</option>
                <option value="Influencer">Influencer</option>
                <option value="Public">Public</option>
                <option value="Bot">Bot</option>
              </select>
            </div>
          </TransitionGroup>

          <!-- Add branch -->
          <button
            v-if="branches.length < 5"
            class="add-branch-btn"
            @click="addBranch"
          >+ Add Branch</button>
        </div>

        <!-- Action buttons -->
        <div class="modal-footer">
          <button class="btn-ghost" @click="$emit('close')">Cancel</button>
          <button
            class="btn-primary"
            :disabled="!canSubmit || loading"
            @click="handleSubmit"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Creating experiment...' : 'Run Experiment \u2192' }}
          </button>
        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createBranchExperiment, runBranchExperiment } from '../api/simulation'

// ─── Props / Emits ───────────────────────────────────────────────────────────
const props = defineProps({
  simulationId: { type: String, required: true },
  visible: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'experiment-created'])

// ─── State ───────────────────────────────────────────────────────────────────
let _keySeq = 0
const createEmptyBranch = () => ({
  _key: ++_keySeq,
  name: '',
  description: '',
  narrative: '',
  initialPost: '',
  posterType: 'Official',
})

const branches = ref([createEmptyBranch(), createEmptyBranch()])
const loading = ref(false)
const error = ref(null)

// ─── Computed ────────────────────────────────────────────────────────────────
const canSubmit = computed(() =>
  branches.value.length >= 2 &&
  branches.value.every(b => b.name.trim() && b.narrative.trim()),
)

// ─── Methods ─────────────────────────────────────────────────────────────────
const addBranch = () => {
  if (branches.value.length < 5) {
    branches.value = [...branches.value, createEmptyBranch()]
  }
}

const removeBranch = (index) => {
  if (branches.value.length > 2) {
    branches.value = branches.value.filter((_, i) => i !== index)
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    const payload = {
      base_simulation_id: props.simulationId,
      branches: branches.value.map(b => ({
        name: b.name,
        description: b.description,
        injection: {
          narrative_direction: b.narrative,
          initial_posts: b.initialPost
            ? [{ content: b.initialPost, poster_type: b.posterType }]
            : [],
        },
      })),
    }

    const createRes = await createBranchExperiment(payload)

    if (createRes.data?.success) {
      const experimentId = createRes.data.data.experiment_id
      await runBranchExperiment(experimentId)
      emit('experiment-created', {
        experimentId,
        manifest: createRes.data.data,
      })
    } else {
      error.value = createRes.data?.error || 'Failed to create experiment'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.branch-overlay {
  position: fixed; inset: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: center;
  background: rgba(0,0,0,0.7); backdrop-filter: blur(4px);
}
.branch-modal {
  display: flex; flex-direction: column;
  width: 100%; max-width: 800px; max-height: 90vh;
  background: #0d1117; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px; color: #f0f0f0; overflow: hidden;
  font-family: 'Space Grotesk','Noto Sans SC',system-ui,sans-serif;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 20px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.07);
}
.label-tag {
  font: 700 10px/1 'JetBrains Mono',monospace; text-transform: uppercase;
  letter-spacing: 0.12em; font-variant: small-caps;
  color: #a5b4fc; background: rgba(99,102,241,0.15);
  border: 1px solid rgba(99,102,241,0.3); padding: 3px 8px; border-radius: 2px;
}
.header-sub { margin: 8px 0 0; font-size: 12px; color: #888; }
.close-btn {
  background: none; border: none; color: #888; font-size: 22px;
  cursor: pointer; padding: 0 4px; line-height: 1; transition: color 0.15s;
}
.close-btn:hover { color: #f0f0f0; }
.modal-body { flex: 1 1 auto; overflow-y: auto; padding: 20px 24px; }
.base-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 4px; padding: 14px 16px; margin-bottom: 20px;
}
.base-label {
  font: 700 9px/1 'JetBrains Mono',monospace;
  letter-spacing: 0.1em; color: #888; margin-right: 6px;
}
.base-note { margin: 8px 0 0; font-size: 11px; color: #666; line-height: 1.5; }
.mono { font-family: 'JetBrains Mono',monospace; color: #a5b4fc; }
.error-banner {
  background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
  color: #ef4444; font-size: 12px; padding: 10px 14px;
  border-radius: 4px; margin-bottom: 16px;
}
.branch-list { display: flex; flex-direction: column; gap: 14px; }
.branch-card {
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
  border-left: 2px solid #6366f1; border-radius: 4px; padding: 16px 18px;
}
.card-head {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 12px;
}
.branch-badge {
  font: 700 9px/1 'JetBrains Mono',monospace; letter-spacing: 0.1em;
  color: #a5b4fc; background: rgba(99,102,241,0.12); padding: 3px 8px; border-radius: 2px;
}
.remove-btn {
  background: none; border: 1px solid rgba(239,68,68,0.25); color: #ef4444;
  font-size: 16px; width: 24px; height: 24px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 3px; cursor: pointer; transition: background 0.15s, border-color 0.15s;
}
.remove-btn:hover { background: rgba(239,68,68,0.12); border-color: rgba(239,68,68,0.5); }
.field-label {
  display: block; font: 700 9px/1 'JetBrains Mono',monospace;
  letter-spacing: 0.08em; text-transform: uppercase; color: #666; margin: 10px 0 4px;
}
.field-input {
  display: block; width: 100%; box-sizing: border-box;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 3px; color: #f0f0f0; font-size: 13px; padding: 8px 10px;
  font-family: 'Space Grotesk','Noto Sans SC',system-ui,sans-serif;
  outline: none; transition: border-color 0.15s;
}
.field-input::placeholder { color: #555; }
.field-input:focus { border-color: rgba(99,102,241,0.5); }
.field-textarea { resize: vertical; }
select.field-input {
  appearance: none; padding-right: 28px;
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23888' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 10px center;
}
.injection-divider {
  font: 700 8px/1 'JetBrains Mono',monospace; letter-spacing: 0.12em;
  color: #555; margin: 14px 0 4px; padding-top: 10px;
  border-top: 1px solid rgba(255,255,255,0.05);
}
.add-branch-btn {
  width: 100%; margin-top: 14px; padding: 12px;
  background: transparent; border: 1px dashed rgba(255,255,255,0.12);
  border-radius: 4px; color: #888; font: 12px 'JetBrains Mono',monospace;
  cursor: pointer; transition: border-color 0.15s, color 0.15s;
}
.add-branch-btn:hover { border-color: rgba(99,102,241,0.4); color: #a5b4fc; }
.modal-footer {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 24px; border-top: 1px solid rgba(255,255,255,0.07);
}
.btn-ghost {
  background: transparent; border: 1px solid rgba(255,255,255,0.1);
  color: #888; font-size: 12px; padding: 8px 18px; border-radius: 4px;
  cursor: pointer; font-family: 'Space Grotesk',system-ui,sans-serif;
  transition: border-color 0.15s, color 0.15s;
}
.btn-ghost:hover { border-color: rgba(255,255,255,0.2); color: #f0f0f0; }
.btn-primary {
  display: flex; align-items: center; gap: 8px;
  background: #6366f1; border: none; color: #fff;
  font: 600 12px 'Space Grotesk',system-ui,sans-serif;
  padding: 8px 22px; border-radius: 4px; cursor: pointer; transition: opacity 0.15s;
}
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-primary:not(:disabled):hover { opacity: 0.85; }
.spinner {
  width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.2);
  border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.overlay-enter-active, .overlay-leave-active { transition: opacity 0.2s ease; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
.branch-enter-active { transition: all 0.25s ease-out; }
.branch-leave-active { transition: all 0.2s ease-in; }
.branch-enter-from { opacity: 0; transform: translateY(-8px); }
.branch-leave-to { opacity: 0; transform: translateY(8px); }
</style>
