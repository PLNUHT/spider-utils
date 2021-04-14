import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with  open("requirements.txt") as freq:
    for line in freq.readlines():
        requirements.append( line.strip() )

setuptools.setup(
    name="spider-utils",
    version="0.0.5",
    author="a710128",
    author_email="qbjooo@qq.com",
    description="spider utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PLNUHT/spider-utils/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "spider_utils": [
            "ualist.txt",
        ]
    },
)
