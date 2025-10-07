from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="surgi_print",
    version="0.0.5",  # <-- make sure this matches __init__.py
    description="CUPS printing for Delivery Note",
    author="Gary Starr",
    author_email="gary.starr@surgishop.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
