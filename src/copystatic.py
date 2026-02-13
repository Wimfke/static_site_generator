import os
import shutil


def copy_static(static, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    items = os.listdir(static)
    
    for item in items:
        src_path = os.path.join(static, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copying file: {src_path} -> {dst_path}")
        else:
            copy_static(src_path, dst_path)