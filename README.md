# PS4 Name 2 NID Plugin

SocraticBliss (R)

An IDA Plugin to help create new NIDs to add to your PS4 NID library

# Installation Instructions
1) Place the ps4_name2nid.py and needed_nids.txt files in your IDA's plugins directory
2) Open the needed_nids.txt file in Notepad and add one NID per row that you are looking for (one NID per line)

Example needed_nids.txt
```
rFCJnwsHUYA
L9bnN8gtIRA
KC23EegtMiY
```
3) Load a PS4 Module file (.prx, .sprx, .elf, .self)
4) Select a name/string that you want to turn into a NID so that it becomes highlighted
5) Press the hotkey Ctrl+N and it will turn it into a NID
6) If the NID is in your needed_nids.txt, it will automatically append the NID and name to your aerolib.csv

If you have any suggestions or ideas, please feel free to create pull requests!

To make the most out of this, we have to work together!
