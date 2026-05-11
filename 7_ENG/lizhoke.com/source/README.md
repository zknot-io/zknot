# lizhoke.com

Single-page site for Liz Hoke Photography. Static HTML/CSS/JS — deployed via GitHub → Cloudflare Pages.

## Tech

- HTML / CSS / vanilla JS (no build step, no framework)
- Cloudflare Pages (free, auto-deploys from `main` branch)
- Stripe + Cal.com for booking + payment (external embeds)

## Local preview

Just open `public/index.html` in a browser. Or, for a proper local server:

```bash
cd public
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Photos

Drop the 10 photos into `public/images/` named:
- `01.jpg` through `10.jpg` (gallery, in priority order — 01 is the best)
- `hero.jpg` (the #1 ranked photo, used full-bleed at the top)
- `liz.jpg` (portrait of Liz for the About section)
- `og-image.jpg` (1200x630, used for link previews on social)

The CSS already references these filenames — no code changes needed once they're in place.

## Other placeholders

Search `index.html` for these tags:

| Tag | What goes there |
|---|---|
| `LOGO_PLACEHOLDER` | Logo SVG/PNG in `public/images/logo.svg`, then update the nav |
| `BIO_PLACEHOLDER` | Liz's bio text |
| `INSTAGRAM/TIKTOK_EMBED_PLACEHOLDER` | Real handles linked |
| `CALENDAR_EMBED_PLACEHOLDER` | Cal.com embed snippet |
| `PHONE_PLACEHOLDER` | Phone number in JSON-LD schema |
| `[X] days` | Real turnaround time |
| Testimonials | 3 placeholder blockquotes |

## Deploy

Auto-deploys via Cloudflare Pages whenever you push to `main`. Build settings:
- Framework: None
- Build command: *(empty)*
- Output directory: `public`

## Update workflow

```bash
git add .
git commit -m "describe what you changed"
git push
```

Live site updates in ~30 seconds.
