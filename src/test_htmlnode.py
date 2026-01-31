import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1_node = LeafNode("b", "Bold")
        child2_node = LeafNode(None, "Normal")
        child3_node = LeafNode("i", "Italic")
        parent_node = ParentNode("div", [child1_node, child2_node, child3_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>Bold</b>Normal<i>Italic</i></div>",
        )

    def test_to_html_with_multiple_parents_and_children(self):
        greatgrandchild_node = LeafNode("li", "Subitem")
        grandchild1_node = LeafNode(None, "Item 2")
        grandchild2_node = ParentNode("ul", [greatgrandchild_node])
        child1_node = LeafNode("li", "Item 1")
        child2_node = ParentNode("li", [grandchild1_node, grandchild2_node])
        parent_node = ParentNode("ul", [child1_node, child2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2<ul><li>Subitem</li></ul></li></ul>",
        )

    def test_to_html_with_child_and_props(self):
        child_node = LeafNode(None, "Click me")
        parent_node = ParentNode("a", [child_node], props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            parent_node.to_html(),
            '<a href="https://boot.dev" target="_blank">Click me</a>'
        )

    def test_monster_node_to_html(self):
        # LeafNodes op het eerste niveau
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, "Normal")
        leaf3 = LeafNode("i", "Italic")

        # Diepere ParentNode-structuur
        inner_leaf1 = LeafNode("p", "Paragraph")
        inner_leaf2 = LeafNode(None, "Text")
        inner_leaf3 = LeafNode(None, "More Text")
        inner_leaf4 = LeafNode(None, "Even More Text")
        inner_leaf5 = LeafNode(None, "Click me")

        inner_a_node = ParentNode(
            "a",
            [inner_leaf5],
            props={"href": "https://boot.dev"}
        )

        inner_span2 = ParentNode(
            "span",
            [inner_leaf3, inner_leaf4, inner_a_node]
        )

        inner_span1 = ParentNode(
            "span",
            [inner_leaf2, inner_span2]
        )

        section_node = ParentNode(
            "section",
            [inner_leaf1, inner_span1]
        )

        monster_node = ParentNode(
            "div",
            [leaf1, leaf2, leaf3, section_node]
        )

        expected_html = (
            "<div>"
            "<b>Bold</b>Normal<i>Italic</i>"
            "<section>"
            "<p>Paragraph</p>"
            "<span>"
            "Text"
            "<span>"
            "More TextEven More Text"
            '<a href="https://boot.dev">Click me</a>'
            "</span>"
            "</span>"
            "</section>"
            "</div>"
        )

        self.assertEqual(monster_node.to_html(), expected_html)




if __name__ == "__main__":
    unittest.main()