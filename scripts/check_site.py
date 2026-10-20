"""Check the built site without network access: python scripts/check_site.py _site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urljoin
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
origin = 'https://thisisjskim.github.io'
errors = []
pages = {}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.figures = 0
        self.math = 0
        self.titles = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                errors.append(f'duplicate ID: {self.path}: {a["id"]}')
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.titles += 1
        if tag == 'figure': self.figures += 1
        if 'math-inline' in a.get('class', ''): self.math += 1
        for attr in ('href', 'src'):
            if a.get(attr): self.links.append(a[attr])
        if tag == 'img' and 'alt' not in a:
            errors.append(f'image without alt text: {self.path}')

for path in root.rglob('*.html'):
    p = Page()
    p.path = path.relative_to(root).as_posix()
    text = path.read_text(encoding='utf-8')
    p.feed(text)
    pages[p.path] = p
    if p.titles != 1: errors.append(f'{p.path}: expected one title')
    if p.path != 'publications/index.html' and not (p.path.startswith('paper-notes/') and p.path != 'paper-notes/index.html') and p.h1 != 1:
        errors.append(f'{p.path}: expected one h1, got {p.h1}')
    for marker in ('notion-file-block://', '<unknown ', 'X-Amz-Signature', 'Your Sidebar Name', 'Red Brick University', 'none@example.org'):
        if marker in text: errors.append(f'{p.path}: unmigrated or placeholder content: {marker}')
    if '{: #section-' in text:
        errors.append(f'{p.path}: unprocessed heading anchor')
    for m in re.findall(r'<span class="math-inline">(.*?)</span>', text, re.S):
        if not m.startswith('\\(') or not m.endswith('\\)'):
            errors.append(f'{p.path}: lost TeX delimiters: {m[:60]}')

for rel, page in pages.items():
    page_url = origin + '/' + (rel[:-10] if rel.endswith('index.html') else rel)
    for link in page.links:
        url = urlparse(urljoin(page_url, link))
        if url.scheme not in ('http', 'https') or url.netloc != 'thisisjskim.github.io':
            continue
        path = unquote(url.path).lstrip('/')
        target = root / path
        if target.is_dir(): target /= 'index.html'
        if not target.is_file():
            errors.append(f'{rel}: missing local target: {link}')
            continue
        if url.fragment and target.suffix == '.html':
            dest = pages.get(target.relative_to(root).as_posix())
            if dest and unquote(url.fragment) not in dest.ids:
                errors.append(f'{rel}: missing anchor: {link}')

notes = [p for key, p in pages.items() if key.startswith('paper-notes/') and key != 'paper-notes/index.html']
if len(notes) != 6: errors.append(f'expected 6 notes, got {len(notes)}')
if sum(p.figures for p in notes) != 52: errors.append('expected 52 migrated figures')
if not all((root / p).is_file() for p in ('index.html', 'cv/index.html', 'paper-notes/index.html', '404.html', 'sitemap.xml')):
    errors.append('missing required page or sitemap')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(pages)} HTML pages, {len(notes)} notes, 52 figures, {sum(p.math for p in notes)} inline equations; local targets, anchors, metadata and placeholders checked.')
