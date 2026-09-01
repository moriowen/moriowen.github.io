import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Every section shares one shape, so adding a section is copy-paste.
// - title    : entry heading, links through to the detail page
// - subtitle : the line under it (employer, authors, degree)
// - meta     : right-aligned on the overview (dates, venue, stack)
// - summary  : one paragraph shown on the overview and section index
// - bullets  : optional resume-style points shown on the overview
// - external : optional off-site link (paper PDF, repo, live demo)
// - order    : lower sorts first
const entry = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  meta: z.string().optional(),
  summary: z.string().optional(),
  bullets: z.array(z.string()).default([]),
  // Multiple stints at one employer: the company is the entry, roles nest under it.
  roles: z
    .array(
      z.object({
        title: z.string(),
        when: z.string().optional(),
        where: z.string().optional(),
        kind: z.string().optional(),
        bullets: z.array(z.string()).default([]),
      })
    )
    .default([]),
  external: z.array(z.object({ label: z.string(), href: z.string().url() })).default([]),
  order: z.number().default(99),
  draft: z.boolean().default(false),
});

const section = (dir: string) =>
  defineCollection({
    loader: glob({ pattern: '**/*.md', base: `./src/content/${dir}` }),
    schema: entry,
  });

export const collections = {
  experience: section('experience'),
  publications: section('publications'),
  projects: section('projects'),
  education: section('education'),
  awards: section('awards'),
  pages: defineCollection({
    loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
    schema: z.object({ title: z.string(), description: z.string().optional() }),
  }),
};
