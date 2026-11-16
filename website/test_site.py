"""AI Security Lab 정적 홈페이지 회귀 검사 (Python 표준 라이브러리만 사용)."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

INDEX = Path(__file__).with_name("index.html")
REQUIRED_IDS = {"main", "top", "research", "workflow", "projects", "contact"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.tags = []
        self.heading_counts = {"h1": 0, "h2": 0}
        self.nav_labels = []
        self.meta = {}
        self.external_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        if tag in self.heading_counts:
            self.heading_counts[tag] += 1
        if tag == "nav":
            self.nav_labels.append(attrs.get("aria-label"))
        if tag == "meta" and attrs.get("name"):
            self.meta[attrs["name"]] = attrs.get("content")
        if tag in {"script", "iframe", "link", "img"} and attrs.get("src", attrs.get("href", "")).startswith(("http://", "https://")):
            self.external_assets.append((tag, attrs))


class WebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.page = PageParser()
        cls.page.feed(cls.html)

    def test_korean_document_and_title(self):
        self.assertIn('<html lang="ko">', self.html)
        self.assertIn("<title>AI Security Lab | AI보안 연구소</title>", self.html)
        self.assertIn("description", self.page.meta)

    def test_sections_exist_and_have_unique_ids(self):
        self.assertTrue(REQUIRED_IDS <= set(self.page.ids))
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))

    def test_internal_links_resolve(self):
        for a in self.page.links:
            target = a.get("href", "")
            if target.startswith("#"):
                self.assertIn(target[1:], self.page.ids, f"깨진 내부 링크: {target}")

    def test_heading_and_landmarks(self):
        self.assertEqual(self.page.heading_counts["h1"], 1)
        self.assertGreaterEqual(self.page.heading_counts["h2"], 4)
        self.assertIn("main", self.page.tags)
        self.assertIn("주요 메뉴", self.page.nav_labels)
        self.assertTrue(any(a.get("href") == "#main" for a in self.page.links))

    def test_safe_external_links(self):
        for a in self.page.links:
            href = a.get("href", "")
            self.assertFalse(href.startswith("http://"), href)
            if href.startswith("https://"):
                self.assertEqual(a.get("target"), "_blank")
                self.assertIn("noopener", a.get("rel", "").split())
                self.assertIn("noreferrer", a.get("rel", "").split())

    def test_no_paid_or_remote_runtime_dependencies(self):
        self.assertFalse(self.page.external_assets)
        self.assertNotIn("<script", self.html.lower())
        self.assertNotIn("<form", self.html.lower())
        self.assertNotIn("@import", self.html)

    def test_responsive_accessibility(self):
        self.assertIn("width=device-width", self.page.meta.get("viewport", ""))
        self.assertIn("@media (max-width:640px)", self.html)
        self.assertIn("prefers-reduced-motion", self.html)
        self.assertIn(":focus-visible", self.html)

    def test_repo_and_public_data_warning(self):
        self.assertIn("https://github.com/MetaStudy999/ai-security-lab-001", self.html)
        self.assertIn("개인정보·보안 비밀", self.html)
        self.assertIn("공식 홈페이지가 아닙니다", self.html)


if __name__ == "__main__":
    unittest.main()
