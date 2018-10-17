# -*- coding: utf-8 -*-
#
# Display an estimate of the currently collected exploration data worth
#

import explore_bank as eb
import sys

import Tkinter as tk
import myNotebook as nb


from config import config
from l10n import Locale

VERSION = '0.6.3'
DEF_HONK=500
DEF_VISIBILITY='Y'

this = sys.modules[__name__]	# For holding module globals
this.bank = None
this.frame = None
this.value = None
this.events = None

# Used during preferences
this.settings = []


def plugin_start():
   # App isn't initialised at this point so can't do anything interesting
   return 'ExploreBank'

def plugin_stop():
   # EDMC is shutting down
   this.bank.writeHardBank()
   return "Stopping ExploreBank"

def plugin_app(parent):
   # Create and display widgets
   this.frame = tk.Frame(parent)
   #this.frame.columnconfigure(3, weight=1)
   nb.Label(frame, text = 'Approx. Value Banked:').grid(row = 0, column = 0, sticky=tk.W)
   this.value = nb.Label(frame)
   this.value.grid(row = 0, column = 1)
   this.events = nb.Label(frame)
   settings = get_settings()
   update_visibility(settings[1])

   this.bank = eb.ExploreBank()
   this.bank.honkValue = settings[0]
   display_value()
   display_event()
   return this.frame

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    settings = get_settings()

    if this.settings == []:
        this.settings = [tk.StringVar(), tk.StringVar()]

    nb.Label(frame, text = 'Value for each body in a discovery scan:').grid(row = 0, column = 0, padx = 10, pady = (10,0))
    this.settings[0].set(settings[0])
    nb.Entry(frame, textvariable=this.settings[0]).grid(row = 0, column = 1, sticky = tk.W, pady = (10,0))

    this.settings[1].set(settings[1])
    nb.Checkbutton(frame, text='Display plugin events.', variable=this.settings[1], 
                          onvalue='Y', offvalue='N').grid(row = 1, column = 0, columnspan = 2, padx = 10, sticky = tk.W)
    nb.Button(frame, text="Clear Banked Data", command=this.bank.clearBank).grid(row = 2, column = 0, padx = 10, sticky = tk.W)
    nb.Label(frame, text = "WARNING: Clearing your banked data is irreversable.").grid(row = 2, column = 1, sticky = tk.W)    

    nb.Label(frame, text = 'Version {}'.format(VERSION)).grid(padx = 10, pady = 10, sticky=tk.W)

    return frame

def prefs_changed(cmdr, is_beta):
    #This is for if the honk value is not a number
    settings = get_settings()
    honk = 0
    try:
      honk = int(this.settings[0].get())
    except:
      honk = settings[0]

    events = this.settings[1].get()
    settings = (honk, events)
    set_settings(settings)

    update_visibility(settings[1])
    this.bank.honkValue = settings[0]

    #Display our fields for the case where the bank was cleared
    display_value()
    display_event()

def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] in ['Location', 'FSDJump']:
       this.bank.setLocation(entry)
    elif entry['event'] == 'DiscoveryScan':
       this.bank.honk(entry)
    elif entry['event'] in ['Died', 'SelfDestruct']:
       this.bank.clearBank()
    elif entry['event'] == 'Scan':
       this.bank.scanBody(entry)
    elif entry['event'] == 'SellExplorationData':
       this.bank.sellData(entry)
    elif entry['event'] == 'Shutdown':
       this.bank.writeHardBank()

    display_value()
    display_event()

def display_value():
   this.value['text'] = "{:,}".format(this.bank.getTotalValue())

def display_event():
   this.events['text'] = this.bank.notif_string

def update_visibility(visibility):
   if visibility == "Y":
      this.events.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W)
   else:
      this.events.grid_forget()

def get_settings():
   honk = config.getint("eb-honkVal")
   event = config.get("eb-eventVis")
   if honk == 0:
      honk = DEF_HONK
   if event == None:
      event = DEF_VISIBILITY
   return (honk, event)

def set_settings(settings):
   config.set("eb-honkVal", settings[0])
   config.set("eb-eventVis", settings[1])
    

   
