#!/usr/bin/env python3
"""
Setup script for PII Deidentification Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pii-deidentifier",
    version="1.0.0",
    author="Research Team",
    author_email="research@example.com",
    description="A tool for deidentifying PII in markdown files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pii-deidentifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "deidentify-pii=deidentify_pii:main",
        ],
    },
    scripts=["deidentify_pii.py"],
    include_package_data=True,
    package_data={
        "": ["README.md", "LICENSE"],
    },
    keywords="pii deidentification anonymization privacy markdown research",
    project_urls={
        "Bug Reports": "https://github.com/your-username/pii-deidentifier/issues",
        "Source": "https://github.com/your-username/pii-deidentifier",
        "Documentation": "https://github.com/your-username/pii-deidentifier#readme",
    },
)