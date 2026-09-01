// Order here is the order sections appear on the overview page.
export const sections = [
  {
    slug: 'experience',
    title: 'Experience',
    blurb: 'Where I have worked and what I actually built there.',
  },
  {
    slug: 'publications',
    title: 'Publications',
    blurb:
      'Four undergraduate papers. The arc runs from detecting a license plate in a single frame, ' +
      'through surveying how vehicles perceive the world, to asking a long surveillance video a ' +
      'question in plain English.',
  },
  {
    slug: 'projects',
    title: 'Projects',
    blurb: 'Things built outside of work, usually because something was annoying.',
  },
  {
    slug: 'education',
    title: 'Education',
    blurb: 'Degrees, coursework, and what I went there to learn.',
  },
  {
    slug: 'awards',
    title: 'Awards',
    blurb: 'Hackathons and competitions.',
  },
] as const;

export type SectionSlug = (typeof sections)[number]['slug'];

export const sectionBySlug = Object.fromEntries(sections.map((s) => [s.slug, s]));
