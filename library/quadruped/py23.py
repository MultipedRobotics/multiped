##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Simple wrappers to be more python 2/3 compatable

from __future__ import print_function
from __future__ import division
import sys

PYVER = sys.winver

def kzip(kargs):
    if PYVER == '2.7':
        return zip(kargs)
    else:
        return list(zip(kargs))

# maybe do this instead?
if PYVER == '2.7':
    # zip will now produce an iterator
    import intertools.izip as zip
    import intertools.imap as map

    def input(prompt):
        return raw_input(prompt)

else: # python 3
    def callable(obj):
        hasattr(obj, '__call__')
