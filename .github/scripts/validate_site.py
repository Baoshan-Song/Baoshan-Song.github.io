"""Check rendered research pages and their internal destinations after Jekyll builds."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

SITE = Path('_site')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids, self.classes, self.video_ids = [], [], [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        self.classes.extend(attrs.get('class', '').split())
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if 'data-video-id' in attrs:
            self.video_ids.append(attrs['data-video-id'])


def destination(path):
    relative = unquote(path).lstrip('/')
    file = SITE / relative
    return file / 'index.html' if file.is_dir() else file


for route in ('videos', 'open-source', 'publications'):
    file = SITE / route / 'index.html'
    assert file.is_file(), f'Missing page: {route}'
    page = Page(file)
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {route}'
    for required in ('/videos/', '/open-source/', '/publications/'):
        assert any(urlsplit(link).path == required for link in page.links), (route, required)
    for link in page.links:
        assert link.strip(), f'Empty link on {route}'
        url = urlsplit(link)
        if url.scheme in ('mailto', 'tel') or (url.netloc and url.netloc != 'baoshan-song.github.io'):
            continue
        target = destination(url.path) if url.path.startswith('/') else file if not url.path else file.parent / url.path
        assert target.is_file(), f'Broken internal link on {route}: {link}'
        if url.fragment and url.path.startswith('/videos'):
            assert unquote(url.fragment) in Page(target).ids, f'Broken video deep link: {link}'
    if route == 'videos':
        assert len(page.video_ids) == len(set(page.video_ids)) == 7
        assert all(re.fullmatch(r'[A-Za-z0-9_-]{11}', video) for video in page.video_ids)
        assert {'tutorials', 'talks', 'demos'} <= set(page.ids)
    if route == 'open-source':
        assert page.classes.count('resource-card') == 4
    if route == 'publications':
        assert page.classes.count('publication-card') == len(list(Path('_publications').glob('*.md')))
        assert {'manuscripts', 'conferences', 'preprints'} <= set(page.ids)
        assert 'Initialization-Free LEO Doppler Positioning' in file.read_text()
        assert 'Towards Certifiable State Estimation under Observability Degeneracy' in file.read_text()
print('Verified research pages, 7 videos, 4 projects, all publications, and internal links.')
