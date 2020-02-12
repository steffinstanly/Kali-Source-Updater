import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kali-source-updater",
    version="1.2",
    author="Steffin Stanly",
    author_email="steffinstanly@gmail.com",
    description="A script for updating kali linux source list based on the latency",
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
    entry_points={
         'console_scripts': [
              'kali-source-updater=kali_source_updater.kali_updater:main'
         ]
      },
)





