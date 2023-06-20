from base64 import b64encode, b64decode


def encode(text, coding='utf-8'):
    return b64encode(text.encode(coding)).decode(coding)


def decode(text, coding='utf-8'):
    return b64decode(text.encode(coding)).decode(coding)
