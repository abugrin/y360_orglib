from setuptools import setup, find_packages

setup(
    name="y360-orglib",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Anton Bugrin",
    description="Unofficial Collection library for Y360 API",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourproject",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # зависимости вашей библиотеки
        "requests>=2.25.0",
    ],
)