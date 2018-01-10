# -*- coding: future_fstrings -*-
from __future__ import absolute_import, unicode_literals

import base64
import json
import requests
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes

import boto.utils
from six.moves.urllib.parse import urlparse, parse_qs, quote
from boto import provider
from boto.connection import HTTPRequest
from boto.auth import HmacAuthV3HTTPHandler

from .constants import APP_KEY, HOST, USER_AGENT, BASE_URI


class ZuluHmacAuthV3HTTPHandler(HmacAuthV3HTTPHandler):

    def sign_string(self, string_to_sign):
        new_hmac = self._get_hmac()
        new_hmac.update(string_to_sign)
        return encodebytes(new_hmac.digest()).decode('utf-8').strip()

    def headers_to_sign(self, http_request):
        headers_to_sign = {'Host': self.host}
        for name, value in http_request.headers.items():
            lname = name.lower()
            if lname.startswith('x-amz'):
                headers_to_sign[name] = value
        return headers_to_sign

    def canonical_query_string(self, http_request):
        if http_request.method == 'POST':
            return ''
        qs_parts = []
        for param in sorted(http_request.params):
            value = boto.utils.get_utf8_value(http_request.params[param])
            param_ = quote(param, safe='-_.~')
            value_ = quote(value, safe='-_.~')
            qs_parts.append(f'{param_}={value_}')
        return '&'.join(qs_parts)

    def string_to_sign(self, http_request):
        headers_to_sign = self.headers_to_sign(http_request)
        canonical_qs = self.canonical_query_string(http_request)
        canonical_headers = self.canonical_headers(headers_to_sign)
        string_to_sign = '\n'.join((
            http_request.method,
            http_request.path,
            canonical_qs,
            canonical_headers,
            '',
            http_request.body
        ))
        return string_to_sign, headers_to_sign


def _get_credentials():
    url = f'{BASE_URI}/authentication/credentials/temporary/ios82'
    response = requests.post(
        url, json={"appKey": APP_KEY}, headers={'User-Agent': USER_AGENT}
    )
    response.raise_for_status()
    return json.loads(response.content)['resource']


def get_auth_headers(url_path):
    creds = _get_credentials()
    handler = ZuluHmacAuthV3HTTPHandler(
        host=HOST,
        config={},
        provider=provider.Provider(
            name='aws',
            access_key=creds['accessKeyId'],
            secret_key=creds['secretAccessKey'],
            security_token=creds['sessionToken'],
        )
    )
    params = {
        key: val[0] for key, val in parse_qs(urlparse(url_path).query).items()
    }
    request = HTTPRequest(
        method='GET', protocol='https', host=HOST,
        port=443, path=urlparse(url_path).path, auth_path=None, params=params,
        headers={}, body=''
    )
    handler.add_auth(req=request)
    headers = request.headers
    headers['User-Agent'] = USER_AGENT
    return headers
