import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

src = "static"
dst = "public"
content = "content"
template = "template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    print("Copying static files to public directory...")
    copy_files_recursive(src, dst)

    generate_pages_recursive(content, template, dst)


if __name__ == "__main__":
    main()