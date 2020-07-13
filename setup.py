from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="KivyAuth",
    version="1.0",
    packages=["kivyauth"],
    package_data={"kivyauth": ["*.py"],},
    # metadata to display on PyPI
    author="Shashi Ranjan",
    author_email="shashiranjankv@gmail.com",
    description="Integrate Google, Facebook, Github & Twitter login in kivy applications ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="social-login google-login facebook-login firebase-auth kivy-application kivy python",
    url="https://github.com/shashi278/social-auth-kivy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
    ],
    install_requires=["kivy",],
    python_requires=">=3.6",
)
