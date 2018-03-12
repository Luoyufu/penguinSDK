# -*- coding: utf-8 -*-

from doclink import Consumer
from ..endpoints import auth as endpoints
from .. import utils

consumer = Consumer(
    endpoints.base_uri,
    expected_status_code=200)
consumer.resp_hook(utils.preprocess_resp)


@consumer.post(endpoints.access_token)
def access_token(resp):
    """Exchange access_token from auth code.

    Ags:
        client_id (str): client id of penguin dev account.
        client_secret (str): client id of penguin dev account.

    Returns:
        dict: access_token, expires_in, expiry, openid, refresh_token.

    <meta>
        args:
            query:
                - grant_type: authorization_code
                - client_id
                - client_secret
                - code:
                    required: False
    </meta>
    """
    data = resp.json_['data']
    expiry = utils.parse_expiry_timestamp(data.get('expires_in'))
    data.update(expiry=expiry)

    return data


@consumer.post(endpoints.refresh_token)
def refresh_token(resp):
    """Refresh access_token.

    Args:
        openid (str): the openid from penguin.
        client_id (str): the client_id from penguin dev account.
        refresh_token (str): the refresh_token from penguin.

    Returns:
        dict: access_token, expires_in, expiry, openid, refresh_token.

    <meta>
        args:
            query:
                - openid
                - grant_type: refreshtoken
                - client_id
                - refresh_token
    </meta>
    """
    data = resp.json_['data']
    expiry = utils.parse_expiry_timestamp(data.get('expires_in'))
    data.update(expiry=expiry)

    return data


@consumer.get(endpoints.check_token)
def check_token(resp):
    """Check token status.

    Args:
        openid (str): the openid from penguin.
        access_token (str): the access_token from penguin.

    Returns:
        bool: Ture if the access_token valid else False.

    <meta>
        args:
            query:
                - openid
                - access_token
    </meta>
    """
    return resp.json_['data']['validity']
