// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://moriowen.github.io',
  build: { inlineStylesheets: 'always' },
  compressHTML: true,
});
