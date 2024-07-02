import argparse
import json
import os
import sys
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


argparser = argparse.ArgumentParser(
    description="Grabbers Deobfuscator\nPls star https://github.com/TaxMachine/Grabbers-Deobfuscator",
    epilog="Made by TaxMachine"
)
argparser.add_argument(
    "filename",
    help="File to deobfuscate"
)
argparser.add_argument(
    "-d", "--download",
    help="Download the file from a link",
    action="store_true"
)
argparser.add_argument(
    "-j", "--json",
    help="output details in a json format",
    action="store_true"
)

args = argparser.parse_args()

def ifprint(message):
    if not args.json:
        print(message)

def main():
    if args.download:
        ifprint("[+] Downloading file")
        # Implement TryDownload logic if needed
        # filename = TryDownload(args.filename)
        filename = args.filename  # For testing without downloading
        ifprint("[+] File downloaded")
    else:
        if not os.path.exists(args.filename):
            ifprint("[-] This file does not exist")
            sys.exit(1)
        filename = args.filename

    filename = os.path.abspath(filename)
    webhook = ""

    if ".jar" in filename:
        ifprint("[+] Java grabber suspected, scanning strings...")
        javadir = unzipJava(filename)
        ben = BenDeobf(javadir)
        webhook = ben.Deobfuscate()
        ifprint(f"[+] Webhook: {webhook}")
        ifprint("[+] Java grabber deobfuscated")
    else:
        if checkUPX(filename):
            ifprint("[!] File packed with UPX")
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
                    ifprint(f"[!] Trying {deobfuscator.__name__} method")
                    deobf = deobfuscator(extractiondir, archive.entrypoints)
                    webhook = deobf.Deobfuscate()
                    if webhook:
                        ifprint(f"[+] Webhook: {webhook}")
                        ifprint(f"[+] {deobfuscator.__name__} deobfuscator succeeded")
                        break
                except Exception as e:
                    continue
        except ExtractionError as e:
            ifprint(e)
            sys.exit(1)

    if webhook == "" or webhook is None:
        ifprint("[-] No valid webhook found.")
        sys.exit(1)

    # Output the webhook
    print(webhook)


if __name__ == '__main__':
    main()
