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


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node = []
        matches = extract_markdown_images(node.text)
        remaining_text = node.text
        for alt, url in matches:
            full_match = f"![{alt}]({url})"
            before, after = remaining_text.split(full_match, 1)
            if before != "":
                split_node.append(TextNode(before, TextType.TEXT))
            split_node.append(TextNode(alt, TextType.IMAGE, url=url))
            remaining_text = after
        if remaining_text:
            split_node.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_node)

    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node = []
        matches = extract_markdown_links(node.text)
        remaining_text = node.text
        for link_text, href in matches:
            full_match = f"[{link_text}]({href})"
            before, after = remaining_text.split(full_match, 1)
            if before != "":
                split_node.append(TextNode(before, TextType.TEXT))
            split_node.append(TextNode(link_text, TextType.LINK, url=href))
            remaining_text = after
        if remaining_text:
            split_node.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_node)
    
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


if __name__ == "__main__":
    nodes = [TextNode("This is **bold** text", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    for node in result:
        print(node.text, node.text_type)
    print(result)