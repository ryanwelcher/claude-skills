import os
import re
import unittest

PAGE = os.path.join(os.path.dirname(__file__), "..", "scripts", "page.html")


class PageTest(unittest.TestCase):
    def test_page_static(self):
        with open(PAGE, encoding="utf-8") as f:
            page = f.read()
        self.assertNotIn("—", page)
        self.assertEqual(re.findall(r'(?:src|href)\s*=\s*["\']https?:', page), [])
        for ref in ("/api/state", "/api/render", "/api/stop", "/proxy.mp4", "/api/shorts",
                    "/api/shorts/preview", "/api/shorts/draft", "/api/shorts/captions", "/api/shorts/render"):
            self.assertIn(ref, page)
        # Shorts render progress: per clip and overall.
        self.assertIn('id="shorts-progress"', page)
        self.assertIn("st.percent", page)
        self.assertIn("Making the audio", page)
        # Streams tab and Show in Finder.
        for ref in ('id="tab-streams"', 'id="streams-view"', "/api/streams", "/api/reveal",
                    "Show in Finder", "navigator.clipboard", 'id="reveal-final"', 'id="reveal-shorts"'):
            self.assertIn(ref, page)
        # Title picker, early shorts, finding progress.
        for ref in ("/api/title", "SH.titles", 'id="finding"', 'id="final-title"', "Use this title",
                    "Outside your trim", "Transcribing"):
            self.assertIn(ref, page)
        self.assertNotIn('id="tab-shorts" disabled', page)
        # The "Claude needs you in the terminal" banner.
        for ref in ("/api/attention", 'id="attention"', "document.title"):
            self.assertIn(ref, page)
        # The profile name shows next to the recording.
        self.assertIn('id="profile"', page)
        self.assertIn("S.profile", page)
        # Suggested caption fixes start ticked and applied.
        self.assertIn('class="sugg" data-i="${i}" checked', page)
        self.assertIn("accepted: Object.fromEntries(sugg)", page)


if __name__ == "__main__":
    unittest.main()
