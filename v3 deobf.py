import os
import requests
import tkinter as tk
from tkinter import filedialog
from mega import Mega

from methods.ben import BenDeobf
from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.notobf import NotObfuscated
from methods.other import OtherDeobf
from utils.decompile import unzipJava, checkUPX
from utils.pyinstaller.pyinstaller import ExtractPYInstaller
from utils.pyinstaller.pyinstallerExceptions import ExtractionError

def hide_console():
    import ctypes
    import sys
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

hide_console()

def download_file(url):
    if "github.com" in url:
        url = url.replace("github.com", "api.github.com/repos") + "/zipball"
    response = requests.get(url, allow_redirects=True)
    filename = "downloaded_file"
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename

def download_from_mega(url):
    mega = Mega().login()
    return mega.download_url(url)

def display_message(message):
    output_text.insert(tk.END, message + "\n")

def run_deobfuscator(filename, download=False, is_github=False):
    try:
        if is_github or download:
            display_message("[+] Downloading file")
            if "mega.nz" in filename:
                filename = download_from_mega(filename)
            else:
                filename = download_file(filename)
            display_message("[+] File downloaded")

        if not os.path.exists(filename):
            display_message("[-] This file does not exist")
            return

        filename = os.path.abspath(filename)
        webhook = ""

        if filename.endswith(".jar"):
            display_message("[+] Java grabber suspected, scanning strings...")
            javadir = unzipJava(filename)
            webhook = BenDeobf(javadir).Deobfuscate()
        else:
            if checkUPX(filename):
                display_message("[!] File packed with UPX")
            try:
                archive = ExtractPYInstaller(filename)
                obfuscators = [BlankDeobf, LunaDeobf, VespyDeobf, OtherDeobf, NotObfuscated]

                for Deobf in obfuscators:
                    try:
                        display_message(f"[!] Trying {Deobf.__name__} method")
                        deobf = Deobf(os.getcwd(), archive.entrypoints)
                        webhook = deobf.Deobfuscate()
                        if webhook:
                            break
                    except Exception:
                        continue
            except ExtractionError as e:
                display_message(str(e))
                return

        if not webhook:
            display_message("[-] No valid webhook found.")
        else:
            display_message(f"[+] Webhook: {webhook}")

    except Exception as e:
        display_message(f"Error: {str(e)}")

def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def start_deobfuscation():
    filename = file_entry.get()
    download = download_var.get()
    is_github = github_var.get()
    output_text.delete(1.0, tk.END)
    run_deobfuscator(filename, download, is_github)

root = tk.Tk()
root.title("Deobfuscator GUI")

tk.Label(root, text="File to Deobfuscate (or GitHub URL):").pack(pady=5)
file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_file).pack(pady=5)

download_var = tk.BooleanVar()
tk.Checkbutton(root, text="Download the file from a link", variable=download_var).pack(pady=5)

github_var = tk.BooleanVar()
tk.Checkbutton(root, text="Download from GitHub", variable=github_var).pack(pady=5)

tk.Button(root, text="Run Deobfuscator", command=start_deobfuscation).pack(pady=20)

output_text = tk.Text(root, height=15, width=80)
output_text.pack(pady=10)

root.mainloop()
