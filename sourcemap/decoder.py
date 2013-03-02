"""
sourcemap.decoder
=================
"""
from .objects import Sourcemap

class SourcemapDecoder(object):
    def __init__(self):
        pass

    def decode(self, source):
        return Sourcemap()
