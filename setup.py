# setup.py

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="termux-remember",
    version="1.1.2",
    author="Mallik Mohammad Musaddiq",
    author_email="mallikmusaddiq1@gmail.com",
    description="A secure and POSIX-style CLI note keeper for Termux users with tagging and password protection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mallikmusaddiq1/termux-remember",
    packages=find_packages(),  # Automatically find all Python packages in the source directory
    entry_points={
        "console_scripts": [
            "remember=termux_remember.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "Topic :: Terminals"
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=13.0.0"
    ],
    include_package_data=True,
    license="MIT",
    keywords=[
        "termux", "notes", "cli", "secure", "password", "tagging", "posix"
    ],
    project_urls={
        "Homepage": "https://github.com/mallikmusaddiq1/termux-remember",
        "Repository": "https://github.com/mallikmusaddiq1/termux-remember",
        "Issues": "https://github.com/mallikmusaddiq1/termux-remember/issues"
    }
)