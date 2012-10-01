#!/usr/bin/python

import platform
import os
import urllib
import subprocess
import glob

KEYDBURL = 'http://vlc-bluray.whoknowsmy.name/files/KEYDB.cfg'

libaacsURL = {
    'Windows_32bit': 'http://vlc-bluray.whoknowsmy.name/files/win32/libaacs.dll',
    'Windows_64bit': 'http://vlc-bluray.whoknowsmy.name/files/win64/libaacs.dll',
    'Darwin_64bit': 'http://vlc-bluray.whoknowsmy.name/files/mac/libaacs.dylib',
    'Linux_32bit' : 'http://vlc-bluray.whoknowsmy.name/files/linux32/libaacs.so.0',
    'Linux_64bit': 'http://vlc-bluray.whoknowsmy.name/files/linux64/libaacs.so.0'
    }

libaacsLocation = {
    'Windows_32bit': 'C:\\Program Files\\VideoLAN\\VLC\\libaacs.dll',
    'Windows_64bit': 'C:\\Program Files\\VideoLAN\\VLC\\libaacs.dll',
    'Darwin_64bit': os.path.expanduser('~/lib/libaacs.dylib'),
    'Linux_32bit' : '/usr/lib/libaacs.so.0',
    'Linux_64bit': '/usr/lib64/libaacs.so.0'
    }

KEYDBLocation = {
    'Windows_32bit': os.path.expanduser('~\\AppData\\Roaming\\aacs\\KEYDB.cfg'),
    'Windows_64bit': os.path.expanduser('~\\AppData\\Roaming\\aacs\\KEYDB.cfg'),
    'Darwin_64bit': os.path.expanduser('~/Library/Preferences/aacs/KEYDB.cfg'),
    'Linux_32bit' : os.path.expanduser('~/.config/aacs/KEYDB.cfg'),
    'Linux_64bit': os.path.expanduser('~/.config/aacs/KEYDB.cfg')
    }

VLCBinary = {
    'Windows_32bit': 'C:\\Program Files\\VideoLAN\\VLC\\VLC.exe',
    'Windows_64bit': 'C:\\Program Files\\VideoLAN\\VLC\\VLC.exe',
    'Darwin_64bit': '/Applications/VLC.app/Contents/MacOS/VLC',
    'Linux_32bit' : 'vlc',
    'Linux_64bit': 'vlc'
    }


CurrentOS = platform.system()
CPUArch = platform.architecture()[0]
CurrentSystem = CurrentOS + '_' + CPUArch

###
### libaacs verification
###

print "Checking for libaacs..."
libaacsExists = os.path.isfile(libaacsLocation[CurrentSystem])

if libaacsExists == True:
    print "libaacs was found at: " + libaacsLocation[CurrentSystem]
else:
    print "libaacs needs to be installed at: " + libaacsLocation[CurrentSystem]
    if raw_input('Would you like to install it? (y/n)') == "y":
        if CurrentOS == 'Darwin':
            os.makedirs(os.path.dirname(libaacsLocation[CurrentSystem]))
        else:
            pass
        
        if urllib.urlretrieve(libaacsURL[CurrentSystem], libaacsLocation[CurrentSystem]):
            print "libaacs was downloaded successfully."
        else:
            print "There was a problem downloading libaacs.  Aborting."
            exit  
    else:
        print "Aborting.  libaacs needs to be installed."
        exit
    
###
### KEYS.DB verification
###

print ""
print "Checking for KEYDB.cfg..."
KEYDBExists = os.path.isfile(KEYDBLocation[CurrentSystem])

if KEYDBExists == True:
    print "KEYDB.cfg was found at: " + KEYDBLocation[CurrentSystem]
else:
    print "KEYDB.cfg needs to be installed at: " + KEYDBLocation[CurrentSystem]
    if raw_input('Would you like to create it? (y/n)') == "y":
        if os.makedirs(os.path.dirname(KEYDBLocation[CurrentSystem])):
            pass
        else:
            print "Unable to create directory (or maybe it already exists): " + os.path.dirname(KEYDBLocation[CurrentSystem])
            ##exit
        
        if urllib.urlretrieve (KEYDBURL, KEYDBLocation[CurrentSystem]):
            print "KEYDB.cfg was downloaded successfully."
        else:
            print "There was a problem downloading KEYDB.cfg.  Aborting."
            exit 
    else:
        print "Aborting.  KEYDB.cfg needs to be installed."
        exit

print ""
print "Support files installed.  Launching VLC..."


if CurrentOS == 'Windows':
    import wmi
    for drive in wmi.WMI().Win32_LogicalDisk():
        BDMVDir = os.path.isdir(drive.caption + '\\BDMV')
        if BDMVDir == True:
            print "Bluray disk found at drive " + drive.caption + "\\."
            BlurayDir = drive.caption
            break
if CurrentOS == 'Darwin':
    BDMVDir = glob.glob('/Volumes/*/BDMV')
    BlurayDir = os.path.dirname(BDMVDir[0])
if CurrentOS == 'Linux':
    BDMVDir = glob.glob(os.path.join('/media/*/BDMV'))
    BlurayDir = os.path.dirname(BDMVDir[0])
else:
    exit

process_one = subprocess.Popen([VLCBinary[CurrentSystem], 'bluray:///' + BlurayDir])
