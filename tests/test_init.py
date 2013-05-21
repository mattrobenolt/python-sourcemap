try:
    import unittest2 as unittest
except ImportError:
    import unittest
import sourcemap


class DiscoverTestCase(unittest.TestCase):
    def test_finds_sourcemap(self):
        fixture = """
hey
this is some code
it's really awesome
//@ sourceMappingURL=file.js
"""
        self.assertFoundSourcemap(fixture, 'file.js')

    def test_finds_sourcemap_alt(self):
        fixture = """
hey
this is some code
it's really awesome
//# sourceMappingURL=file.js
"""
        self.assertFoundSourcemap(fixture, 'file.js')

    def test_doesnt_find_sourcemap(self):
        fixture = """
there
is no sourcemap
here
"""
        self.assertNotFoundSourcemap(fixture)

    def assertNotFoundSourcemap(self, fixture):
        self.assertIsNone(sourcemap.discover(fixture))

    def assertFoundSourcemap(self, fixture, expected):
        self.assertEqual(sourcemap.discover(fixture), expected)
