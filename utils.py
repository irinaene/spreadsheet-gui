"""Functions to help with importing and pre-processing input data."""

import csv
import glob
from datetime import datetime


def readInputData(input_dir, desc_len=50, cat_len=20, output_file="exported_items.csv"):
    """Function to read data from files living inside input_dir.
    Data is later used to populate the input listbox of GUI."""
    
    # set of currently fixed formatting parameters
    date_len = 10
    amt_len = 11
    # list to hold all the data rows from relevant files
    list_in = []
    # get files from input_dir
    files = glob.glob(f"{input_dir}/*.csv")
    files.extend(glob.glob(f"{input_dir}/*.CSV"))
    # on windows, glob + wildcard returns duplicates, fix by using set to select unique values
    files = list(set(files))
    # exclude the ouput file, if it exists
    files = [file for file in files if output_file not in file]
    # always open files in same order
    files = sorted(files)
    # add header with column descriptions, nicely formatted
    c1 = "Date".ljust(date_len)
    c2 = "Description".ljust(desc_len)
    c3 = "Category".ljust(cat_len)
    header_line = f"{c1} | {c2} | {c3} | Amount"
    list_in.append(header_line)
    # define separator line between different files
    sep_line = "-" * date_len + "-|-" + "-" * desc_len + "-|-" + "-" * cat_len + "-|-" + "-" * amt_len
    list_in.append(sep_line)
    for input_file in files:
        # import data using csv module
        with open(input_file) as fin:
            csv_reader = csv.reader(fin, delimiter=',', quotechar='"')
            header = ",".join(next(csv_reader))
            for row in csv_reader:
                row_str = " ".join(row).lower()
                # skip the autopay lines and empty line
                if ("autopay" in row_str) or ("automatic payment" in row_str) or (len(row) == 0):
                    continue
                # format row depending on csv header info
                new_row = formatRow(row, header=header, desc_len=desc_len, cat_len=cat_len)
                # create one long string per row
                concat_row = " | ".join(new_row)
                # add to input listbox
                list_in.append(concat_row)
        # add a line to separate between the different data sources
        list_in.append(sep_line)
    # fix last line not showing properly b/c of scrollbar
    list_in.append("")
    # dict containing the params for formatting the various fields
    format_dict = {'desc_len': desc_len, 'cat_len': cat_len}
    
    return list_in, format_dict

def formatRow(row, header, desc_len, cat_len):
    """Function to format a row given the header of the input csv file."""
    
    # use header to decide what info is contained in row
    if header == "Date,Description,Amount":
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
        # add a default category
        row.insert(2, "Food")
        # amount: ensure consistent signs, debit -, credit +
        row[3] = f"{-1 * float(row[3]):.2f}"
    elif header == "Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit":
        idx = [0, 3, 4, 5, 6]
        row = [row[id] for id in idx]
        # amount: ensure consistent signs, debit -, credit +
        if row[3] == "":
            row[3] = row[4]
        else:
            row[3] = f"{-1 * float(row[3]):.2f}"
        # remove credit info
        row.pop(len(row) - 1)
    elif header == "Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #":
        idx = [1, 2, 3]
        row = [row[id] for id in idx]
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
        # add a default category
        row.insert(2, "Food")
    elif header == "Transaction Date,Post Date,Description,Category,Type,Amount,Memo":
        idx = [0, 2, 3, 5]
        row = [row[id] for id in idx]
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
    # set max length for description
    if len(row[1]) < desc_len:
        row[1] = row[1].ljust(desc_len)
    else:
        row[1] = row[1][:desc_len]
    # set default category for all rows and max length for category
    row[2] = "Food".ljust(cat_len)
    
    return row
