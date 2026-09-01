# moriowen.github.io

Personal site. Astro, static, zero JavaScript shipped to the browser.

## Editing

Content lives in Markdown, one file per entry, under `src/content/`:

```
src/content/
  experience/*.md     projects/*.md      awards/*.md
  publications/*.md   education/*.md     pages/about.md
```

Frontmatter drives the resume-style overview on `/`. The Markdown body below it is the detailed
writeup, shown on that entry's own page. Every entry file currently has `TODO` headings sketching
what belongs there.

Frontmatter fields (all optional except `title`):

| field | shows up as |
|---|---|
| `title` | entry heading, links to the detail page |
| `subtitle` | line under the title (employer, authors, degree) |
| `meta` | right-aligned (dates, venue, stack) |
| `summary` | one paragraph on the overview and section index |
| `bullets` | resume-style points on the overview, used instead of `summary` |
| `external` | off-site links on the detail page: `[{label, href}]` |
| `order` | lower sorts first |
| `draft` | `true` hides it everywhere |

## Routes

| path | what |
|---|---|
| `/` | resume-style overview, every section and entry clickable |
| `/about/` | long-form bio, from `src/content/pages/about.md` |
| `/<section>/` | section index with summaries |
| `/<section>/<slug>/` | the full writeup |

Sections and their order are `src/data/sections.ts`. To add one: add it there, make the matching
folder under `src/content/`, and register it in `src/content.config.ts`. Routes generate themselves.

Site title, tagline, links, skills, and the short intro are `src/data/site.ts`.
Styling is one file, `src/styles/global.css`, with the palette as CSS variables at the top.

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
- `external` links on each entry (paper PDFs, repos, live demos), currently empty
- The `TODO` sections inside every file under `src/content/`
