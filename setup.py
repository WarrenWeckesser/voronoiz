from setuptools import setup


setup(
    name='voronoiz',
    version='0.1.0',
    author='Warren Weckesser',
    description="Functions for generating Voronoi diagrams with "
                "alternate metrics.",
    license="MIT",
    url="https://github.com/WarrenWeckesser/voronoiz",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="voronoi",
    packages=['voronoiz'],
    install_requires=['scipy', 'shapely']
)
