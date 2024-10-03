"""
File: user_interface.py
Author: Jack Hinchliffe
Date: September 18th 2024
Version: 1.0
Python: v3.8.1 (WARNING: Not tested on any other version)
Dependencies: - tkinter (included with Python install)
              - file_metadata_finder.py
Description: GUI For file meta data finder tool
             - Draws a simple GUI with buttons for people unfamiliar with the tool
             - Use for building .exe file
Changelog:
    1.0 - Initial development
"""

import tkinter as tk
from file_metadata_finder import selectRootDirectory, scanFolders, genFileName, writeToCSV

class FileMetadataFinder(tk.Tk):
    """
    Top-level GUI Window widget for the File Metadata Finder
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("File Metadata Finder Tool")
        self.geometry('400x200')

        self.frames = {}
        self.minsize(width=400, height=200)

        for F in ({MainPage}):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainPage(tk.Frame):

    def __initVars(self):
        """
        Initialize class vars
        """
        self.folderPath = None
        self.data = []
        self.statusVar = tk.StringVar(value='Status: No Directory Selected')

    def chooseFolder(self) -> None:
        """
        Triggers folder selection method from file_metadata_finder
        """
        self.folderPath = selectRootDirectory()
        if self.folderPath: # If there is a folder path, enable the program to run
            self.text_folderpath_disp['state'] = 'normal'
            self.text_folderpath_disp.delete('1.0', 'end')
            self.text_folderpath_disp.insert("end", self.folderPath)
            self.statusVar.set('Status: Ready To Run')
            self.text_folderpath_disp['state'] = 'disabled'
            self.button_run['state'] = 'normal'
        else: # If there is not a folder path, don't allow program to run
            self.button_run['state'] = 'disabled'
            self.text_folderpath_disp['state'] = 'normal'
            self.text_folderpath_disp.delete('1.0', 'end')
            self.text_folderpath_disp['state'] = 'disabled'
            self.statusVar.set('Status: No Directory Selected')
    
    def run(self):
        """
        Runs scanFolder and writeToCSV methods from file_metadata_finder
        """
        # GUI Widget Updates
        self.button_run['state'] = 'disabled'
        self.button_chooseFolder['state'] = 'disabled'
        self.statusVar.set('Status: Searching Files...')

        # Start searching for file metadata and write it to a csv file
        self.data = scanFolders(self.folderPath)
        writeToCSV(genFileName(self.folderPath), self.data)

        # GUI Widget Updates
        self.statusVar.set('Status: Search Complete, Results Saved to File')
        self.button_run['state'] = 'normal'
        self.button_chooseFolder['state'] = 'normal'

    def __init__(self, parent:tk.Frame, controller):
        """
        Create Tkinter frame and contents
        """
        tk.Frame.__init__(self, parent)

        self.bg_colour = '#d6d6d6' # Light grey background for widgets

        self.configure(bg=self.bg_colour)
        
        # Assign basic weights to columns and rows, allows for widgets to resize with window
        for r in range(0, 4):
            self.grid_rowconfigure(r, weight=1)
        for c in range(0, 2):
            self.grid_columnconfigure(c, weight=1)
        

        self.__initVars() # initialize instance variables

        # Title label initialization
        title = tk.Label(self, text='File Metadata Finder Tool', font='arial 16 bold')
        title.configure(bg=self.bg_colour)
        title.grid(column=0, row=0, columnspan=2, sticky='ew')

        # Choose folder button initialization
        self.button_chooseFolder = tk.Button(self, text='Select Top-Level Folder', command=self.chooseFolder)
        self.button_chooseFolder.configure(cursor='hand2', state='normal')
        self.button_chooseFolder.grid(column=0, row=1, sticky='ew', padx=5, pady=5)
        
        # Run button initialization
        self.button_run = tk.Button(self, text='Start Search', command=self.run)
        self.button_run.configure(cursor='hand2', state='disabled')
        self.button_run.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

        # Filepath explainer label initialization
        label_explainer = tk.Label(self, text='Search all subfolders and files under:')
        label_explainer.configure(bg=self.bg_colour)
        label_explainer.grid(column=0, row=2, sticky='sw', padx=5)

        # Filepath textbox initialization
        self.text_folderpath_disp = tk.Text(self)
        self.text_folderpath_disp.configure(height=1, font='arial 10', state='disabled')
        self.text_folderpath_disp.grid(column=0, row=3,sticky="nwe",pady=5, padx=5, columnspan=2)

        # Status label initialization
        self.label_status = tk.Label(self, textvariable=self.statusVar, font='arial 11 bold')
        self.label_status.configure(bg=self.bg_colour)
        self.label_status.grid(column=0, row=4, padx=5, pady=5, sticky='new', columnspan=2)

# Launch the GUI mainloop if this file is run
if __name__ == "__main__":
    app = FileMetadataFinder()
    app.mainloop()