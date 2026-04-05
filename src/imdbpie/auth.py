# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import tempfile
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import diskcache
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from dateutil.parser import parse
from dateutil.tz import tzutc

from .constants import APP_KEY, HOST, USER_AGENT, BASE_URI


def _get_credentials():
    url = '{0}/authentication/credentials/temporary/ios82'.format(BASE_URI)
    response = requests.post(
        url, json={"appKey": APP_KEY}, headers={'User-Agent': USER_AGENT}
    )
    response.raise_for_status()
    return json.loads(response.content.decode('utf8'))['resource']


class Auth(object):
    SOON_EXPIRES_SECONDS = 60
    _CREDS_STORAGE_KEY = 'imdbpie-credentials'

    def __init__(self):
        self._cachedir = tempfile.gettempdir()

    def _get_creds(self):
        with diskcache.Cache(directory=self._cachedir) as cache:
            return cache.get(self._CREDS_STORAGE_KEY)

    def _set_creds(self, creds):
        with diskcache.Cache(directory=self._cachedir) as cache:
            cache[self._CREDS_STORAGE_KEY] = creds
        return creds

    def clear_cached_credentials(self):
        with diskcache.Cache(directory=self._cachedir) as cache:
            cache.delete(self._CREDS_STORAGE_KEY)

    def _creds_soon_expiring(self):
        creds = self._get_creds()
        if not creds:
            return creds, True
        expires_at = parse(creds['expirationTimeStamp'])
        now = datetime.now(tzutc())
        if now < expires_at:
            time_diff = expires_at - now
            if time_diff.total_seconds() < self.SOON_EXPIRES_SECONDS:
                # creds will soon expire, so renew them
                return creds, True
            return creds, False
        else:
            return creds, True

    def get_auth_headers(self, url_path):
        creds, soon_expires = self._creds_soon_expiring()
        if soon_expires:
            creds = self._set_creds(creds=_get_credentials())
        credentials = Credentials(access_key=creds['accessKeyId'], secret_key=creds['secretAccessKey'],
                        token=creds['sessionToken'])


        parsed_url = urlparse(url_path)
        params = {
            key: val[0] for key, val in parse_qs(parsed_url.query).items()
        }
        req = requests.Request('GET', f'https://{HOST}{parsed_url.path}', params=params, data='', headers={})
        prepared_request = req.prepare()
        prepared_request.headers['User-Agent'] = USER_AGENT
        aws_request = AWSRequest(method=prepared_request.method, url=prepared_request.url, data=prepared_request.body,
                                 headers=prepared_request.headers)
        SigV4Auth(credentials, 'imdbapi', 'us-east-1').add_auth(aws_request)
        return aws_request.prepare().headers

