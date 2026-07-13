"""generators/render_html.py için davranış testleri (stdlib unittest, ek bağımlılık yok)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generators import render_html


def _minimal_lesson(notes):
    return {
        "day": 1, "total_days": 20, "week": 1, "slug": "x", "title": "Başlık",
        "tagline": "tagline", "tier": None, "date_label": "2026",
        "intro": "intro", "flow": [], "prerequisites": [], "tools_needed": [],
        "objectives": [], "sections": [],
        "challenge": {
            "title": "Challenge", "task": "task", "requirements": [], "success": [],
            "solution": {
                "intro": "sol-intro", "prompts": [], "notes": notes, "pitfalls": [],
            },
        },
        "takeaways": [], "reading": {}, "next_preview": "next", "checklist": [],
    }


class SolutionNotesRendering(unittest.TestCase):
    def test_single_line_note_renders_as_plain_list_item(self):
        html = render_html.render(_minimal_lesson(["Tek satırlık not"]))
        self.assertIn("<li>Tek satırlık not</li>", html)

    def test_multiline_note_renders_first_line_plus_pre_block(self):
        note = "Beklenen dosya yapısı:\ncapstone-microservices/\n├── CLAUDE.md"
        html = render_html.render(_minimal_lesson([note]))
        self.assertIn("<li>Beklenen dosya yapısı:<pre><code>", html)
        self.assertIn("capstone-microservices/\n├── CLAUDE.md", html)


if __name__ == "__main__":
    unittest.main()
