try:
    import unittest2 as unittest
except ImportError:
    import unittest
from sourcemap.objects import Token, SourceMapIndex


class TokenTestCase(unittest.TestCase):
    def test_eq(self):
        assert Token(1, 1, 'lol.js', 1, 1, 'lol') == Token(1, 1, 'lol.js', 1, 1, 'lol')
        assert Token(99, 1, 'lol.js', 1, 1, 'lol') != Token(1, 1, 'lol.js', 1, 1, 'lol')


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
