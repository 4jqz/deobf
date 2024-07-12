import argparse
import json
import os
import sys
import requests
from os.path import join, dirname, exists

from methods.ben import BenDeobf
from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.notobf import NotObfuscated
from methods.other import OtherDeobf
from utils.decompile import unzipJava, checkUPX
from utils.pyinstaller.pyinstaller import ExtractPYInstaller
from utils.pyinstaller.pyinstallerExceptions import ExtractionError
from utils.webhookspammer import Webhook

import tkinter as tk
from tkinter import filedialog, messagebox

from mega import Mega

def download_from_github(url):
    if "github.com" not in url:
        raise ValueError("URL must be a GitHub repository link")
    
    api_url = url.replace("github.com", "api.github.com/repos") + "/zipball"
    response = requests.get(api_url)
    if response.status_code == 200:
        filename = "downloaded_repo.zip"
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        raise Exception("Failed to download from GitHub")

def download_from_mediafire(url):
    response = requests.get(url, allow_redirects=True)
    download_url = response.url
    file_response = requests.get(download_url)
    filename = "downloaded_file"  # Example filename, adjust as needed
    with open(filename, "wb") as f:
        f.write(file_response.content)
    return filename

def download_from_mega(url):
    mega = Mega()
    m = mega.login()  # Using anonymous login
    file = m.download_url(url)
    return file

def download_from_gofile(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        direct_link = json_response['data']['downloadPage']
        filename = "downloaded_file"
        file_response = requests.get(direct_link)
        if file_response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(file_response.content)
            return filename
        else:
            raise Exception("Failed to download file from Gofile.io")
    else:
        raise Exception("Failed to fetch direct link from Gofile.io")

def ifprint_gui(message):
    output_text.insert(tk.END, message + "\n")

def run_deobfuscator(filename, download=False, output_json=False, is_github=False):
    try:
        if is_github:
            ifprint_gui("[+] Downloading from GitHub")
            filename = download_from_github(filename)
            ifprint_gui("[+] Downloaded from GitHub")
        elif download:
            ifprint_gui("[+] Downloading file")
            if "mediafire.com" in filename:
                filename = download_from_mediafire(filename)
            elif "mega.nz" in filename:
                filename = download_from_mega(filename)
            elif "gofile.io" in filename:
                filename = download_from_gofile(filename)
            else:
                raise ValueError("Unsupported download URL")
            ifprint_gui("[+] File downloaded")

        if not os.path.exists(filename):
            ifprint_gui("[-] This file does not exist")
            return

        filename = os.path.abspath(filename)
        webhook = ""

        if ".jar" in filename:
            ifprint_gui("[+] Java grabber suspected, scanning strings...")
            javadir = unzipJava(filename)
            ben = BenDeobf(javadir)
            webhook = ben.Deobfuscate()
            ifprint_gui(f"[+] Webhook: {webhook}")
            ifprint_gui("[+] Java grabber deobfuscated")
        else:
            if checkUPX(filename):
                ifprint_gui("[!] File packed with UPX")
            try:
                archive = ExtractPYInstaller(filename)
                extractiondir = join(os.getcwd())
                obfuscators = [
                    BlankDeobf,
                    LunaDeobf,
                    VespyDeobf,
                    OtherDeobf,
                    NotObfuscated
                ]
                for deobfuscator in obfuscators:
                    try:
                        ifprint_gui(f"[!] Trying {deobfuscator.__name__} method")
                        deobf = deobfuscator(extractiondir, archive.entrypoints)
                        webhook = deobf.Deobfuscate()
                        if webhook:
                            ifprint_gui(f"[+] Webhook: {webhook}")
                            ifprint_gui(f"[+] {deobfuscator.__name__} deobfuscator succeeded")
                            break
                    except Exception as e:
                        continue
            except ExtractionError as e:
                ifprint_gui(str(e))
                return

        if webhook == "" or webhook is None:
            ifprint_gui("[-] No valid webhook found.")
            return

        # Output the webhook
        ifprint_gui(webhook)

    except Exception as e:
        ifprint_gui(f"Error: {str(e)}")

def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def start_deobfuscation():
    filename = file_entry.get()
    download = download_var.get()
    output_json = json_var.get()
    is_github = github_var.get()
    output_text.delete(1.0, tk.END)
    run_deobfuscator(filename, download, output_json, is_github)

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

json_var = tk.BooleanVar()
tk.Checkbutton(root, text="Output details in JSON format", variable=json_var).pack(pady=5)

tk.Button(root, text="Run Deobfuscator", command=start_deobfuscation).pack(pady=20)

output_text = tk.Text(root, height=15, width=80)
output_text.pack(pady=10)

root.mainloop()
