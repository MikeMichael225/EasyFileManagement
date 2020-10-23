# Created 21.10.2020 by MikeMichael225
# Version 22.10.2020
# This script moves all of the files inside a specified folder to folder with name of their suffixes (extensions)

import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


ARG_LIST = (sys.argv)
if not '-path' in ARG_LIST:
    print('Path not specified! Use argument -path! For example: -path C:\\Users\\username\\Downloads')
    os._exit(1)

FOLDER = Path(ARG_LIST[ARG_LIST.index("-path")+1].replace('\\', '/'))

UPDATE_DELAY = 30
# Delay before moving the files (on error).

DIVIDE_DELAY_BY = 30
# UPDATE_DELAY/DIVIDE_DELAY_BY inside a update() function. It shortenes the delay before first attempt of moving files to the rigth folder.


def clear_unused_folders(folder):
    for file in folder.rglob("*"):
        if file.is_dir() and len(os.listdir(f'{folder}/{file.name}')) == 0:
            try:
                Path(f'{folder}/{file.name}').rmdir()
                print(f'Folder {file.name} has been deleted!')
            except:
                print('Something went very wrong!')

# Deletes all of the unused folders.


def create_folders(folder):
    for file in folder.glob('*'):
        newFolderPath = Path(f"{folder}/{file.suffix}")
        if file.is_file() and not newFolderPath.is_dir():
            newFolderPath.mkdir()


# Creates folders with suffixes (extensions) of files inside a folder specified by the user.


def move_files(folder, index):
    for file in folder.glob("*"):
        if file.is_file():
            try:
                INDEX = f"({index})"
                Path(f"{folder}/{file.name}").rename(Path(
                    f"{folder}/{file.suffix}/{file.stem}{INDEX if not index == 0 else ''}{file.suffix}"))
                index = 0
            except:
                move_files(folder, index=index+1)

# Moves all of the files inside a folder specified by the user to newly created folders with file extension names.
# Variable 'index' in this function is put on the end of the file's name when there already is a file with the same name inside a folder.


def start(folder):
    print("Program started!")
    update(folder)
    add_event_listener(folder)

# This function starts the program.


def update(folder):
    try:
        time.sleep(UPDATE_DELAY/DIVIDE_DELAY_BY)
        create_folders(folder)
        move_files(folder, 0)
        clear_unused_folders(folder)
        print("Folders updated!")
    except:
        print(f"Couldn't some of the files! Trying again in {UPDATE_DELAY}s")
        time.sleep(UPDATE_DELAY)
        update(folder)

# This function updates folders, deletes unused folders and moves the files.
# When the file cannot be moved it handles an exeption. It will wait a number of seconds specified inside the constant UPDATE_DELAY then try to execute the function again.


def add_event_listener(folder):
    class OnMyWatch:
        # Set the directory on watch
        watchDirectory = folder

        def __init__(self):
            self.observer = Observer()

        def run(self):
            event_handler = Handler()
            self.observer.schedule(
                event_handler, self.watchDirectory, recursive=False)
            self.observer.start()
            try:
                while True:
                    time.sleep(5)
            except:
                self.observer.stop()
                print("Program stopped!")

            self.observer.join()

    class Handler(FileSystemEventHandler):

        @ staticmethod
        def on_any_event(event):
            if event.is_directory:
                return None

            elif event.event_type == 'created':
                update(FOLDER)

    if __name__ == '__main__':
        watch = OnMyWatch()
        watch.run()

# This function listenes for an event (file moved to the folder or created), then call an update() function which updates all of the folders and their content.


start(FOLDER)
