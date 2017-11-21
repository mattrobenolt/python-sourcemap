try:
    import unittest2 as unittest
except ImportError:
    import unittest
from sourcemap.objects import Token, SourceMapIndex, SectionedSourceMapIndex


class TokenTestCase(unittest.TestCase):
    def test_eq(self):
        assert Token(1, 1, 'lol.js', 1, 1, 'lol') == Token(1, 1, 'lol.js', 1, 1, 'lol')
        assert Token(99, 1, 'lol.js', 1, 1, 'lol') != Token(1, 1, 'lol.js', 1, 1, 'lol')

class SectionedSourceMapIndexTestCase(unittest.TestCase):
    def get_index(self):
        offsets = [(0, 0), (1, 14), (2, 28)]
        tokens0 = [
            Token(dst_line=0, dst_col=0),
            Token(dst_line=0, dst_col=5),
            Token(dst_line=1, dst_col=0),
            Token(dst_line=1, dst_col=12),
        ]
        tokens1 = [
            Token(dst_line=0, dst_col=0),
            Token(dst_line=0, dst_col=5),
            Token(dst_line=1, dst_col=0),
            Token(dst_line=1, dst_col=12),
        ]
        tokens2 = [
            Token(dst_line=0, dst_col=0),
            Token(dst_line=0, dst_col=5),
            Token(dst_line=1, dst_col=0),
            Token(dst_line=1, dst_col=12),
        ]
        maps = [
            SourceMapIndex({}, tokens0,
                [
                    [0, 5],
                    [0, 12],
                ],
                {
                    (0, 0):  tokens0[0],
                    (0, 5):  tokens0[1],
                    (1, 0):  tokens0[2],
                    (1, 12): tokens0[3],
                }),
            SourceMapIndex({}, tokens1,
                [
                    [0, 5],
                    [0, 12],
                ],
                {
                    (0, 0):  tokens1[0],
                    (0, 5):  tokens1[1],
                    (1, 0):  tokens1[2],
                    (1, 12): tokens1[3],
                }),
            SourceMapIndex({}, tokens2,
                [
                    [0, 5],
                    [0, 12],
                ],
                {
                    (0, 0):  tokens2[0],
                    (0, 5):  tokens2[1],
                    (1, 0):  tokens2[2],
                    (1, 12): tokens2[3],
                }),
        ]

        return SectionedSourceMapIndex(offsets, maps), [tokens0, tokens1, tokens2]

    def test_lookup(self):
        index, tokens = self.get_index()

        for i in range(5):
            assert index.lookup(0, i) is tokens[0][0]

        for i in range(5, 10):
            assert index.lookup(0, i) is tokens[0][1]

        for i in range(12):
            assert index.lookup(1, i) is tokens[0][2]

        for i in range(12, 14):
            assert index.lookup(1, i) is tokens[0][3]

        for i in range(14, 19):
            assert index.lookup(1, i) is tokens[1][0]

        for i in range(19, 25):
            assert index.lookup(1, i) is tokens[1][1]

        for i in range(12):
            assert index.lookup(2, i) is tokens[1][2]

        for i in range(12, 28):
            assert index.lookup(2, i) is tokens[1][3]

        for i in range(28, 33):
            assert index.lookup(2, i) is tokens[2][0]

        for i in range(33, 40):
            assert index.lookup(2, i) is tokens[2][1]

        for i in range(12):
            assert index.lookup(3, i) is tokens[2][2]

        for i in range(12, 14):
            assert index.lookup(3, i) is tokens[2][3]


class SourceMapIndexTestCase(unittest.TestCase):
    def get_index(self):
        tokens = [
            Token(dst_line=0, dst_col=0),
            Token(dst_line=0, dst_col=5),
            Token(dst_line=1, dst_col=0),
            Token(dst_line=1, dst_col=12),
        ]

        rows = [
            [0, 5],
            [0, 12],
        ]

        index = {
            (0, 0):  tokens[0],
            (0, 5):  tokens[1],
            (1, 0):  tokens[2],
            (1, 12): tokens[3],
        }

        raw = {}

        return SourceMapIndex(raw, tokens, rows, index), tokens

    def test_lookup(self):
        index, tokens = self.get_index()

        for i in range(5):
            assert index.lookup(0, i) is tokens[0]

        for i in range(5, 10):
            assert index.lookup(0, i) is tokens[1]

        for i in range(12):
            assert index.lookup(1, i) is tokens[2]

        for i in range(12, 20):
            assert index.lookup(1, i) is tokens[3]

    def test_getitem(self):
        index, tokens = self.get_index()

        for i in range(4):
            assert index[i] is tokens[i]

    def test_iter(self):
        index, tokens = self.get_index()
        for idx, token in enumerate(index):
            assert token is tokens[idx]

    def test_len(self):
        index, tokens = self.get_index()
        assert len(index) == len(tokens)
