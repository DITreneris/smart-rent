/**
 * End-to-end tests for the property listing functionality.
 */

const { test, expect } = require('@playwright/test');

test.describe('Property Listing Page', () => {
  // Navigate to the property listing page before each test
  test.beforeEach(async ({ page }) => {
    await page.goto('/properties');
    // Ensure the page is fully loaded
    await page.waitForSelector('h1:has-text("Properties")');
  });

  test('should display property listings', async ({ page }) => {
    // Check if property listings are displayed
    const propertyCards = page.locator('.property-card');
    await expect(propertyCards).toHaveCount({ min: 1 });
    
    // Check if property cards have basic information
    await expect(propertyCards.first().locator('.property-title')).toBeVisible();
    await expect(propertyCards.first().locator('.property-price')).toBeVisible();
    await expect(propertyCards.first().locator('.property-location')).toBeVisible();
  });

  test('should filter properties by type', async ({ page }) => {
    // Select property type filter
    await page.selectOption('select[name="property_type"]', 'apartment');
    await page.click('button:has-text("Apply Filters")');
    
    // Wait for filtered results
    await page.waitForResponse(response => 
      response.url().includes('/api/properties') && 
      response.status() === 200
    );
    
    // Check that all displayed properties are apartments
    const propertyTypes = page.locator('.property-type');
    await expect(propertyTypes).toHaveCount({ min: 0 });
    
    // For each property, check if it's an apartment
    const count = await propertyTypes.count();
    for (let i = 0; i < count; i++) {
      await expect(propertyTypes.nth(i)).toHaveText(/apartment/i);
    }
  });

  test('should search properties by keyword', async ({ page }) => {
    // Enter search term
    await page.fill('input[name="search"]', 'luxury');
    await page.click('button:has-text("Search")');
    
    // Wait for search results
    await page.waitForResponse(response => 
      response.url().includes('/api/properties/search') && 
      response.status() === 200
    );
    
    // Check that search results contain the keyword
    const propertyTitles = page.locator('.property-title');
    const propertyDescriptions = page.locator('.property-description');
    
    const titleCount = await propertyTitles.count();
    const descCount = await propertyDescriptions.count();
    
    // Check if at least one property title or description contains the search term
    let foundMatch = false;
    
    for (let i = 0; i < titleCount; i++) {
      const titleText = await propertyTitles.nth(i).textContent();
      if (titleText.toLowerCase().includes('luxury')) {
        foundMatch = true;
        break;
      }
    }
    
    if (!foundMatch) {
      for (let i = 0; i < descCount; i++) {
        const descText = await propertyDescriptions.nth(i).textContent();
        if (descText.toLowerCase().includes('luxury')) {
          foundMatch = true;
          break;
        }
      }
    }
    
    expect(foundMatch).toBeTruthy();
  });

  test('should navigate to property details page', async ({ page }) => {
    // Click on the first property card
    await page.click('.property-card:first-child');
    
    // Check if we've navigated to the property details page
    await page.waitForSelector('.property-details');
    
    // Verify property details page elements
    await expect(page.locator('h1.property-title')).toBeVisible();
    await expect(page.locator('.property-images')).toBeVisible();
    await expect(page.locator('.property-description')).toBeVisible();
    await expect(page.locator('.property-features')).toBeVisible();
    await expect(page.locator('.property-price-details')).toBeVisible();
  });

  test('should display correct price range when using price filter', async ({ page }) => {
    // Set min and max price
    await page.fill('input[name="min_price"]', '1000');
    await page.fill('input[name="max_price"]', '2000');
    await page.click('button:has-text("Apply Filters")');
    
    // Wait for filtered results
    await page.waitForResponse(response => 
      response.url().includes('/api/properties') && 
      response.status() === 200
    );
    
    // Check that all displayed properties are within the price range
    const propertyPrices = page.locator('.property-price');
    const count = await propertyPrices.count();
    
    for (let i = 0; i < count; i++) {
      const priceText = await propertyPrices.nth(i).textContent();
      const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
      
      expect(price).toBeGreaterThanOrEqual(1000);
      expect(price).toBeLessThanOrEqual(2000);
    }
  });

  test('should sort properties by price', async ({ page }) => {
    // Select sort by price (ascending)
    await page.selectOption('select[name="sort"]', 'price_asc');
    await page.click('button:has-text("Apply")');
    
    // Wait for sorted results
    await page.waitForResponse(response => 
      response.url().includes('/api/properties') && 
      response.status() === 200
    );
    
    // Check that properties are sorted by price in ascending order
    const propertyPrices = page.locator('.property-price');
    const count = await propertyPrices.count();
    
    if (count > 1) {
      let prevPrice = 0;
      
      for (let i = 0; i < count; i++) {
        const priceText = await propertyPrices.nth(i).textContent();
        const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
        
        if (i > 0) {
          expect(price).toBeGreaterThanOrEqual(prevPrice);
        }
        
        prevPrice = price;
      }
    }
  });
}); 