from setuptools import setup, find_packages

setup(
    name='pevy',
    version='0.0.1',
    description='Pieter en Evy 2017',
    # url='https://github.com/pypa/sampleproject',
    # author='The Python Packaging Authority',
    # author_email='pypa-dev@googlegroups.com',
    license='MIT',
    packages=['pevy', 'pevy.sources'],
    install_requires=['requests', 'python-twitter'],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pevy=pevy:main',
        ],
    },
)
