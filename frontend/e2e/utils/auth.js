// Helper for seeding the ENDORA auth state directly into localStorage.
// The frontend reads `endora_user` from localStorage at module load time
// (see src/store/auth.js), so we must set it BEFORE any protected
// navigation. We first navigate to `/` to gain a same-origin context for
// localStorage, then write the key, then the caller can navigate freely.

const DEFAULT_USER = {
  name: 'Demo User',
  email: 'demo@endora.ai',
  company: 'ENDORA QA',
  industry: 'Healthcare',
  loggedInAt: '2025-01-01T00:00:00.000Z',
}

export async function loginAs(page, user = DEFAULT_USER) {
  const profile = { ...DEFAULT_USER, ...user }
  await page.goto('/')
  await page.evaluate((p) => {
    localStorage.setItem('endora_user', JSON.stringify(p))
  }, profile)
  return profile
}

export async function clearAuth(page) {
  await page.goto('/')
  await page.evaluate(() => localStorage.removeItem('endora_user'))
}
