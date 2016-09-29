from __future__ import absolute_import, unicode_literals

import re
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


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(regex.match(url))
