from setuptools import setup
import os, re

with open("README.md", "r") as fh:
    long_description = fh.read()


def is_android():
    if "ANDROID_BOOTLOGO" in os.environ:
        return True
    return False


def get_version() -> str:
    """Get __version__ from __init__.py file."""
    version_file = os.path.join(os.path.dirname(__file__), "kivyauth", "__init__.py")
    version_file_data = open(version_file, "rt", encoding="utf-8").read()
    version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
    try:
        version = re.findall(version_regex, version_file_data, re.M)[0]
        return version
    except IndexError:
        raise ValueError(f"Unable to find version string in {version_file}.")


setup(
    name="KivyAuth",
    version=get_version(),
    packages=["kivyauth"],
    package_data={"kivyauth": ["*.py", "desktop/*", "android/*"],},
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
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent"
    ],
    install_requires=["kivy>=2.0.0", "oauthlib", "werkzeug==2.0.3", "flask==2.0.3", "requests"]
    if not is_android()
    else [],
    python_requires=">=3.6",
)
