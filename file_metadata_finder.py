"""
File: File metadata finder.py
Author: Jack Hinchliffe
Date: June 14th 2024
Version: 1.1
Python: v3.8.1 (WARNING: Not tested on any other version)
Dependencies: All libraries should be included in the Python install
Description: Lightweight script for finding information of all files in a folder structure
             - Launches a GUI window for user to select a folder. 
             - Using this folder as a top-level, search all folders and collect file metadata for all items found.
             - Creates a .csv file and writes the collected data to it. File given a unique name and saved to the same folder the user selected
             - Program exits upon finishing writing to file.
             - Data available in csv: Filename, Date Created, Date Modified, File size (bytes), Complete Filepath
Changelog:
    1.1 - Added better documentation
    1.0 - Initial development
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path, PureWindowsPath
from datetime import datetime
import csv

def selectRootDirectory() -> PureWindowsPath:
    """
    Opens a tkinter GUI to ask user to select a top-level directory.
    If no folder selected, exit script.

    Returns
    -------
    PureWindowsPath object of the selected directory
    """
    root = tk.Tk()
    root.withdraw()
    dir_path = PureWindowsPath(filedialog.askdirectory(title="Select Top-Level Folder"))
    
    if not dir_path:
        messagebox.showerror("Error", "No directory selected")
        exit()
    return dir_path

def getFileMetadata(filepath:str, topDir:PureWindowsPath) -> tuple | None:
    """
    Tries to collect metadata of a single file
        If found, return data
    Exception just skips over the file
        Returns nothing

    Parameters
    ---------
    filepath : str
        Path to file to collect stats from
    topDir : PureWindowsPath
        Path to the folder acting as the top-level directory

    Returns
    ------
    - Tuple : filename, date created, date modified, file size(bytes), filepath relative to topDir
    - None : Returns none if an error occured
    """
    try:
        stats = os.stat("\\\\?\\"+filepath) # Using \\?\ prefix to allow getting stats of files with paths exceeding Window's 256 char limit.
        createdOn = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modifiedOn = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = stats.st_size # file size in bytes
        return os.path.basename(filepath), createdOn, modifiedOn, size, "\\" + os.path.relpath(filepath, topDir) # return stats
    except Exception as e: # If there was a reason that the prior file data couldn't be found, notify in terminal and skip
        print(f'Error getting metadata for {filepath}: {e}')
        return None

def writeToCSV(outputFile:str, data:list) -> None:
    """
    Takes data and writes it to csv file specified by outputFile

    Adds headers to data file

    Parameters
    ---------
    outputFile : str
        Filepath and name to create
    data : list
        The collected data in a list format to print

    Returns
    ------
    None : Void function
    """
    with open(outputFile, mode='w', newline='', encoding='utf-8') as file:
        writer =csv.writer(file)
        writer.writerow(["Filename", "Created On", "Modifed On", "File Size (bytes)", "File Path"]) # Add header row to csv file
        writer.writerows(data) # Write rest of data after

    print(f'File Data saved to {outputFile}')

def main() -> None:
    """
    Main function, calls the other functions.
        Starts by asking for top directory 
        Loops through the folders and files to get meta data
        Ends by writing using the writeToCsv function to create a file with the data

    Returns
    ------
    None : Void function
    """
    top_level_dir = selectRootDirectory() # prompt user for starting directory
    print(f"Beginning Search from {top_level_dir}")
    files_metadata = [] 

    skipExtensions = ['.lnk', '.url'] # file extensions that should skipped during walk (to avoid going into another directory)

    for root, dirs, files in os.walk(top_level_dir): # Iterate through the folders
        print(f'Searching folder: {root}')
        for file in files: # Iterate through files in the current folder
            if any(file.lower().endswith(ext) for ext in skipExtensions): # skip over unwanted files
                continue
            filepath = os.path.join(top_level_dir,root, file) # Get a full filepath for the file
            metadata = getFileMetadata(filepath, top_level_dir) # Get the file's metadata
            if metadata: # If it was able to find data, add it to the data list
                files_metadata.append(metadata)
        print(f'Done searching folder: {root}')
    
    outputFile = f"{top_level_dir}\\file_metadata_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv" #Create a csv at top level containing results
    writeToCSV(outputFile, files_metadata)

# Execute main function if script is being ran rather than as a module
if __name__ == "__main__":
    main()
    
