import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"'
        )

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)
    
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()