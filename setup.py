import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    longa_priskribo = readme.read()

setuptools.setup(
    name="miavortaro",
    version="0.2-alpha",
    author="Alex Couch",
    author_email="alcouch65@gmail.com",
    description="Python-a libraro por interagi kun la servilo de MiaVortaro",
    long_description=longa_priskribo,
    url="https://github.com/alexcouch/miavortaro-py",
    project_urls=[
        "https://github.com/AlexCouch/miavortaro-py/issues",
        "https://alexcouch.github.io/miavortaro-py/build/"
    ],
    license="Apache 2.0",
    packages=["miavortaro"],
    install_requires=["requests"]
)