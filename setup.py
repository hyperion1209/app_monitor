from setuptools import find_namespace_packages, setup

INSTALL_REQUIREMENTS = []


BUILD_REQUIREMENTS = [
    "flake8",
    "black",
    "mypy",
    "setuptools-scm",
    "wheel",
    "pytest",
    "pytest-cov",
    "pylint",
]


DOCS_REQUIREMENTS = []


DEV_REQUIREMENTS = [
    *BUILD_REQUIREMENTS,
    *DOCS_REQUIREMENTS,
    "ipython>=7.4.0",
    "jedi<0.18",
]


def _get_bitbucket_repo_url(repository: str, project: str = "NETAUTO") -> str:
    return (
        "https://bitbucket.workday.com/projects/" f"{project}/repos/{repository}/browse"
    )


setup(
    name="app_monitor",
    use_scm_version={"write_to": "src/app_monitor/_version.py"},
    description=("App that monitors app response"),
    license="Proprietary",
    maintainer="Workday NetAuto",
    maintainer_email="netauto.team@workday.com",
    download_url=_get_bitbucket_repo_url("app_monitor"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    package_data={"app_monitor": ["py.typed"]},
    python_requires=">=3.11",
    install_requires=INSTALL_REQUIREMENTS,
    extras_require={
        "testing": BUILD_REQUIREMENTS,
        "dev": DEV_REQUIREMENTS,
        "docs": DOCS_REQUIREMENTS,
    },
    setup_requires=["wheel", "setuptools_scm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: Other/Proprietary License",
    ],
)
