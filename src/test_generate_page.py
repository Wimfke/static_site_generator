import unittest

from generate_page import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        result = extract_title("# Hello")
        self.assertEqual("Hello", result)

    def test_extract_title_multiple_headings(self):
        markdown = """
# Heading 1
# Heading 2
"""
        result = extract_title(markdown)
        self.assertEqual(
            "Heading 1",
            result
        )

    def test_extract_title_h2_first(self):
        markdown = """
## Heading 1
# Heading 2
"""
        result = extract_title(markdown)
        self.assertEqual(
            "Heading 2",
            result
        )
    
    def test_extract_title_cleaned_whitespace(self):
        markdown = """
#    Hello   
"""
        result = extract_title(markdown)
        self.assertEqual(
            "Hello",
            result
        )

    def test_no_h1(self):
        markdown = "## Just a subtitle"
        with self.assertRaises(ValueError):
            extract_title(markdown)