#!/usr/bin/env python3
"""Dependency-free image audit for Forsk Technologies. Reports only; never mutates assets."""
from __future__ import annotations
import argparse, hashlib, html, json, os, re, struct
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

IMAGE_EXTS={".png",".jpg",".jpeg",".webp",".gif",".svg",".avif",".cur"}
TEXT_EXTS={".html",".css",".js",".json",".xml",".php"}
LOGO_ROOT=Path("assets/images/logo")
IMG_RE=re.compile(r"<img\b[^>]*>",re.I|re.S)
ATTR_RE=re.compile(r"""([:\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?""",re.S)
REF_RE=re.compile(r"""(?P<p>(?:\.{0,2}/|/)?assets/images/[A-Za-z0-9_./%()\- +]+?\.(?:png|jpe?g|webp|gif|svg|avif|cur))""",re.I)

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def dims(path):
    ext=path.suffix.lower()
    try:
        if ext==".png":
            b=path.read_bytes()[:24]
            return struct.unpack(">II",b[16:24]) if b[:8]==b"\x89PNG\r\n\x1a\n" else (None,None)
        if ext==".gif":
            b=path.read_bytes()[:10]
            return struct.unpack("<HH",b[6:10]) if b[:6] in {b"GIF87a",b"GIF89a"} else (None,None)
        if ext in {".jpg",".jpeg"}:
            with path.open("rb") as f:
                if f.read(2)!=b"\xff\xd8": return None,None
                while True:
                    b=f.read(1)
                    if not b:return None,None
                    if b!=b"\xff":continue
                    m=f.read(1)
                    while m==b"\xff":m=f.read(1)
                    if not m:return None,None
                    code=m[0]
                    if code in (0xD8,0xD9):continue
                    n=f.read(2)
                    if len(n)!=2:return None,None
                    length=struct.unpack(">H",n)[0]
                    if code in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}:
                        d=f.read(5)
                        if len(d)==5:
                            h,w=struct.unpack(">HH",d[1:5]);return w,h
                        return None,None
                    f.seek(max(length-2,0),os.SEEK_CUR)
        if ext==".webp":
            b=path.read_bytes()[:64]
            if b[:4]!=b"RIFF" or b[8:12]!=b"WEBP":return None,None
            kind=b[12:16]
            if kind==b"VP8X" and len(b)>=30:
                return 1+int.from_bytes(b[24:27],"little"),1+int.from_bytes(b[27:30],"little")
            if kind==b"VP8L" and len(b)>=25 and b[20]==0x2F:
                a,c,d,e=b[21:25]
                return 1+a+((c&0x3F)<<8),1+(c>>6)+(d<<2)+((e&0x0F)<<10)
            if kind==b"VP8 ":
                i=b.find(b"\x9d\x01\x2a")
                if i>=0 and i+7<=len(b):
                    w,h=struct.unpack("<HH",b[i+3:i+7]);return w&0x3FFF,h&0x3FFF
        if ext==".svg":
            r=ET.parse(path).getroot()
            def number(v):
                m=re.match(r"\s*([0-9]+(?:\.[0-9]+)?)",v or "")
                return float(m.group(1)) if m else None
            w,h=number(r.get("width")),number(r.get("height"))
            if w and h:return round(w),round(h)
            vb=re.split(r"[\s,]+",(r.get("viewBox") or "").strip())
            if len(vb)==4:return round(float(vb[2])),round(float(vb[3]))
    except Exception: pass
    return None,None

def norm(raw):
    raw=html.unescape(unquote((raw or "").strip()))
    if not raw or raw.startswith(("data:","http://","https://","//")):return None
    p=urlsplit(raw).path.replace("\\","/")
    p=re.sub(r"^(?:\./)+","",p).lstrip("/")
    i=p.find("assets/images/")
    return p[i:] if i>=0 else None

def attrs(tag):
    out={}
    for m in ATTR_RE.finditer(tag):
        k=m.group(1).lower()
        if k=="img":continue
        out[k]=next((x for x in m.groups()[1:] if x is not None),None)
    return out

