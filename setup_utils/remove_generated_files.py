from pathlib import Path
import os


def remove_generated_c_cpp_files():
    c_paths = sorted(Path('./strpipe').rglob("*.c"))
    cpp_paths = sorted(Path('./strpipe').rglob("*.cpp"))
    all_paths = c_paths + cpp_paths

    for path in all_paths:
        if str(path) != 'strpipe/toolkit/MurmurHash3.cpp':
            os.remove(str(path.resolve()))


if __name__ == '__main__':
    remove_generated_c_cpp_files()
