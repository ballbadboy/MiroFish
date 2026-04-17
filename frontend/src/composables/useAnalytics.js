import { trackEvent, trackPageView } from '../utils/analytics'

/**
 * Vue composable that exposes the analytics tracking API.
 *
 * @returns {{
 *   trackEvent: (name: string, properties?: object) => void,
 *   trackPageView: (path: string, title?: string) => void
 * }}
 */
export function useAnalytics() {
  return { trackEvent, trackPageView }
}
