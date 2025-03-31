from setuptools import setup, find_packages

setup(
    name="buero",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.2",
        "cryptography==42.0.5",
        "requests==2.31.0",
        "pycryptodome==3.20.0",
        "pytest==8.0.2",
        "python-dotenv==1.0.1",
    ],
    python_requires=">=3.8",
) 