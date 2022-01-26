from setuptools import setup, find_packages

from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError


# Configuration is in setup.cfg
setup(
    name="data-transform-api",
    url="https://github.com/firewut/data-transform-pipelines-api",
    version=1.0,
    license="MIT",
    description="Data Transformation Pipelines API Backend",
    author="Andrew Chibisov",
    author_email="andrey844@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(".", exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=[
        "celery==5.1",
        "coreapi==2.3.3",
        "django-filter==21.1",
        "django-rest-framework==0.1.0",
        "django==4.0.1",
        "djangorestframework-queryfields==1.0.0",
        "djangorestframework==3.13.1",
        "flock==0.1",
        "jsonschema==4.4.0",
        "markdown2==2.4.2",
        "mock==4.0.3",
        "numpy==1.22.1",
        "opencv-python==4.5.5.62",
        "psycopg2==2.9.3",
        "python-magic==0.4.24",
        "python-resize-image==1.1.20",
        "readability-lxml==0.8.1",
        "Redis==4.1.1",
        "requests==2.27.1",
        "textblob==0.17.1",
        "uwsgi==2.0.20",
        "xlsxwriter==3.0.2",
    ],
)
