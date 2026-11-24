import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'docs/index.html').read_text(encoding='utf-8')
JS=(ROOT/'docs/app.js').read_text(encoding='utf-8')
CSS=(ROOT/'docs/style.css').read_text(encoding='utf-8')

class LinkParser(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.ids=set();self.labels=[]
    def handle_starttag(self, tag, attrs):
        attributes=dict(attrs)
        if 'id' in attributes: self.ids.add(attributes['id'])
        if tag in ('a','script','link'):
            href=attributes.get('href') or attributes.get('src')
            if href: self.links.append(href)

class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parse=LinkParser();cls.parse.feed(HTML)
    def test_static_site_exists(self):
        self.assertTrue((ROOT/'docs/.nojekyll').exists())
        self.assertTrue((ROOT/'docs/pdf/antigravity-guide.pdf').exists())
        self.assertGreater((ROOT/'docs/pdf/antigravity-guide.pdf').stat().st_size,10000)
    def test_all_paths_local_exist(self):
        for url in self.parse.links:
            if url.startswith('./'):
                self.assertTrue((ROOT/'docs'/url[2:]).exists(), url)
            if url.startswith('#'):
                self.assertIn(url[1:],self.parse.ids,url)
    def test_expected_modules(self):
        self.assertEqual(HTML.count('class="lesson-card"'),12)
        self.assertEqual(HTML.count('class="prompt-item"'),18)
        self.assertEqual(HTML.count('class="day-card"'),7)
        self.assertEqual(len(list((ROOT/'guides').glob('*.md'))),12)
    def test_accessible_controls(self):
        self.assertIn('for="lessonSearch"',HTML)
        self.assertIn('aria-expanded="false"',HTML)
        self.assertIn('prefers-reduced-motion',CSS)
        self.assertIn('label for="genGoal"',HTML)
    def test_relative_paths_no_external_trackers(self):
        for banned in ['google-analytics.com','googletagmanager.com','hotjar','fbq(','api.mixpanel.com']:
            self.assertNotIn(banned,HTML+JS)
        self.assertNotIn('fetch(',JS)
        self.assertNotIn('XMLHttpRequest',JS)
        self.assertIn('localStorage',JS)
    def test_authorship_and_disclosure(self):
        self.assertIn('AI 酋长 Andy',HTML)
        self.assertIn('非 Google 官方',HTML)
        self.assertIn('metaver.vip',HTML)
        self.assertIn('AIPMAndy',HTML)
        self.assertIn('https://www.a6no1.cn/',HTML)
    def test_new_interaction_controls(self):
        for key in ['undoProgress','lessonReset','promptReset','lessonCount','promptCount','genStatus']:
            self.assertIn(key,self.parse.ids)
        self.assertIn('aria-valuenow="0"',HTML)
        self.assertIn('copyGenerated.disabled=true',JS)
        self.assertIn('signature()!==snapshot',JS)
        self.assertIn('replaceProgress(safe',JS)
        self.assertIn('lesson-search:focus-within',CSS)
        self.assertIn('transition:none!important',CSS)

if __name__=='__main__': unittest.main()
