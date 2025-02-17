from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:
    requirement_list:List[str]=[]
    try:
        with open("requirements.txt") as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!="-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_list
setup(
    name="us_visa",
    version="0.0.1",
    author="Sivakumar",
    author_email="mshivakumarreddy78@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)