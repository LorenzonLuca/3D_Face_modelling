import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		https: {
			key: './../3dfacemodelling-privateKey.key',
			cert: './../3dfacemodelling.crt',
		}
	},
	plugins: [sveltekit(), purgeCss()]
});