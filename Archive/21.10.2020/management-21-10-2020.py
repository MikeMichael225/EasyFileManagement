# Created 21.10.2020 by MikeMichael225

# This script moves all of the files inside a specified folder to folder with name of their suffixes (extensions)

from pathlib import Path
import os
import sys

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time

ARG_LIST = (sys.argv)
if not '-path' in ARG_LIST:
    print('Path not specified! Use argument -path! For example: -path C:\\Users\\username\\Downloads')
    os._exit(1)

FOLDER = Path(ARG_LIST[ARG_LIST.index("-path")+1].replace('\\', '/'))

UPDATE_DELAY = 60  # Delay before moving files (on error)

# Creates folders with suffixes (extensions) of files inside a folder specified by the user


def clear_unused_folders(folder):
    for file in folder.rglob("*"):
        if file.is_dir():
            if len(os.listdir(f'{folder}/{file.name}')) == 0:
                try:
                    Path(f'{folder}/{file.name}').rmdir()
                    print(f'Folder {file.name} deleted!')
                except:
                    print('Something went very wrong!')


def create_folders(folder):
    for file in folder.glob('*'):
        if file.is_file():
            newFolderPath = Path(f"{folder}/{file.suffix}")
            if not newFolderPath.is_dir():
                newFolderPath.mkdir()

# Moves all of the files inside a folder specified by the user to newly created folders with file extension names


def move_files(folder):
    for file in folder.glob("*"):
        if file.is_file():
            Path(
                f"{folder}/{file.name}").replace(Path(f"{folder}/{file.suffix}/{file.name}"))


def start(folder):
    print("Program started!")
    update(folder)
    add_event_listener(folder)


def update(folder):
    try:
        time.sleep(UPDATE_DELAY/60)
        create_folders(folder)
        move_files(folder)
        clear_unused_folders(folder)
        print("Folders updated!")
    except:
        print(f"Couldn't some of the files! Trying again in {UPDATE_DELAY}s")
        time.sleep(UPDATE_DELAY)
        update(folder)


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

        @staticmethod
        def on_any_event(event):
            if event.is_directory:
                return None

            elif event.event_type == 'created':
                update(FOLDER)

    if __name__ == '__main__':
        watch = OnMyWatch()
        watch.run()


start(FOLDER)
