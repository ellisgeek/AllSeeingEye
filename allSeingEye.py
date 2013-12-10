"""
All Seeing Eye
Oracle Client Configurator
Elliott Saille
12/3/13
"""

from subprocess import call
from os import name
from os import system
from shutil import copy2

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print("please enter y or n.")
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def backup():
    location = "C:\oracle\product\10.2.0\client\NETWORK\ADMIN\tnsnames.ora"
    print("Backing up current tnsnames.ora")
    
    print("from %s" % location
    

    confirm("Return To main Menu?", True)
    mainMenu()

def end():
    quit()

def clear():
    system('cls' if name=='nt' else 'clear')
    
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
        end()
    print("Please make a selection!")
    confirm("Return To main Menu?", True)
    mainMenu()

mainMenu()