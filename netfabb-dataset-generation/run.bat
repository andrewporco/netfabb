@echo off

set USER_ID=2
set CONDA_EXE="\\andrew.ad.cmu.edu\users\users%USER_ID%\%username%\miniconda\Scripts\conda.exe"
set PYTHON_SCRIPT="\\andrew.ad.cmu.edu\users\users%USER_ID%\%username%\Desktop\netfabb-dataset-generation\batch-simulate.py"
set INDEX_FILE="\\andrew.ad.cmu.edu\users\users%USER_ID%\%username%\Desktop\netfabb-dataset-generation\start-stop-indices.txt"

set /P INDICES=<%INDEX_FILE%

echo.
echo Beginning batch simulation for shape indices: %INDICES%
echo Running Python script through Conda...
echo Check progress in C:\Users\%username%\SandBox\messages.txt
echo.

CALL %CONDA_EXE% run -n base python %PYTHON_SCRIPT% %INDICES% %username%

pause
