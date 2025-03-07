"""
sourcemap.exceptions
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
class SourceMapDecodeError(ValueError):
    "lol sourcemap error"
    pass

class SourceMapTypeError(TypeError):
    "invalid sourcemap due to a type error"
    pass
