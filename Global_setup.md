# VHDL_parse Global Setup 🚀
If you want to use these scripts from anywhere on your computer here is how.
---
1. Add the scripts folder to your computers PATH [guide here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
2. make sure that you compputer is set to open .py files with python and not a code editor like VS Code
3. On windows change your register for python to allow it to acept arguments when opened without the 'python' comand preceding the script name [guide here] (https://eli.thegreenplace.net/2010/12/14/problem-passing-arguments-to-python-scripts-on-windows/)
     Set HKEY_CLASSES_ROOT\Applications\python26.exe\shell\open\command key to "C:\Python26\python26.exe" "%1" %*"
     Where the C:\...... path is what ever your curent path to python is, but now you have %* at the end
