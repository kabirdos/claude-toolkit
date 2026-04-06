---
name: vercel-preview-auth
description: Configure Supabase Auth to work with Vercel preview deployments by adding wildcard redirect URLs. Use when setting up a new project with Supabase + Vercel, when OAuth login on Vercel preview URLs redirects to production instead of the preview, or when the user mentions "preview auth", "OAuth preview", "Vercel preview login broken", or "sign in redirects to production". Triggers on setup of Supabase auth with Vercel, or when preview deployment auth is broken.
---

# Vercel Preview Auth Setup

Configure Supabase to accept OAuth callbacks from all Vercel preview deployments using a wildcard redirect URL.

## Steps

### 1. Find the Vercel team slug

```bash
gh api repos/{owner}/{repo}/deployments --jq '.[0].id' | xargs -I{} gh api repos/{owner}/{repo}/deployments/{}/statuses --jq '.[0].target_url'
```

Extract the team slug from the URL: `https://{app}-{hash}-{TEAM-SLUG}.vercel.app`. The team slug is stable across all projects (e.g., `craigs-projects-1c8806a8`).

### 2. Add wildcard to supabase/config.toml

In `[auth]`, add `https://*-{TEAM-SLUG}.vercel.app/**` to `additional_redirect_urls`:

```toml
additional_redirect_urls = ["http://localhost:3000", "https://myapp.com/auth/callback", "https://*-craigs-projects-1c8806a8.vercel.app/**"]
```

### 3. Push to remote

```bash
npx supabase projects list  # find linked project ref
echo "Y" | npx supabase config push --project-ref {ref}
```

Confirm the diff shows only the redirect URL change.

### 4. Verify code uses dynamic origin

Ensure `signInWithOAuth` uses `window.location.origin`, not a hardcoded URL:

```tsx
// Correct
redirectTo: `${window.location.origin}/auth/callback`;
```

## Notes

- Supabase uses glob syntax (`*` = one segment, `**` = any depth), not regex
- No OAuth provider (Google Console, etc.) changes needed — Supabase validates redirects
- One-time setup per Supabase project; the Vercel team slug is shared across all projects
