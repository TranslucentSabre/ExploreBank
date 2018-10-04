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
