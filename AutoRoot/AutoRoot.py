#!/usr/bin/env python

__doc__ = """AutoRoot - Automatically reset the root password

AutoRoot will scan for any logical volume containing the word root or for block devices starting from /dev/sda1.../dev/sda10, 
/dev/sdb1.../dev/sdb10, /dev/sdc1.../dev/sdc10, it will then try to mount the volume and check for the password file, if found, 
it will change the root password to: vNugget.com

Requirement:
============
This script require system rescue cd which can be found on http://www.system-rescue-cd.org/

Usage:
======
Download system rescue CD and put AutoRoot.py and autorun on the root directory of the ISO image, reboot your machine using the iso file,
and that's it!

"""
__author__ = "http://vNugget.com"

import subprocess, os
from stat import S_ISBLK
from time import sleep


def findRootPartition():
    try:
        listA = ["sda"+str(i) for i in range(1,11)]
        listB = ["sdb" + str(i) for i in range(1, 11)]
        listC = ["sdc" + str(i) for i in range(1, 11)]
        globalList = listA, listB, listC
        device = []

        for i,l in enumerate(globalList):
            for disk in l:
                if S_ISBLK(os.stat("/dev/"+str(disk)).st_mode ) != 0:
                    print("\n[+] Found Device : /dev/" + disk)
                    device.append(disk)

    except:
        pass
        #print("Device : /dev/" + disk + " doesn't exist")

    return device


def findLv():

    found = None
    res = subprocess.Popen("/sbin/lvscan", shell=True, stdout=subprocess.PIPE)
    out = res.stdout.readlines()
    for l in out:

        res2 = str(l).rpartition('\'')
        lv = res2[0].split('\'')[1]
        if 'root' in lv:
            found = True
            break

    if found != True:
        print("\n[-] Root LV not found")
        lv = None

    return lv


def mountDevice(lv):

    found = None
    mountCmd = "mount -o bind /proc /mnt/sysimage/proc;mount -o bind /sys /mnt/sysimage/sys;mount -o bind /dev /mnt/sysimage/dev"
    print("\n[+] Mounting {}".format(str(lv)))
    
    res = subprocess.Popen("mount " + str(lv) + " /mnt/sysimage", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if res.stdout != None:
        print("\n[+] Volume {} mounted successfully".format(str(lv)))
        sleep(2)
        if (os.path.isfile("/mnt/sysimage/etc/passwd")):
            found = True
            print("\n[+] Password file found on mounted volume")
            print("\n[+] Changing root password")
            if (subprocess.Popen(mountCmd,shell=True) != None):
                print("[+] Chrooting...")
                if (subprocess.Popen("chroot /mnt/sysimage /bin/bash -c \"echo root:vNugget.com | chpasswd;touch /.autorelabel;exit\"", shell=True) != None):
                    print("\n[+] Root Password was reset successfully\n")
                    sleep(2)
                else:
                    print("\n[-] Error while changing the password...")
            else:
                print("\n[-] Unable to mount the required file system... Exiting")
                raise SystemExit(-1)

        else:
            print("\n[-] Password file NOT found in mounted volume " + str(lv))

    subprocess.Popen("umount --recursive /mnt/sysimage", shell=True)

    return found


def main():
    try:
        os.mkdir("/mnt/sysimage")
    except OSError:
        print("\n[!] /mnt/sysimage already exist")

    device = []
    lv = findLv()
    if lv == None:
        print("\n[-] No Lv Found... Trying block device")
        device = findRootPartition()
        if len(device) != 0:
            for d in device:
                if (mountDevice("/dev/"+str(d))):
                    break
        else:
            print("\n[-] No Root file system detected on block device")
            raise SystemExit(-1)
    else:
        mountDevice(lv)


main()
