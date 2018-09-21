import os
import re

def dir_regex(name):
    """
    Checks to see if a duplicate folder already exists and will instead
    add +1 to whatever number is currently assigned to the duplicate
    folder.
    """
    pattern = re.compile(r"^\(\d+\).+")
    match = pattern.search(name)
    return match


def check_duplicate(txt, directory):
    """
    Checks for any duplicate folders. First checks to see if
    there is a regex match which must mean there is a folder with
    (digit) already so it will loop through until there isn't.
    If the regex check doesn't pass the first time then we can
    prepend the folder/file with (1).
    """
    while True:
        if os.path.exists(os.path.join(directory, txt)):
            match = dir_regex(txt)
            if match is not None:
                 num = int(txt[1])
                 num += 1
                 num = str(num)
                 txt = "(" + num + ")" + txt[3:]
            else:
                txt = "(1)" + txt
        else:
            break
    return txt
