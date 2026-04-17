import { test, expect } from '@playwright/test'
import { clearAuth, loginAs } from './utils/auth.js'

test.describe('Auth page UI', () => {
  test('shows Sign In and Create Account tabs', async ({ page }) => {
    await page.goto('/auth')
    const tabs = page.locator('.tab-bar .tab-btn')
    await expect(tabs).toHaveCount(2)
    await expect(tabs.nth(0)).toHaveText('Sign In')
    await expect(tabs.nth(1)).toHaveText('Create Account')
  })
})

test.describe('Login flow', () => {
  test.beforeEach(async ({ page }) => {
    await clearAuth(page)
  })

  test('submits login and redirects to dashboard', async ({ page }) => {
    await page.goto('/auth')
    await page.locator('input[type="email"]').fill('demo@endora.ai')
    await page.locator('input[type="password"]').fill('password123')
    await page.getByRole('button', { name: /Sign In/i }).click()

    await expect(page).toHaveURL(/\/dashboard$/)
  })

  test('shows "Welcome back to ENDORA" toast', async ({ page }) => {
    await page.goto('/auth')
    await page.locator('input[type="email"]').fill('demo@endora.ai')
    await page.locator('input[type="password"]').fill('password123')
    await page.getByRole('button', { name: /Sign In/i }).click()

    await expect(page.getByText('Welcome back to ENDORA')).toBeVisible()
  })

  test('navbar shows username and Sign Out after login', async ({ page }) => {
    await loginAs(page, { name: 'Jane Demo', email: 'jane@endora.ai' })
    await page.goto('/')

    await expect(page.getByText('Jane Demo')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Sign Out' })).toBeVisible()
  })

  test('Sign Out clears localStorage and returns to home', async ({ page }) => {
    await loginAs(page)
    await page.goto('/')

    await page.getByRole('button', { name: 'Sign Out' }).click()
    await expect(page).toHaveURL(/\/$/)

    const user = await page.evaluate(() => localStorage.getItem('endora_user'))
    expect(user).toBeNull()
  })
})

test.describe('Auth guard & redirect', () => {
  test.beforeEach(async ({ page }) => {
    await clearAuth(page)
  })

  test('visiting /dashboard logged-out redirects to /auth?redirect=/dashboard', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/auth\?redirect=%2Fdashboard|\/auth\?redirect=\/dashboard/)
  })

  test('after login from redirect, lands on /dashboard (not /auth)', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/auth\?redirect=/)

    await page.locator('input[type="email"]').fill('demo@endora.ai')
    await page.locator('input[type="password"]').fill('password123')
    await page.getByRole('button', { name: /Sign In/i }).click()

    await expect(page).toHaveURL(/\/dashboard$/)
  })
})
