import os, sys
path1 = os.path.dirname(sys.executable)
path2 = path1
path1 = path1.replace("\\","/").replace("C:","/C")
print(f'''Run in Git Bash:\n
export PATH=$PATH:"{path1}/Scripts"\n
{"="*40}
Run in CommandPrompt:\n
set PATH=%PATH%;"{path2}\\Scripts"\n''')
input()
