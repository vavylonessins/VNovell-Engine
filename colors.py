from pygame import *


def ColorHex(text):
    text = text[1:][::2]
    ret = []
    for c in text:
        ret.append(eval("0x"+c))
    return tuple(ret.copy())
