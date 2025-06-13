#!/usr/bin/env python

import sys
from window import Window
from utils import readInputData

if __name__ == "__main__":
    # get dir name from CLI args
    input_dir = sys.argv[1]
    # run the main tkinter loop
    window = Window()
    readInputData(input_dir=input_dir, frame=window)
    window.mainloop()
