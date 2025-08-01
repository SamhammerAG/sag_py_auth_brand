import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fin:
    REQS = fin.read().splitlines()

with open("requirements-dev.txt", "r") as fin:
    REQS_DEV = [item for item in fin.read().splitlines() if not item.endswith(".txt")]

setuptools.setup(
    name="sag-py-auth-brand",
    version="1.2.3",
    description="Keycloak brand/instance authentication for python projects",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/SamhammerAG/sag_py_auth_brand",
    author="Samhammer AG",
    author_email="support@samhammer.de",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
    ],
    keywords="auth, fastapi, keycloak",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"sag_py_auth_brand": REQS_DEV},
    python_requires=">=3.12",
    install_requires=REQS,
    extras_require={"dev": ["pytest"]},
    project_urls={
        "Documentation": "https://github.com/SamhammerAG/sag_py_auth_brand",
        "Bug Reports": "https://github.com/SamhammerAG/sag_py_auth_brand/issues",
        "Source": "https://github.com/SamhammerAG/sag_py_auth_brand",
    },
)
