# -*- coding: utf-8 -*-

from time import time

import pytest

from penguinsdk.auth.credential import Credential
from penguinsdk.auth.credential import auth
from penguinsdk.utils import (
    CLOCK_GAP_SECS,
    KIND_CONTENT_SITE,
    KIND_3RD_PARTY)


@pytest.fixture
def timestamp_now():
    return int(time())


@pytest.fixture
def timestamp_expired():
    return int(time()) + CLOCK_GAP_SECS + 1


class TestCredential(object):

    def test_expired_true(self, timestamp_now):
        credential = Credential(expiry=timestamp_now)
        assert credential.expired

    def test_expired_false(self, timestamp_expired):
        credential = Credential(expiry=timestamp_expired)
        assert not credential.expired

    def test_valid_without_access_token(self):
        credential = Credential()
        assert not credential.valid

    def test_valid_expired(self, timestamp_expired):
        credential = Credential(access_token='access_token',
                                expiry=timestamp_expired)
        assert not credential.valid

    def test_valid_without_expiry(self, mocker):
        credential = Credential(access_token='access_token')
        mock_method = mocker.patch.object(credential, 'check_token', autospec=True)
        credential.valid

        mock_method.assert_called_once_with()

    def test_check_token_openid_or_accesstoken_missing(self):
        credential = Credential(access_token='access_token')
        assert not credential.check_token()

    def test_check_token(self, mocker):
        credential = Credential(access_token='access_token', openid='openid')
        mocker.patch.object(auth, 'check_token', autospec=True, return_value=True)

        assert credential.check_token()

    def test_content_site_share_params(self):
        credential = Credential(KIND_CONTENT_SITE, access_token='access_token', openid='openid')
        assert credential.share_params == {'access_token': 'access_token'}

    def test_3rd_party_share_params(self):
        credential = Credential(KIND_3RD_PARTY, access_token='access_token', openid='openid')
        assert credential.share_params == {'access_token': 'access_token',
                                           'openid': 'openid'}

    def test_refresh_success(self, mocker):
        credential = Credential(access_token='access_token',
                                openid='openid',
                                refresh_token='refresh_token',
                                client_id='client_id')
        mocker.patch.object(
            auth,
            'refresh_token',
            autospec=True,
            return_value={
                'access_token': 'new_access_token',
                'expiry': 20000,
                'openid': 'new_openid',
                'refresh_token': 'new_refresh_token'
            })

        credential.refresh()

        assert credential.access_token == 'new_access_token'
        assert credential.openid == 'new_openid'
        assert credential.refresh_token == 'new_refresh_token'
