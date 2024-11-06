from setuptools import setup, find_packages

setup(
    name="pynetuse",               
    version="1.0.0",       
    author="Matej Barton",
    author_email="info@mjvbarton.cz",
    description="A python wrapper for Windows net use",
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",  
    url="https://github.com/mjvbarton/pynetuse",  
    packages=find_packages(),
    install_requires=[               
        "numpy>=1.18.0",
        "requests>=2.20.0"
    ],
    classifiers=[             
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires=">=3.6",
)
