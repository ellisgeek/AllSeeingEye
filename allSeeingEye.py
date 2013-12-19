"""
All Seeing Eye
Oracle Client Install Helper!
Elliott Saille
12/3/13
"""
#Include only specific functions
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
setupOpts = "\"FROM_LOCATION=%CD%\stage\products.xml\" -responseFile \"%CD%\response\ExLibrisOracle.rsp\""
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
    #Display path to file that will be changed
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
    """
    Prompts for yes or no response from the user. Returns True for yes and
    False for no.

    "resp" should be set to the default value assumed by the caller when
    user simply types ENTER.
    """
    #set default prompt if none set
    if prompt is None:
        prompt = "Confirm"
        
    #Change the default response
    if resp:
        prompt = "%s [%s]|%s: " % (prompt, "y", "n")
    else:
        prompt = "%s [%s]|%s: " % (prompt, "n", "y")
        
    #Check for user input
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
    """
    Clears the screen
    """
    system("cls")
    
def backup():
    """
    Backs up current tnsnames if it exists
    """
    clear()
    print("Backing up current tnsnames.ora from:")
    print(tnsnames)
    #make sure we can access the file
    if access(tnsnames, R_OK) == True:
        try:
            #Copy it to the Temp Dir
            copy2(tnsnames, tnsnamesTemp)
        #or throw error
        except IOError as e:
            print("\n")
            print("({})".format(e))
            print("\n")
            confirm("Backup Failed!\nReturn to main menu?", True)
            mainMenu()
        #be happy
        else:
         print("\nBackup Complete!\n")
    else:
        clear()
        print("Unable to access tnsnames.ora at:")
        print(tnsnames)
    confirm("Return To main Menu?", True)
    mainMenu()

def download():
    """
    Copies oracle installer from network share
    """
    #Check if installer exists on share
    if path.exists(oraInstaller):
        try:
            #Copy it local
            system("xcopy" +" /I /S \""+ oraInstaller +"\" \""+ installTemp +"\"")
        #Throw a useful error
        except IOError as e:
            print("\n")
            print("({})".format(e))
            print("\n")
            confirm("Installation Failed!\nReturn to main menu?", True)
            mainMenu()
        #If no errors print happy message!
        else:
            print("\nInstaller Copied Successfully!\n")
    #No installer :(
    else:
        confirm("\nInstaller does not exist on share!\nReturn to main menu?", True)
        mainMenu()
    
    #Check if installer has been downloaded
    if path.exists(setup):
        #Change compatibility mode
        compatabilityChange(setup, compatMode, True, False)
    #Or Fail!
    else:
        clear()
        print("Could not find installer,\nnothing to set compatibility for!\n")
        confirm("Return to main menu?", True)
        mainMenu()

def install():
    """
    Sets environment up to run the oracle installer
    """
    clear()
    print("Installing Oracle database client\n")
    
    #Are you shure this is what you want to do?
    if confirm("Continue Installation?", True) == False:
        clear()
        print("Installation aborted")
        sleep(2)
        mainMenu()
    
    #Check if installer has already been downloaded this session
    if path.exists(setup):
        #Ask if you want to reuse downloaded installer and if not re-download
        if confirm("Installer exists!\nUse downloaded installer?", True) == False:
            clear()
            print("Will re-download installer")
            rmtree(installTemp)
            download()
    #If not download the installer
    else:
     download()
    
    #Write some initial configuration stuff to the Registry
    system("reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\MSDTC\MTxOCI /v OracleOciLib /t REG_SZ /d oci.dll /f")
    system("reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\MSDTC\MTxOCI /v OracleSqlLib /t REG_SZ /d orasql10.dll /f")
    system("reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\MSDTC\MTxOCI /v OracleXaLib  /t REG_SZ /d oraclient10.dll /f")
    
    #Call the installer
    call("%s" % setup + " " + setupOpts, shell=True)
    
    confirm("Return To main Menu?", True)
    mainMenu()

def tnsnames():
    """
    Copy preconfigured tnsnames.ora to oracle install location
    Will eventually include option to add custom entries to tnsnames
    """

def mainMenu():
    """
    Display the Main Menu
    """
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
        tnsnames()
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

#Do Stuff!
mainMenu()
