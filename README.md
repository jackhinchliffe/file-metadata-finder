# File Metadata Finder

User can select a folder/drive. Script will search all subdirectories and files, collecting filepath, date of creation/modification, and file size.

Script will write this information to a .csv file and save it to the same top-level directory as the search began in.

Useful for quickly collecting information throughout folder tree structure for analysis.

## File Header
File: File_metadata_finder.py

Author: Jack Hinchliffe

Date: June 14th 2024

Version: 1.1

Python: v3.8.1 (WARNING: Not tested on any other version)

Dependencies: All libraries should be included in the Python install

Description: 
Lightweight script for finding information of all files in a folder structure
- Launches a GUI window for user to select a folder. 
- Using this folder as a top-level, search all folders and collect file metadata for all items found.
- Creates a .csv file and writes the collected data to it. File given a unique name and saved to the same folder the user selected
- Program exits upon finishing writing to file.
- Data available in csv: Filename, Date Created, Date Modified, File size (bytes), Complete Filepath

Changelog:
 + 1.1 - Added better documentation
 + 1.0 - Initial development
