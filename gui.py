#!/usr/bin/env python

import os
import sys
from tkinter.filedialog import askdirectory

from utils import readInputData
from window import Window

if __name__ == "__main__":
    # create the GUI object
    window = Window()
    # open window on top
    window.focus_force()
    # run mainloop once to update position of window (otherwise filedialog will mess up the geom)
    window.update_idletasks()
    
    # check if using script with file picker or in CLI mode
    if len(sys.argv) == 1:
        # get starting directory for open dialog box
        curr_dir = os.getcwd()
        # get files from open dialog
        input_dir = askdirectory(initialdir=curr_dir, title="Select Folder", parent=window)
    else:
        # get dir name from CLI args
        input_dir = sys.argv[1]
    
    # read input data and format appropriately
    data_lst, format_dict = readInputData(input_dir=input_dir)
    
    # add data to the GUI
    window.importData(data_lst, format_dict=format_dict)
    
    # run the main tkinter loop
    window.mainloop()
