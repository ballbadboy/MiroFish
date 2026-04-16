<template>
  <div class="sentiment-chart-wrap" ref="wrapRef">
    <div v-if="legend.length > 1" class="chart-legend">
      <span
        v-for="(item, idx) in legend"
        :key="item.name"
        class="legend-item"
        :class="{ 'is-winner': winnerName && item.name === winnerName }"
      >
        <svg width="20" height="10" class="legend-line-svg">
          <line
            x1="0" y1="5" x2="20" y2="5"
            stroke="#a5b4fc"
            :stroke-width="winnerName && item.name === winnerName ? 2.5 : 1.5"
            :stroke-dasharray="DASH_STYLES[idx % DASH_STYLES.length]"
          />
        </svg>
        {{ item.name }}
        <span v-if="winnerName && item.name === winnerName" class="winner-badge">WINNER</span>
      </span>
    </div>

    <svg ref="svgRef" class="sentiment-svg" :style="{ height: `${height}px` }"></svg>

    <div v-if="divergenceRound" class="divergence-note">
      <span class="divr-dot"></span>
      Divergence detected at Round {{ divergenceRound }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import {
  select,
  scaleLinear,
  line,
  curveCatmullRom,
  axisBottom,
  axisLeft,
} from 'd3'

// ─── Props ────────────────────────────────────────────────────────────────────
const props = defineProps({
  /** Array of { name, data: number[] } — multi-series (scenario comparison) */
  series: { type: Array, default: () => [] },
  /** Single series shorthand: number[] — overrides series prop */
  data:   { type: Array, default: null },
  /** Round number where branches diverge (draws vertical dashed line) */
  divergenceRound: { type: Number, default: null },
  /** Branch name to highlight as winner */
  winnerName: { type: String, default: null },
  /** Chart height in px */
  height: { type: Number, default: 180 },
})

// ─── SVG refs ─────────────────────────────────────────────────────────────────
const svgRef  = ref(null)
const wrapRef = ref(null)

// Dash patterns for up to 5 series (visual legend must match)
const DASH_STYLES = ['none', '6 3', '2 3', '8 2 2 2', '4 2']
const LINE_WEIGHTS = [2, 2, 2, 1.5, 1.5]
const LINE_OPACITIES = [1, 0.8, 0.65, 0.7, 0.6]

// ─── Normalize input ──────────────────────────────────────────────────────────
const normalizedSeries = computed(() => {
  if (props.data?.length) return [{ name: 'Sentiment', data: props.data }]
  return (props.series || []).filter(s => s.data?.length)
})

const legend = computed(() => normalizedSeries.value.map(s => ({ name: s.name })))

// ─── Draw function ────────────────────────────────────────────────────────────
function draw() {
  const svgEl  = svgRef.value
  const wrapEl = wrapRef.value
  if (!svgEl || !wrapEl) return

  const allSeries = normalizedSeries.value
  if (!allSeries.length) return

  const W      = wrapEl.clientWidth || 400
  const H      = props.height
  const margin = { top: 12, right: 28, bottom: 32, left: 40 }
  const iW     = W - margin.left - margin.right
  const iH     = H - margin.top  - margin.bottom

  const maxLen = Math.max(...allSeries.map(s => s.data.length))
  if (maxLen < 2) return

  const xScale = scaleLinear().domain([0, maxLen - 1]).range([0, iW])
  const yScale = scaleLinear().domain([0, 1]).range([iH, 0])

  // ── Clear & size ──
  const svg = select(svgEl)
  svg.selectAll('*').remove()
  svg.attr('width', W).attr('height', H)

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  // ── Horizontal grid lines ──
  g.append('g').attr('class', 'grid')
    .selectAll('line')
    .data([0.25, 0.5, 0.75])
    .join('line')
      .attr('x1', 0).attr('x2', iW)
      .attr('y1', d => yScale(d)).attr('y2', d => yScale(d))
      .attr('stroke', d => d === 0.5 ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.05)')
      .attr('stroke-width', 1)

  // ── X axis ──
  const xTicks = Math.min(maxLen, 8)
  g.append('g')
    .attr('transform', `translate(0,${iH})`)
    .call(
      axisBottom(xScale)
        .ticks(xTicks)
        .tickFormat(d => `R${Math.round(d) + 1}`)
    )
    .call(ax => ax.select('.domain').attr('stroke', 'rgba(255,255,255,0.12)'))
    .call(ax => ax.selectAll('.tick line').attr('stroke', 'rgba(255,255,255,0.12)'))
    .call(ax => ax.selectAll('.tick text')
      .attr('fill', '#666')
      .attr('font-size', '10')
      .attr('font-family', 'JetBrains Mono, monospace')
    )

  // ── Y axis ──
  g.append('g')
    .call(axisLeft(yScale).ticks(4).tickFormat(d => `${Math.round(d * 100)}%`))
    .call(ax => ax.select('.domain').remove())
    .call(ax => ax.selectAll('.tick line').remove())
    .call(ax => ax.selectAll('.tick text')
      .attr('fill', '#666')
      .attr('font-size', '10')
      .attr('font-family', 'JetBrains Mono, monospace')
    )

  // ── Divergence marker ──
  if (props.divergenceRound != null && props.divergenceRound > 0) {
    const dx = xScale(Math.min(props.divergenceRound - 1, maxLen - 1))
    g.append('line')
      .attr('x1', dx).attr('x2', dx).attr('y1', 0).attr('y2', iH)
      .attr('stroke', '#ef4444').attr('stroke-width', 1.5).attr('stroke-dasharray', '4 3').attr('opacity', 0.7)
    g.append('text')
      .attr('x', dx + 4).attr('y', 10)
      .attr('fill', '#ef4444').attr('font-size', '9')
      .attr('font-family', 'JetBrains Mono, monospace')
      .text(`÷R${props.divergenceRound}`)
  }

  // ── Baseline label ──
  g.append('text')
    .attr('x', iW + 4).attr('y', yScale(0.5) + 3)
    .attr('fill', '#555').attr('font-size', '9')
    .attr('font-family', 'JetBrains Mono, monospace')
    .text('50%')

  // ── Series lines ──
  const lineGen = line()
    .x((_, i) => xScale(i))
    .y(d  => yScale(Math.max(0, Math.min(1, d ?? 0.5))))
    .curve(curveCatmullRom.alpha(0.5))

  // Line color palette for dark theme
  const LINE_COLORS = ['#a5b4fc', '#6ee7b7', '#fbbf24', '#f87171', '#c084fc']

  allSeries.forEach((s, idx) => {
    const dash    = DASH_STYLES[idx % DASH_STYLES.length]
    const weight  = LINE_WEIGHTS[idx % LINE_WEIGHTS.length]
    const opacity = LINE_OPACITIES[idx % LINE_OPACITIES.length]
    const isWin   = props.winnerName && s.name === props.winnerName
    const color   = LINE_COLORS[idx % LINE_COLORS.length]

    // Draw path (initially solid for animation)
    const path = g.append('path')
      .datum(s.data)
      .attr('fill', 'none')
      .attr('stroke', color)
      .attr('stroke-width', isWin ? 2.5 : weight)
      .attr('opacity', isWin ? 1 : opacity)
      .attr('d', lineGen)

    // Animate stroke-dashoffset draw-on
    const len = path.node().getTotalLength()
    path
      .attr('stroke-dasharray', `${len} ${len}`)
      .attr('stroke-dashoffset', len)
      .transition()
      .duration(700 + idx * 120)
      .attr('stroke-dashoffset', 0)
      .on('end', () => {
        // Restore the real dash pattern after animation
        path.attr('stroke-dasharray', dash === 'none' ? null : dash)
      })

    // End-of-line dot
    const lastVal = s.data.at(-1)
    if (lastVal != null) {
      g.append('circle')
        .attr('cx', xScale(s.data.length - 1))
        .attr('cy', yScale(lastVal))
        .attr('r', isWin ? 4.5 : 3)
        .attr('fill', isWin ? color : '#0d1117')
        .attr('stroke', color)
        .attr('stroke-width', 1.5)
        .attr('opacity', opacity)
    }
  })
}

// ─── Reactivity & lifecycle ───────────────────────────────────────────────────
watch(
  () => [normalizedSeries.value, props.divergenceRound, props.winnerName, props.height],
  () => nextTick(draw),
  { deep: true }
)

let ro = null
onMounted(() => {
  nextTick(draw)
  ro = new ResizeObserver(() => draw())
  if (wrapRef.value) ro.observe(wrapRef.value)
})
onUnmounted(() => ro?.disconnect())
</script>

<style scoped>
.sentiment-chart-wrap {
  width: 100%;
  position: relative;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 8px;
  padding: 0 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  color: #888;
  font-weight: 500;
}

.legend-item.is-winner {
  color: #f0f0f0;
  font-weight: 700;
}

.legend-line-svg {
  flex-shrink: 0;
}

.winner-badge {
  font-size: 9px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.06em;
  background: rgba(99,102,241,0.2);
  color: #a5b4fc;
  border: 1px solid rgba(99,102,241,0.4);
  padding: 1px 5px;
  border-radius: 3px;
}

.sentiment-svg {
  display: block;
  width: 100%;
  overflow: visible;
}

.divergence-note {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 10px;
  font-family: 'JetBrains Mono', monospace;
  color: #ef4444;
  letter-spacing: 0.03em;
}

.divr-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  box-shadow: 0 0 4px rgba(239,68,68,0.5);
  flex-shrink: 0;
}
</style>
