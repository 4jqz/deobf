import os
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk  # For handling the icon image
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

# File download functions
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

# GUI message display function
def display_message(message):
    output_text.insert(tk.END, message + "\n")

# Deobfuscation function
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

# Function to reset the icon
def reset_icon():
    root.iconbitmap(default='')

# GUI functions
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

def select_icon():
    file_path = filedialog.askopenfilename(filetypes=[("ICO files", "*.ico")])
    if file_path:
        root.iconbitmap(file_path)
        display_message(f"[+] Icon changed to {file_path}")

# Set default program icon with fallback
default_icon_path = "/mnt/data/image.png"  # Path to the icon image file
icon = None

if os.path.exists(default_icon_path):
    img = Image.open(default_icon_path)
    img = img.resize((64, 64), Image.ANTIALIAS)
    icon = ImageTk.PhotoImage(img)
else:
    print(f"Warning: Icon file '{default_icon_path}' not found. Using default tkinter icon.")

# Create the main window
root = tk.Tk()
root.title("Deobfuscator GUI")
root.geometry("600x400")

# Set background color to white
root.configure(bg='white')

# Set the program icon
if icon:
    root.iconphoto(False, icon)

# Create and place widgets
style = ttk.Style()
style.configure('TLabel', background='white', foreground='black', font=('Helvetica', 12))
style.configure('TButton', background='white', foreground='black', font=('Helvetica', 12), borderwidth=0)
style.configure('TEntry', background='white', foreground='black', font=('Helvetica', 12))
style.configure('TCheckbutton', background='white', foreground='black', font=('Helvetica', 12))

# Create a Frame for the sidebar with a gray background
sidebar = tk.Frame(root, width=150, bg='gray')
sidebar.pack(fill='y', side='left')

# Function to handle button click animations
def on_enter(event):
    event.widget.configure(style='TButton.SmoothOnHover')

def on_leave(event):
    event.widget.configure(style='TButton')

# Create the "Deobfuscator" button with smooth animation
deobfuscator_button = ttk.Button(sidebar, text="Deobfuscator", style='TButton', command=start_deobfuscation)
deobfuscator_button.pack(pady=10, padx=10, fill='x')
deobfuscator_button.bind("<Enter>", on_enter)
deobfuscator_button.bind("<Leave>", on_leave)

# Create the "Settings" button with smooth animation
settings_button = ttk.Button(sidebar, text="Settings", style='TButton', command=select_icon)
settings_button.pack(pady=10, padx=10, fill='x')
settings_button.bind("<Enter>", on_enter)
settings_button.bind("<Leave>", on_leave)

# Create a Notebook for tabs in the main area
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Create the Deobfuscator tab
deobfuscator_tab = ttk.Frame(notebook)
notebook.add(deobfuscator_tab, text="Deobfuscator")

ttk.Label(deobfuscator_tab, text="File to Deobfuscate (or GitHub URL):").pack(pady=10)

file_entry = ttk.Entry(deobfuscator_tab, width=50)
file_entry.pack(pady=5)

ttk.Button(deobfuscator_tab, text="Browse", command=select_file).pack(pady=5)

download_var = tk.BooleanVar()
ttk.Checkbutton(deobfuscator_tab, text="Download the file from a link", variable=download_var).pack(pady=5)

github_var = tk.BooleanVar()
ttk.Checkbutton(deobfuscator_tab, text="Download from GitHub", variable=github_var).pack(pady=5)

ttk.Button(deobfuscator_tab, text="Run Deobfuscator", command=start_deobfuscation).pack(pady=20)

output_text = tk.Text(deobfuscator_tab, height=10, width=70, bg='white', fg='black', insertbackground='black')
output_text.pack(pady=10)

# Create the Settings tab
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="Settings")

ttk.Label(settings_tab, text="Change Program Icon:").pack(pady=10)

ttk.Button(settings_tab, text="Select Icon", command=select_icon).pack(pady=5)
ttk.Button(settings_tab, text="Reset Icon", command=reset_icon).pack(pady=5)

root.mainloop()
