# PS4 Name 2 NID Plugin

SocraticBliss (R)

ps4_name2nid.py: IDA plugin to help create new NIDs to extend aerolib.csv

# Installation Instructions
0) Install the latest https://github.com/SocraticBliss/ps4_module_loader
1) Place the **ps4_name2nid.py** and **needed_nids.txt** files in your IDA's **plugins** directory
2) Open the needed_nids.txt file in Notepad and insert **one** needed PS4 NID per row

Example needed_nids.txt
```
rFCJnwsHUYA
L9bnN8gtIRA
KC23EegtMiY
```
3) Load a PS4 Module file (.prx, .sprx, .elf, .self)
4) Select a **name/string** so that it becomes **highlighted** in IDA
5) Press the hotkey **Ctrl+N** and it will turn the name/string into a PS4 NID and show up in the Output window
6) If the PS4 NID is in your needed_nids.txt, it will automatically append the PS4 NID and name to your aerolib.csv!

If you have any suggestions or ideas, please feel free to create pull requests!

To make the most out of this, we have to work together!
