from setuptools import setup, find_packages

setup(
    name="batch_file_rename",
    version="0.1",
    description="A batch file renaming CLI tool",
    author="Marshall Jacobs",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
)