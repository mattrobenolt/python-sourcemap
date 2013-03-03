"""
sourcemap.objects
=================
"""
from collections import namedtuple

class Token(object):
    def __init__(self, dst_line, dst_col, src, src_line, src_col, name):
        self.dst_line = dst_line
        self.dst_col = dst_col
        self.src = src
        self.src_line = src_line
        self.src_col = src_col
        self.name = name

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        args = self.dst_line, self.dst_col, self.src, self.src_line, self.src_col, self.name
        return '<Token: dst_line=%d dst_col=%d src=%r src_line=%d src_col=%d name=%r>' % args


class SourceMapIndex(object):
    def __init__(self, tokens, keys, sources):
        self.tokens = tokens
        self.keys = keys
        self.sources = sources

    def lookup(self, line, column):
        raise ValueError((line, column))

    def __getitem__(self, item):
        return self.tokens[item]

    def __iter__(self):
        return iter(self.tokens)

    def __repr__(self):
        return '<SourceMapIndex: %s>' % ', '.join(map(str, self.sources))

