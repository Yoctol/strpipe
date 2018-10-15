from pathlib import Path

from setuptools import setup, find_packages
from setuptools import Extension

from setup_utils.get_pxd_path import get_pxd_path

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True


readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
        try:
            from pypandoc import convert_text
            long_description = convert_text(
                long_description, 'rst', format='md')
        except ImportError:
            print("warning: pypandoc module not found, could not convert Markdown to RST")
else:
    long_description = '-'


cmdclass = {}
ext_modules = []


if use_cython:
    pyx_paths = sorted(Path('./strpipe').rglob("*.pyx"))

    for pyx_path in pyx_paths:
        pxd_path = get_pxd_path(pyx_path)
        if pxd_path is not None:
            sources = [str(pyx_path), str(pxd_path)]
        else:
            sources = [str(pyx_path)]

        first_line = pyx_path.read_text().split('\n')[0]
        if ('cpp' in first_line) or ('c++' in first_line):
            extension = Extension(
                str(pyx_path)[:-4].replace('/', '.'),
                sources,
                language='c++',
            )
        else:
            extension = Extension(
                str(pyx_path)[:-4].replace('/', '.'),
                sources,
            )

        # Have Cython embed function call signature information in docstrings,
        # so that Sphinx can extract and use those signatures.
        extension.cython_directives = {"embedsignature": True}
        ext_modules.append(extension)
    cmdclass.update({'build_ext': build_ext})

else:
    # .c files
    pyx_paths = sorted(Path('./strpipe').rglob("*.c"))
    for pyx_path in pyx_paths:
        path_str = str(pyx_path)
        ext_modules.append(
            Extension(
                path_str[:-2].replace('/', '.'),
                [path_str],
            )
        )

    # .cpp files
    pyx_paths = sorted(Path('./strpipe').rglob("*.cpp"))
    for pyx_path in pyx_paths:
        path_str = str(pyx_path)
        ext_modules.append(
            Extension(
                path_str[:-4].replace('/', '.'),
                [path_str],
            )
        )

setup(
    name='strpipe',
    version='0.4.2',
    description='Reversible String Process Pipeline',
    long_description=long_description,
    python_requires='>=3.6',
    author='Yoctol Info',
    author_email='cph@yoctol.com',
    url='https://github.com/Yoctol/strpipe',
    license='MIT',
    install_requires=[
        'tokenizer-hub',
        'text-normalizer',
    ],
    packages=find_packages(),
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
