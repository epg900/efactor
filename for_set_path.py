import os, sys
import pyperclip
path1 = os.path.dirname(sys.executable)
path2 = path1
path1 = path1.replace("\\","/").replace("C:","/C")
inp = input("\n1. Windows\n2. Linux\nSelect Your OS: ")
if inp=='2':
    pyperclip.copy(f'export PATH=$PATH:"{path1}/Scripts"')
elif inp=='1':
    pyperclip.copy(f'set PATH=%PATH%;"{path2}\\Scripts"')


