import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="growth_ptf_maker",
    version="1.0.0",
    author="Leonardo Urbano",
    author_email="leonardo.urbano87@libero.it",
    packages=setuptools.find_packages(),
    description="Creates a portfolio using the Gordon Growth Model and the DJIA components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/leourb/ggm-index-maker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)