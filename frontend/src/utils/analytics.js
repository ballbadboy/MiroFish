/**
 * Privacy-friendly analytics module.
 *
 * Sends events to a single configurable endpoint. No third-party trackers.
 * Honors Do-Not-Track. Buffers events offline via localStorage and flushes
 * on reconnect / pagehide using sendBeacon when available.
 */

const QUEUE_KEY = '__endora_analytics_queue'
const SESSION_KEY = '__endora_analytics_session'
const MAX_QUEUE = 50

const config = Object.freeze({
  endpoint: null,
  debug: false,
  enabled: true,
  sessionId: null
})

let state = config

/**
 * Return a frozen merge of state + patch (immutable update).
 * @param {object} patch
 */
const updateState = (patch) => Object.freeze({ ...state, ...patch })

/** @returns {boolean} true when the browser signals Do-Not-Track. */
const isDntEnabled = () => {
  if (typeof navigator === 'undefined') return false
  const dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack
  return dnt === '1' || dnt === 'yes'
}

/** Generate a uuid-v4-like anonymous id. */
const makeSessionId = () =>
  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })

/** Load existing session id from sessionStorage or create a new one. */
const loadOrCreateSessionId = () => {
  try {
    const existing = sessionStorage.getItem(SESSION_KEY)
    if (existing) return existing
    const fresh = makeSessionId()
    sessionStorage.setItem(SESSION_KEY, fresh)
    return fresh
  } catch {
    return makeSessionId()
  }
}

/** Read queued events from localStorage. Returns a new array. */
const readQueue = () => {
  try {
    const raw = localStorage.getItem(QUEUE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? [...parsed] : []
  } catch {
    return []
  }
}

/** Persist queue (capped to MAX_QUEUE most recent events). */
const writeQueue = (events) => {
  try {
    const capped = events.slice(-MAX_QUEUE)
    localStorage.setItem(QUEUE_KEY, JSON.stringify(capped))
  } catch {
    /* storage full or unavailable — drop silently */
  }
}

/** Append payload to queue (returns new queue, never mutates). */
const enqueue = (payload) => {
  const next = [...readQueue(), payload]
  writeQueue(next)
}

/** Build an immutable event payload. */
const buildPayload = (type, name, properties) => {
  const screen = typeof window !== 'undefined' && window.screen
    ? { width: window.screen.width, height: window.screen.height }
    : { width: 0, height: 0 }
  const viewport = typeof window !== 'undefined'
    ? { width: window.innerWidth, height: window.innerHeight }
    : { width: 0, height: 0 }
  return Object.freeze({
    type,
    name,
    properties: Object.freeze({ ...(properties || {}) }),
    session_id: state.sessionId,
    timestamp: Date.now(),
    url: typeof window !== 'undefined' ? window.location.href : '',
    referrer: typeof document !== 'undefined' ? document.referrer : '',
    user_agent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
    screen,
    viewport
  })
}

/**
 * Attempt to send a payload (or array of payloads) to the endpoint.
 * Tries sendBeacon → fetch(keepalive). Returns true on apparent success.
 */
const sendPayload = (payload) => {
  if (!state.endpoint) return false
  const body = JSON.stringify(payload)
  try {
    if (typeof navigator !== 'undefined' && typeof navigator.sendBeacon === 'function') {
      const blob = new Blob([body], { type: 'application/json' })
      if (navigator.sendBeacon(state.endpoint, blob)) return true
    }
  } catch {
    /* fall through to fetch */
  }
  try {
    fetch(state.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
      mode: 'cors',
      credentials: 'omit'
    }).catch(() => enqueue(Array.isArray(payload) ? payload[0] : payload))
    return true
  } catch {
    return false
  }
}

const dispatch = (payload) => {
  if (!state.enabled) return
  if (state.debug) console.log('[analytics]', payload)
  if (!state.endpoint) return
  if (!sendPayload(payload)) enqueue(payload)
}

/**
 * Flush any buffered events from localStorage as a single batch.
 * @returns {boolean} true when nothing remains queued.
 */
export const flushQueue = () => {
  if (!state.enabled || !state.endpoint) return false
  const queued = readQueue()
  if (queued.length === 0) return true
  const ok = sendPayload(queued)
  if (ok) {
    try { localStorage.removeItem(QUEUE_KEY) } catch { /* noop */ }
  }
  return ok
}

/**
 * Initialize analytics. Safe to call once at app boot.
 * @param {{endpoint?: string, debug?: boolean}} options
 */
export const init = (options = {}) => {
  if (isDntEnabled()) {
    state = updateState({ enabled: false, debug: !!options.debug })
    if (options.debug) console.log('[analytics] disabled (DNT=1)')
    return
  }
  state = updateState({
    endpoint: options.endpoint || null,
    debug: !!options.debug,
    enabled: true,
    sessionId: loadOrCreateSessionId()
  })
  if (typeof window === 'undefined') return
  window.addEventListener('online', () => flushQueue())
  window.addEventListener('pagehide', () => flushQueue())
  flushQueue()
}

/**
 * Track a page view.
 * @param {string} path
 * @param {string} [title]
 */
export const trackPageView = (path, title) => {
  dispatch(buildPayload('page_view', path, { title: title || '' }))
}

/**
 * Track a custom event.
 * @param {string} name
 * @param {object} [properties]
 */
export const trackEvent = (name, properties = {}) => {
  dispatch(buildPayload('event', name, properties))
}
