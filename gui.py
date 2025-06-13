#!/usr/bin/env python

import sys
from window import Window
from utils import readInputData

if __name__ == "__main__":
    # get dir name from CLI args
    input_dir = sys.argv[1]
    # create the GUI object
    window = Window()
    # read input data and format appropriately
    data_lst = readInputData(input_dir=input_dir)
    # add data to the GUI
    window.importData(data_lst)
    # run the main tkinter loop
    window.mainloop()
