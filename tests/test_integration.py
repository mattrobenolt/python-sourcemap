import unittest

import sourcemap


class IntegrationTestCase(unittest.TestCase):
    def get_fixtures(self, base):
        source = open('tests/fixtures/%s.js' % base).read()
        minified = open('tests/fixtures/%s.min.js' % base).read()
        min_map = open('tests/fixtures/%s.min.map' % base).read()
        return source, minified, min_map

    def test_jquery(self):
        source, minified, min_map = self.get_fixtures('jquery')

        source_lines = source.splitlines()

        assert sourcemap.discover(minified) == 'jquery.min.map'

        index = sourcemap.loads(min_map)
        for token in index:
            # Ignore tokens that are None.
            # There's no simple way to verify they're correct
            if token.name is None:
                continue
            source_line = source_lines[token.src_line]
            start = token.src_col
            end = start + len(token.name)
            substring = source_line[start:end]

            # jQuery's sourcemap has a few tokens that are identified
            # incorrectly.
            # For example, they have a token for 'embed', and
            # it maps to '"embe', which is wrong. This only happened
            # for a few strings, so we ignore
            if substring[0] == '"':
                continue
            assert token.name == substring

    def test_coolstuff(self):
        source, minified, min_map = self.get_fixtures('coolstuff')

        source_lines = source.splitlines()

        assert sourcemap.discover(minified) == 'tests/fixtures/coolstuff.min.map'

        index = sourcemap.loads(min_map)
        for token in index:
            if token.name is None:
                continue

            source_line = source_lines[token.src_line]
            start = token.src_col
            end = start + len(token.name)
            substring = source_line[start:end]
            assert token.name == substring


