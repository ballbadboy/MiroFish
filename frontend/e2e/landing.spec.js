import { test, expect } from '@playwright/test'

test.describe('Landing page (public)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('hero renders with H1 containing "Predict" and "Decide"', async ({ page }) => {
    const h1 = page.locator('h1.hero-h1')
    await expect(h1).toBeVisible()
    await expect(h1).toContainText('Predict')
    await expect(h1).toContainText('Decide')
  })

  test('navbar shows Sign In when logged out', async ({ page }) => {
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible()
  })

  test('Start Simulation CTA is visible', async ({ page }) => {
    await expect(page.getByRole('link', { name: /Start Simulation/i })).toBeVisible()
  })

  test('industries section renders 6 vertical cards', async ({ page }) => {
    const cards = page.locator('#industries .bento-card')
    await expect(cards).toHaveCount(6)
  })

  test('pricing section is visible with 3 plans', async ({ page }) => {
    const pricing = page.locator('#pricing')
    await expect(pricing).toBeVisible()
    await expect(pricing.locator('.pricing-card')).toHaveCount(3)
  })
})

test.describe('Industry card navigation', () => {
  const industries = [
    { name: 'Healthcare & Medical', path: '/industry/healthcare' },
    { name: 'Finance & Investment', path: '/industry/finance' },
    { name: 'Defense & Security', path: '/industry/defense' },
    { name: 'Real Estate & Urban', path: '/industry/real-estate' },
    { name: 'Environment & Climate', path: '/industry/environment' },
    { name: 'Political & Policy', path: '/industry/politics' },
  ]

  for (const { name, path } of industries) {
    test(`clicking "${name}" navigates to ${path}`, async ({ page }) => {
      await page.goto('/')
      await page.locator('#industries .bento-card', { hasText: name }).click()
      await expect(page).toHaveURL(new RegExp(`${path}$`))
    })
  }
})

test.describe('404 page', () => {
  test('renders for unknown routes', async ({ page }) => {
    await page.goto('/does-not-exist')
    await expect(page.locator('.nf-code')).toHaveText('404')
    await expect(page.getByText('Simulation Not Found')).toBeVisible()
  })
})
