from enum import Enum


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