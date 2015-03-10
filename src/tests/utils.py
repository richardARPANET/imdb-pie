from __future__ import absolute_import, unicode_literals

import os
import json
import cgi

from six.moves.urllib_parse import urlparse


def load_test_data(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, 'test_data', filename)
    with open(full_path) as f:
        return json.load(f)


def assert_urls_match(url_a, url_b):
    url_a = urlparse(url_a)
    url_b = urlparse(url_b)

    assert url_a.scheme == url_b.scheme
    assert url_a.netloc == url_b.netloc
    assert url_a.path == url_b.path
    assert cgi.parse_qs(url_a.query) == cgi.parse_qs(url_b.query)
