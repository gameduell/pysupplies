from setuptools import setup, find_packages

setup(
    name = "pysupplies",
    version = "0.1",
    packages = find_packages(),
    scripts = [],
    package_data = {
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "wabu",
    author_email = "wabu@fooserv.net",
    description = "supplies for our python infrastructions with annotation, cooperative typing and more",
    license = "MIT",
    keywords = "python tools utils",
    url = "https://github.com/gameduell/pysupplies",
)
