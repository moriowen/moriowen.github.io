// Site-wide bits that are not section content.
// Section content lives in src/content/<section>/*.md — edit the Markdown, not this file.

export const site = {
  name: 'Atharva Mohite',
  title: 'Atharva Mohite',
  tagline:
    'Software engineer. MS CS at Georgia Tech, starting Aug 2026. Distributed systems, and machine learning for video.',
  description:
    'Atharva Mohite - software engineer working on distributed systems and machine learning. MS CS student at Georgia Tech.',
  location: 'Atlanta, GA',
};

// TODO: fill in the Scholar id and drop a resume.pdf in public/, then uncomment.
export const links = [
  { label: 'Email', href: 'mailto:amohite8@gatech.edu' },
  { label: 'GitHub', href: 'https://github.com/moriowen' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/atharva-mohite/' },
  // { label: 'Scholar', href: 'https://scholar.google.com/citations?user=REPLACE_ME' },
  // { label: 'Resume', href: '/resume.pdf' },
];

// Short intro on the overview page. The long version is src/content/pages/about.md.
export const intro = [
  `I build backend systems that move a lot of money and a lot of messages. For the last three years
   that has meant trade settlement infrastructure at JP Morgan Chase. Before that, computer vision
   research on long surveillance video, which produced four papers.`,
  `In August 2026 I start an MS in Computer Science at Georgia Tech, specializing in machine
   learning.`,
];

export const skills = [
  { group: 'Languages', items: 'Java, Python, TypeScript, SQL' },
  {
    group: 'Technologies',
    items:
      'Spring Boot, Kafka, Elasticsearch, React, Next.js, Node.js, Django, Flask, Oracle, AWS, Terraform, Kubernetes, Docker, Jenkins',
  },
  {
    group: 'Other',
    items:
      'Distributed systems design, event-driven architecture, REST and GraphQL API design, CI/CD, testing, observability (Splunk, Grafana)',
  },
];

export const elsewhere =
  'Away from a keyboard: boxing, lifting, running, dancing, cooking, and writing. Collecting places to go and poems worth rereading.';
