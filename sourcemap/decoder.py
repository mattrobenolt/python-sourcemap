"""
sourcemap.decoder
=================
"""

from .exceptions import SourceMapDecodeError
from .objects import Token, SourceMapIndex
try:
    import simplejson as json
except ImportError:
    import json


__all__ = ('SourceMapDecoder')


class SourceMapDecoder(object):
    def __init__(self):
        pass

    def parse_vlq(self, segment):
        """
        Parse a string of VLQ-encoded data.

        Returns:
          a list of integers.
        """

        values = []

        cur, shift = 0, 0
        for c in segment:
            val = B64[c]
            # Each character is 6 bits:
            # 5 of value and the high bit is the continuation.
            val, cont = val & 0b11111, val >> 5
            cur += val << shift
            shift += 5

            if not cont:
                # The low bit of the unpacked value is the sign.
                cur, sign = cur >> 1, cur & 1
                if sign:
                    cur = -cur
                values.append(cur)
                cur, shift = 0, 0

        if cur or shift:
            raise SourceMapDecodeError('leftover cur/shift in vlq decode')

        return values

    def decode(self, source):
        # According to spec (https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#heading=h.h7yy76c5il9v)
        # A SouceMap may be prepended with ")]}'" to cause a Javascript error.
        # If the file starts with that string, ignore the entire first line.
        if source[:4] == ")]}'":
            source = source.split('\n', 1)[1]

        smap = json.loads(source)
        sources = smap['sources']
        sourceRoot = smap.get('sourceRoot')
        names = smap['names']
        mappings = smap['mappings']
        lines = mappings.split(';')

        if sourceRoot is not None:
            sources = ['%s/%s' % (sourceRoot, source) for source in sources]

        tokens = []
        keys = []

        dst_col, src_id, src_line, src_col, name_id = 0, 0, 0, 0, 0
        for dst_line, line in enumerate(lines):
            segments = line.split(',')
            dst_col = 0
            for segment in segments:
                if not segment:
                    continue
                parse = self.parse_vlq(segment)
                dst_col += parse[0]

                src = None
                name = None
                if len(parse) > 1:
                    src_id += parse[1]
                    src = sources[src_id]
                    src_line += parse[2]
                    src_col += parse[3]

                    if len(parse) > 4:
                        name_id += parse[4]
                        name = names[name_id]

                try:
                    assert dst_line >= 0
                    assert dst_col >= 0
                    assert src_line >= 0
                    assert src_col >= 0
                except AssertionError:
                    raise SourceMapDecodeError

                # print dst_line, dst_col, src, src_line, src_col, name

                token = Token(dst_line, dst_col, src, src_line, src_col, name)
                tokens.append(token)
                keys.append((dst_line, dst_col))
        return SourceMapIndex(tokens, keys, sources)



# Mapping of base64 letter -> integer value.
B64 = dict(
    (c, i) for i, c in
    enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
)
