import setuptools
from mccli.options import OPTIONS

with open("README.md") as file:
    long_description = file.read()

setuptools.setup(
    name="mccli",
    version=OPTIONS["version"],
    author="Alve Svarén",
    author_email="alve@hotmail.se",
    description="A feature-rich command line interface for minecraft servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alvesvaren/mccli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
