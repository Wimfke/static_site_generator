import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://boot.dev", "target": "_blank"})
        expected_html = '<a href="https://boot.dev" target="_blank">Click me</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_raw_text(self):
        node = LeafNode(None, "Just text")
        expected_html = "Just text"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_different_value(self):
        node1 = LeafNode("p", "Hello")
        node2 = LeafNode("p", "Goodbye")
        self.assertNotEqual(node1.to_html(), node2.to_html())

    def test_repr_equality(self):
        node1 = LeafNode("p", "Hello", {"class": "primary"})
        node2 = LeafNode("p", "Hello", {"class": "primary"})
        self.assertEqual(node1.__repr__(), node2.__repr__())

    def test_repr_inequality(self):
        node1 = LeafNode("p", "Hello", {"class": "primary"})
        node2 = LeafNode("p", "Hello", {"class": "secondary"})
        self.assertNotEqual(node1.__repr__(), node2.__repr__())


if __name__ == "__main__":
    unittest.main()