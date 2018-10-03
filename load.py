# -*- coding: utf-8 -*-
#
# Display an estimate of the currently collected exploration data worth
#

import sys

import Tkinter as tk
from ttkHyperlinkLabel import HyperlinkLabel
import myNotebook as nb


from config import config
from l10n import Locale

VERSION = '0.01'

#Indices
DETAILED_INDEX = 0
BASIC_INDEX = 1
#Stars
T_TTauri = (2895, 1208)
WolfRaynet = (2931, 1221)
Carbon = (2930, 1222)
WhiteDwarf = (34294, 14289)
BlackHole = (60589, 25819)
GiantStar = (3122, 1301)
#Planets
WaterGiant = (1824, 760)
HeGiant = (2095, 986)
IcyBody = (1246, 535)
BODIES = { 
# Stars
           "O" : (6135, 2556),
           "B" : (3012, 1255),
           "A" : (2949, 1226),
           "F" : (2932, 1222),
           "G" : (2919, 1216),
           "K" : (2916, 1216),
           "M" : (2903, 1208),
           "L" : (2889, 1204),
           "T" : T_TTauri,
           "Y" : (2881, 1200),
           "TTS" : T_Tauri,
           "AeBe" : (3077, 1282),
           "W" : WolfRaynet,
           "WN" : WolfRaynet,
           "WNC" : WolfRaynet,
           "WC" : WolfRaynet,
           "WO" : WolfRaynet,
           "CS" : Carbon,
           "C" : Carbon,
           "CN" : Carbon,
           "CJ" : Carbon,
           "CH" : Carbon,
           "CHd" : Carbon,
# I don't know about MS and S but I'm guessing similar to carbon so
# thats what I'm going with
           "MS" : Carbon,
           "S" : Carbon,
           "D" : WhiteDwarf,
           "DA" : WhiteDwarf,
           "DAB" : WhiteDwarf,
           "DAO" : WhiteDwarf,
           "DAZ" : WhiteDwarf,
           "DAV" : WhiteDwarf,
           "DB" : WhiteDwarf,
           "DBZ" : WhiteDwarf,
           "DBV" : WhiteDwarf,
           "DO" : WhiteDwarf,
           "DOV" : WhiteDwarf,
           "DQ" : WhiteDwarf,
           "DC" : WhiteDwarf,
           "DCV" : WhiteDwarf,
           "DX" : WhiteDwarf,
           "N" : (54782, 22814),
           "H" : BlackHole,
           "SupermassiveBlackHole" : BlackHole,
           "A_BlueWhiteSuperGiant" : GiantStar,
           "F_WhiteSuperGiant" : GiantStar,
           "M_RedSuperGiant" : GiantStar,
           "M_RedGiant" : GiantStar,
           "K_OrangeGiant" : GiantStar,
# Planets
           "Metal rich body" : (65045, 27102),
           "High metal content body" : (34310, 13866),
           "Terraformable High metal content body" : (412249, 171770),
           "Rocky body" : (928, 500)
           "Terraformable Rocky body" : (181104, 75460)
           "Icy body" : IcyBody,
           "Rocky ice body" : IcyBody,
           "Earthlike body" : (627885, 261619),
           "Water world" : (301410, 125587),
           "Terraformable Water world" : (694971, 289587),
           "Ammonia world" : (320203, 133418),
           "Water giant" : WaterGiant,
           "Water giant with life" : WaterGiant,
           "Gas giant with water based life" : (2314, 964),
           "Gas giant with ammonia based life" : (1721, 717),
           "Sudarsky class I class giant" : (7013, 2922),
           "Sudarsky class II class giant" : (53663, 22360),
           "Sudarsky class III class giant" : (2693, 1122),
           "Sudarsky class IV class giant" : (2799, 1166),
           "Sudarsky class V class giant" : (2761, 1150),
           "Helium gas giant" : HeGiant,
           "Helium rich gas giant" : HeGiant
}


this = sys.modules[__name__]	# For holding module globals
this.frame = None

# Used during preferences
this.settings = None


def plugin_start():
    # App isn't initialised at this point so can't do anything interesting
    return 'ExploreBank'

def plugin_app(parent):
    # Create and display widgets
    this.frame = tk.Frame(parent)
    this.frame.columnconfigure(3, weight=1)
    this.spacer = tk.Frame(this.frame)	# Main frame can't be empty or it doesn't resize
    update_visibility()
    return this.frame

def plugin_prefs(parent, cmdr, is_beta):
   pass

def prefs_changed(cmdr, is_beta):
   pass

def journal_entry(cmdr, is_beta, system, station, entry, state):
   pass

def update_visibility():
   pass
