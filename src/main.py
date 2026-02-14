import os
import sys
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

src = "static"
dst = "docs"
content = "content"
template = "template.html"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Copying static files to public directory...")
    copy_files_recursive(src, dst)

    generate_pages_recursive(content, template, dst, basepath)


if __name__ == "__main__":
    main()