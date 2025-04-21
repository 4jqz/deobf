**If it doesn't work I will fix it at some point**



# Grabbers Deobfuscator

This repository contains some methods to disassemble and deobfuscate discord malwares (Blank, and others). It will give you the webhook and validate it if it found one.

## V2 Usage

```cmd
you can also just open v2 just browse for a file as links dont work (This is the old version of v2 the new one looks abit diffrent but works the same)
```
![Tut](https://github.com/user-attachments/assets/be8201a7-93d2-45ed-9591-250fe973f985)

## Help 
You can also do this to get help

```cmd
python deobf.py -h
```

some grabbers like empyrean need python 3.10 so be sure to check the extractor warnings if there are.
**if you have an error with thiefcat deobfuscation, use python 3.11.4**

## Decompiler & Disassembler

pycdc is precompiled and the binaries are in this repo but if you think these are not safe, please build your own (recommended). Here's the decompiler repository: [https://github.com/zrax/pycdc]

## TODO

if you wish to add a grabber to the methods, Dm me on Discord: `Veinsworld` (link the source code if existing and send me a sample of it (.exe)) or fork this repository and make a pull request.

- [x] Blank (python)
- [x] Vespy (python)
- [x] Luna (python)
- [x] Red Tiger (python)
- [x] Vare obfuscation (Potna stealer?) (python)
- [x] All the random python grabbers with no obfuscation
- [x] W4SP (python)
- [x] Thiefcat (python)
- [x] Ben (Java)
- [x] Creal (python)

## Issues

If you encounter an issue, before creating one on github, please read this. Provide as much informations as possible (stacktraces, with what you used it). If its because your grabber is unsupported, submit your sample in my Discord dms

## Credits

- [PyInstxtractor](https://github.com/extremecoders-re/pyinstxtractor) for the pyinstaller archive extractor
- [PyInstxtractor-ng](https://github.com/extremecoders-re/pyinstxtractor) for the encrypted pyinstaller archive extractor
- [pycdc](https://github.com/zrax/pycdc) for the python bytecode disassembler
