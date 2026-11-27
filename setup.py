from setuptools import find_packages, setup

setup(
    name="sublation",
    version="0.4.1",
    description="Non-boolean truth structures for dialectical reasoning, an alternative to boolean binarism, inspired by Hegelian logic.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.12",
    license="MIT",
    license_files=["LICENSE"],
    author="Germano Castanho",
    author_email="germanocastanho@proton.me",
    url="https://github.com/germanocastanho/sublation-lib",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"sublation": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
