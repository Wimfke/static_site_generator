import unittest
from functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://path_to_/image2.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://path_to_/image2.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links("This is a text without links")
        self.assertEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](www.boot.dev) and another [second link](www.yahoo.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "www.yahoo.com"),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        nodes = [
            TextNode("This is text with an ![image](www.image.info)", TextType.TEXT),
            TextNode("This is text with two pictures: ![picture1](www.pic1.com) and ![picture2](www.pic2.be)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.info"),
                TextNode("This is text with two pictures: ", TextType.TEXT),
                TextNode("picture1", TextType.IMAGE, "www.pic1.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("picture2", TextType.IMAGE, "www.pic2.be"),
            ],
            new_nodes
        )

    def test_image_at_start(self):
        node = TextNode("![img](url) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_non_text_node_unchanged(self):
        node = TextNode("image", TextType.IMAGE, "url")
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_image_then_link(self):
        node = TextNode(
            "![img](url) and [link](href)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)
        self.assertEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "href"),
            ],
            nodes,
        )

    def test_text_to_textnodes_all_options(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_text_to_textnodes_no_normal_text(self):
        text = "**BOLD**[link](www.boot.dev)_italic_![image](www.image.com)`code block`"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("BOLD", TextType.BOLD),
                TextNode("link", TextType.LINK, "www.boot.dev"),
                TextNode("italic", TextType.ITALIC),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode("code block", TextType.CODE),
            ],
            nodes
        )


if __name__ == "__main__":
    unittest.main()
