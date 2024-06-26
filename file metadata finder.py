# File metadata finder

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path, PureWindowsPath
from collections import Counter
from datetime import datetime
import csv
import math

# Function to prompt user to select the root directory
def selectRootDirectory():
    root = tk.Tk()
    root.withdraw()
    dir_path = PureWindowsPath(filedialog.askdirectory(title="Select Top-Level Folder"))
    
    if not dir_path:
        messagebox.showerror("Error", "No directory selected")
        exit()
    return dir_path

# get metadata from current file, and return information
# returns file name, date created on and modified, and the file path RELATIVE to the user selected directory
def getFileMetadata(filepath, topDir):
    try:
        stats = os.stat("\\\\?\\"+filepath) # Using \\?\ prefix to allow getting stats of files with paths exceeding Window's 256 char limit.
        createdOn = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modifiedOn = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = stats.st_size # file size in bytes
        return os.path.basename(filepath), createdOn, modifiedOn, size, "\\" + os.path.relpath(filepath, topDir) # return stats
    except Exception as e:
        print(f'Error getting metadata for {filepath}: {e}')
        return None

# writes the collected data to a csv file
def writeToCSV(outputFile, data):
    with open(outputFile, mode='w', newline='', encoding='utf-8') as file:
        writer =csv.writer(file)
        writer.writerow(["Filename", "Created On", "Modifed On", "File Size (bytes)", "File Path"])
        writer.writerows(data)

    print(f'File Data saved to {outputFile}')

# main function where methods are called
def main():
    top_level_dir = selectRootDirectory() # prompt user for starting directory
    print(f"Beginning Search from {top_level_dir}")
    files_metadata = []

    skipExtensions = ['.lnk', '.url'] # file extensions that should skipped during walk

    for root, dirs, files in os.walk(top_level_dir):
        print(f'Searching folder: {root}')
        for file in files:
            if any(file.lower().endswith(ext) for ext in skipExtensions): # skip over unwanted files
                continue
            filepath = os.path.join(top_level_dir,root, file)
            metadata = getFileMetadata(filepath, top_level_dir)
            if metadata:
                files_metadata.append(metadata)
        print(f'Done seraching folder: {root}')
    
    outputFile = f"{top_level_dir}\\file_metadata_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv" #Create a csv at top level containing results
    writeToCSV(outputFile, files_metadata)


if __name__ == "__main__":
    main()
    