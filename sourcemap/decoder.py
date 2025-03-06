"""
sourcemap.decoder
~~~~~~~~~~~~~~~~~

Includes source from:
    https://github.com/martine/python-sourcemap
Original source under Apache license, see:
    https://github.com/martine/python-sourcemap/blob/master/COPYING

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
import os
import sys
from functools import partial
from .exceptions import SourceMapDecodeError, SourceMapInvalidError
from .objects import Token, SourceMapIndex, SectionedSourceMapIndex
try:
    import simplejson as json
except ImportError:
    import json  # NOQA

__all__ = ('SourceMapDecoder',)

if sys.version_info[0] == 2:
    from itertools import imap as map
    text_type = unicode
else:
    text_type = str


class SourceMapDecoder(object):
    def parse_vlq(self, segment):
        """
        Parse a string of VLQ-encoded data.

        Returns:
          a list of integers.
        """

        values = []

        cur, shift = 0, 0
        for c in segment:
            val = B64[ord(c)]
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
        """Decode a source map object into a SourceMapIndex or
        SectionedSourceMapIndex.

        For SourceMapIndex:
        The index is keyed on (dst_line, dst_column) for lookups,
        and a per row index is kept to help calculate which Token to retrieve.

        For example:
            A minified source file has two rows and two tokens per row.

            # All parsed tokens
            tokens = [
                Token(dst_row=0, dst_col=0),
                Token(dst_row=0, dst_col=5),
                Token(dst_row=1, dst_col=0),
                Token(dst_row=1, dst_col=12),
            ]

            Two dimentional array of columns -> row
            rows = [
                [0, 5],
                [0, 12],
            ]

            Token lookup, based on location
            index = {
                (0, 0):  tokens[0],
                (0, 5):  tokens[1],
                (1, 0):  tokens[2],
                (1, 12): tokens[3],
            }

            To find the token at (1, 20):
              - Check if there's a direct hit on the index (1, 20) => False
              - Pull rows[1] => [0, 12]
              - bisect_right to find the closest match:
                  bisect_right([0, 12], 20) => 2
              - Fetch the column number before, since we want the column
                lte to the bisect_right: 2-1 => row[2-1] => 12
              - At this point, we know the token location, (1, 12)
              - Pull (1, 12) from index => tokens[3]

        For SectionedSourceMapIndex:
        The offsets are stored as tuples in sorted order:
        [(0, 0), (1, 10), (1, 24), (2, 0), ...]

        For each offset there is a corresponding SourceMapIndex
        which operates as described above, except the tokens
        are relative to their own section and must have the offset
        replied in reverse on the destination row/col when the tokens
        are returned.

        To find the token at (1, 20):
            - bisect_right to find the closest index (1, 20)
            - Supposing that returns index i, we actually want (i - 1)
              because the token we want is inside the map before that one
            - We then have a SourceMapIndex and we perform the search
              for (1 - offset[0], column - offset[1]). [Note this isn't
              exactly correct as we have to account for different lines
              being searched for and the found offset, so for the column
              we use either offset[1] or 0 depending on if line matches
              offset[0] or not]
            - The token we find we then translate dst_line += offset[0],
              and dst_col += offset[1].
        """
        # According to spec (https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#heading=h.h7yy76c5il9v)
        # A SouceMap may be prepended with ")]}'" to cause a Javascript error.
        # If the file starts with that string, ignore the entire first line.
        if source[:4] == ")]}'" or source[:3] == ")]}":
            source = source.split('\n', 1)[1]

        smap = json.loads(source)
        if smap.get('sections'):
            offsets = []
            maps = []
            for section in smap.get('sections'):
                offset = section.get('offset')
                offsets.append((offset.get('line'), offset.get('column')))
                maps.append(self._decode_map(section.get('map')))
            return SectionedSourceMapIndex(smap, offsets, maps)
        else:
            return self._decode_map(smap)

    def _decode_map(self, smap):
        sources = smap['sources']
        if not all(isinstance(item, str) for item in sources):
            raise SourceMapInvalidError("Sources must be a list of strings")

        sourceRoot = smap.get('sourceRoot')
        names = list(map(text_type, smap['names']))
        mappings = smap['mappings']
        lines = mappings.split(';')

        if sourceRoot is not None:
            sources = list(map(partial(os.path.join, sourceRoot), sources))

        # List of all tokens
        tokens = []

        # line_index is used to identify the closest column when looking up a token
        line_index = []

        # Main index of all tokens
        # The index is keyed on (line, column)
        index = {}

        dst_col, src_id, src_line, src_col, name_id = 0, 0, 0, 0, 0
        for dst_line, line in enumerate(lines):
            # Create list for columns in index
            line_index.append([])

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
                    try:
                        src_id += parse[1]
                        if not 0 <= src_id < len(sources):
                            raise SourceMapDecodeError(
                                "Segment %s references source %d; there are "
                                "%d sources" % (segment, src_id, len(sources))
                            )

                        src = sources[src_id]
                        src_line += parse[2]
                        src_col += parse[3]

                        if len(parse) > 4:
                            name_id += parse[4]
                            if not 0 <= name_id < len(names):
                                raise SourceMapDecodeError(
                                    "Segment %s references name %d; there are "
                                    "%d names" % (segment, name_id, len(names))
                                )

                            name = names[name_id]
                    except IndexError:
                        raise SourceMapDecodeError(
                            "Invalid segment %s, parsed as %r"
                            % (segment, parse)
                        )

                try:
                    assert dst_line >= 0, ('dst_line', dst_line)
                    assert dst_col >= 0, ('dst_col', dst_col)
                    assert src_line >= 0, ('src_line', src_line)
                    assert src_col >= 0, ('src_col', src_col)
                except AssertionError as e:
                    error_info = e.args[0]
                    raise SourceMapDecodeError(
                        "Segment %s has negative %s (%d), in file %s"
                        % (segment, error_info[0], error_info[1], src)
                    )

                token = Token(dst_line, dst_col, src, src_line, src_col, name)
                tokens.append(token)

                # Insert into main index
                index[(dst_line, dst_col)] = token

                # Insert into specific line index
                line_index[dst_line].append(dst_col)

        return SourceMapIndex(smap, tokens, line_index, index, sources)


# Mapping of base64 letter -> integer value.
# This weird list is being allocated for faster lookups
B64 = [-1] * 123
for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'):
    B64[ord(c)] = i
