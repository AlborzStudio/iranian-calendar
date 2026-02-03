"""
Setup configuration for Iranian Calendar package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iranian-calendar",
    version="1.0.0",
    author="Iranian Calendar Project",
    author_email="",
    description="Iranian Calendar (IC) - Solar calendar with epoch at 3000 BCE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (all built-in)
    ],
    extras_require={
        "astro": ["ephem>=4.1.4"],  # For astronomical calculations
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    entry_points={
        "console_scripts": [
            "ic=ic.cli:main",
        ],
    },
)
