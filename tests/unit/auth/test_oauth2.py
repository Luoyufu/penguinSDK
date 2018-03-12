# -*- coding: utf-8 -*-

from time import time

import pytest

from penguinsdk.auth.oauth2 import AuthFlow, auth
from penguinsdk.auth.credential import Credential


@pytest.fixture
def auth_flow():
    return AuthFlow('client_id', 'client_secret')


def test_get_authorization_url_with_state(auth_flow):
    assert (auth_flow.get_authorization_url('redirect_uri', 'STATE') ==
            'https://auth.om.qq.com/omoauth2/authorize?'
            'response_type=code&'
            'client_id=client_id&'
            'redirect_uri=redirect_uri&'
            'state=STATE')


def test_get_authorization_url_without_state(auth_flow):
    assert (auth_flow.get_authorization_url('redirect_uri') ==
            'https://auth.om.qq.com/omoauth2/authorize?'
            'response_type=code&'
            'client_id=client_id&'
            'redirect_uri=redirect_uri')


def test_exchange_access_token(auth_flow, mocker):
    mocker.patch.object(
        auth,
        'access_token',
        autospec=True,
        return_value={
            'access_token': 'access_token',
            'expiry': int(time()) + 20000,
            'openid': 'openid',
            'refresh_token': 'refresh_token'
        })

    credential = auth_flow.exchange_access_token('code')

    assert credential.access_token == 'access_token'
    assert credential.refresh_token == 'refresh_token'
    assert credential.expiry + 10 > int(time()) + 20000
    assert credential.openid == 'openid'


def test_get_access_token(auth_flow, mocker):
    mocker.patch.object(
        auth,
        'access_token',
        autospec=True,
        return_value={
            'access_token': 'access_token',
            'expiry': int(time()) + 20000,
            'openid': 'openid',
            'refresh_token': 'refresh_token'
        })

    credential = auth_flow.get_access_token()

    assert credential.access_token == 'access_token'
    assert credential.refresh_token == 'refresh_token'
    assert credential.expiry + 10 > int(time()) + 20000
    assert credential.openid == 'openid'


def test_refresh_token_with_credential(auth_flow, mocker):
    credential = Credential()

    mock = mocker.patch.object(
        credential,
        'refresh',
        autospec=True)

    auth_flow.refresh_token(credential=credential)

    assert mock.called


def test_refresh_token_with_openid_and_refresh_token(auth_flow, mocker):
    mock = mocker.patch(
        'penguinsdk.auth.oauth2.Credential.refresh',
        autospec=True)
    auth_flow.refresh_token(openid='openid', refresh_token='refresh_token')

    assert mock.called


def test_refresh_token_with_args_missing(auth_flow):
    with pytest.raises(RuntimeError):
        auth_flow.refresh_token(refresh_token='refresh_token')
