from setuptools import setup

setup(
    # Application name:
    name="Election 2016 Twitter Tracker",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Jason Florack",
    author_email="jasonflorack@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/jasonflorack/Election2016TwitterTracker.git",
    description="An app that searches Twitter for past and live tweets related to the 2016 US Presidential Election. "
                "Uses Tweepy.",

    # Dependent packages (distributions)
    install_requires=[
        "oauthlib >= 1.0",
        "requests >= 2.9",
        "requests-oauthlib >= 0.6",
        "six >= 1.10",
        "tweepy >= 3.5",
    ],
)