def name_flags(rel):
    n=Path(rel).name; f=[]
    if " " in n:f.append("spaces")
    if re.search(r"[A-Z]",n):f.append("uppercase")
    if ".svg.svg" in n.lower():f.append("double-extension")
    if re.search(r"(cirlce|technlogies)",n,re.I):f.append("likely-typo")
    if re.search(r"-[123](?=\.[^.]+$)",n):f.append("generated-copy-suffix")
    return sorted(set(f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    ap.add_argument("--out",default="docs/image-audit-generated.json")
    ap.add_argument("--markdown",default="docs/image-audit-generated.md")
    ap.add_argument("--oversized",type=int,default=150_000)
    a=ap.parse_args()
    root=Path(a.root).resolve(); image_root=root/"assets/images"
    if not image_root.exists():raise SystemExit(f"Missing {image_root}")

    assets={}; groups=defaultdict(list)
    for p in sorted(image_root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:continue
        rel=p.relative_to(root).as_posix(); w,h=dims(p); digest=sha(p)
        groups[digest].append(rel)
        assets[rel]={"path":rel,"bytes":p.stat().st_size,"format":p.suffix.lower().lstrip("."),
                     "width":w,"height":h,"official_logo":Path(rel).is_relative_to(LOGO_ROOT),
                     "filename_flags":name_flags(rel),"references":[]}

    refs=defaultdict(list); tags=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:continue
        rel=p.relative_to(root).as_posix()
        try:text=p.read_text("utf-8",errors="replace")
        except Exception:continue
        for m in REF_RE.finditer(text):
            r=norm(m.group("p"))
            if r:refs[r].append({"file":rel,"offset":m.start()})
        if p.suffix.lower()==".html":
            for m in IMG_RE.finditer(text):
                at=attrs(m.group(0)); src=norm(at.get("src"))
                tags.append({"file":rel,"offset":m.start(),"src":src,
                    "alt_present":"alt" in at,"alt":at.get("alt"),
                    "width":at.get("width"),"height":at.get("height"),
                    "loading":at.get("loading"),"decoding":at.get("decoding"),
                    "fetchpriority":at.get("fetchpriority")})
    for r,u in refs.items():
        if r in assets:assets[r]["references"]=u

    duplicates=[]; redundant=0
    for digest,paths in sorted(groups.items()):
        if len(paths)<2:continue
        each=assets[paths[0]]["bytes"]; save=each*(len(paths)-1); redundant+=save
        duplicates.append({"sha256":digest,"paths":sorted(paths),"bytes_each":each,
                           "redundant_bytes_if_consolidated":save})

    oversized=sorted((x for x in assets.values() if x["bytes"]>=a.oversized),key=lambda x:x["bytes"],reverse=True)
    convert=sorted((x for x in assets.values() if x["format"] in {"jpg","jpeg","png"} and
                    x["bytes"]>=20_000 and not x["official_logo"]),key=lambda x:x["bytes"],reverse=True)
    poor=[x for x in assets.values() if x["filename_flags"]]
    unused=[x for x in assets.values() if not x["references"]]
    missing_alt=[x for x in tags if not x["alt_present"]]
    empty_alt=[x for x in tags if x["alt_present"] and not (x["alt"] or "").strip()]
    missing_dims=[x for x in tags if not x["width"] or not x["height"]]

    summary={"image_assets":len(assets),"total_image_bytes":sum(x["bytes"] for x in assets.values()),
             "duplicate_groups":len(duplicates),"redundant_duplicate_bytes":redundant,
             "oversized_assets":len(oversized),"legacy_conversion_candidates":len(convert),
             "poor_filenames":len(poor),"unreferenced_assets_static_scan":len(unused),
             "img_tags":len(tags),"img_missing_alt_attribute":len(missing_alt),
             "img_empty_alt":len(empty_alt),"img_missing_width_or_height":len(missing_dims)}
    report={"summary":summary,"duplicates":duplicates,"oversized":oversized,
            "conversion_candidates":convert,"poor_filenames":poor,
            "unreferenced_assets_static_scan":unused,"img_markup":tags}

    out=root/a.out; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2),"utf-8")

    md=["# Generated image audit","","> Reporting only; no assets were modified.","","## Summary",""]
    for k,v in summary.items():md.append(f"- {k.replace('_',' ').title()}: **{v:,}**")
    md += ["","## Oversized assets","","| Asset | Bytes | Dimensions | References |","|---|---:|---:|---:|"]
    for x in oversized:
        d=f"{x['width']}×{x['height']}" if x["width"] and x["height"] else "unknown"
        md.append(f"| `{x['path']}` | {x['bytes']:,} | {d} | {len(x['references'])} |")
    md += ["","## Exact duplicate groups",""]
    for d in duplicates:
        md.append(f"- {d['bytes_each']:,} B each; {d['redundant_bytes_if_consolidated']:,} B potentially redundant: "+
                  ", ".join(f"`{p}`" for p in d["paths"]))
    md += ["","## Safety note","",
           "Do not delete, rename, or consolidate files until all references are migrated and verified. "
           "Official logo masters must remain visually unchanged.",""]
    m=root/a.markdown; m.parent.mkdir(parents=True,exist_ok=True); m.write_text("\n".join(md),"utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
