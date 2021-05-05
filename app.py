"""This is multy-functional app."""

import datetime
import json
import os
import shutil
import time
import subprocess

# This module helps in extracting the info from paths.
from pathlib import Path


class App:
    """The application object."""
    def __init__(self, dirPath):
        """Constructor."""
        os.chdir(dirPath)
        self.path = dirPath

    def scanDirectory(self):
        """Get list of files in directory."""
        dirPath = self.path
        if not dirPath.endswith('/'):
            self.path = dirPath + '/'
        return os.listdir(self.path)

    def isOlderThan(self, file, days):
        """Compare file modification time to given value."""
        today = datetime.datetime.today()
        modif_date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        duration = today - modif_date
        if duration.days > days:
            return True

    def addFileToFolder(self, file, dropbox=None):
        """Put file to a folder named oldFiles."""
        folder = self.path
        if dropbox:
            shutil.move(file, "~/Dropbox")
            return 
        if not os.path.isdir(os.path.join(folder, "oldFiles")):
            os.mkdir(os.path.join(folder, "oldFiles"))
        shutil.move(file, "oldFiles/" + file)

    def isFile(self, file):
        """Check if is file."""
        if os.path.isfile(file) and file != 'app.py':
            return True

    def getMask(self, file):
        """Get mask for given file."""
        status = os.stat(self.path + file)
        return oct(status.st_mode)[-3:]

    def findVulnerable(self):
        """Find files with full permission and delete them."""
        files = self.scanDirectory()
        for file in files:
            if self.isFile(file):
                mask = self.getMask(file)
                owner = Path(self.path).owner()
                if mask == '777':
                    subprocess.Popen(['notify-send', f"The user {owner} of the file {file} is vulnerable! Deleting.."])
                    os.remove(file)

    def structPath(self, path=None):
        """Script to convert a directory structure to the JSON format."""
        if not path:
            path = self.path
        status = os.stat(self.path)

        # Adding values to the dictionary
        struct = dict()
        struct['name'] = os.path.basename(path)
        struct['path'] = "./" + os.path.basename(path)
        struct['mask'] = oct(status.st_mode)[-3:]
        struct['owner'] = Path(path).owner()

        # Classify path by files and directories
        if os.path.isdir(path):
            struct['type'] = "directory"
            struct['children'] = [self.structPath(os.path.join(path, i)) for i in self.scanDirectory()]
        else:
            struct['type'] = "file"
        return struct

    def task1(self):
        """Find files with full permission."""
        while True:
            self.findVulnerable()
            time.sleep(15)

    def task2(self, days, dropbox=None):
        """Script to classify files - based on modification date."""
        files = self.scanDirectory()
        for file in files:
            if self.isFile(file) and self.isOlderThan(file, days):
                if dropbox:
                    self.addFileToFolder(file, dropbox)
                else:
                    self.addFileToFolder(file, dropbox)

    def task3(self):
        """Script to convert a directory structure to the JSON format."""
        jsonObject = json.dumps(self.structPath(), indent=4)
        print(jsonObject)


if __name__ == '__main__':
    path = input("Insert path: ")
    path = '/Users/kareen/Desktop/homework-1-kaarut/demo'
    path = '/home/parallels/homework-1-kaarut/demo'
    newApp = App(path)
    task = int(input("Select which task (1,2,3) : "))
    if task == 1:
        newApp.task1()
    if task == 2:
        days = int(input("Select how old file are u looking for : "))
        dropbox = input("Would you like to use dropbox (y/n) : ")
        if dropbox == 'y':
            newApp.task2(days, True)
        newApp.task2(days)
    elif task == 3:
        newApp.task3()
    else:
        task = int(input("Select which task (1,2,3) : "))
