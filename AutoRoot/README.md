##**AutoRoot - Automatically reset the root password**

AutoRoot will scan for any logical volume containing the word root or for block devices starting from /dev/sda1.../dev/sda10, 
/dev/sdb1.../dev/sdb10, /dev/sdc1.../dev/sdc10, it will then try to mount the volume and check for the password file, if found, 
it will change the root password to: vNugget.com

##Requirement:

This script require system rescue cd which can be found on http://www.system-rescue-cd.org/ 

##Usage:

Download system rescue CD and put AutoRoot.py and autorun on the root directory of the ISO image, reboot your machine using the iso file,
and that's it!

##More info:

http://vnugget.com/python/autoroot-automatically-reset-the-root-password-on-linux-machines
