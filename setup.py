from pathlib import Path

from setuptools import setup, find_packages
from setuptools import Extension


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
    ext_modules += [
        Extension(
            'strpipe.toolkit.compute_maxlen',
            ['strpipe/toolkit/compute_maxlen.pyx'],
        ),
        Extension(
            'strpipe.toolkit.consistent_hash',
            ['strpipe/toolkit/consistent_hash.pyx'],
            language='c++',
        ),
        Extension(
            'strpipe.toolkit.index_to_token',
            ['strpipe/toolkit/index_to_token.pyx'],
        ),
        Extension(
            'strpipe.toolkit.build_vocabulary',
            ['strpipe/toolkit/build_vocabulary.pyx'],
        ),
        Extension(
            'strpipe.toolkit.token_to_index',
            ['strpipe/toolkit/token_to_index.pyx'],
        ),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension(
            'strpipe.toolkit.compute_maxlen',
            ['strpipe/toolkit/compute_maxlen.c'],
        ),
        Extension(
            'strpipe.toolkit.consistent_hash',
            ['strpipe/toolkit/consistent_hash.cpp'],
        ),
        Extension(
            'strpipe.toolkit.index_to_token',
            ['strpipe/toolkit/index_to_token.c'],
        ),
        Extension(
            'strpipe.toolkit.build_vocabulary',
            ['strpipe/toolkit/build_vocabulary.c'],
        ),
        Extension(
            'strpipe.toolkit.token_to_index',
            ['strpipe/toolkit/token_to_index.c'],
        ),
    ]

setup(
    name='strpipe',
    version='0.1.0',
    description='Reversible String Process Pipeline',
    long_description=long_description,
    python_requires='>=3.6',
    author='Yoctol Info',
    author_email='cph@yoctol.com',
    url='https://github.com/Yoctol/strpipe',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
