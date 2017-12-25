#!/usr/bin/env python

# This script can be used to backup & restore a directory tree permission until a certain specified depth level
# Author : Gassim Salah-eddine
# http://vnugget.com
#

import os
import json


sourceDir = "/root/Downloads"
extractOut = "/root/extract.txt"

dirRight = {}
dirRightTmp = {}
# operation : B= Backup / R= Restore
op = "R"
# directory depth level
level = 3 
if op == "B":
    print("Backing up {0} into {1}".format(sourceDir,extractOut))
    resOut = open(extractOut,"w")
    for root, dirs, files in os.walk(sourceDir):
        depth = root[len(sourceDir):].count(os.sep)
    # check the depth level
        if depth <= level:
            rights = os.lstat(root)
            dirRight[root] = root
            dirRight[root] = {'st_mode' : rights.st_mode , 'st_uid' : rights.st_uid, 'st_gid' : rights.st_uid}
            dirRightTmp.update(dirRight)
            dirRight.clear()
            del dirs[len(dirs):len(dirs)-level]
    json.dump(dirRightTmp,resOut,indent=4)
    print("Done!")
    resOut.close()
else:
    choice = raw_input("Are you sure about retoring right on {} using {} [Y]?".format(sourceDir,extractOut))
    if choice == "Y":
        print("Restoring")
        resOut = open(extractOut,"r")
        dirRight = json.load(resOut)
        for path in dirRight.keys():
            if os.path.lexists(path):
                os.chmod(path,dirRight[path]["st_mode"])
                # not available on windows
                os.chown(path,dirRight[path]["st_uid"],dirRight[path]["st_gid"])
            else:
                print("Directory {0} no longer exist...".format(path))

    else:
        print("Exiting... nothing was modified!")
        resOut.close()
