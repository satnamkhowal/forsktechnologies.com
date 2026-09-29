from __future__ import annotations

import collections
import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(".")
html_files = sorted(ROOT.glob("*.html"))
if not html_files:
    raise SystemExit("No root HTML pages found; refusing to refactor.")

originals = {p.name: p.read_text(encoding="utf-8") for p in html_files}

# Include trailing whitespace with the shared block. PHP removes one newline
# immediately after a closing ?> tag; absorbing/re-emitting the whitespace
# keeps the rendered response byte-identical to the original static HTML.
footer_re = re.compile(r'<footer class="xb-footer\b[\s\S]*?</footer>\s*')
scripts_re = re.compile(
    r'<script id="popper-js"[\s\S]*?'
    r'<script src="assets/js/search-index\.js"></script>'
    r'<script src="assets/js/static\.js"></script>\s*'
)

def group_blocks(pattern):
    groups = collections.defaultdict(list)
    blocks = {}
    for name, text in originals.items():
        match = pattern.search(text)
        if not match:
            continue
        block = match.group(0)
        digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
        groups[digest].append(name)
        blocks[digest] = block
    if not groups:
        raise SystemExit("No matching reusable blocks detected.")
    digest, pages = max(groups.items(), key=lambda item: len(item[1]))
    return blocks[digest], pages

canonical_footer, footer_pages = group_blocks(footer_re)
canonical_scripts, scripts_pages = group_blocks(scripts_re)

if len(footer_pages) < 2:
    raise SystemExit("Footer reuse count is below 2; refusing fake reuse.")
if len(scripts_pages) < 2:
    raise SystemExit("Script-bundle reuse count is below 2; refusing fake reuse.")

includes = ROOT / "includes"
includes.mkdir(exist_ok=True)
(includes / "footer.php").write_text(canonical_footer, encoding="utf-8")
(includes / "scripts.php").write_text(canonical_scripts, encoding="utf-8")

footer_marker = "<?php require __DIR__ . '/includes/footer.php'; ?>"
scripts_marker = "<?php require __DIR__ . '/includes/scripts.php'; ?>"

converted = []
footer_converted = []
scripts_converted = []

for source in html_files:
    text = originals[source.name]
    changed = False

    fm = footer_re.search(text)
    if fm and fm.group(0) == canonical_footer:
        text = text[:fm.start()] + footer_marker + text[fm.end():]
        changed = True
        footer_converted.append(source.name)

    sm = scripts_re.search(text)
    if sm and sm.group(0) == canonical_scripts:
        text = text[:sm.start()] + scripts_marker + text[sm.end():]
        changed = True
        scripts_converted.append(source.name)

    if not changed:
        continue

    target = source.with_suffix(".php")
    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing PHP page: {target}")
    target.write_text(text, encoding="utf-8")
    source.unlink()
    converted.append(source.name)

if not converted:
    raise SystemExit("No pages matched verified reusable blocks.")

htaccess = r'''DirectoryIndex index.php index.html

<IfModule mod_rewrite.c>
RewriteEngine On

# Preserve historical/public .html URLs for pages implemented internally in PHP.
RewriteCond %{THE_REQUEST} \s/+(.+?)\.php(?:[?\s]) [NC]
RewriteRule ^(.+)\.php$ $1.html [R=301,L,NE]

# Internally serve a converted PHP file only when the historical .html file is absent.
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} ^(.+)\.html$
RewriteCond %1.php -f
RewriteRule ^(.+)\.html$ $1.php [L]
</IfModule>
'''
Path(".htaccess").write_text(htaccess, encoding="utf-8")

docs = Path("docs")
docs.mkdir(exist_ok=True)

