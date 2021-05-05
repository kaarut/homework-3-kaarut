import os
import json

# This module helps in extracting the info from paths.
from pathlib import Path


def structPath(path):
    # Creating the status object
    status = os.stat(path)

    # Creating a dictionary
    struct = dict()

    # Creating structionary with the file name value
    struct['name'] = os.path.basename(path)
    struct['path'] = os.path.ismount(path)
    struct['mask'] = oct(status.st_mode)[-3:]
    struct['owner'] = Path(path).owner()

    # Filtering the files and directories
    if os.path.isdir(path):
        struct['type'] = "directory"
        struct['children'] = [structPath(os.path.join(path, i)) for i in os.listdir(path)]
    else:
        struct['type'] = "file"
    return struct


# path = input("Insert path: ")
path = input("Insert path: ")
path = '/Users/kareen/Desktop/homework-1-kaarut/demo'
jsonObject = json.dumps(structPath(path), indent=4)
print(jsonObject)
