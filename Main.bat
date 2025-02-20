@echo off
echo Installing required Python packages...

pip install requests mega.py ttkbootstrap Pillow
cls
pip show requests
timeout /t 3 /nobreak > nul
cls
pip show mega.py
timeout /t 3 /nobreak > nul
cls
pip show ttkbootstrap 
timeout /t 3 /nobreak > nul
cls
pip show pillow
timeout /t 3 /nobreak >nul
cls


python -c "import tkinter" 2>NUL
IF ERRORLEVEL 1 (
    echo Installing tkinter...
    python -m pip install tk
) ELSE (
    echo tkinter is already installed.
)

echo Running the Deobfuscator GUI...
python "%~dp0gui2.py"
pause
