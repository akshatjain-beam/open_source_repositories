import os
import sys

from setuptools import find_packages, setup


long_description = ""
if os.path.exists("README.rst"):
    with open("README.rst") as f:
        long_description = f.read()

needs_sphinx = "build_sphinx" in sys.argv
sphinx_requirements = ["sphinx>=3.2.1", "sphinx_rtd_theme"] if needs_sphinx else []

setup(
    name="uncertain_panda",
    description="Calculate bootstrap uncertainties with pandas",
    url="http://github.com/nils-braun/uncertain_panda/",
    maintainer="Nils Braun",
    maintainer_email="nilslennartbraun@gmail.com",
    license="GPLv3+",
    long_description=long_description,
    long_description_content_type="text/rst",
    packages=find_packages(include=["uncertain_panda", "uncertain_panda.*"]),
    use_scm_version=True,
    python_requires=">=3.6",
    setup_requires=["setuptools_scm"] + sphinx_requirements,
    install_requires=[
        "pandas>=0.23.4",
        "uncertainties",
        "matplotlib",
        "dask[dataframe]"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "sphinx",
            "bumpversion"
        ]
    },
    command_options={"build_sphinx": {"source_dir": ("setup.py", "docs"),}},
)
