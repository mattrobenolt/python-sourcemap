"""
sourcemap.objects
~~~~~~~~~~~~~~~~~

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
from bisect import bisect_right


class Token(object):
    """A Token represents one JavaScript symbol.

    Each token holds a reference to:
        Original line number: dst_line
        Original column number: dst_col
        Source file name: src
        Source line number: src_line
        Source column number: src_col
        Name of the token: name
    """

    __slots__ = ['dst_line', 'dst_col', 'src', 'src_line', 'src_col', 'name']

    def __init__(self, dst_line=0, dst_col=0, src='', src_line=0, src_col=0, name=None):
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

    def __eq__(self, other):
        for key in self.__slots__:
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    def __repr__(self):
        args = self.src, self.dst_line, self.dst_col, self.src_line, self.src_col, self.name
        return '<Token: src=%r dst_line=%d dst_col=%d src_line=%d src_col=%d name=%r>' % args


class SourceMapIndex(object):
    """The indexed sourcemap containing all the Tokens
    and precomputed indexes for searching."""

    def __init__(self, raw, tokens, line_index, index, sources=None):
        self.raw = raw
        self.tokens = tokens
        self.line_index = line_index
        self.index = index
        self.sources = sources or []

    def lookup(self, line, column):
        try:
            # Let's hope for a direct match first
            return self.index[(line, column)]
        except KeyError:
            pass

        # Figure out which line to search through
        line_index = self.line_index[line]
        # Find the closest column token
        i = bisect_right(line_index, column)
        if not i:
            # You're gonna have a bad time
            raise IndexError
        # We actually want the one less than current
        column = line_index[i - 1]
        # Return from the main index, based on the (line, column) tuple
        return self.index[(line, column)]

    def __getitem__(self, item):
        return self.tokens[item]

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __repr__(self):
        return '<SourceMapIndex: %s>' % ', '.join(map(str, self.sources))


class SectionedSourceMapIndex(object):
    """The index for a source map which contains sections
    containing all the Tokens and precomputed indexes for
    searching."""

    def __init__(self, offsets, maps):
        self.offsets = offsets
        self.maps = maps

    def lookup(self, line, column):
        map_index = bisect_right(self.offsets, (line, column)) - 1
        line_offset, col_offset = self.offsets[map_index]
        col_offset = 0 if line != line_offset else col_offset
        result = self.maps[map_index].lookup(line - line_offset, column - col_offset)
        result.dst_line += line_offset
        result.dst_col += col_offset
        return result

    def __repr__(self):
        return '<SectionedSourceMapIndex: %s>' % ', '.join(map(str, self.maps))
