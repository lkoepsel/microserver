#!/usr/bin/env python3
# requires a text file containing the following:
# lines starting with '#' are comments and ignored
# lines starting with '/' are directories and are created
# lines starting with '!' are files to be copied and renamed,
#   two fields are required, separated by a ',', localname, piconame
# 1 line starting with '+' will be copied to main.py
# directory lines must appear prior to the files in the directories
# all other lines are considered valid files in the current directory
# local_env.py file must be contain 'port' set to board serial port
# port = '/dev/cu.usbmodem31401'

import argparse
import re
from mpremote.pyboard import Pyboard
import sys
import local_env


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
change = re.compile(r'^!')

parser = argparse.ArgumentParser(description='''Reads names of files from
    build file in current folder. Copies files to attached MicroPython
    board. Use --dry-run or -n to print commands, instead of execution.
Filenames can NOT have blanks in their names.''')
parser.add_argument('build', help='file to use for building Pico',
                    default='files.txt')
parser.add_argument('-n', "--dry-run", action='store_true', default=False,
                    dest='dryrun',
                    help='required to copy the files to the board')
parser.add_argument('-v', "--verbose", action='store_true', default=False,
                    dest='verbose',
                    help='print lines in build file prior to execution')

args = parser.parse_args()


pyb = Pyboard(local_env.port, 115200)
pyb.enter_raw_repl()
with open(args.build, 'r') as files:
    file_list = files.readlines()

dirs = []
for file in file_list:
    if args.verbose:
        print(f"{file.strip()}")
    # line begins with a slash, create a dir using the following text
    if folder.match(file):
        d = file.strip()
        dirs.append(d)
        if args.dryrun:
            print(f"pyb.fs_mkdir({d})")
        else:
            pyb.fs_mkdir(d)

    # line begins with a #, ignore the line its a comment
    elif comment.match(file):
        continue

    # line begins with a +, copy it to main.py
    elif main_prog.match(file):
        s = file[1:].strip()
        if args.dryrun:
            print(f"pyb.fs_put({s}, main.py)")
        else:
            pyb.fs_put(s, 'main.py', progress_callback=show_progress_bar)

    # line begins with a +, copy it to main.py
    elif change.match(file):
        s, d = file[1:].split(',')
        if args.dryrun:
            print(f"pyb.fs_put({s}, {d.strip()})")
        else:
            pyb.fs_put(s, d.strip(), progress_callback=show_progress_bar)

    # all other lines are assumed to be valid files to copy to board
    else:
        s = file.strip()
        if args.dryrun:
            print(f"pyb.fs_put({s}, {s})")
        else:
            pyb.fs_put(s, s, progress_callback=show_progress_bar)

print(f"/")
pyb.fs_ls('/')
for d in dirs:
    print(f"{d}/")
    pyb.fs_ls(d)
pyb.exit_raw_repl()
pyb.close()
