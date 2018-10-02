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

BODIES = { "OStar" : (6135, 2556),
           "BStar" : (3012, 1255),
           "AStar" : (2949, 1226),
           "FStar" : (2932, 1222),
           "GStar" : (2919, 1216),
           "KStar" : (2916, 1216),
           "MStar" : (2903, 1208),
           "WolfRaynet" : (2931, 1221),
           "Herbig" : (3077, 1282),
           "LStar" : (2889, 1204),
           "TStar" : (2895, 1208),
           "YStar" : (2881, 1200),
           "Neutron" : (54782, 22814),
           "DStar" : (34294, 14289),
           "BlackHole" : (60589, 25819),
           "GiantStar" : (3122, 1301),
           "CarbonStar" : (2930, 1222)
           "GasGiantWAmmoniaL" : (1721, 717),
           "GasGiantWWaterL" : (2314, 964),
           "ClassIGiant" : (7013, 2922),
           "ClassIIGiant" : (53663, 22360),
           "ClassIIIGiant" : (2693, 1122),
           "ClassIVGiant" : (2799, 1166),
           "ClassVGiant" : (2761, 1150),
           "WaterGiant" : (1824, 760)
           "HeGiants" : (2095, 986),
           "HMC" : (34310, 13866, 412249, 171770),
           "TWW" : (301410, 125587, 694971, 289587),
           "MRB" : (65045, 27102),
           "ELW" : (627885, 261619),
           "Ammonia" : (320203, 133418),
           "Icy" : (1246, 535),
           "Rocky" : (928, 500, 181104, 75460)
}

VALUE = { "Basic" : {},
          "Detailed" : {}
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
