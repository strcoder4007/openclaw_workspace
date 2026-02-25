#!/usr/bin/env node
/**
 * Teams Checker - Check for unread messages and mentions
 * Run via: node teams-checker.js
 */

import { chromium } from 'playwright';

const TEAMS_URL = 'https://teams.cloud.microsoft/';

async function checkTeams() {
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    await page.goto(TEAMS_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000); // Wait for full load
    
    // Check for unread messages count
    const unreadButton = page.locator('button:has-text("Unread")').first();
    const hasUnread = await unreadButton.isVisible().catch(() => false);
    
    // Check mentions in sidebar
    const mentionsButton = page.locator('text=Mentions').first();
    const hasMentions = await mentionsButton.isVisible().catch(() => false);
    
    // Get recent activity items
    const activitySection = page.locator('text=Activity').first();
    await activitySection.click();
    await page.waitForTimeout(2000);
    
    // Get list of recent notifications
    const notifications = await page.locator('[role="treeitem"]').allTextContents();
    
    console.log('\n=== Teams Check Results ===');
    console.log(`Unread filter visible: ${hasUnread}`);
    console.log(`Mentions section visible: ${hasMentions}`);
    console.log(`Recent notifications: ${notifications.slice(0, 5).join(', ')}`);
    console.log('========================\n');
    
  } catch (error) {
    console.error('Error checking Teams:', error.message);
  } finally {
    await browser.close();
  }
}

checkTeams();
