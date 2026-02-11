from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for num, part in enumerate(parts):
            if part == "":
                continue
            if num % 2 == 0:
                split_node.append(TextNode(part, TextType.TEXT))
            else:
                split_node.append(TextNode(part, text_type))
        new_nodes.extend(split_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


if __name__ == "__main__":
    nodes = [TextNode("This is **bold** text", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    for node in result:
        print(node.text, node.text_type)
    print(result)