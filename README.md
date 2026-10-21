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

## `app-ads.txt` — dilayani dari repo LAIN (user-site)

`app-ads.txt` **tidak** dilayani dari repo ini. AdMob mencari file itu di **root hostname**
dari URL *developer website* yang terdaftar di listing Google Play, dan project-page **tidak
bisa** menyajikan file di root.

Karena itu file-nya dilayani dari repo user-site
[`solusvoidofficial/solusvoidofficial.github.io`](https://github.com/solusvoidofficial/solusvoidofficial.github.io):

```
https://solusvoidofficial.github.io/app-ads.txt
→ google.com, pub-5600327675311414, DIRECT, f08c47fec0942fa0
```

Verifikasi:

```powershell
curl -I https://solusvoidofficial.github.io/app-ads.txt   # -> 200, text/plain
```

Status: **published & live** (2026-10-21). Verifikasi app di AdMob dilakukan setelah listing
Play publik + developer website terisi (±24 jam crawl).

## CTA "Google Play"

Tombol utama di home **belum** link ke listing Play karena app masih dalam closed testing
(link ke listing yang belum ada = dead link = sinyal kualitas rendah saat review AdMob).
Saat listing sudah live, ganti `<span class="btn primary is-disabled">` di `index.html`
menjadi link ke `https://play.google.com/store/apps/details?id=com.solusvoid.myvrplayer`.

## Notes

- `.nojekyll` must stay (empty) so Pages serves files as-is.
- All inter-page links are **relative** (`./`, `../`), so moving to a custom domain later needs 0 HTML edits.
- Canonical URLs for store listings:
  - Privacy Policy (Play Console): `/privacy/`
  - Terms (in-app Legal): `/terms/`
  - Licenses: `/licenses/`

## Contact

Developer: **SolusVoid** — solusvoidofficial@gmail.com
App: My VR Media Player, package `com.solusvoid.myvrplayer`, Android 7.0+.

© 2026 SolusVoid. Site content and artwork all rights reserved.
