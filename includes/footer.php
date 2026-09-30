<?php
/**
 * Reusable Forsk Technologies footer.
 *
 * Optional caller configuration:
 *   $footerBasePath = '../';
 *   $footerLogoPath = 'image/logo/<verified-footer-logo-file>';
 *
 * The logo is intentionally opt-in until an official Forsk logo asset exists
 * in the repository. This prevents the legacy Techco template logo from being
 * shown as Forsk branding.
 */

$footerBasePath = isset($footerBasePath) ? trim((string) $footerBasePath) : '';
if ($footerBasePath !== '' && !str_ends_with($footerBasePath, '/')) {
    $footerBasePath .= '/';
}

$footerLogoPath = isset($footerLogoPath) ? trim((string) $footerLogoPath) : '';

$footerUrl = static function (string $path) use ($footerBasePath): string {
    return htmlspecialchars($footerBasePath . ltrim($path, '/'), ENT_QUOTES, 'UTF-8');
};
?>
<footer class="xb-footer forsk-footer" aria-label="Site footer">
    <style>
        .forsk-footer {
            --forsk-footer-muted: rgba(255, 255, 255, .72);
            --forsk-footer-border: rgba(255, 255, 255, .14);
            color: #fff;
            background: var(--forsk-brand-dark, #020842);
        }
        .forsk-footer * { box-sizing: border-box; }
        .forsk-footer a { color: inherit; }
        .forsk-footer__inner {
            width: min(1320px, calc(100% - 40px));
            margin-inline: auto;
        }
        .forsk-footer__cta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 28px;
            padding: clamp(52px, 6vw, 84px) 0 clamp(38px, 4vw, 56px);
            border-bottom: 1px solid var(--forsk-footer-border);
        }
        .forsk-footer__eyebrow {
            margin: 0 0 8px;
            color: var(--forsk-footer-muted);
            font-size: 14px;
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .forsk-footer__cta-title {
            max-width: 720px;
            margin: 0;
            color: #fff;
            font-size: clamp(32px, 4vw, 54px);
            line-height: 1.12;
            letter-spacing: -.025em;
            text-wrap: balance;
        }
        .forsk-footer__cta-link {
            display: inline-flex;
            min-height: 52px;
            align-items: center;
            justify-content: center;
            padding: 12px 24px;
            border-radius: 999px;
            background: var(--forsk-brand-primary, #0044eb);
            color: #fff;
            font-weight: 700;
            text-decoration: none;
            white-space: nowrap;
            transition: transform .2s ease, filter .2s ease;
        }
        .forsk-footer__cta-link:hover { color: #fff; filter: brightness(1.08); transform: translateY(-1px); }
        .forsk-footer__grid {
            display: grid;
            grid-template-columns: minmax(220px, 1.35fr) repeat(4, minmax(140px, 1fr));
            gap: clamp(28px, 4vw, 56px);
            padding: clamp(48px, 5vw, 72px) 0;
        }
        .forsk-footer__brand-link {
            display: inline-flex;
            align-items: center;
            min-height: 44px;
            color: #fff;
            font-size: clamp(22px, 2vw, 28px);
            font-weight: 700;
            line-height: 1.2;
            text-decoration: none;
        }
        .forsk-footer__logo {
            display: block;
            width: auto;
            max-width: 190px;
            max-height: 58px;
            object-fit: contain;
        }
        .forsk-footer__brand-note {
            max-width: 290px;
            margin: 14px 0 0;
            color: var(--forsk-footer-muted);
            line-height: 1.7;
        }
        .forsk-footer__title {
            margin: 2px 0 14px;
            color: #fff;
            font-size: 16px;
            font-weight: 700;
        }
        .forsk-footer__links {
            margin: 0;
            padding: 0;
            list-style: none;
        }
        .forsk-footer__links li + li { margin-top: 5px; }
        .forsk-footer__links a {
            display: inline-flex;
            min-height: 44px;
            align-items: center;
            color: var(--forsk-footer-muted);
            line-height: 1.45;
            text-decoration: none;
        }
        .forsk-footer__links a:hover { color: #fff; }
        .forsk-footer__bottom {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            padding: 24px 0 30px;
            border-top: 1px solid var(--forsk-footer-border);
            color: var(--forsk-footer-muted);
            font-size: 14px;
        }
        .forsk-footer__bottom p { margin: 0; }
        .forsk-footer__home-link {
            display: inline-flex;
            min-height: 44px;
            align-items: center;
            color: var(--forsk-footer-muted);
            text-decoration: none;
        }
        .forsk-footer__home-link:hover { color: #fff; }
        .forsk-footer a:focus-visible {
            outline: 3px solid var(--forsk-focus, #0068ff);
            outline-offset: 4px;
            border-radius: 6px;
        }
        @media (max-width: 1100px) {
            .forsk-footer__grid { grid-template-columns: minmax(240px, 1.4fr) repeat(2, minmax(160px, 1fr)); }
        }
        @media (max-width: 767px) {
            .forsk-footer__inner { width: min(100% - 32px, 1320px); }
            .forsk-footer__cta { align-items: flex-start; flex-direction: column; }
            .forsk-footer__cta-link { width: 100%; }
            .forsk-footer__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .forsk-footer__brand { grid-column: 1 / -1; }
            .forsk-footer__bottom { align-items: flex-start; flex-direction: column; }
        }
        @media (max-width: 479px) {
            .forsk-footer__grid { grid-template-columns: 1fr; }
            .forsk-footer__brand { grid-column: auto; }
        }
        @media (prefers-reduced-motion: reduce) {
            .forsk-footer__cta-link { transition: none; }
        }
    </style>

    <div class="forsk-footer__inner">
        <div class="forsk-footer__cta">
            <div>
                <p class="forsk-footer__eyebrow">Forsk Technologies</p>
                <h2 class="forsk-footer__cta-title">Have a project or technology requirement to discuss?</h2>
            </div>
            <a class="forsk-footer__cta-link" href="<?= $footerUrl('contact.html') ?>">Contact Us</a>
        </div>

        <div class="forsk-footer__grid">
            <div class="forsk-footer__brand">
                <a class="forsk-footer__brand-link" href="<?= $footerUrl('index.html') ?>" aria-label="Forsk Technologies home">
                    <?php if ($footerLogoPath !== ''): ?>
                        <img class="forsk-footer__logo" src="<?= $footerUrl($footerLogoPath) ?>" alt="Forsk Technologies">
                    <?php else: ?>
                        <span>Forsk Technologies</span>
                    <?php endif; ?>
                </a>
                <p class="forsk-footer__brand-note">Explore the company, services, resources and contact page from one consistent site footer.</p>
            </div>

            <nav aria-labelledby="forsk-footer-company-title">
                <h2 class="forsk-footer__title" id="forsk-footer-company-title">Company</h2>
                <ul class="forsk-footer__links">
                    <li><a href="<?= $footerUrl('about.html') ?>">About</a></li>
                </ul>
            </nav>

            <nav aria-labelledby="forsk-footer-services-title">
                <h2 class="forsk-footer__title" id="forsk-footer-services-title">Services</h2>
                <ul class="forsk-footer__links">
                    <li><a href="<?= $footerUrl('services.html') ?>">All Services</a></li>
                    <li><a href="<?= $footerUrl('software-company.html') ?>">Software Development</a></li>
                    <li><a href="<?= $footerUrl('business-consulting.html') ?>">Business Consulting</a></li>
                    <li><a href="<?= $footerUrl('cloud-solutions.html') ?>">Cloud Solutions</a></li>
                </ul>
            </nav>

            <nav aria-labelledby="forsk-footer-resources-title">
                <h2 class="forsk-footer__title" id="forsk-footer-resources-title">Resources</h2>
                <ul class="forsk-footer__links">
                    <li><a href="<?= $footerUrl('blog.html') ?>">Blog</a></li>
                </ul>
            </nav>

            <nav aria-labelledby="forsk-footer-contact-title">
                <h2 class="forsk-footer__title" id="forsk-footer-contact-title">Contact</h2>
                <ul class="forsk-footer__links">
                    <li><a href="<?= $footerUrl('contact.html') ?>">Contact Us</a></li>
                </ul>
            </nav>
        </div>

        <div class="forsk-footer__bottom">
            <p>&copy; <?= date('Y') ?> Forsk Technologies. All rights reserved.</p>
            <a class="forsk-footer__home-link" href="<?= $footerUrl('index.html') ?>">Back to homepage</a>
        </div>
    </div>
</footer>
