# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Atharva Mohite's personal site: Astro 5, fully static, no client JavaScript, no UI framework. There
are no tests, no linter, and no formatter configured. `npm run build` is the only check — it type
checks the content collections against `src/content.config.ts`, so a bad frontmatter field fails the
build.

```sh
npm run dev      # http://localhost:4321
npm run build    # -> dist/ (also the only validation step)
npm run preview  # serve the built output
```

Deploy: push to `main`. `.github/workflows/deploy.yml` builds with `withastro/action` and publishes
to GitHub Pages. `dist/` is gitignored and never committed.

## Architecture

The whole site is generated from two data files plus Markdown. Nothing is hand-routed.

`src/data/sections.ts` is the spine. It lists the sections in the order they appear on the overview
page, and everything downstream reads from it:

- `src/pages/index.astro` renders one `Section` per entry in that array.
- `src/pages/[section]/index.astro` and `[slug].astro` build their `getStaticPaths` from it, so all
  section index and detail routes appear automatically.
- `src/components/Nav.astro` builds the sticky nav from it. On `/` the links are in-page anchors
  (`#projects`); everywhere else they point at the real pages (`/projects/`). One component, both
  behaviors, keyed off `Astro.url.pathname === '/'`.

Adding a section takes three edits: `src/data/sections.ts`, a folder under `src/content/`, and a
line in `src/content.config.ts`. Routes, nav, and the overview follow.

Every section shares one Zod schema in `src/content.config.ts` (`title`, `subtitle`, `meta`,
`summary`, `bullets`, `roles`, `external`, `order`, `draft`), which is why sections are
copy-paste to add. `order` sorts ascending within a section; `draft: true` hides an entry
everywhere. `external[].href` is validated: absolute URL or site-root path only.

Each Markdown file is two things at once. The frontmatter feeds the resume-style summary shown on
`/` and on the section index; the Markdown body is the long writeup shown only on that entry's own
page. Most entry bodies still carry `TODO` headings sketching what belongs there — those are the
author's own placeholders, not defects to silently fill in.

`src/components/Entry.astro` renders one entry on both the overview and the section index. Its
`dense` prop is what differentiates them: dense drops bullets and role detail so the section index
stays a summary. `roles` exists for one employer with several stints.

Other pieces: `src/data/site.ts` (name, description, header links, tagline), `src/layouts/Base.astro`
(head, meta, and the `Nav`), `src/styles/global.css` (the only stylesheet, palette as CSS variables
at the top, inlined at build time via `inlineStylesheets: 'always'`).

`notes/` is version-controlled reference material behind the resume and research writeups. Astro
publishes only `src/pages/` and `public/`, so it is never served. `notes/research-source-review.md`
is the source of truth for what the papers actually claim; the publication entries derive from it.

## Content conventions

Prose on this site is dry, specific, and first-person. Claims are numbers the author can defend. Do
not add a fact, number, or stack detail that is not confirmed — an unverified stack in `meta` or an
invented metric in a bullet is worse than leaving it out.

The nav has no About item; `/about/` still builds and is reachable directly.

`README.md` documents the same structure for a human reader, but it has drifted: it mentions an
`awards/` collection that no longer exists, and its "Still to fill in" list is partly stale. Trust
the code over the README where they disagree.

---

An OpenAI Codex config exists at `~/.codex/config.toml`. To pull anything from it into Claude Code
(MCP servers, slash commands, subagents, skills, instructions), reply `/import` to scan and list
what's importable, then `/import --yes=<digest>` with the digest the scan prints. If `/import`
isn't available on this surface, run `claude import` from a terminal.
