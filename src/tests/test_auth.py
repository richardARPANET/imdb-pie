import pytest
from freezegun import freeze_time

from imdbpie.auth import Auth


@pytest.fixture
def auth():
    return Auth(creds={
        'expirationTimeStamp': '2018-01-12T06:23:05Z',
    })


@pytest.mark.parametrize('current_datetime, exp_expired', [
    ('2018-01-12T06:23:05Z', True),  # matching expiry time
    ('2018-01-12T06:24:05Z', True),  # 1 min after expiry time
    ('2018-01-12T06:23:04Z', True),  # 1 sec before, must be 60+ before
    ('2018-01-12T06:22:06Z', True),  # 59 sec before, must be 60+ before
    ('2018-01-12T06:22:05Z', False),  # 60 sec before, must be 60+ before
    ('2018-01-11T06:23:05Z', False),  # 1 day before expiry time
    ('2017-11-11T06:23:05Z', False),  # a few weeks before expiry time
])
def test_creds_soon_expiring(auth, current_datetime, exp_expired):
    with freeze_time(current_datetime):
        assert auth._creds_soon_expiring() is exp_expired
