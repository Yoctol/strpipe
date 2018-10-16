from pathlib import Path

from setuptools import setup, find_packages
from setuptools import Extension

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
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
    ext_modules = [
        Extension(
            name='strpipe.toolkit.consistent_hash',
            sources=[
                'strpipe/toolkit/consistent_hash.pxd',
                'strpipe/toolkit/consistent_hash.pyx',
                'strpipe/toolkit/MurmurHash3.cpp',
            ],
            extra_compile_args=['-O3'],
            language='c++'
        ),
        Extension(
            name='*',
            sources=['./**/*.pyx'],
            extra_compile_args=['-O3'],
        ),
    ]
    ext_modules = cythonize(ext_modules, exclude=['./setup_utils/**/*.pyx'])
    for e in ext_modules:
        e.cython_directives = {"embedsignature": True}
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
    version='0.4.5',
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
    packages=find_packages(exclude=('tests', 'setup_utils')),
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
