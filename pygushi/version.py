from collections import namedtuple

__all__ = ['version']

Version = namedtuple('Version', ['major', 'minor', 'micro'])
version = Version(1, 2, 0)
