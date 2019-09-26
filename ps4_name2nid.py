#!/usr/bin/env python
'''

PS4 Name2NID IDA Plugin by SocraticBliss (R)

ps4_name2nid.py: IDA plugin for creating NIDs for Sony PlayStation(R) 4 files

'''

from base64 import b64encode as base64enc
from binascii import unhexlify as uhx
from hashlib import sha1
from idaapi import *
from idc import *

import csv
import idaapi
import idc
import shutil
import struct

NEW_NIDS = {}
AEROLIB  = 'aerolib.csv'
NEEDED   = 'needed_nids.txt'

# PROGRAM START

# Load NID Library...
def load_nids(directory, library):

    try:
        path = '%s/%s/%s' % (idc.idadir(), directory, library)
        
        with open(path) as database:
            if library == AEROLIB:
                NIDS = dict(row for row in csv.reader(database, delimiter=' '))
            else:
                NIDS = [row.strip() for row in database]
    
    except IOError:
        retry = idaapi.ask_file(0, '%s|*.csv|All files (*.*)|*.*', 'Please gimme your %s file' % (library))
        
        if retry != None:
            try:
                with open(retry) as database:
                    if library == AEROLIB:
                        NIDS = dict(row for row in csv.reader(database, delimiter=' '))
                    else:
                        NIDS = [row.strip() for row in database]
                        shutil.copy2(retry, path)
            except:
                print('Ok, no NIDs for you!')
        else:
            print('Ok, no NIDs for you!')
    
    return NIDS

# Save NID Library...
def save_nids(directory, library, NIDS):

    try:
        path = '%s/%s/%s' % (idc.idadir(), directory, library)
        mode = 'a' if library == AEROLIB else 'w'
        
        with open(path, mode) as database:
            if library == AEROLIB:
                for nid, name in sorted(NIDS.items(), key=lambda x: x[1]):
                    database.write('%s %s\n' % (nid, name))
            else:
                for nid in NIDS:
                    database.write('%s\n' % nid)
    except:
        idc.error('Error saving the %s :(' % library)
    

class NIDify_Handler(idaapi.action_handler_t):

    def __init__(self):
    
        idaapi.action_handler_t.__init__(self)
    
    def activate(self, ctx):
    
        # Load Needed NIDs...
        NEEDED_NIDS = load_nids('plugins', NEEDED)
        #print('Needed NIDs: %s' % NEEDED_NIDS)
        
        # Get the name from IDA...
        name = idaapi.get_highlighted_identifier()
        if name is None:
            print('# Error: Please select a valid string in IDA...')
            return 1
        
        # Make the NID...
        symbol = sha1(name.encode() + uhx('518D64A635DED8C1E6B039B1C3E55230')).digest()
        id     = struct.unpack('<Q', symbol[:8])[0]
        nid    = base64enc(uhx('%016x' % id), b'+-').rstrip(b'=')
        
        print('%s %s' % (nid, name))
        
        # If the NID is Needed and isn't in our list, add it!
        if nid in NEEDED_NIDS:
        
            print('# Found a missing NID!')
            
            # Add the NID and name to our dictionary...
            NEW_NIDS[nid] = name
            #print(NEW_NIDS)
            
            # Update the Aerolib file...
            save_nids('loaders', AEROLIB, NEW_NIDS)
            print('# Successfully updated aerolib.csv!')
            
            # Remove the nid from the New list...
            
            # Next remove the NID...
            NEW_NIDS.pop(nid)
            #print(NEW_NIDS)
            NEEDED_NIDS.remove(nid)
            #print(NEEDED_NIDS)
            
            # Update the Needed file...
            save_nids('plugins', NEEDED, NEEDED_NIDS)
            print('# Successfully updated needed_nids.txt!')
            
            print('---------------------------------------------------------------------------------------------')
        
        return 1
    
    def update(self, ctx):
    
        return idaapi.AST_ENABLE_ALWAYS
    
'''
class Print_Handler(idaapi.action_handler_t):

    def __init__(self):
    
        idaapi.action_handler_t.__init__(self)
    
    def activate(self, ctx):
    
        if len(NEW_NIDS) > 0:
            print('# New NIDs:')
            for nid, name in sorted(NEW_NIDS.items(), key=lambda x: x[1]):
                print('%s %s' % (nid, name))
        else:
            print('# No New NIDs found!')
        
        print('---------------------------------------------------------------------------------------------')
        
        return 1
    
    def update(self, ctx):
    
        return idaapi.AST_ENABLE_ALWAYS
    

class Save_Handler(idaapi.action_handler_t):

    def __init__(self):
    
        idaapi.action_handler_t.__init__(self)
    
    def activate(self, ctx):
        
        if len(NEW_NIDS) > 0:
            # Save the NIDs to Aerolib...
            save_nids('loaders', AEROLIB, NEW_NIDS)
            print('# Successfully updated aerolib.csv!')
        else:
            print('# No New NIDs saved!')
        
        print('---------------------------------------------------------------------------------------------')
        
        return 1
    
    def update(self, ctx):
    
        return idaapi.AST_ENABLE_ALWAYS
    
'''
class ps4_name2nid_t(idaapi.plugin_t):

    flags   = PLUGIN_UNL
    comment = 'PS4 Name2NID'
    help    = 'Select a name and use the assigned hotkey'
    
    wanted_name   = 'PS4 Name2NID'
    wanted_hotkey = ''
    
    def init(self):
    
        print('# PS4 Name2NID Plugin')
        
        if idaapi.IDA_SDK_VERSION < 700:
        
            print('Error: This plugin has only been tested on 7.0+')
            return PLUGIN_SKIP
        
        else:
            # Load Aerolib...
            #NIDS = load_nids('loaders', AEROLIB)
            
            idaapi.create_menu('PS4', 'PS4')
            
            action_desc = idaapi.action_desc_t('NIDify', 'NIDify', NIDify_Handler(), 'Ctrl+N', 'NIDify the selected name', 199)
            idaapi.register_action(action_desc)
            idaapi.attach_action_to_menu('PS4/NIDify', 'NIDify', idaapi.SETMENU_APP)
            '''
            action_desc = idaapi.action_desc_t('Print NIDs', 'Print NIDs', Print_Handler(), 'Ctrl+H', 'Print the New NIDs', 199)
            idaapi.register_action(action_desc)
            idaapi.attach_action_to_menu('PS4/Print NIDs', 'Print NIDs', idaapi.SETMENU_APP)
            
            action_desc = idaapi.action_desc_t('Save NIDs', 'Save NIDs', Save_Handler(), 'Ctrl+Y', 'Save the New NIDs', 199)
            idaapi.register_action(action_desc)
            idaapi.attach_action_to_menu('PS4/Save NIDs', 'Save NIDs', idaapi.SETMENU_APP)
            '''
            return PLUGIN_KEEP
    
    def run(self, arg):
    
        pass
    
    def term(self):
    
        pass
    

def PLUGIN_ENTRY():

    return ps4_name2nid_t()

# PROGRAM END