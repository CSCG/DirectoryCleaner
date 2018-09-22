from setuptools import setup, find_packages

setup(
    name = "DirectoryCleaner",
    version = "0.1",
    description = "An easy to use program that will clean a specified directory by placing all loose files in one folder with specified sub folders.",
    author = "Danny Canter",
    packages = find_packages(),
    # include_package_data = True,
    license = "MIT",
    url="https://github.com/Cantasaurus/DirectoryCleaner",
    install_requires = [
        "tqdm >= 4.25.0",
        "pyfiglet >= 0.7.5"
    ],
    data_files=[
    ("", ["LICENSE.txt", "README.md"])
    ],
    package_data={
        "": ["data/*.json", "scripts/*.py", "tests/*.py"],
    },
    extras_require = {
        "Scraper": ["beautifulsoup4 >= 4.6.3", "requests >= 2.19.1"],
    },
    entry_points = {
        'console_scripts': [
            'DirectoryCleaner = directorycleaner.main:main',
        ],
    }
)
