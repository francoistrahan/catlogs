# coding=UTF-8

from setuptools import find_packages, setup

from catlog import VERSION



setup(
    name="catlog",
    version=VERSION,
    author="François Trahan",
    author_email="francois.trahan@gmail.com",

    packages=find_packages(exclude=["test"]),

    entry_points={
        'console_scripts': [
            'catlog = catlog.__main__:main',
            ],
        },

    )
