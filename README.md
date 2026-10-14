# My VR Media Player — Website

[![Deploy to GitHub Pages](https://github.com/solusvoidofficial/MyVRMediaPlayer/actions/workflows/pages.yml/badge.svg)](https://github.com/solusvoidofficial/MyVRMediaPlayer/actions/workflows/pages.yml)

Public website for **My VR Media Player** (`com.solusvoid.myvrplayer`) by **SolusVoid** — an offline-first local VR video player for Android.

**Live site:** https://solusvoidofficial.github.io/MyVRMediaPlayer/

## Contents

| Public URL | File |
|---|---|
| `/` | `index.html` (home) |
| `/privacy/` (canonical, for Play Console) | `privacy/index.html` |
| `/privacy.html` (alias redirect) | `privacy.html` |
| `/terms/` (Terms of Use, for in-app Legal) | `terms/index.html` |
| `/licenses/` (open-source attribution) | `licenses/index.html` |
| `/app-ads.txt` | `app-ads.txt` (placeholder pub-ID) |
| `/robots.txt` | `robots.txt` |
| `/404.html` | `404.html` |

## Local preview

No build step — pure static HTML/CSS/SVG.

```powershell
python -m http.server 8080
# open http://localhost:8080/
```

## Deployment

Auto-deploy to GitHub Pages on every push to `main` via `.github/workflows/pages.yml` (official `deploy-pages` action, artifact path `.`).

One-time repo setting: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Notes

- `.nojekyll` must stay (empty) so Pages serves files as-is (`app-ads.txt` as `text/plain`).
- All inter-page links are **relative** (`./`, `../`), so moving to a custom domain later needs 0 HTML edits.
- `app-ads.txt` is still `pub-XXXXXXXXXXXXXXXX` (placeholder). To go live: replace with the real AdMob publisher ID, push, wait ±24h for crawl, then verify:
  `curl -I https://solusvoidofficial.github.io/MyVRMediaPlayer/app-ads.txt` → `200` + `content-type: text/plain`.
- Canonical URLs for store listings:
  - Privacy Policy (Play Console): `/privacy/`
  - Terms (in-app Legal): `/terms/`
  - Licenses: `/licenses/`

## Contact

Developer: **SolusVoid** — solusvoidofficial@gmail.com
App: My VR Media Player, package `com.solusvoid.myvrplayer`, Android 7.0+.

© 2026 SolusVoid. Site content and artwork all rights reserved.
