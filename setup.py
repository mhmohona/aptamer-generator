from setuptools import setup, find_packages

setup(
    name='aptamer-generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'biopython',
    ],
    author='Mahfuza',
    description='A package for generating candidate aptamers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mhmohona/aptamer-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