report_lines = [
    "# PHP include architecture audit",
    "",
    "This refactor is intentionally conservative. It extracts only blocks proven byte-identical across multiple root pages and leaves page-specific markup in place.",
    "",
    "## Shared includes created",
    "",
    f"- `includes/footer.php` — exact repeated footer block, including its trailing whitespace; detected on **{len(footer_pages)}** HTML pages.",
    f"- `includes/scripts.php` — exact repeated common JavaScript bundle, including its trailing whitespace; detected on **{len(scripts_pages)}** HTML pages.",
    "",
    "## Converted pages",
    "",
    f"**{len(converted)}** root pages were converted from `.html` files to internal `.php` files. Existing public/internal links remain `.html`; `.htaccess` internally maps a missing historical `.html` file to its matching PHP implementation without changing the browser URL.",
    "",
    f"Footer include used on **{len(footer_converted)}** converted pages. Common scripts include used on **{len(scripts_converted)}** converted pages.",
    "",
    "## Intentionally not extracted",
    "",
    "- **Header/navigation:** kept page-local because the export contains page-specific current-menu/current-page classes. A static shared header would mark the wrong navigation item on some pages.",
    "- **Head:** kept page-local because titles and Elementor/post-specific CSS links differ by page. This preserves existing SEO metadata and CSS order; page-specific metadata remains directly configurable per page.",
    "- **Enquiry/contact CTA:** not promoted to a global include because the audit did not prove one exact reusable block across the converted page set.",
    "- **Breadcrumbs:** retained page-local because their content is page-specific and no normalization is required for this safe pass.",
    "",
    "## Compatibility rules",
    "",
    "- Existing `.html` links and visible URLs are preserved.",
    "- Relative asset paths remain unchanged because browser-visible URLs remain the historical root-level `.html` URLs.",
    "- Direct requests for converted `.php` URLs redirect back to `.html` on Apache/LiteSpeed via `.htaccess`.",
    "- Unconverted `.html` pages continue to work as static files.",
    "- Converted pages require PHP plus Apache/LiteSpeed rewrite support; a purely static host cannot execute the includes.",
    "",
    "## Validation",
    "",
    "Every converted page is PHP-linted, rendered with PHP CLI, and compared byte-for-byte with its original HTML source. The build fails on any rendering difference. It also checks for duplicate include markers and verifies each removed historical HTML file has exactly one PHP replacement.",
    "",
    "## Converted legacy filenames",
    "",
]
report_lines.extend(f"- `{name}`" for name in converted)
report_lines.append("")
(docs / "php-architecture.md").write_text("\n".join(report_lines), encoding="utf-8")

readme = Path("README.md")
readme_text = readme.read_text(encoding="utf-8")
readme_text = readme_text.replace(
    "# Techco — standalone HTML website",
    "# Techco — PHP include architecture with legacy HTML URLs",
    1,
)
readme_text = readme_text.replace(
    "Open `index.html` in your browser. Upload the entire folder to any static website host to publish it. No WordPress installation, PHP, database, npm install, or build step is needed.",
    "Public links continue to use the existing `.html` URLs. Repeated verified site chrome is now served through PHP includes, so converted pages require a PHP-capable Apache/LiteSpeed host with rewrite support. No WordPress installation, database, npm install, or build step is needed.",
    1,
)
if "## PHP includes" not in readme_text:
    readme_text += "\n\n## PHP includes\n\nSee `docs/php-architecture.md` for the conservative conversion scope, URL-preservation rules, skipped components, and validation details.\n"
readme.write_text(readme_text, encoding="utf-8")

# Syntax and exact-output validation.
subprocess.run(["php", "-v"], check=True, stdout=subprocess.DEVNULL)
lint_targets = [includes / "footer.php", includes / "scripts.php"] + [
    Path(name).with_suffix(".php") for name in converted
]
for target in lint_targets:
    subprocess.run(["php", "-l", str(target)], check=True, stdout=subprocess.DEVNULL)

for legacy in converted:
    php_page = Path(legacy).with_suffix(".php")
    result = subprocess.run(
        ["php", str(php_page)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    rendered = result.stdout.decode("utf-8")
    if rendered != originals[legacy]:
        limit = min(len(rendered), len(originals[legacy]))
        idx = next((i for i in range(limit) if rendered[i] != originals[legacy][i]), limit)
        raise SystemExit(
            f"Rendered output changed for {legacy} at byte/character {idx}; refusing to commit."
        )

    transformed = php_page.read_text(encoding="utf-8")
    if transformed.count(footer_marker) > 1 or transformed.count(scripts_marker) > 1:
        raise SystemExit(f"Duplicate include marker detected in {php_page}.")

for legacy in converted:
    if Path(legacy).exists():
        raise SystemExit(f"Legacy file unexpectedly still exists after conversion: {legacy}")
    if not Path(legacy).with_suffix(".php").is_file():
        raise SystemExit(f"Missing PHP replacement for converted page: {legacy}")

print(f"Converted {len(converted)} pages.")
print(f"Footer exact-reuse count: {len(footer_pages)}")
print(f"Script bundle exact-reuse count: {len(scripts_pages)}")
