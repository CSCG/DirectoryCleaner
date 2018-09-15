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

        self.check_extensions()


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
        parser.add_argument('--main_folder_name', '-mfn', action='store_const', const=True, help='Set this flag and specify the name you would like the main folder to be called. The date will always be apart of the name, only DirectoryCleaner will be changed.')
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

        #If folder cleanup is not specified ignore folders.
        try:
            print("\n" + BColors.HEADER + "Opening files..." + BColors.ENDC)
            files = os.scandir(self.directory)
            print("\n" + BColors.OKGREEN + "Files succesfully opened." + BColors.ENDC)
            for file in files:
                if self.folder_cleanup:
                    file_tuple = (file.name, file.path)
                    self.files_info.append(file_tuple)
                else:
                    if os.path.isdir(file):
                        pass
                    else:
                        file_tuple = (file.name, file.path)
                        self.files_info.append(file_tuple)
        except FileNotFoundError:
                print("\n" + BColors.FAIL + "ERROR: The directory you entered could not be found." + BColors.ENDC)
                sys.exit(1)
        print(self.files_info)
        self.double_check()


    def call_flags(self):
        """
        This is a horrible implementation. Will most likely rework
        the flag variables to be stored in a dict and programmatically
        call these methods.
        """
        if self.revert_settings:
            self.default_settings()

        if self.change_folder_names:
            self.change_folder_name()

        if self.main_folder_name:
            self.change_main_folder()


    def set_vars(self, args):
        """
        Sets cmdline vars passed in to instance variables.
        """
        self.directory = args.path[0]

        if args.folder_cleanup:
            self.folder_cleanup = True
        elif args.folder_cleanup == None:
            self.folder_cleanup = False

        if args.main_folder_name:
            self.main_folder_name = True
        elif args.main_folder_name == None:
            self.main_folder_name == False

        if args.change_folder_names:
            self.change_folder_names = True
        elif args.change_folder_names == None:
            self.change_folder_names == False

        if args.revert_settings:
            self.revert_settings = True
        elif args.revert_settings == None:
            self.revert_settings = False


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


    def open_extensions(self):
        """Load extensions into dict from JSON file. File is generated from
        scraper.py. If you ever want to go back to the
        default settings simply use the command --revertsettings."""
        try:
            print("\n" + BColors.HEADER + "Opening settings." + BColors.ENDC)
            with open(DIRNAMES["data"], "r") as f:
                extensions = json.load(f)
        except FileNotFoundError:
            print("Data file could not be located. Please make sure 'extensions.json' is in the 'Data' directory.")
            sys.exit(1)
        print("\n" + BColors.OKGREEN + "Settings succesfully opened." + BColors.ENDC)
        return extensions


    def check_extensions(self):
        """
        Checks file extensions for the directory specified and will place them in
        lists depending on if the file type can be identified. Then calls make_dirs to actually do the
        work. Huge thanks to https://www.online-convert.com/file-type as this is where the file extensions
        data came from.
        """
        results = {
                    "total": 0,
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
                try:
                    if file[0].split(".")[1] in self.extensions["extensions"]:
                        # print(file[0], "is a", self.extensions["extensions"][file[0].split(".")[1]])
                        results["success"].append(file)
                        results["total"] += 1
                    else:
                        results["error"].append(file)
                        results["total"] += 1
                except:
                    results["error"].append(file)
        results["success_percent"] = len(results["success"]) / results["total"] * 100.00
        results["error_percent"] = len(results["error"]) / results["total"] * 100.00
        self.final_output(results)
        self.make_dirs(results)


    def dir_regex(self):
        """
        Checks to see if folder already exists and will instead
        add a (Number) to the front of the folder if it does.
        """
        pattern = re.compile(r".*\(\d+\)" + self.extensions["main_folder_name"] + ".*")
        return pattern


    def make_dirs(self, results):
        """
        Will make all the required folders to store the files in the directory, will make
        a 'Folders' folder depending on the corresponding folder_cleanup flag passed in. If a DirectoryCleaner folder
        has already been made it will check and add a corresponding integer after the folder name.
        Ex: If DirectoryCleaner(2018-8-23) exists it will instead make (1)DirectoryCleaner(2018-8-23) and so on
        and so forth.
        """
        i = 1
        dir_cleaner_folder = os.path.join(self.directory, self.extensions["main_folder_name"] + "(" + str(datetime.date.today()) + ")")
        final_paths = []

        try:
            os.makedirs(dir_cleaner_folder)
        except FileExistsError:
            while os.path.exists(dir_cleaner_folder):
                dir_cleaner_folder = f"({str(i)})" + dir_cleaner_folder
                i += 1
            os.makedirs(dir_cleaner_folder)

        for file in tqdm(results["success"], total=len(results["success"])):
            new_dir = os.path.join(dir_cleaner_folder, self.extensions["extensions"][file[0].split(".")[1]]) #new_dir = directorycleaner(2018 blah blah)/(png)Portable Network Graphics
            #dir_cleaner_folder = directorycleaner(2018 blah blah)
            try:
                old_location = os.path.join(self.directory, file[0])
                new_location = os.path.join(new_dir, file[0])
                locations = (old_location, new_location)
                os.makedirs(new_dir)
                os.rename(old_location, new_location)
                final_paths.append(locations)
            except FileExistsError:
                print("\nThe directory", os.path.join(self.directory, self.extensions["extensions"][file[0].split(".")[1]]), "already exists.")

        print("\n" + BColors.OKGREEN + "Finished cleaning directory. Let's see where those things went: " + BColors.ENDC)
        print("-------------------------------------")
        for elem in final_paths:
            print(f"\nOriginal Location: {elem[0]}\nNew Location: {elem[1]}")
        print("-------------------------------------")


    def final_output(self, results):
        print("""\nFile type checking complete

Results:
----------

% Success: {0:.1f}

% Error: {1:.1f}
""".format(results["success_percent"], results["error_percent"]))