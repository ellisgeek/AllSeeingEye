"""
All Seeing Eye
Oracle Client Configurator
Elliott Saille
12/3/13
"""

from subprocess import call
from os import name
from os import system
from os import access
from os import R_OK
from os import W_OK
from os import makedirs
from os import path
from os import environ
from os import walk
from shutil import rmtree
from shutil import copy2
from sys import exit
from time import sleep
from subprocess import call

#Variables
tempDir  = environ["TEMP"] + "/allSeeingEye"
tnsnamesTemp = tempDir + "/tnsnames.ora"
tnsnames = "C:/oracle/product/10.2.0/client/NETWORK/ADMIN/tnsnames.ora"
oraInstaller = "M:/INSTALL/Voyager8/10203_client_vista-win7"
installTemp = tempDir + "/oracle"
setup = installTemp + "/setup.exe"
compatMode = "VISTASP2"

def compatabilityChange(path, mode="WINXPSP3", runasadmin=True, verbose=False):   
    """
    Borrowed from http://techdiary-viki.blogspot.com/2011/03/script-to-set-compatibility-mode-of.html
    Change the compatibility mode of a windows EXE
    Valid Compatibility modes are:
    WIN95:      Windows 95
    WIN98:      Windows 98 / Windows ME
    WINXPSP2:   Windows XP (Service Pack 2)
    WINXPSP3:   Windows XP (Service Pack 3)
    VISTARTM:   Windows Vista
    VISTASP1:   Windows Vista (Service Pack 1)
    VISTASP2:   Windows Vista (Service Pack 2)
    WIN7RTM:    Windows 7
    WIN8RTM:    Windows 8
    """

    print("Processing path %s" % path)

    files = []
    for dirpath, dirnames, filenames in walk(path):
        files.extend(filenames)
        
    exec_files = filter(lambda x: x.endswith('.exe'), files)
    if verbose:
        print("%d files to process" % len(exec_files))
        print("Setting mode to %s" % mode)
        if runasadmin == True:
            print("Program will run as Administrator")

    for ef in exec_files:
        if verbose:
            print("Processing file %s" % path + '\\' + ef)
        system('REG.EXE ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v "%s" /t REG_SZ /d "%s" /f' % (ef, mode))

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    "resp" should be set to the default value assumed by the caller when
    user simply types ENTER.
    """
    
    if prompt is None:
        prompt = "Confirm"

    if resp:
        prompt = "%s [%s]|%s: " % (prompt, "y", "n")
    else:
        prompt = "%s [%s]|%s: " % (prompt, "n", "y")
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ["y", "Y", "n", "N"]:
            print("please enter y or n.")
            continue
        if ans == "y" or ans == "Y":
            return True
        if ans == "n" or ans == "N":
            return False

def clear():
    system("cls")
    
def backup():
    clear()
    print("Backing up current tnsnames.ora from:")
    print(tnsnames)
    if access(tnsnames, R_OK) == True:
        try:
            copy2(tnsnames, tnsnamesTemp)
        except IOError as e:
            print("\n")
            print("({})".format(e))
            print("\n")
            confirm("Backup Failed!\nReturn to main menu?", True)
            mainMenu()
        else:
         print("\nBackup Complete!\n")
    else:
        clear()
        print("Unable to access tnsnames.ora at:")
        print(tnsnames)
    confirm("Return To main Menu?", True)
    mainMenu()

def download():
    if path.exists(oraInstaller):
        try:
            system("xcopy" +" /I /S \""+ oraInstaller +"\" \""+ installTemp +"\"")
        except IOError as e:
            print("\n")
            print("({})".format(e))
            print("\n")
            confirm("Installation Failed!\nReturn to main menu?", True)
            mainMenu()
        else:
            print("\nInstaller Copied Successfully!\n")
    else:
        confirm("\nFailed to Copy Installer!\nReturn to main menu?", True)
        mainMenu()
    
    if path.exists(setup):
        compatabilityChange(setup, compatMode, True, False)
    else:
        clear()
        print("Could not change compatability mode on:\n%s\n" % setup)
        confirm("Return to main menu?", True)
        mainMenu()

def install():
    clear()
    print("Installing Oracle database client\n")
    if confirm("Continue Installation?", True) == False:
        clear()
        print("Installation aborted")
        sleep(2)
        mainMenu()
        
    if path.exists(setup):
        if confirm("Installer exists!\nUse downloaded installer?", True) == False:
            clear()
            print("Will re-download installer")
            rmtree(installTemp)
            download()
    else:
     download()
    
    call("%s" % setup, shell=True)
    
    confirm("Return To main Menu?", True)
    mainMenu()
    
def mainMenu():
    clear()
    print("Oracle Installation and Configuration Helper")
    print("\n")
    print("1. Backup current tnsnames.ora")
    print("2. Install Oracle 10g Client")
    print("3. Create tnsnames.ora")
    print("4. Add ODBC Configuration")
    print("Q. Exit")
    choise = input("Please Make a Selection: ")
    
    if choise == "1":
        backup()
    elif choise == "2":
        install()
    elif choise == "3":
        print("2")
    elif choise == "4":
        print("2")
    elif choise == "Q" or choise == "q":
        clear()
        quit()
    clear()
    print("Please make a selection!")
    confirm("Return To main Menu?", True)
    mainMenu()

#Clean up and Create Temp Dir for session
if path.exists(tempDir):
    print ("Old temp directory found at %s" % tempDir)
    if confirm("Remove Temp Directory?", True) == True:
        try:
            rmtree(tempDir)
        except IOError as e:
            print("({})".format(e))
        try:
            makedirs(tempDir)
        except IOError as e:
            print("({})".format(e))
    else:
        exit("Will not remove Temp Directory! Please Manually delete directory %s!" % tempDir)
else:
    try:
       makedirs(tempDir)
    except IOError as e:
        print("({})".format(e))

mainMenu()
