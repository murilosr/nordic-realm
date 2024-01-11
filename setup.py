from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Web framework for FastAPI'
LONG_DESCRIPTION = 'Web framework for FastAPI'

# Setting up
setup(
       # the name must match the folder name 'b'
        name="nordic_realm",
        version=VERSION,
        author="Murilo Rocha",
        author_email="<libs@thorson.tech>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['web', 'fastapi'],
        classifiers= [
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)