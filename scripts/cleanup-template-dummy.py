from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ADDRESS = '122/67, Madhyam Marg, Sector 12, Mansarovar, Jaipur, Rajasthan 302020'
EMAIL = 'info@forsktechnologies.com'
PHONE = '+91 9610967825'

LEGACY_ARTICLES = {
    'cloud-security-best-practices-company-should-know.html',
    'future-proofing-your-business-with-cloud-modernization.html',
    'harnessing-the-power-of-ai-and-machine-learning-in-business.html',
    'hello-world.html',
    'innovation-in-action-how-consulting-firms-foster-creative-solutions.html',
    'insider-perspectives-on-it-solutions-with-techco-thought-leaders.html',
    'leading-the-digital-age-with-groundbreaking-it-technologies.html',
    'seamless-integration-of-hybrid-and-multi-cloud-environments.html',
    'the-next-big-thing-quantum-computing-and-its-business-applications.html',
    'top-cloud-migration-strategies-for-growing-businesses.html',
    'transforming-your-business-with-consulting-to-drive-operational-excellence.html',
    'unlocking-new-possibilities-with-advanced-cloud-computing-solutions.html',
}

def matching_end(text, start, tag):
    token = re.compile(rf'<\/?{tag}\b[^>]*>', re.I)
    depth = 0
    for m in token.finditer(text, start):
        depth += -1 if m.group(0).lstrip().startswith('</') else 1
        if depth == 0:
            return m.end()
    return None

def nearest_ancestor_start(text, pos, tag, class_token=None):
    token = re.compile(rf'<\/?{tag}\b[^>]*>', re.I)
    stack = []
    for m in token.finditer(text, 0, pos):
        if m.group(0).lstrip().startswith('</'):
            if stack:
                stack.pop()
        else:
            stack.append(m)
    for m in reversed(stack):
        if class_token is None or class_token in m.group(0):
            return m.start()
    return None

def remove_nearest(text, marker, tag='section', class_token=None):
    pos = text.find(marker)
    if pos < 0:
        return text
    start = nearest_ancestor_start(text, pos, tag, class_token)
    if start is None:
        return text
    end = matching_end(text, start, tag)
    return text[:start] + text[end:] if end else text

def ensure_noindex(text):
    if re.search(r'<meta\s+name=["\']robots["\']', text, re.I):
        return re.sub(r'<meta\s+name=["\']robots["\'][^>]*>', '<meta name="robots" content="noindex,follow">', text, count=1, flags=re.I)
    return re.sub(r'(<meta\s+name=["\']viewport["\'][^>]*>)', r'\1\n<meta name="robots" content="noindex,follow">', text, count=1, flags=re.I)

def replace_visible_brand(text):
    parts = re.split(r'(<[^>]+>)', text)
    blocked = 0
    for i, part in enumerate(parts):
        if not part.startswith('<'):
            if not blocked:
                parts[i] = re.sub(r'\bTechco\b', 'Forsk Technologies', part, flags=re.I)
            continue
        low = part.lower().lstrip()
        if re.match(r'<(?:script|style)\b', low):
            blocked += 1
        elif re.match(r'</(?:script|style)\b', low):
            blocked = max(0, blocked - 1)
    return ''.join(parts)

def quarantine(name):
    return (
        name.startswith(('project-', 'archive-', 'author-', 'category-', 'tag-', 'blog'))
        or name in {'portfolio.html', 'pricing.html', 'team.html', 'team-details.html', 'index-old.html'}
        or name in LEGACY_ARTICLES
    )

