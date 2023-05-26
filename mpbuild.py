#!/usr/bin/env python3
# requires files.txt file in the current directory
# lines starting with '#' are comments and ignored
# lines starting with '/' are directories and are created
# 1 line starting with '+' will be copied to main.py
# directory lines must appear prior to the files in the directories
# all other lines are considered valid files in the current directory
# PYBOARD_DEVICE environmental variable must be set to board


import argparse
import re
from mpremote.pyboard import Pyboard
import sys
import os


def show_progress_bar(size, total_size, op="copying"):
    if not sys.stdout.isatty():
        return
    verbose_size = 2048
    bar_length = 20
    if total_size < verbose_size:
        return
    elif size >= total_size:
        # Clear progress bar when copy completes
        print("\r" + " " * (13 + len(op) + bar_length) + "\r", end="")
    else:
        bar = size * bar_length // total_size
        progress = size * 100 // total_size
        print(
            "\r ... {} {:3d}% [{}{}]".format
            (op, progress, "#" * bar, "-" * (bar_length - bar)),
            end="",
        )


folder = re.compile(r'^/')
comment = re.compile(r'^#')
main_prog = re.compile(r'^\+')

parser = argparse.ArgumentParser(description='''Reads names of files from
    files.txt file in current folder. Copies files to attached MicroPython
    board. Requires a -e or --execute to execute copy
    functionality, otherwise it will only print which files will be copied.
''')
parser.add_argument('-e', "--execute", action='store_true', default=False,
                    dest='execute',
                    help='required to copy the files to the board')
parser.add_argument('-v', "--verbose", action='store_true', default=False,
                    dest='verbose',
                    help='show file names as action is performed')

args = parser.parse_args()


pyb = Pyboard(os.environ['PYBOARD_DEVICE'], 115200)
pyb.enter_raw_repl()
with open('files.txt', 'r') as files:
    file_list = files.readlines()

for file in file_list:
    if args.verbose:
        print(f"{file.strip()}")
    # line begins with a slash, create a dir using the following text
    if folder.match(file) and args.execute:
        d = file.strip()
        pyb.fs_mkdir(d)

    # line begins with a #, ignore the line its a comment
    elif comment.match(file):
        continue

    # line begins with a +, copy it to main.py
    elif main_prog.match(file) and args.execute:
        s = file[1:].strip()
        pyb.fs_put(s, 'main.py', progress_callback=show_progress_bar)

    # all other lines are assumed to be valid files to copy to board
    elif args.execute:
        s = file.strip()
        pyb.fs_put(s, s, progress_callback=show_progress_bar)

pyb.fs_ls('/')
pyb.exit_raw_repl()
pyb.close()
