# moriowen.github.io

Personal site. Astro, static, zero JavaScript shipped to the browser.

## Editing

Almost everything lives in one file: `src/data/site.ts`. Bio, experience, publications,
projects, skills, awards, links. Change it there and the page updates.

Layout is `src/pages/index.astro`, styling is `src/styles/global.css` (one file, CSS
variables at the top for the palette, light and dark).

## Running it

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # -> dist/
npm run preview  # serve the built output
```

## Deploying

Push to `main`. The workflow in `.github/workflows/deploy.yml` builds and publishes.

One-time setup on GitHub: **Settings > Pages > Build and deployment > Source: GitHub Actions**.

Because the repo is named `moriowen.github.io`, it serves at the root:
<https://moriowen.github.io>.

## Still to fill in

- Google Scholar link (`links` in `src/data/site.ts`, commented out)
- `public/resume.pdf` and the resume link (commented out)
- `href` on publications and projects, currently empty strings so nothing renders as a link
