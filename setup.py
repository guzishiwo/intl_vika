from setuptools import setup, find_packages

setup(
    name='intl_vika',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'vika'
    ],
    entry_points={
        'console_scripts': [
            'intl_vika = intl_vika.main:cli',
        ],
    },
)