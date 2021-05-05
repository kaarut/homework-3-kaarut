"""This is task2 script."""

import os, datetime
# This module helps in automating process of
# copying and removal of files and directories.
import shutil


def searchForOldies(dirPath):
    # Get todays date
    today = datetime.datetime.today()

    # Change directory
    os.chdir(dirPath)

    # List all files
    files = os.listdir(dirPath)

    # Iterate all files
    for file in files:
        if os.path.isfile(file) and file != "app.py":
            if isOlderThan(file, 7):
                addFileToFolder(file)

def isOlderThan(file, days):
    # Get todays date
    today = datetime.datetime.today()
    modif_date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    duration = today - modif_date
    if duration.days > days:
        return True

def addFileToFolder(file):
    # Add the file that
    folder = os.getcwd()
    if not os.path.isdir(os.path.join(folder, "oldFiles")):
        os.mkdir(os.path.join(folder, "oldFiles"))
    shutil.move(file, "oldFiles/"+file)

# def modificationTime(file):
# return datetime.datetime.fromtimestamp(os.path.getctime(file))

dirPath = input("Insert directory path: ")
searchForOldies(dirPath)
