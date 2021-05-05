"""This is task1 script."""


import os, time

def scanDirectory(dirPath):

    # Search for all files that have 777 permission
    # and delete them
    if not dirPath.endswith('/'):
        dirPath = dirPath + '/'

    # List all files
    files = os.listdir(dirPath)


    # Scan for vulnerable files
    for file in files:
        status = os.stat(dirPath + file)
        mask = oct(status.st_mode)[-3:]
        if mask == '777':
            print(f"The file {file} is vulnerable! Deleting..")
            os.remove(file)

# While True search for files in a directory
dirPath = input("Insert directory path: ")

while True:
    scanDirectory(dirPath)
    time.sleep(15)
