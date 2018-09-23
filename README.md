# DirectoryCleaner

#### For when you're tired of all that garbage

![demo](https://s3.amazonaws.com/gfyshare/directorycleanergif.gif)


---
## Why?

The main focus of this application is to make it as easy as possible to clean up directories that just have a bunch of loose files laying around that may not be that important. I DO NOT recommend using this on a software project directory for obvious reasons. It is fully customizable and any of the default names can be changed if for some reason you don't like the default folder names or perhaps even the extremely inventive name DirectoryCleaner.

---

## Setup

First install with pip.
```
pip install DirectoryCleaner
```
Then this should make DirectoryCleaner available from your path. To test this type
```
DirectoryCleaner -h
```
If you get the help commands you're all set.

### Windows Specific Extra Step

If you don't already, set your default encoding for cmd to UTF-8 using this command.
```
chcp 65001
``` 

## Example Usage

The most basic form of usage is to clean a messy directory with all the default names. The default names take the form of (file_extension)Full_name_of_file_extension. For example a png files default name is (png)Portable Network Graphics. The default directory name everything will be placed in is named DirectoryCleaner(Current_date).
```
DirectoryCleaner /users/username/desktop
```
#### Grouping files

The -gf or --group_files flag will group common file types together into the default group directory names. For example all image files of the format jpg, jpeg, png, tif, tiff, gif, bmp, eps, raw, cr2, nef, orf, and sr2 will be placed in an 'Images' folder with this flag set.
```
DirectoryCleaner /users/username/desktop -gf
```

#### Changing defaults

With these three flags you can change all the default directory names that your files will be placed in. The prompts they will give you will tell you exactly how to change them. After any of the names are changed those names will be the new defaults everytime you run the program.
```
DirectoryCleaner /users/username/desktop -mfn -cfn -cgn
```

#### Reverting to the default settings

With this flag you can revert to the default settings if you decided that you in fact love and miss the sensible defaults 😏.
```
DirectoryCleaner /users/username/Desktop -rs
```

---

## Commands

```
positional arguments:
  path                  The path to the directory that you want to cleanup not
                        actually the word path. Ex. DirectoryCleaner
                        /Users/Username/desktop

optional arguments:
  -h, --help            show this help message and exit
  --folder_cleanup, -fc
                        Set this flag if you want folders to also be included
                        in the clean up.
  --main_folder_name, -mfn
                        Set this flag and specify the name you would like the
                        main folder to be called. The date will always be
                        apart of the name, only DirectoryCleaner will be
                        changed.
  --revert_settings, -rs
                        Revert the settings file to its default state when the
                        program was downloaded. Will use the default settings
                        to run the program as well.
  --group_files, -gf    Set this flag if you would like to group commonly used
                        files like Word Docs, Excel files, PDFs, music files
                        etc. in folders named after the type of media they
                        are.
  --change_folder_names, -cfn
                        Set this flag if you want to rename one of the default
                        folder names Directory Cleaner uses for that type of
                        file.
  --change_group_names, -cgn
                        Set this flag if you'd like to rename one of the
                        default group names.

```                        
