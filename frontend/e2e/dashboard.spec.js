import { test, expect } from '@playwright/test'
import { loginAs } from './utils/auth.js'

test.describe('Dashboard (authenticated)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page)
    await page.goto('/dashboard')
  })

  test('renders 4 stat cards', async ({ page }) => {
    const cards = page.locator('.stats-row .stat-card')
    await expect(cards).toHaveCount(4)
  })

  test('search input is visible and accepts text', async ({ page }) => {
    const search = page.locator('input.search-input')
    await expect(search).toBeVisible()
    await search.fill('ICU')
    await expect(search).toHaveValue('ICU')
  })

  test('all four filter pills are clickable', async ({ page }) => {
    const labels = ['All', 'Running', 'Completed', 'Failed']
    for (const label of labels) {
      const pill = page.locator('.filter-pills .pill', { hasText: label })
      await expect(pill).toBeVisible()
      await pill.click()
      await expect(pill).toHaveClass(/pill-active/)
    }
  })

  test('at least one simulation card is visible (mock fallback)', async ({ page }) => {
    const cards = page.locator('.sim-card')
    await expect(cards.first()).toBeVisible()
    await expect(await cards.count()).toBeGreaterThan(0)
  })

  test('"+ New Simulation" button navigates to /new', async ({ page }) => {
    await page.locator('.navbar').getByRole('button', { name: /\+ New Simulation/i }).click()
    await expect(page).toHaveURL(/\/new$/)
  })
})
