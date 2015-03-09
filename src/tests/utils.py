from __future__ import absolute_import, unicode_literals

import os
import json


def load_test_data(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, 'test_data', filename)
    with open(full_path) as f:
        return json.load(f)
