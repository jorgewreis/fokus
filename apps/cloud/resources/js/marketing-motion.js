import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);

export const GUARD_SELECTOR = [
    'form',
    '.platform-access-card',
    '.law-login-card',
    '.lead-login',
    '.lead-login-float',
    '.lp-builder',
    '.lp-summary',
    '.lp-proposal',
    '.lead-builder',
    '.lead-plan-summary',
    '.law-interest-form',
    '.lead-interest-form',
].join(',');

export function motionAllowed(win = globalThis) {
    return !win.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function pageKind(body) {
    const classes = body.classList;
    if (classes.contains('home-page')) return 'home';
    if (classes.contains('legal-document-page')) return 'legal';
    if (classes.contains('law-pricing-page')) return 'law-plans';
    if (classes.contains('law-custom-page')) return 'law-custom';
    if (classes.contains('law-page')) return 'law';
    if (classes.contains('lead-pricing-page')) return 'lead-plans';
    if (classes.contains('lead-page')) return 'lead';
    if (body.querySelector('.showcase-grid')) return 'portfolio';
    if (body.querySelector('.showcase-information')) return 'styles';
    return 'other';
}

export function markScrollGuards(root, selector = GUARD_SELECTOR) {
    root.querySelectorAll(selector).forEach((element) => {
        element.setAttribute('data-lenis-prevent', '');
    });
}

function splitWords(element) {
    if (!element || element.dataset.motionWords === '1') return [];
    element.dataset.motionWords = '1';
    const pieces = [];
    for (const node of [...element.childNodes]) {
        if (node.nodeType === Node.TEXT_NODE) {
            const fragment = document.createDocumentFragment();
            for (const part of node.textContent.split(/(\s+)/)) {
                if (!part) continue;
                if (/^\s+$/.test(part)) {
                    fragment.append(part);
                    continue;
                }
                const span = document.createElement('span');
                span.className = 'motion-word';
                span.textContent = part;
                fragment.append(span);
                pieces.push(span);
            }
            node.replaceWith(fragment);
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            node.classList.add('motion-word');
            pieces.push(node);
        }
    }
    return pieces;
}

function resolveTarget(target) {
    if (typeof target === 'string') return document.querySelector(target);
    return target || null;
}

function inView(element) {
    const node = resolveTarget(element);
    if (!node) return false;
    const box = node.getBoundingClientRect();
    return box.top < window.innerHeight * 0.9 && box.bottom > 0;
}

function reveal(targets, { trigger, y = 28, stagger = 0.08, start = 'top 86%' } = {}) {
    const list = gsap.utils.toArray(targets).filter(Boolean);
    if (!list.length) return;
    const origin = resolveTarget(trigger) || list[0];
    const vars = { y, opacity: 0, duration: 0.7, ease: 'power2.out', stagger };
    if (inView(origin)) {
        gsap.from(list, vars);
        return;
    }
    gsap.from(list, {
        ...vars,
        scrollTrigger: { trigger: origin, start, once: true },
    });
}

function revealWords(element, position = 0, timeline = null) {
    const pieces = splitWords(element);
    if (!pieces.length) return;
    const vars = { y: 22, duration: 0.72, stagger: 0.03, ease: 'power3.out' };
    if (timeline) timeline.from(pieces, vars, position);
    else gsap.from(pieces, vars);
}

function liftBackground(element) {
    const computed = getComputedStyle(element);
    if (!computed.backgroundImage || computed.backgroundImage === 'none') return null;
    const media = document.createElement('div');
    media.className = 'motion-hero-media';
    media.setAttribute('aria-hidden', 'true');
    media.style.backgroundImage = computed.backgroundImage;
    media.style.backgroundSize = computed.backgroundSize;
    media.style.backgroundPosition = computed.backgroundPosition;
    media.style.backgroundRepeat = computed.backgroundRepeat;
    element.prepend(media);
    element.style.backgroundImage = 'none';
    gsap.fromTo(media, { y: -16 }, {
        y: 16,
        ease: 'none',
        scrollTrigger: { trigger: element, start: 'top top', end: 'bottom top', scrub: true },
    });
    return media;
}

function watchOffers(container, selector) {
    if (!container) return;
    const paint = () => {
        const cards = [...container.querySelectorAll(selector)];
        if (!cards.length || container.dataset.motionOffers === '1') return;
        container.dataset.motionOffers = '1';
        reveal(cards, { trigger: container, stagger: 0.06 });
        ScrollTrigger.refresh();
    };
    paint();
    const observer = new MutationObserver(paint);
    observer.observe(container, { childList: true });
}

function bindAnchors(lenis, offset) {
    document.addEventListener('click', (event) => {
        const link = event.target instanceof Element ? event.target.closest('a[href^="#"]') : null;
        if (!link || event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        const id = decodeURIComponent(link.getAttribute('href').slice(1));
        if (!id) return;
        const target = document.getElementById(id);
        if (!target) return;
        event.preventDefault();
        lenis.scrollTo(target, { offset });
    }, true);
}

function bootHome() {
    const hero = document.querySelector('.immersive-hero');
    const nav = document.querySelector('.showcase-nav');
    if (hero) liftBackground(hero);
    const timeline = gsap.timeline({ defaults: { ease: 'power3.out' } });
    const kicker = document.querySelector('.immersive-hero-kicker');
    const support = document.querySelector('.immersive-hero-support');
    const action = document.querySelector('.immersive-hero-action');
    const rail = document.querySelector('.immersive-products');
    if (kicker) timeline.from(kicker, { y: 12, opacity: 0, duration: 0.45 }, 0);
    revealWords(document.getElementById('page-title'), 0.05, timeline);
    if (support) timeline.from(support, { y: 16, opacity: 0, duration: 0.5 }, 0.22);
    if (action) timeline.from(action, { y: 12, opacity: 0, duration: 0.4 }, 0.32);
    if (rail) timeline.from(rail, { y: 12, opacity: 0, duration: 0.45 }, 0.28);
    reveal('.immersive-product-story', { trigger: '.immersive-product-stories', stagger: 0.1 });
    reveal('.immersive-about-principle', { trigger: '.immersive-about-principles', stagger: 0.1 });
    reveal('#details-title, #about-title', { y: 20, stagger: 0.05 });
    return { hero, nav };
}

function bootPortfolio() {
    revealWords(document.getElementById('page-title'));
    reveal('.showcase-hero p', { trigger: '.showcase-hero', y: 16 });
    reveal('.showcase-card', { trigger: '.showcase-grid', stagger: 0.12 });
}

function bootStyles() {
    revealWords(document.querySelector('.showcase-hero h1'));
    reveal('.showcase-card-actions', { trigger: '.showcase-hero', y: 16 });
    reveal('.showcase-information h2, .showcase-information h3', { stagger: 0.08, y: 18 });
}

function bootLaw() {
    const timeline = gsap.timeline({ defaults: { ease: 'power3.out' } });
    const eyebrow = document.querySelector('.law-hero .law-eyebrow');
    const lede = document.querySelector('.law-hero-lede');
    const offer = document.querySelector('.law-hero-offer-card');
    if (eyebrow) timeline.from(eyebrow, { y: 12, opacity: 0, duration: 0.4 }, 0);
    revealWords(document.getElementById('law-title'), 0.05, timeline);
    if (lede) timeline.from(lede, { y: 16, opacity: 0, duration: 0.5 }, 0.2);
    if (offer) timeline.from(offer, { y: 16, opacity: 0, duration: 0.45 }, 0.28);
    reveal('.law-audience-card', { trigger: '.law-audience-grid', stagger: 0.1 });
    reveal('.law-contact-copy > *', { trigger: '.law-contact-section', stagger: 0.06 });
    const scene = document.querySelector('.law-contact-visual');
    if (scene) {
        gsap.to(scene.querySelector('.law-contact-number'), {
            y: -16, ease: 'none', scrollTrigger: { trigger: scene, start: 'top bottom', end: 'bottom top', scrub: true },
        });
        gsap.to(scene.querySelector('.law-contact-stamp'), {
            y: 10, ease: 'none', scrollTrigger: { trigger: scene, start: 'top bottom', end: 'bottom top', scrub: true },
        });
    }
    reveal('.law-process-section .law-section-intro, .law-process-judicial', { trigger: '.law-process-section', stagger: 0.08 });
    reveal('.law-module-card', { trigger: '.law-module-grid', stagger: 0.06 });
    reveal('.law-plan-showcase', { trigger: '.law-plans-section' });
    reveal('#custom-title', { trigger: '#sob-medida', y: 20 });
    reveal('#interest-title', { trigger: '#interesse', y: 20 });
    reveal('.law-final-cta > *', { trigger: '.law-final-cta', stagger: 0.08 });
}

function bootLawPlans() {
    revealWords(document.querySelector('.lp-hero h1'));
    reveal('.lp-hero-copy > p, .lp-module-status, .lp-hero-link', { trigger: '.lp-hero', stagger: 0.06, y: 16 });
    reveal('.lp-section-head', { y: 18 });
    watchOffers(document.getElementById('lp-offers'), '.lp-offer');
}

function bootLawCustom() {
    const hero = document.querySelector('.law-hero');
    if (hero) liftBackground(hero);
    revealWords(document.getElementById('custom-title'));
    reveal('.law-hero-lede, .law-hero-offer-button', { trigger: '.law-hero', stagger: 0.06, y: 16 });
    reveal('#custom-scope-title', { trigger: '.law-section', y: 20 });
}

function bootLead() {
    const hero = document.querySelector('.lead-hero');
    if (hero) liftBackground(hero);
    const timeline = gsap.timeline({ defaults: { ease: 'power3.out' } });
    const badge = document.querySelector('.lead-development-badge');
    const kicker = document.querySelector('.lead-hero .lead-kicker');
    const copy = document.querySelector('.lead-hero-copy');
    const action = document.querySelector('.lead-hero-offer-button');
    if (badge) timeline.from(badge, { y: 10, opacity: 0, duration: 0.35 }, 0);
    if (kicker) timeline.from(kicker, { y: 12, opacity: 0, duration: 0.4 }, 0.05);
    revealWords(document.getElementById('lead-title'), 0.08, timeline);
    if (copy) timeline.from(copy, { y: 16, opacity: 0, duration: 0.5 }, 0.24);
    if (action) timeline.from(action, { y: 12, opacity: 0, duration: 0.4 }, 0.32);
    reveal('.lead-proof span', { trigger: '.lead-proof', stagger: 0.05, y: 12 });
    reveal('.lead-step', { trigger: '.lead-workflow-grid', stagger: 0.1 });
    reveal('.lead-context-copy > *, .lead-context-board > *', { trigger: '.lead-context', stagger: 0.06 });
    reveal('.lead-module-card', { trigger: '.lead-module-grid', stagger: 0.08 });
    reveal('.lead-audience-card', { trigger: '.lead-audience-grid', stagger: 0.1 });
    reveal('.lead-catalog .lead-section-intro, .lead-catalog-banner', { trigger: '.lead-catalog', stagger: 0.08 });
    reveal('#lead-interest-title', { trigger: '#interesse', y: 20 });
}

function bootLeadPlans() {
    revealWords(document.querySelector('.lead-pricing-hero h1'));
    reveal('.lead-pricing-hero p, .lead-pricing-hero a', { trigger: '.lead-pricing-hero', stagger: 0.06, y: 16 });
    reveal('.lead-pricing-heading', { y: 18 });
    watchOffers(document.getElementById('lead-offers-grid'), '.lead-price-card');
}

const pages = {
    home: bootHome,
    portfolio: bootPortfolio,
    styles: bootStyles,
    law: bootLaw,
    'law-plans': bootLawPlans,
    'law-custom': bootLawCustom,
    lead: bootLead,
    'lead-plans': bootLeadPlans,
};

export function boot(doc = document, win = window) {
    markScrollGuards(doc);
    if (!motionAllowed(win)) return null;
    const lenis = new Lenis({
        lerp: 0.1,
        anchors: false,
        autoRaf: false,
        stopInertiaOnNavigate: true,
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
    const kind = pageKind(doc.body);
    bindAnchors(lenis, kind === 'home' ? -76 : -8);
    const started = pages[kind]?.() ?? null;
    if (kind === 'home' && started?.nav && started?.hero) {
        const update = (scroll) => {
            started.nav.classList.toggle('is-ivory', scroll > started.hero.offsetHeight - 72);
        };
        lenis.on('scroll', ({ scroll }) => update(scroll));
        update(win.scrollY || 0);
    }
    return lenis;
}

if (typeof document !== 'undefined' && typeof window !== 'undefined') boot();
