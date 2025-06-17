# setup.py

from setuptools import setup, find_packages

setup(
    name="termux-remember",
    version="1.1.1",
    author="Mallik Mohammad Musaddiq",
    author_email="mallikmusaddiq1@gmail.com",
    description="Secure CLI note keeper for Termux with tagging and password protection",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mallikmusaddiq1/termux-remember",
    packages=find_packages(),  # finds all modules in termux_remember/
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
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    include_package_data=True,
)