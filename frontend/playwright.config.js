/**
 * Playwright configuration for end-to-end testing.
 * @see https://playwright.dev/docs/test-configuration
 */

const { defineConfig, devices } = require('@playwright/test');
const { globalSetup, globalTeardown, getAuthFile } = require('./tests/e2e/setup');

module.exports = defineConfig({
  // Global setup and teardown
  globalSetup,
  globalTeardown,
  
  // Basic test configuration
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list']
  ],
  
  // Configure projects for different browsers
  projects: [
    {
      name: 'chromium',
      use: {
        browserName: 'chromium',
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        video: 'on-first-retry',
        trace: 'on-first-retry',
        storageState: getAuthFile()
      },
    },
    {
      name: 'firefox',
      use: {
        browserName: 'firefox',
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        video: 'on-first-retry',
        trace: 'on-first-retry',
        storageState: getAuthFile()
      },
    },
    {
      name: 'webkit',
      use: {
        browserName: 'webkit',
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        video: 'on-first-retry',
        trace: 'on-first-retry',
        storageState: getAuthFile()
      },
    },
    {
      name: 'mobile-chrome',
      use: {
        browserName: 'chromium',
        ...devices['Pixel 5'],
        ignoreHTTPSErrors: true,
        video: 'on-first-retry',
        trace: 'on-first-retry',
        storageState: getAuthFile()
      },
    },
    {
      name: 'mobile-safari',
      use: {
        browserName: 'webkit',
        ...devices['iPhone 12'],
        ignoreHTTPSErrors: true,
        video: 'on-first-retry',
        trace: 'on-first-retry',
        storageState: getAuthFile()
      },
    },
  ],
  
  // Configure development web server
  webServer: {
    command: 'npm run start',
    port: 3000,
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
  },
  
  // Configure test outputs
  outputDir: 'test-results/',
  
  // Configure Playwright's built-in expect
  expect: {
    timeout: 5000,
    toHaveScreenshot: {
      maxDiffPixels: 100,
    },
  },
  
  // Use the same directory for all test metadata
  use: {
    baseURL: 'http://localhost:3000',
    actionTimeout: 10000,
    navigationTimeout: 15000,
    screenshot: 'only-on-failure',
    testIdAttribute: 'data-testid',
  },
}); 