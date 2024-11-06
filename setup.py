from setuptools import setup, find_packages

setup(
    name="pynetuse",               # Name of the package
    version="1.0.0",                # Version of the package
    author="Matej Barton",
    author_email="info@mjvbarton.cz",
    description="A python wrapper for Windows net use",
    long_description=open("README.md").read(),  # Optional: add README.md content
    long_description_content_type="text/markdown",  # Type of README (e.g., Markdown)
    url="https://github.com/username/mypackage",  # URL to the project
    packages=find_packages(),        # Automatically find package directories
    install_requires=[               # List of dependencies
        "numpy>=1.18.0",             # Example dependency
        "requests>=2.20.0"
    ],
    classifiers=[                    # Optional: metadata for searchability on PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
