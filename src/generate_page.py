import os

from markdown_blocks import markdown_to_html_node
from htmlnode import LeafNode


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
           return line[2:].strip()
    raise ValueError("Error: No title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace("{{ Content }}", html)
    template = template.replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)

        if os.path.isfile(from_path):
            if item.endswith(".md"):
                name, _ = os.path.splitext(item)
                dest_path = os.path.join(dest_dir_path, f"{name}.html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(from_path, template_path, new_dest_dir, basepath)