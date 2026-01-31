from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


dummy_node = TextNode(
    "This is some anchor text",
    TextType.LINK,
    "https://www.boot.dev"
)

dummy_leaf = LeafNode(
    "p",
    "Dit is een paragraaf",
    {"href": "https://www.google.com"}
)

html_leaf = dummy_leaf.to_html()

print(dummy_node)
print(dummy_leaf)
print(html_leaf)