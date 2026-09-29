#!/usr/bin/env python3
"""
Dependency-free image asset audit for the Forsk Technologies static site.

Checks:
- image inventory, file size, intrinsic dimensions
- exact byte-for-byte duplicates
- oversized files
- legacy PNG/JPEG conversion candidates
- poor filenames
- references from HTML/CSS/JS
- <img> alt/width/height/loading/decoding/fetchpriority attributes

This script reports; it does not delete, rename, transcode, or modify brand assets.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import struct
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif", ".cur"}
TEXT_EXTS = {".html", ".css", ".js", ".json", ".xml", ".php"}
OFFICIAL_LOGO_DIR = Path("assets/images/logo")
DIRECT_IMAGE_RE = re.compile(
    r"""(?P<path>(?:\.{0,2}/|/)?assets/images/[A-Za-z0-9_./%()\- +]+?\.(?:png|jpe?g|webp|gif|svg|avif|cur))""",
    re.I,
)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
ATTR_RE = re.compile(
    r"""([:\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?""",
    re.S,
)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def svg_dimensions(path: Path):
    try:
        root = ET.parse(path).getroot()
        def num(v):
            if not v:
                return None
            m = re.match(r"\s*([0-9]+(?:\.[0-9]+)?)", v)
            return float(m.group(1)) if m else None
        w, h = num(root.get("width")), num(root.get("height"))
        if w and h:
            return int(round(w)), int(round(h))
        vb = root.get("viewBox")
        if vb:
            vals = re.split(r"[\s,]+", vb.strip())
            if len(vals) == 4:
                return int(round(float(vals[2]))), int(round(float(vals[3])))
    except Exception:
        pass
    return None, None

def jpeg_dimensions(path: Path):
    try:
        with path.open("rb") as f:
            if f.read(2) != b"\xff\xd8":
                return None, None
            while True:
                b = f.read(1)
                if not b:
                    return None, None
                if b != b"\xff":
                    continue
                while b == b"\xff":
                    marker = f.read(1)
                    if not marker:
                        return None, None
                    b = marker
                m = b[0]
                if m in (0xD8, 0xD9):
                    continue
                length_raw = f.read(2)
                if len(length_raw) != 2:
                    return None, None
                length = struct.unpack(">H", length_raw)[0]
                if m in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}:
                    data = f.read(5)
                    if len(data) == 5:
                        h, w = struct.unpack(">HH", data[1:5])
                        return w, h
                    return None, None
                f.seek(max(length - 2, 0), os.SEEK_CUR)
    except Exception:
        return None, None

def webp_dimensions(path: Path):
    try:
        data = path.read_bytes()[:64]
        if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
            return None, None
        kind = data[12:16]
        if kind == b"VP8X" and len(data) >= 30:
            w = 1 + int.from_bytes(data[24:27], "little")
            h = 1 + int.from_bytes(data[27:30], "little")
            return w, h
        if kind == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
            b0, b1, b2, b3 = data[21:25]
            w = 1 + b0 + ((b1 & 0x3F) << 8)
            h = 1 + (b1 >> 6) + (b2 << 2) + ((b3 & 0x0F) << 10)
            return w, h
        if kind == b"VP8 ":
            pos = data.find(b"\x9d\x01\x2a")
            if pos >= 0 and pos + 7 <= len(data):
                w, h = struct.unpack("<HH", data[pos+3:pos+7])
                return w & 0x3FFF, h & 0x3FFF
    except Exception:
        pass
    return None, None

def intrinsic_dimensions(path: Path):
    ext = path.suffix.lower()
    try:
        if ext == ".png":
            data = path.read_bytes()[:24]
            if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
                return struct.unpack(">II", data[16:24])
        elif ext in {".jpg", ".jpeg"}:
            return jpeg_dimensions(path)
        elif ext == ".gif":
            data = path.read_bytes()[:10]
            if data[:6] in {b"GIF87a", b"GIF89a"} and len(data) >= 10:
                return struct.unpack("<HH", data[6:10])
        elif ext == ".webp":
            return webp_dimensions(path)
        elif ext == ".svg":
            return svg_dimensions(path)
    except Exception:
        pass
    return None, None

def normalize_ref(raw: str) -> str | None:
    raw = html.unescape(unquote(raw.strip()))
    if not raw or raw.startswith(("data:", "http://", "https://", "//")):
        return None
    raw = urlsplit(raw).path.replace("\\", "/")
    raw = re.sub(r"^(?:\./)+", "", raw)
    raw = raw.lstrip("/")
    idx = raw.find("assets/images/")
    if idx < 0:
        return None
    return raw[idx:]

def parse_attrs(tag: str) -> dict[str, str | None]:
    attrs = {}
    for m in ATTR_RE.finditer(tag):
        key = m.group(1).lower()
        if key == "img":
            continue
        val = m.group(2) if m.group(2) is not None else m.group(3)
        if val is None:
            val = m.group(4)
        attrs[key] = val
    return attrs

def bad_filename_reasons(rel: str):
    name = Path(rel).name
    reasons = []
    if " " in name:
        reasons.append("spaces")
    if re.search(r"[A-Z]", name):
        reasons.append("uppercase")
    if re.search(r"\.(png|jpe?g|webp|svg|gif|avif)\.\1$", name, re.I):
        reasons.append("double-extension")
    if ".svg.svg" in name.lower():
        reasons.append("double-extension")
    if re.search(r"\b(?:cirlce|technlogies)\b", name, re.I):
        reasons.append("likely-typo")
    if re.search(r"-[123](?=\.[^.]+$)", name):
        reasons.append("generated-copy-suffix")
    return sorted(set(reasons))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repository root")
    ap.add_argument("--out", default="docs/image-audit-generated.json")
    ap.add_argument("--markdown", default="docs/image-audit-generated.md")
    ap.add_argument("--oversized", type=int, default=150_000)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    image_root = root / "assets/images"
    if not image_root.exists():
        raise SystemExit(f"Missing {image_root}")

    assets = {}
    hash_groups = defaultdict(list)

    for p in sorted(image_root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        w, h = intrinsic_dimensions(p)
        digest = sha256_file(p)
        hash_groups[digest].append(rel)
        assets[rel] = {
            "path": rel,
            "bytes": size,
            "format": p.suffix.lower().lstrip("."),
            "width": w,
            "height": h,
            "official_logo": Path(rel).is_relative_to(OFFICIAL_LOGO_DIR),
            "filename_flags": bad_filename_reasons(rel),
            "references": [],
        }

    img_markup = []
    all_refs = defaultdict(list)

    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:
            continue
        rel_text = p.relative_to(root).as_posix()
        try:
            text = p.read_text("utf-8", errors="replace")
        except Exception:
            continue

        for m in DIRECT_IMAGE_RE.finditer(text):
            ref = normalize_ref(m.group("path"))
            if ref:
                all_refs[ref].append({"file": rel_text, "offset": m.start()})

        if p.suffix.lower() == ".html":
            for tag_m in IMG_TAG_RE.finditer(text):
                tag = tag_m.group(0)
                attrs = parse_attrs(tag)
                src = normalize_ref(attrs.get("src") or "")
                srcset = attrs.get("srcset") or ""
                refs = [src] if src else []
                for candidate in srcset.split(","):
                    candidate = candidate.strip().split(" ", 1)[0]
                    r = normalize_ref(candidate)
                    if r:
                        refs.append(r)
                img_markup.append({
                    "file": rel_text,
                    "offset": tag_m.start(),
                    "src": src,
                    "alt_present": "alt" in attrs,
                    "alt": attrs.get("alt"),
                    "width": attrs.get("width"),
                    "height": attrs.get("height"),
                    "loading": attrs.get("loading"),
                    "decoding": attrs.get("decoding"),
                    "fetchpriority": attrs.get("fetchpriority"),
                    "refs": sorted(set(refs)),
                })

    for ref, uses in all_refs.items():
        if ref in assets:
            assets[ref]["references"] = uses

    duplicates = []
    redundant_bytes = 0
    for digest, paths in sorted(hash_groups.items()):
        if len(paths) > 1:
            size = assets[paths[0]]["bytes"]
            redundant = size * (len(paths) - 1)
            redundant_bytes += redundant
            duplicates.append({
                "sha256": digest,
                "paths": sorted(paths),
                "bytes_each": size,
                "redundant_bytes_if_consolidated": redundant,
            })

    oversized = sorted(
        [a for a in assets.values() if a["bytes"] >= args.oversized],
        key=lambda x: x["bytes"], reverse=True
    )
    conversion_candidates = sorted(
        [
            a for a in assets.values()
            if a["format"] in {"jpg", "jpeg", "png"}
            and a["bytes"] >= 20_000
            and not a["official_logo"]
        ],
        key=lambda x: x["bytes"], reverse=True
    )
    poor_names = [a for a in assets.values() if a["filename_flags"]]
    unused = [a for a in assets.values() if not a["references"]]

    missing_alt = [x for x in img_markup if not x["alt_present"]]
    empty_alt = [x for x in img_markup if x["alt_present"] and (x["alt"] or "").strip() == ""]
    missing_dims = [x for x in img_markup if not x["width"] or not x["height"]]
    lazy = [x for x in img_markup if (x["loading"] or "").lower() == "lazy"]

    report = {
        "root": str(root),
        "summary": {
            "image_assets": len(assets),
            "total_image_bytes": sum(a["bytes"] for a in assets.values()),
            "duplicate_groups": len(duplicates),
            "redundant_duplicate_bytes": redundant_bytes,
            "oversized_assets": len(oversized),
            "legacy_conversion_candidates": len(conversion_candidates),
            "poor_filenames": len(poor_names),
            "unreferenced_assets_static_scan": len(unused),
            "img_tags": len(img_markup),
            "img_missing_alt_attribute": len(missing_alt),
            "img_empty_alt": len(empty_alt),
            "img_missing_width_or_height": len(missing_dims),
            "img_loading_lazy": len(lazy),
        },
        "duplicates": duplicates,
        "oversized": oversized,
        "conversion_candidates": conversion_candidates,
        "poor_filenames": poor_names,
        "unreferenced_assets_static_scan": unused,
        "img_markup": img_markup,
    }

    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), "utf-8")

    md = []
    s = report["summary"]
    md += [
        "# Generated image audit", "",
        "> Generated by `scripts/audit_images.py`. This is a reporting tool only; it makes no asset changes.", "",
        "## Summary", "",
        f"- Image assets: **{s['image_assets']}**",
        f"- Total image bytes: **{s['total_image_bytes']:,}**",
        f"- Exact duplicate groups: **{s['duplicate_groups']}**",
        f"- Potential duplicate bytes removable after reference consolidation: **{s['redundant_duplicate_bytes']:,}**",
        f"- Assets >= {args.oversized:,} bytes: **{s['oversized_assets']}**",
        f"- PNG/JPEG conversion candidates >= 20 KB (excluding official logo directory): **{s['legacy_conversion_candidates']}**",
        f"- Poor filename flags: **{s['poor_filenames']}**",
        f"- Unreferenced assets in static source scan: **{s['unreferenced_assets_static_scan']}**",
        f"- `<img>` tags: **{s['img_tags']}**",
        f"- `<img>` tags missing alt attribute: **{s['img_missing_alt_attribute']}**",
        f"- `<img>` tags with empty alt: **{s['img_empty_alt']}**",
        f"- `<img>` tags missing width or height: **{s['img_missing_width_or_height']}**", "",
        "## Oversized assets", "",
        "| Asset | Bytes | Dimensions | Referenced |",
        "|---|---:|---:|---:|",
    ]
    for a in oversized:
        dims = f"{a['width']}×{a['height']}" if a["width"] and a["height"] else "unknown"
        md.append(f"| `{a['path']}` | {a['bytes']:,} | {dims} | {len(a['references'])} |")
    md += ["", "## Exact duplicate groups", ""]
    for d in duplicates:
        md.append(
            f"- {d['bytes_each']:,} B each; {d['redundant_duplicate_bytes_if_consolidated']:,} B potentially redundant: "
            + ", ".join(f"`{p}`" for p in d["paths"])
        )
    md += [
        "", "## Safety note", "",
        "No file listed as duplicate or unreferenced should be deleted until its references are migrated/verified. "
        "Official logo artwork must not be altered; retain masters and use separate optimized derivatives when needed.", "",
    ]
    md_path = root / args.markdown
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md), "utf-8")

    print(json.dumps(report["summary"], indent=2))

if __name__ == "__main__":
    main()
