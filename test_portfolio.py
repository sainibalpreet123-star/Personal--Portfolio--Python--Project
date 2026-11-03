"""Automated tests for the portfolio generator.  Run:  python -m unittest -v"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import build_portfolio as bp


def base_profile():
    return bp.load_profile(bp.BASE / "profile.json")


class PortfolioTests(unittest.TestCase):
    def build(self, profile):
        tmp = Path(tempfile.mkdtemp())
        pf = tmp / "profile.json"
        pf.write_text(json.dumps(profile), encoding="utf-8")
        result = bp.build_site(pf, tmp / "site")
        return tmp / "site", result

    def test_01_files_created(self):
        out, _ = self.build(base_profile())
        for name in ("index.html", "style.css", "assets/skills.png"):
            self.assertTrue((out / name).exists(), name)

    def test_02_content_present(self):
        p = base_profile()
        out, _ = self.build(p)
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn(p["name"], html)
        for pr in p["projects"]:
            self.assertIn(pr["title"], html)
        for s in p["skills"]:
            self.assertIn(s["name"], html)

    def test_03_html_is_escaped(self):
        p = base_profile()
        p["name"] = "<script>alert(1)</script>"
        out, _ = self.build(p)
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_04_unsafe_link_rejected(self):
        p = base_profile()
        p["projects"][0]["url"] = "javascript:alert(1)"
        with self.assertRaises(ValueError):
            bp.validate_profile(p)

    def test_05_missing_field_rejected(self):
        p = base_profile()
        del p["about"]
        with self.assertRaises(ValueError):
            bp.validate_profile(p)

    def test_06_skill_level_range(self):
        p = base_profile()
        p["skills"][0]["level"] = 120
        with self.assertRaises(ValueError):
            bp.validate_profile(p)

    def test_07_project_without_link_has_no_anchor(self):
        p = copy.deepcopy(base_profile())
        out, res = self.build(p)
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count("View project"), sum(1 for x in p["projects"] if x["url"]))
        self.assertTrue(any("no link" in w for w in res["warnings"]))

    def test_08_placeholder_warning(self):
        warnings = bp.validate_profile(base_profile())
        self.assertTrue(any("placeholder" in w for w in warnings))

    def test_09_invalid_json_reported(self):
        tmp = Path(tempfile.mkdtemp()) / "bad.json"
        tmp.write_text("{ not valid json", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            bp.load_profile(tmp)

    def test_10_navigation_anchors_exist(self):
        import re
        out, _ = self.build(base_profile())
        html = (out / "index.html").read_text(encoding="utf-8")
        anchors = set(re.findall(r'href="#([a-z]+)"', html))
        ids = set(re.findall(r'id="([a-z]+)"', html))
        self.assertTrue(anchors)
        self.assertTrue(anchors <= ids, anchors - ids)

    def test_11_images_have_alt_text(self):
        import re
        out, _ = self.build(base_profile())
        html = (out / "index.html").read_text(encoding="utf-8")
        for tag in re.findall(r"<img[^>]*>", html):
            self.assertIn("alt=", tag)


if __name__ == "__main__":
    unittest.main()
