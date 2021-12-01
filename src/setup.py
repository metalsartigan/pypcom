import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pcom',
    version='0.8',
    packages=setuptools.find_packages(),
    url='',
    license='MIT License',
    author='Jerther',
    author_email='jtheriault@metalsartigan.com',
    description='A basic PCOM implementation in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
