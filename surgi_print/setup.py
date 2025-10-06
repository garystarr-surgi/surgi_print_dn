from setuptools import setup, find_packages

setup(
    name='surgi_print',
    version='0.0.5',
    description='CUPS direct printing for Delivery Notes.',
    author='Gary Starr',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
