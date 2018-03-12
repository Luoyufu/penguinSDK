# -*- coding: utf-8 -*-

from penguinsdk.endpoints import Endpoints, get_url


def test_endpoints():
    endpoints = Endpoints(
        'base_uri',
        endpoint1='/endpoint1',
        endpoint2='/endpoint2')

    assert endpoints.get_url('endpoint1') == 'base_uri/endpoint1'


def test_get_auth_url():
    assert get_url('auth', 'check_token') == 'https://auth.om.qq.com/omoauth2/checktoken'


def test_get_api_url():
    assert get_url('api_3rd_party', 'media_info') == 'https://api.om.qq.com/media/basicinfoauth'
