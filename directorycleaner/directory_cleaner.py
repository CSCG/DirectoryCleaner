import os
import re
import sys
import json
import datetime
from tqdm import tqdm
from .settings import Settings
from .color_print import BColors
from main import DIRNAMES

class DirectoryCleaner(Settings):
    """
    Heart of the program. Pass in argparse object and add arguments directly to class.
    """
    def __init__(self, parser):
        """
        File names and full paths of those stored in this list.
        Tuple of names and paths. Uses the great scandir added to 3.5
        to get full paths.
        """
        self.files_info = []

        self.directory = ''
        self.main_folder_name = False
        self.folder_cleanup = False
        self.change_folder_names = False
        self.group_files = False
        self.revert_settings = False

        args = self.register_args(parser)
        self.run(args)

        # jimmy = self.check_extensions()
        # print(jimmy)


    def run(self, args):
        """
        Starts program
        """
        self.set_vars(args)
        self.extensions = self.open_extensions()
        self.call_flags()
        self.open_dir()


    def register_args(self, parser):
        """
        All arguments for Directory Cleaner
        """
        parser.add_argument('path', type=str, nargs=1, help='The path to the directory that you want to cleanup not actually the word path. Ex. DirectoryCleaner /Users/Username/desktop')
        parser.add_argument('--folder_cleanup', '-fc', action='store_const', const=True, help='Set this flag if you want folders to also be included in the clean up.')
        parser.add_argument('--main_folder_name', '-mfm', action='store_const', const=True, help='Set this flag and specify the name you would like the main folder to be called. The date will always be apart of the name, only DirectoryCleaner will be changed.')
        parser.add_argument('--revert_settings', '-rs', action='store_const', const=True, help='Revert the settings file to its default state when the program was downloaded. Will use the default settings to run the program as well.')
        parser.add_argument('--group_files', '-gf', action='store_const', const=True, help='Set this flag if you would like to group commonly used files like Word Docs, Excel files, PDFs, music files etc. in folders named after the type of media they are.')
        parser.add_argument('--change_folder_names', '-cfn', action='store_const', const=True, help='Set this flag if you want to rename one of the default folder names Directory Cleaner uses for that type of file.')
        args = parser.parse_args()
        return args


    def open_dir(self):
        """
        Opens the directory the user specified. If file_names and full_paths are not empty
        this means that the user has already run this method, and thus they're only here
        because they entered the wrong path and arrived back here from double_check.
        If this is the case file_names and full_paths are emptied.
        """
        if len(self.files_info) > 0:
            self.files_info = []

        try:
            print("\n" + BColors.HEADER + "Opening files..." + BColors.ENDC)
            files = os.scandir(self.directory)
            print("\n" + BColors.OKGREEN + "Files succesfully opened." + BColors.ENDC)
            for file in files:
                file_tuple = (file.name, file.path)
                self.files_info.append(file_tuple)
        except FileNotFoundError:
                print("\n" + BColors.FAIL + "ERROR: The directory you entered could not be found." + BColors.ENDC)
                sys.exit(1)
        self.double_check()


    def call_flags(self):
        """
        This is a horrible implementation. Will most likely rework
        the flag variables to be stored in a dict and programmatically
        call these methods.
        """
        if self.revert_settings:
            self.revert_settings()

        if self.change_folder_names:
            self.change_folder_name()

        if self.main_folder_name:
            self.change_main_folder()


    def set_vars(self, args):
        """
        Sets cmdline vars passed in to instance variables.
        """
        print(args)
        self.directory = args.path[0]

        if args.folder_cleanup:
            self.folder_cleanup = True
        elif args.folder_cleanup == None:
            self.folder_cleanup = False

        if args.main_folder_name:
            self.main_folder_name = True
        elif args.change_folder_names == None:
            self.change_folder_names == False

        if args.change_folder_names:
            self.change_folder_names = True
        elif args.change_folder_names == None:
            self.change_folder_names == False


    def double_check(self):
        """
        Presents a double check to the user on if the directory entered is the correct one
        and if they would like to change it.
        """
        print("\n\n" + BColors.OKBLUE + "Directory Cleaner is about to clean this directory. Are you sure " + self.directory + " is the directory you want cleaned? Here's a short preview of some of the files in this directory..." + BColors.ENDC)
        print("----------------------------------------")

        if len(self.files_info) < 20:
            for file in self.files_info:
                print(f"{file[0]}")
        else:
            for i in range(20):
                print(f"{self.files_info[i][0]}")
        print("----------------------------------------")

        while True:
            response = input("\n" + BColors.OKBLUE + "Enter 'yes' or 'y' if this is correct else enter 'no' or 'n' if it is not: " + BColors.ENDC)
            response = response.strip()

            if response in Settings.ANSWERS["yes"]:
                return
            elif response in Settings.ANSWERS["no"]:
                new_dir = input("\n" + BColors.OKBLUE + "Please enter the new path of the directory you would like to be cleaned: " + BColors.ENDC)
                self.directory = new_dir.strip()
                self.open_dir()
                return
            else:
                print("\n" + BColors.FAIL + "ERROR: The input received was not a valid option. Please read the options again." + BColors.ENDC)


    """
    Huge thanks to https://www.online-convert.com/file-type as this is where the file extensions
    data came from.
    """
    def check_extensions(self):
        results = {
                    "total": 0,
                    "folders": [],
                    "success": [],
                    "success_percent": 0,
                    "error": [],
                    "error_percent": 0
                 }

        """
        Fairly straightforward. folder_cleanup variable determines whether folders get cleaned up as well.
        They will be moved to a 'Folders' folder. If the program is used more than once in a day and a
        DirectoryCleaner folder already exists in the directory it will be ignored so a clear hierarchy can
        be seen. So if the program was run and DirectoryCleaner(date) exists and in the same day the
        program is ran again, (1)DirectoryCleaner(date) will be made but DirectoryCleaner(date) will still
        be in the same directory and not be moved to the new folder.
        """
        for file in self.files_info:
            if self.folder_cleanup:
                try:
                    if os.path.isdir(file[0]):
                        print(file[0], "is a folder.")
                        results["success"].append(file)
                        results["folders"].append(file)
                        results["total"] += 1
                    elif file[0].split(".")[1] in EXTENSIONS["extensions"]:
                         print(file[0], "is a", EXTENSIONS["extensions"][file[0].split(".")[1]])
                         results["success"].append(file)
                         results["total"] += 1
                    else:
                        results["error"].append(file)
                        results["total"] += 1
                except:
                    results["error"].append(file)
            else:
                try:
                    if file.split(".")[1] in EXTENSIONS["extensions"]:
                        print(file, "is a", EXTENSIONS["extensions"][file.split(".")[1]])
                        results["success"].append(file)
                        results["total"] += 1
                    else:
                        results["error"].append(file)
                        results["total"] += 1
                except:
                    results["error"].append(file)

        results["success_percent"] = len(results["success"]) / results["total"] * 100.00
        results["error_percent"] = len(results["error"]) / results["total"] * 100.00
        # make_dirs(results["success"], directory)
        return results


    def dir_regex(self):
        pattern = re.compile(r".*\(\d+\)" + self.folder_name + ".*")
        match = pattern.match("()" + folder_name + "(")
        return match


    """Load extensions into dict from JSON file. File is generated from
    scraper.py. If you ever want to go back to the
    default settings simply use the command --revertsettings."""
    def open_extensions(self):
        try:
            print("\n" + BColors.HEADER + "Opening settings." + BColors.ENDC)
            with open(DIRNAMES["data"], "r") as f:
                extensions = json.load(f)
        except FileNotFoundError:
            print("Data file could not be located. Please make sure 'extensions.json' is in the 'Data' directory.")
            sys.exit(1)
        print("\n" + BColors.OKGREEN + "Settings succesfully opened." + BColors.ENDC)
        return extensions


    def make_dirs(self, files, directory, nameOfFile, folder_cleanup):
        """Will make all the required folders to store the files in the directory, will make
        a 'Folders' folder depending on the corresponding folder_cleanup flag passed in. If a DirectoryCleaner folder
        has already been made it will check and add a corresponding integer after the folder name.
        Ex: If DirectoryCleaner(2018-8-23) exists it will instead make (1)DirectoryCleaner(2018-8-23) and so on
        and so forth."""

        #Matches repeat folders i.e (digits)DirectoryCleaner so all repeat folders. Explained above.
        pattern = re.compile(r".*\(\d+\)" + nameOfFile + ".*")
        for file in files:
            i = 0
            dir_cleaner_folder = os.path.join(directory, "DirectoryCleaner(" + str(datetime.date.today()) + ")")

        try:
            os.makedirs(dir_cleaner_folder)
        except FileExistsError:
            os.makedirs(dir_cleaner_folder)

        for file in files:
            new_dir = os.path.join(directory, EXTENSIONS["extensions"][file.split(".")[1]])
            try:
                os.makedirs(new_dir)
                os.rename(os.path.join(directory, file), os.path.join(new_dir, file))
            except FileExistsError:
                print("The directory", os.path.join(directory, EXTENSIONS["extensions"][file.split(".")[1]]), "already exists.")
                os.rename(os.path.join(directory, file), os.path.join(new_dir, file))


    def final_output(self, results):
        print("""\nFile type checking complete

        Results:
        ----------
        Success: {0}
        Error: {1}
        Success %: {2:.1f}%
        Error %: {3:.1f}%
        """.format(results["success"], results["error"], results["success_percent"], results["error_percent"]))
