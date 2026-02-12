from enum import Enum
from htmlnode import LeafNode, ParentNode
from functions import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks: 
        stripped = block.strip()
        if stripped:
            clean_blocks.append(stripped) 
    return clean_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(tuple("#" * i + " " for i in range (1, 7))):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    ordered = True
    for num, line in enumerate(lines, 1):
        if not line.startswith(f"{num}. "):
            ordered = False
            break
    if ordered:
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_value = ""
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_string = html_node.to_html()
        html_value += html_string
    return html_value

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:    
            html = text_to_children(block.replace("\n", " "))
            children.append(LeafNode("p", html))

        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level+1:]
            html = text_to_children(text)
            children.append(LeafNode(f"h{level}", html))

        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1])
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                clean_lines.append(line[1:].strip())
            text = " ".join(clean_lines)
            html = text_to_children(text)
            children.append(LeafNode("blockquote", html))

        elif block_type == BlockType.ULIST:
            clean_lines = [line[2:] for line in block.split("\n")]
            items = []
            for clean_line in clean_lines:
                html = text_to_children(clean_line)
                items.append(LeafNode("li", html))
            children.append(ParentNode("ul", items))

        elif block_type == BlockType.OLIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                slice_index = line.index(".") + 2
                text = line[slice_index:]
                html = text_to_children(text)
                items.append(LeafNode("li", html))
            children.append(ParentNode("ol", items))
        
    return ParentNode("div", children)