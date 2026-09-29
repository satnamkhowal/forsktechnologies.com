#!/usr/bin/env python3
"""
Contextual internal-link auditor for the standalone Forsk Technologies website.

Outputs:
  reports/internal-link-audit.csv
  reports/internal-link-summary.json

The auditor separates contextual body links from repeated header/nav/footer links,
normalizes pretty URLs through page-map.json, and reports:
- orphan/weakly linked primary pages
- broken internal targets
- excessive link loads
- cross-cluster links that deserve human relevance review

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, unquote

SITE_HOSTS = {"forsktechnologies.com", "www.forsktechnologies.com"}

ARCHIVE_PREFIXES = (
    "archive-",
    "author-",
    "category-",
    "tag-",
    "service-category-",
    "project-category-",
)

CORE_TYPES = {
    "index.html": "homepage",
    "services.html": "service_hub",
    "software-company.html": "service_hub",
    "business-consulting.html": "service_hub",
    "cloud-solutions.html": "service_hub",
    "ai-machine-learning.html": "service_hub",
    "about.html": "company",
    "team.html": "company",
    "team-details.html": "company",
    "our-fields.html": "company",
    "portfolio.html": "resource",
    "pricing.html": "conversion_support",
    "contact.html": "conversion",
    "blog.html": "resource_hub",
}

CLUSTER_PATTERNS = {
    "software": (
        "custom-software",
        "web-application",
        "website-development",
        "mobile-app",
        "ui-ux",
        "maintenance-and-customer-support",
        "modern-technology",
        "it-management",
    ),
    "cloud": (
        "cloud-",
        "aws-managed",
        "ci-cd",
        "prometheus",
        "optimize-your-cloud",
        "streamlined-cloud",
    ),
    "consulting": (
        "business-process",
        "change-management",
        "market-analysis",
        "performance-metrics",
        "strategic-planning",
        "digital-transformation",
        "audit-it-consulting",
    ),
    "security": (
        "data-tracking-and-security",
        "cloud-security",
        "cybersecurity",
    ),
    "ai": (
        "ai-machine-learning",
        "machine-learning",
        "artificial-intelligence",
        "quantum-computing",
    ),
}

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

NON_CONTEXTUAL_MARKERS = (
    "header", "footer", "menu", "nav", "navigation", "offcanvas",
    "sidebar", "breadcrumb", "mobile-menu", "copyright",
)


@dataclass(frozen=True)
class Link:
    source: str
    href: str
    anchor: str
    context: str


class LinkParser(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.active: dict | None = None
        self.links: list[Link] = []

    @staticmethod
    def _attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k.lower(): (v or "") for k, v in attrs}

    def _context(self, current_attrs: dict[str, str]) -> str:
        ancestors = self.stack + [("a", current_attrs)]
        for tag, attrs in ancestors:
            if tag in {"header", "nav", "footer"}:
                return "navigation"
            marker_text = " ".join(
                [attrs.get("id", ""), attrs.get("class", ""), attrs.get("role", "")]
            ).lower()
            if any(marker in marker_text for marker in NON_CONTEXTUAL_MARKERS):
                return "navigation"
        return "contextual"

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        ad = self._attrs_dict(attrs)
        if tag == "a":
            href = ad.get("href", "").strip()
            self.active = {
                "href": href,
                "text": [],
                "context": self._context(ad),
            }
        if tag not in VOID_TAGS:
            self.stack.append((tag, ad))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_data(self, data: str) -> None:
        if self.active is not None:
            self.active["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "a" and self.active is not None:
            anchor = re.sub(r"\s+", " ", "".join(self.active["text"])).strip()
            self.links.append(
                Link(
                    source=self.source,
                    href=self.active["href"],
                    anchor=anchor,
                    context=self.active["context"],
                )
            )
            self.active = None

        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def load_page_map(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    path = root / "page-map.json"
    if not path.exists():
        return {}, {}
    data = json.loads(path.read_text(encoding="utf-8"))
    old_to_flat = {str(k).lstrip("/"): str(v) for k, v in data.items()}
    flat_to_pretty: dict[str, str] = {}
    for old_path, flat in old_to_flat.items():
        pretty = "/" if old_path == "index.html" else "/" + old_path.removesuffix("index.html")
        flat_to_pretty.setdefault(flat, pretty)
    return old_to_flat, flat_to_pretty


def classify_page(name: str) -> str:
    if name in CORE_TYPES:
        return CORE_TYPES[name]
    if name.startswith("service-") and not name.startswith("service-category-"):
        return "service_page"
    if name.startswith("project-") and not name.startswith("project-category-"):
        return "case_study"
    if name.startswith("blog-page-"):
        return "resource_hub"
    if name.startswith(ARCHIVE_PREFIXES):
        return "archive"
    if name == "hello-world.html":
        return "legacy"
    if name.endswith(".html"):
        return "article"
    return "other"


def page_cluster(name: str) -> str:
    lower = name.lower()
    if name == "software-company.html":
        return "software"
    if name == "cloud-solutions.html":
        return "cloud"
    if name == "business-consulting.html":
        return "consulting"
    if name == "ai-machine-learning.html":
        return "ai"
    matches = [
        cluster for cluster, patterns in CLUSTER_PATTERNS.items()
        if any(p in lower for p in patterns)
    ]
    return matches[0] if len(matches) == 1 else ("mixed" if matches else "general")


def normalize_target(
    href: str,
    source_file: str,
    root: Path,
    old_to_flat: dict[str, str],
) -> tuple[str | None, str]:
    """Return (target file or None, status)."""
    href = (href or "").strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None, "ignored"

    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc.lower() not in SITE_HOSTS:
            return None, "external"
        raw_path = unquote(parsed.path or "/")
    elif parsed.scheme:
        return None, "external"
    else:
        raw_path = unquote(parsed.path or "")

    raw_path = raw_path.split("?", 1)[0].split("#", 1)[0]
    if not raw_path:
        return source_file, "same_page"

    if raw_path.startswith(("assets/", "/assets/")):
        return None, "asset"

    if raw_path.startswith("/"):
        candidate = raw_path.lstrip("/")
    else:
        source_parent = Path(source_file).parent
        candidate = (source_parent / raw_path).as_posix()

    while candidate.startswith("./"):
        candidate = candidate[2:]
    candidate = re.sub(r"/+", "/", candidate)

    if candidate in {"", "."}:
        return "index.html", "ok"

    direct = root / candidate
    if direct.is_file() and direct.suffix.lower() == ".html":
        return candidate, "ok"

    path_key = candidate
    if path_key.endswith("/"):
        path_key += "index.html"
    elif not Path(path_key).suffix:
        path_key += "/index.html"

    if path_key in old_to_flat:
        return old_to_flat[path_key], "ok"

    if path_key == "index.html":
        return "index.html", "ok"

    return candidate or href, "broken"


def iter_html(root: Path) -> Iterable[Path]:
    for path in sorted(root.glob("*.html")):
        if path.is_file():
            yield path


def is_primary(page_type: str) -> bool:
    return page_type not in {"archive", "legacy", "other"}


def audit(root: Path, excessive_unique: int, weak_contextual: int) -> dict:
    old_to_flat, flat_to_pretty = load_page_map(root)
    html_files = [p.name for p in iter_html(root)]
    file_set = set(html_files)

    all_links: list[dict] = []
    broken: list[dict] = []
    inbound_all: dict[str, set[str]] = defaultdict(set)
    inbound_contextual: dict[str, set[str]] = defaultdict(set)
    outbound_unique: dict[str, set[str]] = defaultdict(set)
    outbound_contextual: dict[str, set[str]] = defaultdict(set)
    occurrence_counts = Counter()
    anchor_counts: dict[str, Counter] = defaultdict(Counter)
    cross_cluster_review: list[dict] = []

    for path in iter_html(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        parser = LinkParser(path.name)
        parser.feed(text)

        for link in parser.links:
            target, status = normalize_target(link.href, path.name, root, old_to_flat)
            if status in {"ignored", "external", "asset", "same_page"}:
                continue

            row = {
                "source_file": path.name,
                "source_url": flat_to_pretty.get(path.name, f"/{path.name}"),
                "target_file": target or "",
                "target_url": flat_to_pretty.get(target or "", f"/{target}" if target else ""),
                "anchor": link.anchor,
                "context": link.context,
                "status": status,
            }
            all_links.append(row)

            if status == "broken":
                broken.append(row)
                continue
            if target not in file_set:
                row["status"] = "broken"
                broken.append(row)
                continue

            inbound_all[target].add(path.name)
            outbound_unique[path.name].add(target)
            occurrence_counts[path.name] += 1
            if link.anchor:
                anchor_counts[target][link.anchor.lower()] += 1

            if link.context == "contextual":
                inbound_contextual[target].add(path.name)
                outbound_contextual[path.name].add(target)

                source_cluster = page_cluster(path.name)
                target_cluster = page_cluster(target)
                source_type = classify_page(path.name)
                target_type = classify_page(target)
                if (
                    source_type == "service_page"
                    and target_type == "service_page"
                    and source_cluster not in {"general", "mixed"}
                    and target_cluster not in {"general", "mixed"}
                    and source_cluster != target_cluster
                ):
                    cross_cluster_review.append({
                        "source_file": path.name,
                        "source_url": flat_to_pretty.get(path.name, f"/{path.name}"),
                        "target_file": target,
                        "target_url": flat_to_pretty.get(target, f"/{target}"),
                        "anchor": link.anchor,
                        "reason": f"Cross-cluster service link: {source_cluster} -> {target_cluster}; review for genuine user relevance.",
                    })

    pages = []
    orphan_pages = []
    weak_pages = []
    excessive_pages = []

    for name in html_files:
        ptype = classify_page(name)
        incoming_all_count = len(inbound_all[name])
        incoming_contextual_count = len(inbound_contextual[name])
        outgoing_unique_count = len(outbound_unique[name])
        outgoing_contextual_count = len(outbound_contextual[name])

        row = {
            "file": name,
            "url": flat_to_pretty.get(name, f"/{name}"),
            "type": ptype,
            "cluster": page_cluster(name),
            "incoming_all": incoming_all_count,
            "incoming_contextual": incoming_contextual_count,
            "outgoing_unique": outgoing_unique_count,
            "outgoing_contextual": outgoing_contextual_count,
            "link_occurrences": occurrence_counts[name],
        }
        pages.append(row)

        if name != "index.html" and is_primary(ptype) and incoming_contextual_count == 0:
            orphan_pages.append(row)
        elif (
            name != "index.html"
            and is_primary(ptype)
            and incoming_contextual_count <= weak_contextual
        ):
            weak_pages.append(row)

        if outgoing_unique_count > excessive_unique:
            excessive_pages.append(row)

    anchor_warnings = []
    for target, counts in anchor_counts.items():
        total = sum(counts.values())
        if total < 4:
            continue
        anchor, count = counts.most_common(1)[0]
        share = count / total
        if share >= 0.70 and len(counts) <= 2:
            anchor_warnings.append({
                "target_file": target,
                "target_url": flat_to_pretty.get(target, f"/{target}"),
                "dominant_anchor": anchor,
                "dominant_share": round(share, 3),
                "occurrences": total,
                "reason": "Anchor text is highly concentrated; vary wording only where it reads naturally.",
            })

    return {
        "pages": pages,
        "broken_links": broken,
        "orphan_pages": orphan_pages,
        "weak_pages": weak_pages,
        "excessive_pages": excessive_pages,
        "cross_cluster_review": cross_cluster_review,
        "anchor_warnings": anchor_warnings,
        "counts": {
            "html_pages": len(html_files),
            "links_evaluated": len(all_links),
            "broken_links": len(broken),
            "orphan_primary_pages": len(orphan_pages),
            "weak_primary_pages": len(weak_pages),
            "excessive_pages": len(excessive_pages),
            "cross_cluster_review": len(cross_cluster_review),
            "anchor_warnings": len(anchor_warnings),
        },
    }


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Website repository root")
    parser.add_argument("--out", default="reports", help="Output directory")
    parser.add_argument(
        "--excessive-unique",
        type=int,
        default=60,
        help="Flag pages above this number of unique internal targets",
    )
    parser.add_argument(
        "--weak-contextual",
        type=int,
        default=1,
        help="Primary pages with <= this many contextual inbound sources are weak",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = root / args.out
    result = audit(root, args.excessive_unique, args.weak_contextual)

    out.mkdir(parents=True, exist_ok=True)
    (out / "internal-link-summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    audit_rows = []
    orphan_set = {r["file"] for r in result["orphan_pages"]}
    weak_set = {r["file"] for r in result["weak_pages"]}
    excessive_set = {r["file"] for r in result["excessive_pages"]}
    for row in result["pages"]:
        status = []
        if row["file"] in orphan_set:
            status.append("ORPHAN_CONTEXTUAL")
        if row["file"] in weak_set:
            status.append("WEAK_CONTEXTUAL")
        if row["file"] in excessive_set:
            status.append("EXCESSIVE_LINKS")
        row = dict(row)
        row["finding"] = "|".join(status) or "OK"
        audit_rows.append(row)

    write_csv(
        out / "internal-link-audit.csv",
        audit_rows,
        [
            "url", "file", "type", "cluster", "incoming_all",
            "incoming_contextual", "outgoing_unique", "outgoing_contextual",
            "link_occurrences", "finding",
        ],
    )
    write_csv(
        out / "broken-internal-links.csv",
        result["broken_links"],
        ["source_url", "target_url", "anchor", "context", "status", "source_file", "target_file"],
    )
    write_csv(
        out / "cross-cluster-review.csv",
        result["cross_cluster_review"],
        ["source_url", "target_url", "anchor", "reason", "source_file", "target_file"],
    )

    print(json.dumps(result["counts"], indent=2))
    return 1 if result["broken_links"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
