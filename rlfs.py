"""
project file system module
"""

from include import include
import excs as exc
import os


class Setup:
    def __init__(self, basedir, base=0):
        self.basedir = basedir
        self.base = base
        self.error_anyway = 0

    def list(self):
        return list(os.listdir(self.basedir))

    def cwd(self):
        return self.basedir

    def get_name(self, fp):
        rname = fp.replace("res:/", self.basedir)
        if os.path.dirname(rname) == self.basedir and os.path.isfile(rname) and self.base or self.error_anyway:
            raise exc.AccessError
        return rname

    def system_get_name(self, fp):
        return fp.replace("res:/", self.basedir)

    def open(self, fp, mode):
        return open(self.get_name(fp), mode)
