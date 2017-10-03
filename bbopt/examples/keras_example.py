#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x7cb1e030

# Compiled with Coconut version 1.3.0-post_dev3 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Imports:

sys = _coconut_sys
import csv
import os.path
from pprint import pprint

import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.optimizers import SGD
from keras.utils import to_categorical
from keras.regularizers import l1_l2

# Data processing:

data_folder = os.path.join(os.path.dirname(__file__), "data")
house_votes = np.loadtxt(os.path.join(data_folder, "house_votes.csv"), dtype=str, delimiter=",")

def _coconut_lambda_1(_=None):
    raise TypeError("unknown vote %r" % _)
X = (np.vectorize(lambda _=None: 1 if _ == "y" else -1 if _ == "n" else 0 if _ == "?" else (_coconut_lambda_1)(_)))(house_votes[:, 1:])
def _coconut_lambda_2(_=None):
    raise TypeError("unknown party %r" % _)
y = (to_categorical)((np.vectorize(lambda _=None: 1 if _ == "democrat" else 0 if _ == "republican" else (_coconut_lambda_2)(_)))(house_votes[:, 0]))

train_split = (int)(.6 * len(X))
validate_split = (int)(train_split + .2 * len(X))

X_train, X_validate, X_test = X[:train_split], X[train_split:validate_split], X[validate_split:]
y_train, y_validate, y_test = y[:train_split], y[train_split:validate_split], y[validate_split:]

# BBOpt setup:

from bbopt import BlackBoxOptimizer
bb = BlackBoxOptimizer(file=__file__)

try:
    N = int(sys.argv[1])
except Exception:
    N = 1

for i in bb.loop(n=N, backend="scikit-optimize"):

# Main program:

    print("\n= %d =" % i)

    model = Sequential([Dense(units=bb.randint("hidden neurons", 1, 15, guess=10), input_dim=len(X_train[0]), W_regularizer=l1_l2(l1=bb.uniform("l1", 0, 0.1, guess=0.01), l2=bb.uniform("l2", 0, 0.1, guess=0.01))), Activation("relu"), Dense(units=2), Activation("softmax"),])

    model.compile(loss="categorical_crossentropy", optimizer=SGD(lr=bb.uniform("learning rate", 0, 0.5, guess=0.1), decay=bb.uniform("decay", 0, 0.01, guess=0.001), momentum=bb.uniform("momentum", 0, 1, guess=0.1), nesterov=(bool)(bb.getrandbits("nesterov", 1, guess=1))), metrics=["accuracy"])

    train_history = model.fit(X_train, y_train, epochs=50, batch_size=bb.randint("batch size", 1, 32, guess=16), verbose=0)


    train_loss, train_acc = train_history.history["loss"][-1], train_history.history["acc"][-1]

    validation_loss, validation_acc = model.evaluate(X_validate, y_validate, verbose=0)

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

    bb.remember({"training loss": train_loss, "training accuracy": train_acc, "validation loss": validation_loss, "validation accuracy": validation_acc, "test loss": test_loss, "test accuracy": test_acc})

    bb.minimize(validation_loss)

    pprint(bb.get_current_run())

print("\n= BEST =")
pprint(bb.get_optimal_run())
