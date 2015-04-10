from __future__ import absolute_import, unicode_literals

import hashlib

BASE_URI = 'https://app.imdb.com'
API_KEY = '2wex6aeu6a8q9e49k7sfvufd6rhh0n'
SHA1_KEY = hashlib.sha1(API_KEY.encode('utf8')).hexdigest()
USER_AGENTS = (
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A405',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A406',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 '
    'Safari/7534.48.3',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 '
    'Safari/7534.48.3',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A406 '
    'Safari/7534.48.3',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 '
    'Safari/7534.48.3',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) '
    'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 '
    'Safari/7534.48.3',
    'Mozilla/5.0(iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us)'
    'AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d '
    'Safari/6531.22.7',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) '
    'AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 '
    'Safari/600.1.4'
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4'
    ' (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4',
)
DEFAULT_PROXY_URI = 'http://openwebproxy.pw/browse.php?u={0}'
