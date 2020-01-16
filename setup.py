from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.rst')) as fin:
    long_description = fin.read()

setup(
    name='prettytype',
    version='0.2.0',
    description='Print types of nested structues',
    long_description=long_description,
    url='https://github.com/stuglaser/prettytype',
    author='Stu Glaser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
)