for p in sorted(ROOT.glob('*.html')):
    t = p.read_text(encoding='utf-8', errors='ignore')

    replacements = {
        'Techco@gmail.com': EMAIL,
        'techco@gmail.com': EMAIL,
        'Techco@example.com': EMAIL,
        'gmail.@example.com': EMAIL,
        'eaxmple@techco.com': EMAIL,
        'work@techco.com': EMAIL,
        '+(1) 1230 452 8597': PHONE,
        '+1 573 343 4096': PHONE,
        '+15733434096': PHONE,
        '+420) 318 568 511': PHONE,
        '+8250-3560 6565': PHONE,
        '+88(0) 555-0108': PHONE,
        '+88(0) 555-01117': PHONE,
        '+880-1680-6361-89': PHONE,
        '+8801680636189': PHONE,
        'Waterloo, Park, Australia': ADDRESS,
        'Sunshine Business Park Sector-94, Poland': ADDRESS,
        'Sunshine Business Park': ADDRESS,
        'Las Vegas, NV, USA': ADDRESS,
        '201 Spear Street, San Francisco, CA, USA': ADDRESS,
        'Maverick Phoenix': 'Forsk Technologies',
        'CEO At Techco': 'Technology Services',
        'As a CEO at Techco I have been voice crying in the wilderness, trying to make requirements clear, use every minute to deliver the result, and not reinvent the wheel. Here at Techco, I made that possible for the clients.': 'Software, web, mobile, cloud and consulting services aligned to business requirements.',
        'From <b>200+</b> reviews': 'Technology consultation',
        'From 200+ reviews': 'Technology consultation',
        'We’re Hiring': 'Contact Us',
        "We're Hiring": 'Contact Us',
        'Astarte Medical': 'Technology Services',
        'href="project-astarte-medical.html"': 'href="services.html"',
        'Read Case': 'View Services',
        'Empowering Success Through Strategic Consulting Since 2001': 'Empowering Businesses Through Strategic Technology Consulting',
        'loved by 50K+ Clients across the World': 'Cloud solutions for modern businesses',
    }
    for old, new in replacements.items():
        t = t.replace(old, new)

    t = re.sub(r'Augustenstra.{0,180}?Munich,\s*Bavaria,\s*Example', ADDRESS, t, flags=re.I|re.S)
    t = re.sub(r'<li>\s*<a href="#">\s*<span class="icon_list_text">\s*201 Spear Street,?\s*</span>\s*</a>\s*</li>', '', t, flags=re.I|re.S)
    t = re.sub(r'<li>\s*<a href="#">\s*<span class="icon_list_text">\s*San Francisco, CA, USA\s*</span>\s*</a>\s*</li>', '', t, flags=re.I|re.S)
    t = re.sub(r'(?:<p>)?\s*Developed by\s*<a[^>]*xpressbuddy\.com[^>]*>XpressBuddy</a>\s*(?:</p>)?', '', t, flags=re.I|re.S)
    t = re.sub(r'\s*<(?:meta|link)\b[^>]*wp\.xpressbuddy\.com[^>]*>\s*', '\n', t, flags=re.I)
    t = re.sub(r'/\*#\s*sourceURL=https://wp\.xpressbuddy\.com/techco/.*?\*/', '', t, flags=re.I)

    if p.name in {'index.html', 'business-consulting.html'}:
        t = remove_nearest(t, 'Happy Customer', 'div', 'funfact_block')
        t = remove_nearest(t, 'Company Value', 'div', 'funfact_block')
        t = remove_nearest(t, 'Brands We Collaborate With', 'section')
        t = remove_nearest(t, 'Few Stories from our Client', 'section')

    if p.name == 'about.html':
        t = remove_nearest(t, 'Top Skilled Experts', 'section')
        t = remove_nearest(t, 'Results Guaranteed', 'div', 'funfact_block')
        t = remove_nearest(t, '12000+', 'div', 'our_world_employees')

    if p.name == 'software-company.html':
        t = remove_nearest(t, 'Happy Customer', 'div', 'about_funfact_info')
        t = remove_nearest(t, 'Our latest Case Studies', 'section')
        t = remove_nearest(t, 'Board Member, UNIQA', 'section')

    if p.name == 'ai-machine-learning.html':
        t = remove_nearest(t, 'What Techco Lover Are Aaying', 'section')
        t = remove_nearest(t, 'The hands-on projects gave me the confidence', 'div', 'ml_testimonial')

    if p.name == 'cloud-solutions.html':
        t = remove_nearest(t, 'Featured Success Stories', 'section')
        t = remove_nearest(t, 'Our Recognition & Awards', 'section')

    if p.name.startswith('project-'):
        t = re.sub(r'<li>\s*<span class="icon_list_text">\s*<strong[^>]*>\s*(?:Client:|Location:|Completed Date:)\s*</strong>.*?</span>\s*</li>', '', t, flags=re.I|re.S)

    if quarantine(p.name):
        t = ensure_noindex(t)
    else:
        t = replace_visible_brand(t)

    p.write_text(t, encoding='utf-8', newline='\n')

print('safe dummy cleanup complete')
