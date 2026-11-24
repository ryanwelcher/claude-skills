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


if __name__ == "__main__":
    unittest.main()
