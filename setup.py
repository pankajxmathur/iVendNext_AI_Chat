from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="ivendnext_ai_chat",
    version="0.0.1",
    description="Production-ready AI Chatbot for Frappe Framework",
    author="iVendNext",
    author_email="info@ivendnext.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
