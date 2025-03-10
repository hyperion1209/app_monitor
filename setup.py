from setuptools import find_namespace_packages, setup

INSTALL_REQUIREMENTS = [
    "requests",
    "types-requests",
    "httpx",
    "validators",
]


BUILD_REQUIREMENTS = [
    "flake8",
    "black",
    "mypy",
    "setuptools-scm",
    "wheel",
    "pytest",
    "pytest-cov",
    "pylint",
    "responses",
    "pytest-asyncio",
    "pytest-httpx",
]


DEV_REQUIREMENTS = [
    *BUILD_REQUIREMENTS,
    "ipython",
]


setup(
    name="app_monitor",
    use_scm_version={"write_to": "src/app_monitor/_version.py"},
    description=("App that monitors app response"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    package_data={"app_monitor": ["py.typed"]},
    python_requires=">=3.11",
    install_requires=INSTALL_REQUIREMENTS,
    extras_require={
        "testing": BUILD_REQUIREMENTS,
        "dev": DEV_REQUIREMENTS,
    },
    setup_requires=["wheel", "setuptools_scm"],
    scripts=[
        "run_monitor.py",
    ],
)
