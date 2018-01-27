# -*- coding: utf-8 -*-

from functools import partial
from time import time

from doclink.exceptions import StatusCodeUnexpectedError

from .. import utils
from ..doclinks import auth
from ..doclinks import api
from ..exceptions import (
    CredentialError,
    TokenRefreshFailedError,
    RespWithFailedCodeError,)


class CredentialSession(object):

    def __init__(self, credential, consumer):
        self._consumer = consumer
        self.credential = credential
        self._partial_params = {}

    @property
    def partial_params(self):
        return self._partial_params

    def set_partial_parmas(self, *args, **kwargs):
        self.partial_params.update(*args, **kwargs)

    def __getattr__(self, name):
        return partial(
            self._consumer.apis[name].partial(**self.partial_params))


class Credential(object):
    """docstring for Credential"""

    def __init__(self, openid, access_token=None,
                 expiry=None, refresh_token=None, client_id=None):
        self.access_token = access_token
        self.openid = openid
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.expiry = expiry

    def __str__(self):
        return ('access_token:{self.access_token}\n'
                'openid:{self.openid}\n'
                'refresh_token:{self.refresh_token}\n'
                'client_id:{self.client_id}\n'
                'expiry:{self.expiry}').format(self=self)

    @property
    def expired(self):
        """Means if the access_token in thi Credential expired.

        Returns:
            bool: if expired or not.
        """
        if not self.expiry:
            return False

        gapped_expiry = self.expiry - utils.CLOCK_GAP_SECS
        return time() >= gapped_expiry

    @property
    def valid(self):
        """Means if this Credential is usable.

        If access_token is None, we can not use this credential.
        If expiry is not None, check if it's expired.
        If expiry in None, send check_token request to Penguin to figure it out.

        Returns:
            bool: if valid or not.
        """
        if self.access_token is None:
            return False

        if self.expiry:
            return self.expired
        else:
            return self.check_token()

    def check_token(self):
        if self.access_token is None:
            raise CredentialError('access_token is None')

        return auth.check_token(
            openid=self.openid,
            access_token=self.access_token)

    # to refresh_token, access_token is not required
    def refresh(self):
        if not all((self.client_id, self.refresh_token)):
            raise CredentialError('client_id or refresh_token is None')

        try:
            data = auth.refresh_token(
                openid=self.openid,
                client_id=self.client_id,
                refresh_token=self.refresh_token)
        except StatusCodeUnexpectedError as e:
            raise TokenRefreshFailedError('resp with status_code:{}'.format(e.status_code))
        except RespWithFailedCodeError as e:
            raise TokenRefreshFailedError('resp with failed code:{}'.format(e.code))

        self.access_token = data.get('access_token')
        self.expiry = data.get('expiry')
        self.openid = data['openid']
        self.refresh_token = data.get('refresh_token')

    def to_3rd_party_session(self, consumer=api.consumer):
        if not all((self.openid, self.access_token)):
            raise CredentialError('both openid and access_token are required')

        credential_session = CredentialSession(self, consumer)
        credential_session.set_partial_parmas(
            access_token=self.access_token,
            openid=self.openid)

        return credential_session

    def to_content_site_session(self, consumer=api.consumer):
        if not self.access_token:
            raise CredentialError('access_token is required')

        credential_session = CredentialSession(self, consumer)
        credential_session.set_partial_parmas(
            access_token=self.access_token)

        return credential_session
