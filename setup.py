from setuptools import setup, find_packages

setup(
    name="Framework_Core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.0",
        "pytest-xdist>=3.3.1",
        "allure-pytest>=2.13.2",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "jsonpath>=0.82",
        "loguru>=0.7.0",
        "pymysql>=1.1.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A pytest-based API automation testing framework with Allure reporting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
) 