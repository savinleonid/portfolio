"""Files in OS"""

import os
import time

directory = os.path.curdir  # current directory - module 7

for root, dirs, files in os.walk(directory):  # iterate over walk generator object in given directory
    for file in files:
        filepath = os.path.join(root, file)  # join path with filename to get root path of each element
        filetime = os.path.getmtime(filepath)  # get formated time via timestamp
        formatted_time = time.strftime("%d.%m.%Y %H:%M", time.localtime(filetime))  # format timestamp to visual format
        filesize = os.path.getsize(filepath)  # get size of file in bytes
        parent_dir = os.path.dirname(filepath)  # get path of parent directory
        # print results
        print(f'File found: {file}, '
              f'Path: {filepath}, '
              f'Size: {filesize} byte, '
              f'Formated time: {formatted_time}, '
              f'Parent Directory: {parent_dir}')
