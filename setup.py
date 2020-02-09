import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kali-source-updater",
    version="1.0",
    author="Steffin",
    author_email="steffinstanly@gmail.com",
    description="A script for updating kali linux source list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steffinstanly/Kali-Source-Updater",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	install_requires=[
          'requests',
      	],
)
