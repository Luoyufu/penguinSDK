# -*- coding: utf-8 -*-

from functools import partial

import pytest

from penguinsdk import client
from penguinsdk.auth.oauth2 import AuthFlow
from penguinsdk.auth.credential import Credential


def test_build_3rd_party_credential():
    client_ = client.Client('client_id', 'client_secret')
    client_.build_3rd_party_credential(
        openid='openid',
        access_token='access_token',
        refresh_token='refresh_token',
        expiry=1000)
    credential = client_.credential

    assert credential.openid == 'openid'
    assert credential.access_token == 'access_token'
    assert credential.refresh_token == 'refresh_token'
    assert credential.expiry == 1000


def test_build_content_site_credential_with_access_token():
    client_ = client.Client('client_id', 'client_secret')
    client_.build_content_site_credential(access_token='access_token')

    assert client_.credential.access_token == 'access_token'


def test_build_content_site_credential_without_access_token(mocker):
    client_ = client.Client('client_id', 'client_secret')

    credential = Credential('kind')

    class flow:
        @staticmethod
        def get_access_token():
            return credential

    mocker.patch.object(client, 'create_oauth2_flow', return_value=flow)
    client_.build_content_site_credential()

    assert client_.credential is credential


def test_build_3rd_party_credential_without_code():
    client_ = client.Client('client_id', 'client_secret')
    client_.build_3rd_party_credential(access_token='access_token')

    assert client_.credential.access_token == 'access_token'


def test_build_3rd_party_credential_with_code(mocker):
    client_ = client.Client('client_id', 'client_secret')

    credential = Credential('kind')

    class flow:
        @staticmethod
        def exchange_access_token(code):
            return credential

    mocker.patch.object(client, 'create_oauth2_flow', return_value=flow)
    client_.build_3rd_party_credential('code')

    assert client_.credential is credential


def test_credential_setter():
    client_ = client.Client('client_id', 'client_secret')

    with pytest.raises(ValueError):
        client_.credential = 'credential'


def test_oauth2_flow():
    client_ = client.Client('client_id', 'client_secret')
    flow = client_.oauth2_flow

    assert isinstance(flow, AuthFlow)
    assert flow.client_id == 'client_id'
    assert flow.client_secret == 'client_secret'


def test_getattr():
    class Api:
        def partial(self, *args, **kwargs):
            return partial(self, *args, **kwargs)

        def __call__(self, *args, **kwargs):
            return 'api'

    class consumer:
        apis = {'api1': Api()}

    client_ = client.Client('client_id', 'client_secret')
    client_.build_content_site_credential(access_token='access_token',
                                          consumer=consumer)

    assert client_.api1() == 'api'
