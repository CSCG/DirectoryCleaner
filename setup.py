from setuptools import setup, find_packages

setup(
    name = "DirectoryCleaner",
    version = "0.1",
    description = "An easy to use program that will clean a specified directory by placing all loose files in one folder with specified sub folders.",
    author = "Danny Canter",
    packages = find_packages(),
    include_package_data = True,
    license = "MIT",
    install_requires = [
        "tqdm >= 4.25.0",
        "pyfiglet >= 0.7.5"
    ],
    extras_require = {
        "Scraper": ["beautifulsoup4 >= 4.6.3", "requests >= 2.19.1"],
    }
    entry_points = {
        'console_scripts': [
            'DirectoryCleaner = main:main',
        ],
    }
)
