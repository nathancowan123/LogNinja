from setuptools import setup, find_packages

setup(
    name="logninja_core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="Nathan Cowan",
    description="A powerful logging utility for Python applications",
    url="https://github.com/nathancowan123/LogNinja-Core",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
