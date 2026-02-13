import os

from markdown_blocks import markdown_to_html_node
from htmlnode import LeafNode


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
           return line[2:].strip()
    raise ValueError("Error: No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    filled_template = template.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(filled_template)