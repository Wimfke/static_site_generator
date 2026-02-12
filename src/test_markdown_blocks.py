import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
from textnode import TextNode, TextType


class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_single_block(self):
            md = "This is a single paragraph."
            self.assertEqual(markdown_to_blocks(md), ["This is a single paragraph."])

        def test_multiple_blocks(self):
            md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
            self.assertEqual(
                markdown_to_blocks(md),
                ["First paragraph.", "Second paragraph.", "Third paragraph."]
            )

        def test_blocks_with_extra_whitespace(self):
            md = "  Leading and trailing spaces   \n\n  Another block  "
            self.assertEqual(
                markdown_to_blocks(md),
                ["Leading and trailing spaces", "Another block"]
            )

        def test_empty_lines_ignored(self):
            md = "\n\nFirst block\n\n\n\nSecond block\n\n"
            self.assertEqual(
                markdown_to_blocks(md),
                ["First block", "Second block"]
            )

        def test_markdown_to_blocks_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        # ---- HEADING ----

        def test_heading_level_1(self):
            block = "# Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        def test_heading_level_6(self):
            block = "###### Deep Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        def test_heading_without_space_not_valid(self):
            block = "###Invalid"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_heading_more_than_6_hashes_not_valid(self):
            block = "####### Too many"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ---- CODE ----

        def test_code_block(self):
            block = "```\nprint('hello')\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)

        def test_code_block_single_line_not_valid(self):
            block = "```code```"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ---- QUOTE ----

        def test_quote_single_line(self):
            block = "> This is a quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        def test_quote_multiline(self):
            block = "> line one\n> line two"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        def test_quote_mixed_invalid(self):
            block = "> line one\nnormal line"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ---- UNORDERED LIST ----

        def test_unordered_list(self):
            block = "- item one\n- item two\n- item three"
            self.assertEqual(block_to_block_type(block), BlockType.ULIST)

        def test_unordered_list_missing_space_invalid(self):
            block = "-item one\n-item two"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_unordered_list_mixed_invalid(self):
            block = "- item one\nnot a list item"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ---- ORDERED LIST ----

        def test_ordered_list_valid(self):
            block = "1. First\n2. Second\n3. Third"
            self.assertEqual(block_to_block_type(block), BlockType.OLIST)

        def test_ordered_list_not_starting_at_1_invalid(self):
            block = "2. First\n3. Second"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_ordered_list_not_incrementing_invalid(self):
            block = "1. First\n3. Second"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_ordered_list_missing_space_invalid(self):
            block = "1.First\n2.Second"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ---- PARAGRAPH ----

        def test_regular_paragraph(self):
            block = "This is just a normal paragraph."
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_paragraph_with_symbols(self):
            block = "This # is not a heading because no space."
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_block_to_block_types(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            block = "- list\n- items"
            self.assertEqual(block_to_block_type(block), BlockType.ULIST)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.OLIST)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_paragraph(self):
            md = "Hello world"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<p>Hello world</p>", html)

        def test_heading(self):
            md = "# Title"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<h1>Title</h1>", html)

        def test_quote(self):
            md = "> Hello\n> World"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<blockquote>Hello World</blockquote>", html)

        def test_code_block(self):
            md = "```\nprint('hi')\n```"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<pre>", html)
            self.assertIn("print('hi')", html)

        def test_unordered_list(self):
            md = "- One\n- Two\n- Three"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<ul>", html)
            self.assertIn("<li>One</li>", html)
            self.assertIn("<li>Two</li>", html)
            self.assertIn("<li>Three</li>", html)

        def test_ordered_list(self):
            md = "1. First\n2. Second\n3. Third"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<ol>", html)
            self.assertIn("<li>First</li>", html)
            self.assertIn("<li>Second</li>", html)
            self.assertIn("<li>Third</li>", html)

        def test_multiple_blocks(self):
            md = "# Title\n\nHello\n\n- A\n- B"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertIn("<h1>Title</h1>", html)
            self.assertIn("<p>Hello</p>", html)
            self.assertIn("<ul>", html)



if __name__ == "__main__":
      unittest.main()