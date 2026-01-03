# Playwright Patterns Reference

Detailed code patterns for common Playwright testing scenarios.

## Basic Test Structure

```python
#!/usr/bin/env python3
"""
Test: [Description of what this tests]
Usage: python test_[name].py [--headed]
"""

import argparse
from playwright.sync_api import sync_playwright, expect

def run_test(headed: bool = False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            page.goto('http://localhost:3000')
            expect(page.locator('h1')).to_have_text('Welcome')
            print("✅ Test passed")
            return True
        except Exception as e:
            print(f"❌ Test failed: {e}")
            page.screenshot(path='failure-screenshot.png')
            return False
        finally:
            browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--headed', action='store_true')
    args = parser.parse_args()
    exit(0 if run_test(headed=args.headed) else 1)
```

## Form Submission

```python
page.fill('[name="email"]', 'test@example.com')
page.fill('[name="password"]', 'securepassword')
page.click('button[type="submit"]')

# Wait for navigation or response
page.wait_for_url('**/dashboard')
# or
page.wait_for_selector('.success-message')
```

## Authentication Helper

```python
def login(page, email: str, password: str):
    page.goto('/login')
    page.fill('#email', email)
    page.fill('#password', password)
    page.click('button:has-text("Sign In")')
    page.wait_for_url('**/dashboard')

# Usage
login(page, 'user@example.com', 'password123')
expect(page.locator('.user-greeting')).to_contain_text('Welcome')
```

## Screenshot Comparison

```python
# Full page
page.screenshot(path='screenshots/homepage.png', full_page=True)

# Specific element
header = page.locator('header')
header.screenshot(path='screenshots/header.png')
```

## Network Interception

```python
def handle_route(route):
    route.fulfill(
        status=200,
        content_type='application/json',
        body='{"user": {"name": "Test User"}}'
    )

page.route('**/api/user', handle_route)
```

## Performance Testing

```python
def test_page_load_performance():
    page.goto(BASE_URL)

    timing = page.evaluate('''() => {
        const t = performance.timing;
        return {
            dns: t.domainLookupEnd - t.domainLookupStart,
            connection: t.connectEnd - t.connectStart,
            ttfb: t.responseStart - t.requestStart,
            domLoad: t.domContentLoadedEventEnd - t.navigationStart,
            fullLoad: t.loadEventEnd - t.navigationStart
        };
    }''')

    assert timing['ttfb'] < 200, f"TTFB too slow: {timing['ttfb']}ms"
    assert timing['domLoad'] < 1000, f"DOM load too slow: {timing['domLoad']}ms"
```

## Network Throttling

```python
# Simulate slow 3G
client = page.context.new_cdp_session(page)
client.send('Network.emulateNetworkConditions', {
    'offline': False,
    'downloadThroughput': 500 * 1024 / 8,  # 500 kbps
    'uploadThroughput': 500 * 1024 / 8,
    'latency': 400  # 400ms RTT
})
```

## Mobile Viewport

```python
context = browser.new_context(
    viewport={'width': 390, 'height': 844},
    device_scale_factor=3,
    is_mobile=True,
    has_touch=True
)
```

## Debugging with Traces

```python
context.tracing.start(screenshots=True, snapshots=True)
# ... run test ...
context.tracing.stop(path='trace.zip')
# View: playwright show-trace trace.zip
```

## Server Lifecycle Management

Use [with_server.py](with_server.py) for tests that need a dev server:

```bash
python with_server.py "npm run dev" --port 3000 --test "python test_app.py"
```

Or inline:

```python
import subprocess
import time
import signal
import os
import socket

class ServerManager:
    def __init__(self, command: str, port: int, cwd: str = '.'):
        self.command = command
        self.port = port
        self.cwd = cwd
        self.process = None

    def start(self, timeout: int = 30):
        self.process = subprocess.Popen(
            self.command, shell=True, cwd=self.cwd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', self.port))
                sock.close()
                return True
            except:
                time.sleep(0.5)
        raise TimeoutError(f"Server didn't start within {timeout}s")

    def stop(self):
        if self.process:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
```
