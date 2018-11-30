from pathlib import Path
import os


def remove_so_files():
    so_paths = sorted(
        Path('./strpipe').rglob(
            "*.cpython-36m-x86_64-linux-gnu.so",
        ),
    )
    c_paths = sorted(Path('./strpipe').rglob("*.c"))
    cpp_paths = sorted(Path('./strpipe').rglob("*.cpp"))

    for path in so_paths:
        os.remove(str(path.resolve()))

    for path in c_paths:
        os.remove(str(path.resolve()))

    for path in cpp_paths:
        if str(path) != 'strpipe/toolkit/MurmurHash3.cpp':
            os.remove(str(path.resolve()))

if __name__ == '__main__':
    remove_so_files()
