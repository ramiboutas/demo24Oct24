from django.test import SimpleTestCase

from .markdown_extras import markdown


class TestTemplateTags(SimpleTestCase):
    def test_markdown(self):
        content = "# This is a heading\n\nAnd this a text body"
        out = markdown(content)
        self.assertIn("<h1", out)
