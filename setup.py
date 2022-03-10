from setuptools import find_packages, setup

setup(
    name='blog_api',
    version='0.0.1',
    description='Hatchways Backend Assessment',
    author='Hasar Ali',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)