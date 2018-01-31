#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x842f0f13

# Compiled with Coconut version 1.3.1-post_dev17 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# BBopt boilerplate:
from bbopt import BlackBoxOptimizer
bb = BlackBoxOptimizer(file=__file__)
if __name__ == "__main__":
    bb.run(backend="hyperopt")

# Let's use some parameters!
x0 = bb.randint("x0", 1, 10, guess=5)
x1 = bb.normalvariate("x1", mu=0, sigma=1)
x2 = bb.choice("x2", [-10, -1, 0, 1, 10])

# And let's set our goal!
y = x0 + x1 * x2
bb.minimize(y)

# Finally, we'll print out the value we used for debugging purposes.
if __name__ == "__main__":
    print(repr(y))
