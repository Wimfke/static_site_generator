import unittest
from functions import (
    markdown_to_blocks,
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


if __name__ == "__main__":
      unittest.main()