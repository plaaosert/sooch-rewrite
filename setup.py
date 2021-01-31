from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="sooch",
    version="2.0.0",
    description="Sooch Discord bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plaaosert/sooch-rewrite/",
    author="Plaaosert and Sooch Devs",
    packages=find_packages(),
    install_requires=[
        "discord.py",
        "psycopg2-binary",
        "mysql-connector-python"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)
