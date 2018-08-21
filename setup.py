from pathlib import Path

from setuptools import setup, find_packages
# from setuptools import Extension

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
            long_description = convert_text(long_description, 'rst', format='md')
        except ImportError:
            print("warning: pypandoc module not found, could not convert Markdown to RST")
else:
    long_description = '-'

cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        # Extension('uttut.elements', ['uttut/elements.pyx']),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        # Extension('uttut.elements', ['uttut/elements.c']),
    ]

setup(
    name='strpipe',
    version='0.1.0',
    description='Reversible String Process Pipeline',
    long_description=long_description,
    python_requires='>=3.6',
    packages=find_packages(),
    author='Yoctol Info',
    author_email='cph@yoctol.com',
    url='https://github.com/Yoctol/strpipe',
    license='MIT',
    install_requires=[],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
