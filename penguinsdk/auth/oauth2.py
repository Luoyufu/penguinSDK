# -*- coding: utf-8 -*-

from .. import endpoints
from ..doclinks import auth
from .credential import Credential
from .. import utils


class AuthFlow(object):
    """docstring for AuthFlow"""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, redirect_uri, state=None):
        url = endpoints.get_url('auth', 'authorization')

        return '{}?response_type=code&client_id={}&redirect_uri={}{}'.format(
            url, self.client_id, redirect_uri,
            '&state={}'.format(state) if state else '')

    def exchange_access_token(self, code):  # pragma: no cover
        data = auth.access_token(
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret)

        return Credential(
            utils.KIND_3RD_PARTY,
            openid=data['openid'],
            access_token=data.get('access_token'),
            expiry=data.get('expiry'),
            refresh_token=data.get('refresh_token'),
            client_id=self.client_id)

    def get_access_token(self):
        data = auth.access_token(
            grant_type='clientcredentials',
            client_id=self.client_id,
            client_secret=self.client_secret)

        return Credential(
            utils.KIND_CONTENT_SITE,
            openid=data['openid'],
            access_token=data.get('access_token'),
            expiry=data.get('expiry'),
            refresh_token=data.get('refresh_token'),
            client_id=self.client_id)

    def refresh_token(self, openid=None, refresh_token=None, credential=None):
        if credential is None:
            if not all((openid, refresh_token)):
                raise RuntimeError('both openid and refresh_token are required')
            credential = Credential(
                openid,
                refresh_token=refresh_token,
                client_id=self.client_id)
        credential.refresh()

        return credential


def create_flow(client_id, client_secret):
    return AuthFlow(client_id, client_secret)
