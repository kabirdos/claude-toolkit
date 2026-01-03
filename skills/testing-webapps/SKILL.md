---
name: testing-webapps
description: "Test web applications using the optimal approach for each situation. Routes between Claude for Chrome (visual verification, interactive debugging, exploratory testing) and Playwright scripts (repeatable tests, CI/CD, cross-browser, headless automation). Use when testing frontend functionality, verifying UI behavior, debugging issues, or creating automated test suites."
---

# Web Application Testing

Choose the right tool for each testing scenario: **Claude for Chrome** (interactive browser agent) or **Playwright** (programmatic automation).

## Quick Decision

| Scenario                | Tool       | Why                    |
| ----------------------- | ---------- | ---------------------- |
| "Does this look right?" | Chrome     | Visual judgment needed |
| "Check console errors"  | Chrome     | Live debugging         |
| "Run on every PR"       | Playwright | CI/CD integration      |
| "Test Safari + Firefox" | Playwright | Cross-browser          |
| "Compare to Figma"      | Chrome     | Visual comparison      |
| "Why is this broken?"   | Chrome     | Interactive debugging  |
| "Performance testing"   | Playwright | Precise measurements   |

## Decision Framework

### Use Claude for Chrome when:

- Visual verification: "Does this look right?" / "Compare to design"
- Live debugging: "What's in the console?" / "Debug this"
- Exploratory testing: "Show me what happens when..."
- Requirements are fuzzy and you need to discover what "working" means
- You need human judgment (UX feel, visual polish)

### Use Playwright when:

- Regression testing: "Create a test I can run repeatedly"
- CI/CD: "Add to CI/CD" / "Run on every commit"
- Cross-browser: "Test across browsers"
- Headless execution: "Run without UI"
- Deterministic pass/fail assertions needed
- Performance or load testing required

### The Core Distinction

- **Chrome**: Best when judgment calls matter
- **Playwright**: Best when you need deterministic assertions

## When to Switch Tools

**Chrome → Playwright** (Codify what works)

- Flow works manually → Write Playwright test to lock it in
- Discovered edge cases → Add as Playwright assertions

**Playwright → Chrome** (Debug what fails)

- Test fails unexpectedly → Use Chrome to visually inspect
- Flaky behavior → Use Chrome's console to identify timing issues

## Claude for Chrome Usage

### Invoking Chrome Testing

1. **If using Claude Desktop with Chrome connector:**
   - Tests can be initiated directly from the conversation
   - Claude will control the browser automatically

2. **If using the Chrome extension directly:**
   - Open the Claude side panel in Chrome
   - Navigate to the target URL
   - Describe what to test

### Example Chrome Prompts

- "Navigate to localhost:3000 and verify the login form matches our Figma design"
- "Check if there are any console errors on the checkout page"
- "Test the signup flow and tell me if any steps feel broken"

## Playwright Usage

### Ready-to-Use Scripts

- **[test_template.py](test_template.py)** - Copy and modify for your tests
- **[with_server.py](with_server.py)** - Start dev server, run tests, cleanup automatically

### Quick Start

```bash
# Install
pip install playwright pytest-playwright
playwright install

# Run tests
python test_template.py --headed  # With visible browser
python test_template.py           # Headless
```

### Using with_server.py

```bash
# Start server and run tests
python with_server.py "npm run dev" --port 3000 --test "python test_app.py"

# With health check URL
python with_server.py "npm start" --port 8080 --url http://localhost:8080/health --test "pytest tests/"
```

### Basic Test Pattern

```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto('http://localhost:3000')
    expect(page.locator('h1')).to_have_text('Welcome')
    expect(page.locator('[data-testid="login-btn"]')).to_be_visible()

    browser.close()
```

## Hybrid Workflow: Build-Test-Verify

### 1. Build (Claude Code)

Write code in your terminal.

### 2. Test Interactively (Chrome)

- Visually verify implementation
- Check console for errors
- Explore edge cases

### 3. Codify (Playwright)

Create tests to lock in working behavior and prevent regressions.

### 4. Debug Regressions (Chrome)

When Playwright tests fail, use Chrome to visually inspect and identify root cause.

## Real-World Example: Fixing a Checkout Bug

**Step 1: Exploratory Testing (Chrome)**

> "Test the checkout flow on localhost:3000"

Discovery: Order confirmation sometimes doesn't appear.

**Step 2: Debug (Chrome)**

> "Check console for errors when I click Submit"

Root cause: `TypeError: Cannot read 'orderId' of undefined` - race condition.

**Step 3: Write Regression Test (Playwright)**

```python
def test_checkout_confirmation_displays():
    page.goto('/products')
    page.click('[data-testid="add-to-cart"]')
    page.click('[data-testid="checkout"]')
    page.fill('#card-number', '4242424242424242')
    page.click('button:has-text("Pay Now")')

    expect(page.locator('.order-confirmation')).to_be_visible(timeout=10000)
```

**Step 4: Fix the Code**

```javascript
// Before: submitPayment().then(() => setShowConfirmation(true));
// After:
const order = await submitPayment();
setOrderId(order.id);
setShowConfirmation(true);
```

**Step 5: Test passes in CI** - bug can never return.

## Reference Documentation

For detailed patterns, see:

- [playwright-patterns.md](playwright-patterns.md) - Form handling, auth, screenshots, network mocking, performance testing
- [ci-cd-integration.md](ci-cd-integration.md) - GitHub Actions, project structure, pytest configuration

## Debugging Failed Tests

### With Playwright

```python
# Enable tracing
context.tracing.start(screenshots=True, snapshots=True)
# ... run test ...
context.tracing.stop(path='trace.zip')
# View: playwright show-trace trace.zip
```

### With Chrome

1. Run failing test with `--headed`
2. Pause at failure point
3. Open Claude in Chrome side panel
4. Ask: "What's wrong with this page? Check console for errors."
