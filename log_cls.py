#!/usr/bin/env python3
import os
from datetime import datetime as dt

def walk(path):
    for dir_path, dir_list, file_list in os.walk(path):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            yield full_path

def remove_dir(dir_path):
    for full_path in walk(dir_path):
        os.remove(full_path)
    os.removedirs(dir_path)

def main():
    for dir_path, dir_list, file_list in os.walk('./Logs'):
        date = dt.now().strftime('%Y%m%d')
        for dir_name in dir_list:
            if dir_name != date:
                remove_dir(os.path.join(dir_path, dir_name))

        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            open(full_path, 'w').close()

if __name__ == "__main__":
    main()
