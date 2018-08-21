from pathlib import Path

from setuptools import setup

readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
else:
    long_description = '-'

setup(
    name='strpipe',
    version='0.1.0',
    description='Reversible String Process Pipeline',
    long_description=long_description,
    python_requires='>=3.6',
    packages=[
        'strpipe',
    ],
    author='Yoctol Info',
    author_email='cph@yoctol.com',
    url='https://github.com/samuelcolvin/arq',
    license='MIT',
    install_requires=[],
)
