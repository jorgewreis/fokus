import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { pageKind, motionAllowed, GUARD_SELECTOR } from '../../resources/js/marketing-motion.js';

const pages = [
    ['public/index.html', 'home'],
    ['public/marketing/products/index.html', 'portfolio'],
    ['public/marketing/products/fokus-styles.html', 'styles'],
    ['public/marketing/products/fokus-law.html', 'law'],
    ['public/marketing/products/fokus-law-planos.html', 'law-plans'],
    ['public/marketing/products/fokus-law-sob-medida.html', 'law-custom'],
    ['public/marketing/products/fokus-lead.html', 'lead'],
    ['public/marketing/products/fokus-lead-planos.html', 'lead-plans'],
    ['public/marketing/privacy.html', 'legal'],
    ['public/marketing/terms.html', 'legal'],
];

test('as dez páginas públicas carregam o movimento da mesma origem', async () => {
    for (const [file] of pages) {
        const html = await readFile(new URL(`../../${file}`, import.meta.url), 'utf8');
        assert.match(html, /\/marketing\/motion\.css/);
        assert.match(html, /\/marketing\/motion\.js/);
        assert.doesNotMatch(html, /cdn\.|unpkg|jsdelivr|lenis\.js|gsap\.min/);
    }
});

test('o Fokus Law não carrega mais o movimento antigo', async () => {
    const html = await readFile(new URL('../../public/marketing/products/fokus-law.html', import.meta.url), 'utf8');
    assert.doesNotMatch(html, /law-story-motion\.js/);
    const plans = await readFile(new URL('../../public/marketing/products/fokus-law-plans.js', import.meta.url), 'utf8');
    assert.doesNotMatch(plans, /lp-reveal/);
});

test('a página some o movimento quando o visitante pede menos animação', () => {
    assert.equal(motionAllowed({ matchMedia: () => ({ matches: true }) }), false);
    assert.equal(motionAllowed({ matchMedia: () => ({ matches: false }) }), true);
});

test('cada template cai no movimento previsto', () => {
    for (const [file, kind] of pages) {
        const body = { classList: new Set(), querySelector: () => null };
        if (kind === 'home') body.classList.add('home-page');
        if (kind === 'legal') body.classList.add('legal-document-page', 'showcase-page');
        if (kind === 'law' || kind === 'law-plans' || kind === 'law-custom') body.classList.add('law-page');
        if (kind === 'law-plans') body.classList.add('law-pricing-page');
        if (kind === 'law-custom') body.classList.add('law-custom-page');
        if (kind === 'lead' || kind === 'lead-plans') body.classList.add('lead-page');
        if (kind === 'lead-plans') body.classList.add('lead-pricing-page');
        if (kind === 'portfolio') body.querySelector = (selector) => selector === '.showcase-grid';
        if (kind === 'styles') body.querySelector = (selector) => selector === '.showcase-information';
        body.classList.contains = (name) => body.classList.has(name);
        assert.equal(pageKind(body), kind, file);
    }
});

test('formulários e cartões de acesso ficam fora do scroll suave', () => {
    assert.match(GUARD_SELECTOR, /form/);
    assert.match(GUARD_SELECTOR, /\.law-login-card/);
    assert.match(GUARD_SELECTOR, /\.platform-access-card/);
    assert.match(GUARD_SELECTOR, /\.lead-interest-form/);
    assert.match(GUARD_SELECTOR, /\.lp-builder/);
});
