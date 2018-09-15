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
    #Just a fun welcome message when running the program.
    f = Figlet()
    welcome_message = f.renderText('Directory Cleaner')
    welcome_message = BColors.OKGREEN + welcome_message + BColors.ENDC
    print(welcome_message)

    #Pass parser object to DirectoryCleaner. Feels cleaner to declare the arguments in the class itself.
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    directory_cleaner = DirectoryCleaner(parser=parser)

if __name__ == "__main__":
    from directorycleaner import DirectoryCleaner

    #Don't print stack trace for control-c
    try:
        main()
    except KeyboardInterrupt:
        pass
