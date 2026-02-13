import os
import shutil

from copystatic import copy_static

src = "static"
dst = "public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    print("Copying static files to public directory...")
    copy_static(src, dst)


if __name__ == "__main__":
    main()