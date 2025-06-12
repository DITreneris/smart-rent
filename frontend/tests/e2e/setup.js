/**
 * Setup file for end-to-end testing with Playwright.
 * This script handles the global test environment setup and teardown.
 */

const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

// Store global browser and auth state
let browser;
let authFile;

/**
 * Setup function that runs before all tests
 */
async function globalSetup() {
  console.log('Starting E2E test environment setup...');
  
  // Create auth state directory if it doesn't exist
  const authDir = path.join(__dirname, 'auth-state');
  if (!fs.existsSync(authDir)) {
    fs.mkdirSync(authDir, { recursive: true });
  }
  
  // Path to save auth state
  authFile = path.join(authDir, 'auth.json');
  
  // Launch browser
  browser = await chromium.launch();
  
  // Create a new browser context
  const context = await browser.newContext();
  
  // Create a new page
  const page = await context.newPage();
  
  try {
    // Navigate to login page
    console.log('Navigating to login page...');
    await page.goto('http://localhost:3000/login');
    
    // Login as test user
    console.log('Logging in as test user...');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'securepassword123');
    await page.click('button[type="submit"]');
    
    // Wait for navigation to complete
    await page.waitForURL('http://localhost:3000/dashboard');
    
    // Save authentication state
    console.log('Saving authentication state...');
    await context.storageState({ path: authFile });
    
    console.log('Authentication completed and state saved.');
  } catch (error) {
    console.error('Error during authentication setup:', error);
    throw error;
  } finally {
    // Close page, context and browser
    await page.close();
    await context.close();
  }
  
  console.log('Global setup completed.');
}

/**
 * Teardown function that runs after all tests
 */
async function globalTeardown() {
  console.log('Starting E2E test environment teardown...');
  
  // Close the browser if it's open
  if (browser) {
    await browser.close();
    browser = null;
  }
  
  console.log('Global teardown completed.');
}

/**
 * Creates a new authenticated browser context for tests
 */
async function createAuthenticatedContext() {
  return await chromium.launchPersistentContext('', {
    storageState: authFile
  });
}

module.exports = {
  globalSetup,
  globalTeardown,
  createAuthenticatedContext,
  getAuthFile: () => authFile
}; 