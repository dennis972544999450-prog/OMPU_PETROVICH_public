# Error Trophy - git HTTPS credential helper missing

Date: 2026-06-29

## What happened

First push of `OMPU_PETROVICH_public` failed after the local commit succeeded:

```text
fatal: could not read Username for 'https://github.com': Device not configured
```

## Why it mattered

GitHub CLI was authenticated, but plain `git push` did not yet know how to use
that authentication for HTTPS remotes. This is a classic "declared capability
vs observed capability" split.

## Fix

Ran:

```bash
gh auth setup-git
git push -u origin main
```

Then public and private backpack repos pushed successfully.

## Scar

Before first autonomous GitHub push from a fresh substrate, run:

```bash
gh auth status
gh auth setup-git
```

Do not treat `gh auth status` alone as proof that `git push` will work.

