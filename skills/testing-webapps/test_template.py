#!/usr/bin/env python3
"""
Template Playwright test - copy and modify for your needs.

Usage:
    python test_template.py [--headed] [--slow]
    
Arguments:
    --headed    Run with visible browser window
    --slow      Add delays between actions (useful for debugging)
"""

import argparse
import sys
from playwright.sync_api import sync_playwright, expect, Page


# ============================================================================
# Configuration - Modify these for your project
# ============================================================================

BASE_URL = 'http://localhost:3000'
DEFAULT_TIMEOUT = 30000  # 30 seconds


# ============================================================================
# Test Helpers - Add reusable functions here
# ============================================================================

def login(page: Page, email: str, password: str):
    """Helper to log in a user."""
    page.goto(f'{BASE_URL}/login')
    page.fill('[name="email"]', email)
    page.fill('[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_url('**/dashboard')


def take_screenshot_on_failure(page: Page, name: str):
    """Capture screenshot for debugging."""
    page.screenshot(path=f'screenshots/{name}.png', full_page=True)


# ============================================================================
# Tests - Add your test functions here
# ============================================================================

def test_homepage_loads(page: Page) -> bool:
    """Test that the homepage loads correctly."""
    print("  Testing: Homepage loads...")
    
    page.goto(BASE_URL)
    
    # Check page title
    expect(page).to_have_title_containing('My App')
    
    # Check main heading exists
    expect(page.locator('h1')).to_be_visible()
    
    # Check navigation is present
    expect(page.locator('nav')).to_be_visible()
    
    print("  ✅ Homepage loads correctly")
    return True


def test_navigation_works(page: Page) -> bool:
    """Test that navigation links work."""
    print("  Testing: Navigation...")
    
    page.goto(BASE_URL)
    
    # Click on About link
    page.click('a:has-text("About")')
    expect(page).to_have_url_matching('.*about.*')
    
    # Click on Contact link
    page.click('a:has-text("Contact")')
    expect(page).to_have_url_matching('.*contact.*')
    
    print("  ✅ Navigation works correctly")
    return True


def test_form_validation(page: Page) -> bool:
    """Test form validation behavior."""
    print("  Testing: Form validation...")
    
    page.goto(f'{BASE_URL}/contact')
    
    # Submit empty form
    page.click('button[type="submit"]')
    
    # Check for validation errors
    expect(page.locator('.error-message')).to_be_visible()
    
    # Fill in required fields
    page.fill('[name="name"]', 'Test User')
    page.fill('[name="email"]', 'test@example.com')
    page.fill('[name="message"]', 'This is a test message')
    
    # Submit should work now
    page.click('button[type="submit"]')
    expect(page.locator('.success-message')).to_be_visible()
    
    print("  ✅ Form validation works correctly")
    return True


def test_responsive_layout(page: Page) -> bool:
    """Test responsive design at different viewport sizes."""
    print("  Testing: Responsive layout...")
    
    page.goto(BASE_URL)
    
    # Desktop
    page.set_viewport_size({'width': 1280, 'height': 720})
    expect(page.locator('.desktop-nav')).to_be_visible()
    
    # Tablet
    page.set_viewport_size({'width': 768, 'height': 1024})
    # Adjust expectations for tablet...
    
    # Mobile
    page.set_viewport_size({'width': 375, 'height': 667})
    expect(page.locator('.mobile-menu-button')).to_be_visible()
    
    print("  ✅ Responsive layout works correctly")
    return True


# ============================================================================
# Test Runner
# ============================================================================

def run_all_tests(headed: bool = False, slow: bool = False) -> bool:
    """Run all tests and return overall success status."""
    
    tests = [
        test_homepage_loads,
        test_navigation_works,
        # test_form_validation,  # Uncomment when ready
        # test_responsive_layout,  # Uncomment when ready
    ]
    
    passed = 0
    failed = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not headed,
            slow_mo=500 if slow else 0
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        context.set_default_timeout(DEFAULT_TIMEOUT)
        page = context.new_page()
        
        print(f"\n🧪 Running {len(tests)} tests...\n")
        
        for test_fn in tests:
            try:
                test_fn(page)
                passed += 1
            except Exception as e:
                print(f"  ❌ {test_fn.__name__} failed: {e}")
                take_screenshot_on_failure(page, test_fn.__name__)
                failed += 1
        
        browser.close()
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description='Run Playwright tests')
    parser.add_argument('--headed', action='store_true', help='Run with visible browser')
    parser.add_argument('--slow', action='store_true', help='Run slowly for debugging')
    args = parser.parse_args()
    
    # Create screenshots directory
    import os
    os.makedirs('screenshots', exist_ok=True)
    
    success = run_all_tests(headed=args.headed, slow=args.slow)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
