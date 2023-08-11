"""
b65 - more friendly base64 encode/decode
"""

from base64 import b64encode, b64decode


def encode(text, coding='utf-8'):
    """
    encodes utf-8 string via base64 and returns base64 string
    """
    return b64encode(text.encode(coding)).decode(coding)


def decode(text, coding='utf-8'):
    """
    decodes base64 string and returns utf-8 string
    """
    return b64decode(text.encode(coding)).decode(coding)
