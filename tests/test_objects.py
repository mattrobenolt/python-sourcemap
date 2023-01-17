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
                SourceMapIndex({'file': 'foo0.js'}, tokens0,
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
                SourceMapIndex({'file': 'foo1.js'}, tokens1,
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
                SourceMapIndex({'file': 'foo2.js'}, tokens2,
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

        raw = {}

        return SectionedSourceMapIndex(raw, offsets, maps), [tokens0, tokens1, tokens2]

    def test_lookup(self):
        index, tokens = self.get_index()

        for i in range(5):
            assert index.lookup(0, i)[0] is tokens[0][0]

        for i in range(5, 10):
            assert index.lookup(0, i)[0] is tokens[0][1]

        for i in range(12):
            assert index.lookup(1, i)[0] is tokens[0][2]

        for i in range(12, 14):
            assert index.lookup(1, i)[0] is tokens[0][3]

        for i in range(14, 19):
            assert index.lookup(1, i)[0] is tokens[1][0]

        for i in range(19, 25):
            assert index.lookup(1, i)[0] is tokens[1][1]

        for i in range(12):
            assert index.lookup(2, i)[0] is tokens[1][2]

        for i in range(12, 28):
            assert index.lookup(2, i)[0] is tokens[1][3]

        for i in range(28, 33):
            assert index.lookup(2, i)[0] is tokens[2][0]

        for i in range(33, 40):
            assert index.lookup(2, i)[0] is tokens[2][1]

        for i in range(12):
            assert index.lookup(3, i)[0] is tokens[2][2]

        for i in range(12, 14):
            assert index.lookup(3, i)[0] is tokens[2][3]

    def test_columns_for_line(self):
        index, tokens = self.get_index()
        cols = index.columns_for_line(0)

        assert cols[0] is tokens[0][0].dst_col
        assert cols[1] is tokens[0][1].dst_col

        cols = index.columns_for_line(1)

        assert len(cols) is 4
        assert cols[0] is tokens[0][2].dst_col
        assert cols[1] is tokens[0][3].dst_col
        assert cols[2] is tokens[1][0].dst_col + index.offsets[1][1]
        assert cols[3] is tokens[1][1].dst_col + index.offsets[1][1]

        cols = index.columns_for_line(2)

        assert len(cols) is 4
        assert cols[0] is tokens[1][2].dst_col + index.offsets[1][1]
        assert cols[1] is tokens[1][3].dst_col + index.offsets[1][1]
        assert cols[2] is tokens[2][0].dst_col + index.offsets[2][1]
        assert cols[3] is tokens[2][1].dst_col + index.offsets[2][1]

    def test_lookup_from_columns_for_line(self):
        index, tokens = self.get_index()
        cols = index.columns_for_line(2)
        t, _ = index.lookup(2, cols[2])
        assert t is tokens[2][0]

    def test_files(self):
        index, _ = self.get_index()
        assert len(index.files()) is 3

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
            assert index.lookup(0, i)[0] is tokens[0]

        for i in range(5, 10):
            assert index.lookup(0, i)[0] is tokens[1]

        for i in range(12):
            assert index.lookup(1, i)[0] is tokens[2]

        for i in range(12, 20):
            assert index.lookup(1, i)[0] is tokens[3]

    def test_columns_for_line(self):
        index, tokens = self.get_index()
        cols = index.columns_for_line(0)

        assert cols[0] is tokens[0].dst_col
        assert cols[1] is tokens[1].dst_col

        cols = index.columns_for_line(1)

        assert cols[0] is tokens[2].dst_col
        assert cols[1] is tokens[3].dst_col

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
