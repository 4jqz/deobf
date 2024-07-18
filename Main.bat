@echo off
echo Installing required Python packages...

pip install requests
pip install mega.py

REM Check if tkinter is installed (for Windows, assuming Python is installed in the default location)
python -c "import tkinter" 2>NUL
IF ERRORLEVEL 1 (
    echo Installing tkinter...
    REM Install tkinter using the appropriate method for your system
    python -m pip install tk
) ELSE (
    echo tkinter is already installed.
)

REM Check if ctypes is installed (part of standard library, so this is usually not necessary)
python -c "import ctypes" 2>NUL
IF ERRORLEVEL 1 (
    echo ctypes is part of the standard library and should be installed with Python.
    REM If it's not installed, provide instructions or install it
) ELSE (
    echo ctypes is already installed.
)

echo Running the Deobfuscator GUI...
python path\to\your\script.py
pause
