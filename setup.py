import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmc_post_processor",
    version="develop",
    author="The openmc post processor Development Team",
    author_email="mail@jshimwell.com",
    description="Convert OpenMC tallies into user friendly units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/openmc_post_processor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "openmc_post_processor": [
            # "requirements.txt",
            "README.md",
            "LICENSE.txt",
            "neutronics_units.txt",
        ]
    },
    install_requires=["pint"],
)
