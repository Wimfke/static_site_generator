import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page

src = "static"
dst = "public"
content_index = "content/index.md"
template = "template.html"
dst_index = "public/index.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    print("Copying static files to public directory...")
    copy_files_recursive(src, dst)

    generate_page(content_index, template, dst_index)


if __name__ == "__main__":
    main()