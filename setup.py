import sys
from cx_Freeze import setup, Executable

setup(  name = "All Seeing Eye",
        version = "0.1",
        description = "Oracle and Voyanger install helper!",
        options = {"build_exe": include_files = [./supportFiles]},
        executables = [Executable("allSeeingEye.py", base="Win32GUI")])