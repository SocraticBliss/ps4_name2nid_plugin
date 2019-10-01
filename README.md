# PS4 Name 2 NID Plugin

SocraticBliss (R)

# Installation Instructions
1) Install the latest https://github.com/SocraticBliss/ps4_module_loader
2) Place the **ps4_name2nid.py** and **needed_nids.txt** files in your IDA's **plugins** directory
3) Open the needed_nids.txt file in Notepad and insert **one** needed PS4 NID per row

Example needed_nids.txt
```
rFCJnwsHUYA
L9bnN8gtIRA
KC23EegtMiY
```

# Usage
1) Load a PS4 Module file (.prx, .sprx, .elf, .self)
2) Select a **name/string** so that it becomes **highlighted** in IDA
3) Press the hotkey **Ctrl+N** and it will turn the name/string into a PS4 NID and show up in the Output window
4) If the PS4 NID is in your needed_nids.txt, it will automatically append the PS4 NID and name to your aerolib.csv!
