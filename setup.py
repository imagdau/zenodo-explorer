from setuptools import setup, find_packages

setup(
    name='zenodoExplorer',
    version='1.0.0',
    url='https://github.com/imagdau/zenodo-explorer.git',
    author='Ioan-Bogdan Magdau',
    author_email='Ioan.Magdau@newcastle.ac.uk',
    description='Thin package for accessing the "Exploratory testbed for MLIPs" Zenodo community',
    packages=find_packages(),
    install_requires=[
        "tqdm"
    ]
)

