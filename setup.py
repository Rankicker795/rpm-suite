"""Configuration to install rpm-suite  package"""

from setuptools import setup

setup(
    name='rpmsuite',
    version='1.0',
    packages=['rpmsuite'],
    url='https://github.com/Rankicker795/rpm-suite',
    license='',
    author='Roger Allen',
    author_email='roger.allen795@gmail.com',
    description='Python Tool for creating a Gantt chart from a JSON file',
    install_requires=['setuptools',
                      'pandas',
                      'bokeh',
                      ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        ],
    entry_points={
        'console_scripts': [
            'rpmgantt=rpmsuite.gantt:main'
            ]
        },
    )
