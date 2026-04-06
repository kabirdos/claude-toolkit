# Playwright MCP Patterns

## Navigation

```
browser_navigate(url: "https://example.com/page")
```

## Get Element Refs

Always snapshot before interacting — refs change on every page update:

```
browser_snapshot()  # Returns YAML with ref=eNN for each element
```

## Clicking

```
browser_click(ref: "e42", element: "Submit button")
```

## Filling Forms

Multiple fields at once:

```
browser_fill_form(fields: [
  { name: "Email", type: "textbox", ref: "e10", value: "test@example.com" },
  { name: "State", type: "combobox", ref: "e20", value: "CA" },
  { name: "Agree", type: "checkbox", ref: "e30", value: "true" }
])
```

## Typing Text

```
browser_type(ref: "e15", text: "Hello world", element: "Chat input")
browser_type(ref: "e15", text: "Hello", submit: true)  # Press Enter after
```

## File Upload

Click the upload button first to trigger file chooser, then:

```
browser_file_upload(paths: ["/absolute/path/to/file.pdf"])
```

## Waiting

```
browser_wait_for(text: "Success")           # Wait for text to appear
browser_wait_for(textGone: "Loading...")     # Wait for text to disappear
browser_wait_for(time: 5)                   # Wait N seconds
```

Default timeout is 5s. For longer operations (AI responses, deployments), use `time`.

## Screenshots

```
browser_take_screenshot(type: "png", filename: "qa-results/flow1-step3.png")
browser_take_screenshot(type: "png", fullPage: true, filename: "qa-results/full-page.png")
browser_take_screenshot(type: "png", ref: "e50", element: "Card component", filename: "qa-results/card.png")
```

## Tips

- **Stale refs**: After any click, form fill, or navigation, snapshot again before the next interaction
- **Async content**: AI responses, API calls, and redirects need `wait_for` — don't assume instant
- **Dialogs**: AlertDialogs appear in snapshot as `alertdialog` with their own refs
- **Iframes**: Stripe Checkout and other iframes have refs prefixed with `f` (e.g. `f19e8`)
- **Downloads**: File downloads appear in snapshot Events section
- **Console errors**: Check snapshot for `Console: N errors` to catch runtime issues
- **Modal state**: File choosers appear as `[File chooser]` in snapshot
