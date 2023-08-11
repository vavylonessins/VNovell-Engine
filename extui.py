"""
This module contains functions for multi-window behavior
"""

import os
import sys
import b64


def popup(typ, title, text, extra="None"):
	os.system(sys.executable+" popup.py "+b64.encode(typ)+" "+
		b64.encode(title)+" "+b64.encode(text)+" "+b64.encode(extra))
	if typ==POPUP_ERROR:
		sys.exit()


POPUP_ERROR = "1"
POPUP_INFO = "2"
POPUP_WARNING = "3"
POPUP_IMAGE = "4"
