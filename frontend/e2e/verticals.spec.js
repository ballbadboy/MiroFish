import { test, expect } from '@playwright/test'

const verticals = [
  ['/industry/healthcare', 'Healthcare'],
  ['/industry/finance', 'Institutional-Grade'],
  ['/industry/defense', 'Wargame'],
  ['/industry/real-estate', 'Site'],
  ['/industry/environment', 'Climate'],
  ['/industry/politics', 'Policy'],
]

test.describe('Industry verticals — smoke', () => {
  for (const [path, expectedHeading] of verticals) {
    test(`${path} renders heading mentioning "${expectedHeading}" and a Run/Start CTA`, async ({ page }) => {
      await page.goto(path)

      const h1 = page.locator('h1.hero-h1')
      await expect(h1).toBeVisible()
      await expect(h1).toContainText(new RegExp(expectedHeading, 'i'))

      const cta = page.getByRole('button', { name: /\b(Run|Start)\b/i }).first()
      await expect(cta).toBeVisible()
    })
  }
})
