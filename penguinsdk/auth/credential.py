# -*- coding: utf-8 -*-

from time import time

from doclink.exceptions import StatusCodeUnexpectedError

from .. import utils
from ..doclinks import auth
from ..exceptions import (
    CredentialError,
    TokenRefreshFailedError,
    RespWithFailedCodeError)


class Credential(object):
    """docstring for Credential"""

    def __init__(self, kind=None, openid=None, access_token=None,
                 expiry=None, refresh_token=None, client_id=None):
        self.access_token = access_token
        self.openid = openid
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.expiry = expiry
        self.session = None
        self.kind = kind

    @property
    def share_params(self):
        if self.kind == utils.KIND_3RD_PARTY:
            return {
                'access_token': self.access_token,
                'openid': self.openid
            }
        elif self.kind == utils.KIND_CONTENT_SITE:
            return {
                'access_token': self.access_token
            }

    def __str__(self):  # pragma: no cover
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
        if not all((self.access_token, self.openid)):
            return False

        return auth.check_token(
            openid=self.openid,
            access_token=self.access_token)

    # to refresh_token, access_token is not required
    def refresh(self):
        if self.kind == utils.KIND_CONTENT_SITE:
            raise RuntimeError('content site credential can not be refreshed')

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
        except IOError:
            raise TokenRefreshFailedError('connection failed')

        self.access_token = data.get('access_token')
        self.expiry = data.get('expiry')
        self.openid = data['openid']
        self.refresh_token = data.get('refresh_token')
