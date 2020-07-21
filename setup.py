from setuptools import setup, find_packages

import gpumonitor

setup(
    name=gpumonitor.__name__,
    version=gpumonitor.__version__,
    author=gpumonitor.__author__,
    author_email=gpumonitor.__email__,
    description=gpumonitor.__description__,
    url=gpumonitor.__url__,
    license=gpumonitor.__license__,
    long_description=gpumonitor.__doc__,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['gpumonitor=gpumonitor:main'],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
)
