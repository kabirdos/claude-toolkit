# CI/CD Integration Reference

How to run Playwright tests in continuous integration pipelines.

## Key Principles

CI tests must be deterministic:

- Don't depend on network latency—mock external APIs or use `waitFor` patterns
- Don't use `time.sleep()`—use explicit waits for elements/conditions
- Don't rely on database state—reset or seed data before each test
- Don't hardcode dates—mock `Date.now()` if tests depend on time

## GitHub Actions

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install playwright pytest pytest-playwright
          playwright install chromium

      - name: Start app
        run: |
          npm ci
          npm run build
          npm start &
          sleep 10

      - name: Run tests
        run: pytest tests/e2e/ --headed=false

      - name: Upload screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: failure-screenshots
          path: screenshots/
```

## Pytest Configuration

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
```

## Project Structure

```
project/
├── tests/
│   ├── e2e/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_checkout.py
│   │   └── test_dashboard.py
│   ├── visual/
│   │   └── screenshots/
│   └── fixtures/
│       └── users.json
├── playwright.config.py
└── .github/
    └── workflows/
        └── e2e-tests.yml
```

## Installation

```bash
pip install playwright pytest-playwright
playwright install  # Downloads browser binaries
```

## Running Tests

```bash
# Headless (CI)
pytest tests/e2e/

# Headed (debugging)
pytest tests/e2e/ --headed

# Single test
pytest tests/e2e/test_auth.py::test_login

# With traces
pytest tests/e2e/ --tracing=on
```
