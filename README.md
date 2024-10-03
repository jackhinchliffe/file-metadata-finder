# File Metadata Finder

User can select a folder/drive. Script will search all subdirectories and files, collecting filepath, date of creation/modification, and file size.

Script will write this information to a .csv file and save it to the same top-level directory as the search began in.

Useful for quickly collecting information throughout folder tree structure for analysis.

## How to Use Script
> [!NOTE]
> There is two methods to run the script:

### No GUI, Command Line Execution
If you do not want to use a GUI to launch the script, run the `file_metadata_finder.py` script.

Will only use a GUI window to select the folder, and will automatically start searching files once folder is selected.

Use the command line to execute the script using the command `python \Replace\with\path\to\the\script\file_metadata_finder.py`

### Using User-Friendly GUI
If you would prefer a user-friendly experience, run the `user_interface.py` script.

This will launch a GUI for user to select a folder and choose when to run the script. Terminal will open when running to print search status.

Use the command line to execute the script using the command `python \Replace\with\path\to\the\script\user_interface.py`

> [!TIP]
> Use the `user_interface.py` script with pyinstaller to build an .exe, and use `--onefile` parameter to build both scripts into a single .exe file.
> The result is a self-contained user-friendly application 

### Dependencies
- Python: v3.8.1 (WARNING: Not tested on any other version)
- pywin32 (version 306)


## Module Header: File_metadata_finder
File: File_metadata_finder.py

Author: Jack Hinchliffe

Date: June 14th 2024

Version: 1.4

Python: v3.8.1 (WARNING: Not tested on any other version)

Dependencies: 
- pywin32 (version 306)
- All libraries should be included in the Python install

Description: 
Lightweight script for finding information of all files in a folder structure
- Launches a GUI window for user to select a folder. 
- Using this folder as a top-level, search all folders and collect file metadata for all items found.
- Creates a .csv file and writes the collected data to it. File given a unique name and saved to the same folder the user selected
- Program exits upon finishing writing to file.
- Data available in csv: Filename, Date Created, Date Modified, Date Last Accessed, File size (bytes), File Owner, Complete Filepath

Changelog:
 + 1.4 - Added date last accessed and File Owner to collected data. Requires pywin32 now
 + 1.3 - Refactored functions to use script as module, added scanFolders() and genFileName()
 + 1.2 - Bug fix for type annotation and empty directory selection
 + 1.1 - Added better documentation
 + 1.0 - Initial development
