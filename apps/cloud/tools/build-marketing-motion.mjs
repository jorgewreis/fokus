import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'vite';

const root = fileURLToPath(new URL('..', import.meta.url));

await build({
    root,
    configFile: false,
    publicDir: false,
    logLevel: 'warn',
    build: {
        outDir: path.join(root, 'public/marketing'),
        emptyOutDir: false,
        cssCodeSplit: false,
        lib: {
            entry: path.join(root, 'resources/js/marketing-motion.js'),
            name: 'FokusMarketingMotion',
            formats: ['iife'],
            fileName: () => 'motion.js',
        },
        rollupOptions: {
            output: {
                inlineDynamicImports: true,
            },
        },
    },
});
