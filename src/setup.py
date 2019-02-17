# coding=UTF-8

from setuptools import find_packages, setup

from catlogs import VERSION



setup(
    name="catlogs",
    version=VERSION,
    author="François Trahan",
    author_email="francois.trahan@gmail.com",
    urt="https://github.com/francoistrahan/catlogs",

    packages=find_packages(exclude=["test"]),

    entry_points={
        'console_scripts': [
            'catlogs = catlogs.__main__:main',
            ],
        },

    )
