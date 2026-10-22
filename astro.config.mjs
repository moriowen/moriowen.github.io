// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://moriowen.github.io',
  build: { inlineStylesheets: 'always' },
  compressHTML: true,
  redirects: { '/projects/kv-cache-reuse': '/projects/splice' },
  integrations: [sitemap({ filter: (page) => !page.includes('/404') && !page.includes('/kv-cache-reuse') })],
});
