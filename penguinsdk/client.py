# -*- coding: utf-8 -*-

from .auth import create_oauth2_flow
from .auth import Credential


class Client(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._oauth2_flow = None

    @property
    def oauth2_flow(self):
        if not self._oauth2_flow:
            self._oauth2_flow = create_oauth2_flow(self.client_id, self.client_secret)

        return self._oauth2_flow

    def create_credential(self, openid, access_token=None,
                          expiry=None, refresh_token=None):
        return Credential(openid, access_token=access_token,
                          expiry=expiry, refresh_token=refresh_token,
                          client_id=self.client_id)
