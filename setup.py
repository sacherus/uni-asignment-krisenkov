from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

setup(
    author="Pawel Kopec",
    author_email="pawel@airspace-intelligence.com",
    name="uni-assignment-metars",
    version="1.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        str(x.req) for x in parse_requirements("requirements.txt", session="install")
    ],
    license="Uni Intelligence",
    url="https://github.com/uni-intelligence/uni-assignment-metars",
)
