import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pero",
    version='0.0.1',
    author="Sherevv",
    author_email="sherevv@gmail.com",
    description="Graphic pen based on matplotlib",
    long_description=long_description,
    include_package_data=True,
    url="https://github.com/sherevv/pero",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'numpy==1.14.3',
        'matplotlib==2.2.2'
    ]
)