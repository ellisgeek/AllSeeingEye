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
from shutil import rmtree
from shutil import copy2
from sys import exit

#Variables
"""
tempDir  = environ["TEMP"] + "\\allSeeingEye"
tnsnames = "C:\\oracle\\product\\10.2.0\\client\\NETWORK\\ADMIN\\tnsnames.ora"
tnsnamesTemp = tempDir + "\tnsnames.ora"
"""
tempDir  = environ["TEMP"] + "/allSeeingEye"
tnsnamesTemp = tempDir + "/tnsnames.ora"
tnsnames = "C:/oracle/product/10.2.0/client/NETWORK/ADMIN/tnsnames.ora"


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
            print("({})".format(e))
        else:
         print("\nBackup Complete!\n")
    else:
        clear()
        print("Unable to access tnsnames.ora at:")
        print(tnsnames)
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
        print("2")
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
