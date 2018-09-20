import argparse
import os
from pyfiglet import Figlet
from directorycleaner.color_print import BColors

DESCRIPTION = """Will put all known file types in sub folders inside a parent
folder named whatever you specify(it is DirectoryCleaner(<current-date>) by default)."""

DIRNAMES= {
    "data": os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/extensions.json"),
    "main": os.path.abspath(__file__)
}

def main():
    try:
        f = Figlet()
        welcome_message = f.renderText('Directory Cleaner')
        welcome_message = BColors.OKGREEN + welcome_message + BColors.ENDC
        print(welcome_message + "\nIf at any time you wish to exit the program simply type control + c")

        parser = argparse.ArgumentParser(description=DESCRIPTION)
        from directorycleaner import DirectoryCleaner

        directory_cleaner = DirectoryCleaner(parser=parser)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
