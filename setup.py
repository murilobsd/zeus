"""
Zeus
--------------

Fast create scaffold of flask.
"""

from setuptools import setup

setup(
    name="zeus-lab804",
    version="0.1.2",
    url="https://github.com/murilobsd/zeus",
    license="BSD",
    description="Fast create scaffold of flask.",
    author="Lab804",
    author_email="contato@lab804.com.br",
    long_description=__doc__,
    include_package_data=False,
    packages=["zeusproject"],
    zip_safe=False,
    platforms="any",
    install_requires=[
        "colorama==0.3.7",
        "colorlog==2.7.0",
        "Jinja2==2.11.3",
        "MarkupSafe==0.23",
        "pyfiglet==0.7.5",
        "termcolor==1.1.0",
        "pytest==2.9.2"
    ],
    scripts=["zeus"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
