@echo off
cd /d "%~dp0%"

E:\Miniconda3\python.exe -m nuitka ^
  --standalone ^
  --enable-plugin=pyside6 ^
  --output-dir=build ^
  --remove-output ^
  --assume-yes-for-downloads ^
  --lto=yes ^
  --include-data-dir=x64=x64 ^
  --include-data-file=treeStructure.json=treeStructure.json ^
  --include-data-file=listStructure.json=listStructure.json ^
  --include-data-file=client_info.json=client_info.json ^
  --include-module=uuid,logging ^
  --nofollow-import-to=tkinter,test,unittest,distutils,email,pydoc,xmlrpc,sqlite3,PyQt5,matplotlib,IPython,pygments,docutils,nose,sysconfig,site,lib2to3,ensurepip,venv,tk ^
  main.py

REM "打包完成后暂停，等待用户按任意键退出"
echo.
echo "打包已完成，按任意键关闭窗口..."
pause >nul