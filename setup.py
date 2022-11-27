from setuptools import setup, find_packages

with open('requirements.txt') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs]

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="iibflix",
    version="0.0.1",
    author="Bikash Karmokar",
    author_email="bikash_kuet@yahoo.com",
    packages=find_packages(),
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[install_requires],
    entry_points={
        'console_scripts': [
            'iibflix = cli.__main__:app',
        ],
    },
)


# python3 setup.py sdist bdist_wheel
