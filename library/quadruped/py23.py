##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Simple wrappers to be more python 2/3 compatable
# still  working on these, so maybe ignore for now

from __future__ import print_function
from __future__ import division
import platform

# get tuple of int's for the python version
PYVER = tuple([int(x) for x in platform.python_version().split('.')])

def kzip(kargs):
    if PYVER[0] == 2:
        return zip(kargs)
    elif PYVER[0] == 3:
        return list(zip(kargs))
    else:
        raise Exception("Unknown python version:", PYVER)

# maybe do this instead?
if PYVER[0] == 2:
    # zip will now produce an iterator
    import intertools.izip as zip
    import intertools.imap as map

    def input(prompt):
        return raw_input(prompt)

elif PYVER[0] == 3: # python 3
    def callable(obj):
        hasattr(obj, '__call__')
else:
    raise Exception("Unknown python version:", PYVER)
