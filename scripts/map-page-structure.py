from pathlib import Path
import re,json,html,collections
ROOT=Path(__file__).resolve().parents[1]
TAG=re.compile(r'<[^>]+>'); WS=re.compile(r'\s+')
def clean(s): return WS.sub(' ',html.unescape(TAG.sub(' ',s))).strip()
def family(n):
 if n.startswith('service-category-'): return 'service-category'
 if n.startswith('service-'): return 'service-detail'
 if n.startswith('project-category-'): return 'project-category'
 if n.startswith('project-'): return 'project-detail'
 if n.startswith('category-'): return 'blog-category'
 if n.startswith('tag-'): return 'blog-tag'
 if n.startswith('archive-'): return 'blog-archive'
 if n.startswith('author-'): return 'author-archive'
 if n.startswith('blog'): return 'blog-list'
 return 'core-other'
rows=[]
for p in sorted(ROOT.glob('*.html')):
 t=p.read_text(encoding='utf-8',errors='ignore')
 mt=re.search(r'<title[^>]*>(.*?)</title>',t,re.I|re.S)
 h1=[clean(x) for x in re.findall(r'<h1[^>]*>(.*?)</h1>',t,re.I|re.S) if clean(x)]
 h2=[clean(x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>',t,re.I|re.S) if clean(x)]
 sections=[]
 for attrs in re.findall(r'<section\b([^>]*)>',t,re.I):
  m=re.search(r'class=["\']([^"\']+)',attrs,re.I); sections.append(m.group(1) if m else '')
 rows.append({'file':p.name,'family':family(p.name),'title':clean(mt.group(1)) if mt else '', 'h1':h1,'h2':h2,'section_count':len(sections),'section_classes':sections,'noindex':bool(re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex',t,re.I))})
(ROOT/'docs'/'page-structure-map.json').write_text(json.dumps({'generated':'2026-09-30','page_count':len(rows),'pages':rows},indent=2,ensure_ascii=False),encoding='utf-8')
fams=collections.defaultdict(list)
for r in rows:fams[r['family']].append(r)
lines=['# Forsk Technologies Page Structure Map','','Generated from the current repository after the initial dummy-data cleanup pass.','',f'Total root HTML pages: **{len(rows)}**.','', '## Page families','']
for k in sorted(fams): lines.append(f'- **{k}**: {len(fams[k])} pages')
lines += ['', '## Shared structure', '', '- Shared theme shell: head assets, desktop/mobile navigation, main content, CTA/footer areas, and local JS.', '- Core content pages use Elementor-exported section wrappers plus page-specific sections.', '- Service-detail pages share a service hero/detail/process/outcome/CTA/footer pattern.', '- Project-detail pages share project overview/requirement/result/similar-project shell; these are noindex until real project data is approved.', '- Blog list/category/tag/archive pages share listing/sidebar/CTA/footer patterns.', '- Team, pricing, portfolio and legacy index pages are noindex while template-only facts are being replaced.', '', '## All pages', '']
for r in rows:
 h=' / '.join(r['h1']) if r['h1'] else '(no H1 in source)'
 lines.append(f"- `{r['file']}` — {r['family']} — sections: {r['section_count']} — H1: {h} — noindex: {'YES' if r['noindex'] else 'NO'}")
(ROOT/'docs'/'page-structure-map.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('mapped',len(rows),'pages across',len(fams),'families')
