from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    requirements_list = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and line != '-e .':
                    requirements_list.append(line)
    except FileNotFoundError:
        print("requirements.txt file not found. Please make sure it exists in the project directory.")
    return requirements_list


setup(
    name="Networksecurity",
    version="0.0.1",
    author="yeabsira",
    author_email="yeabsira@example.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
