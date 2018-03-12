# -*- coding: utf-8 -*-

from functools import partial

from . import (
    utils,
    uploader,
    publisher)
from .auth import create_oauth2_flow
from .auth import Credential
from .doclinks import (
    api_3rd_party,
    api_content_site)


class Client(object):

    def __init__(self, client_id, client_secret,
                 uploader=uploader,
                 publisher=publisher):
        self.client_id = client_id
        self.client_secret = client_secret
        self._oauth2_flow = None
        self._credential = None
        self._consumer = None
        self._uploader = uploader
        self._publisher = publisher

    @property
    def credential(self):
        return self._credential

    @credential.setter
    def credential(self, credential):
        if not isinstance(credential, Credential):
            raise ValueError('Credential instance required')

        self._credential = credential

        if credential.kind == utils.KIND_3RD_PARTY:
            self._consumer = api_3rd_party.consumer
        elif credential.kind == utils.KIND_CONTENT_SITE:
            self._consumer = api_content_site.consumer

    def upload_video(self, file_path, monitor_callback=None):
        return self._uploader.upload_video(
            self._consumer,
            file_path=file_path,
            monitor_callback=monitor_callback,
            **self.credential.share_params)

    def upload_thumbnail(self, vid, file_pointer):
        return self._uploader.upload_thumbnail(
            self._consumer,
            vid=vid,
            file_pointer=file_pointer,
            **self.credential.share_params)

    def publish_video(self, publish_info, file_pointer):
        return self._publisher.publish_video(
            self._consumer,
            publish_info=publish_info,
            file_pointer=file_pointer,
            **self.credential.share_params)

    def publish_uploaded_video(self, publish_info, vid):
        return self._publisher.publish_uploaded_video(
            self._consumer,
            publish_info=publish_info,
            vid=vid,
            **self.credential.share_params)

    @property
    def oauth2_flow(self):
        if not self._oauth2_flow:
            self._oauth2_flow = create_oauth2_flow(self.client_id, self.client_secret)

        return self._oauth2_flow

    def build_3rd_party_credential(self, code=None, openid=None, access_token=None,
                                   expiry=None, refresh_token=None,
                                   consumer=None):
        if code:
            self.credential = self.oauth2_flow.exchange_access_token(code)
        else:
            self.credential = Credential(
                utils.KIND_3RD_PARTY,
                openid=openid, access_token=access_token,
                expiry=expiry, refresh_token=refresh_token,
                client_id=self.client_id)

        if consumer:
            self._consumer = consumer

    def build_content_site_credential(self, openid=None, access_token=None,
                                      expiry=None, consumer=None):
        if access_token:
            self.credential = Credential(
                utils.KIND_CONTENT_SITE,
                openid=openid, access_token=access_token,
                expiry=expiry, client_id=self.client_id)
        else:
            self.credential = self.oauth2_flow.get_access_token()

        if consumer:
            self._consumer = consumer

    def __getattr__(self, name):
        return partial(
            self._consumer.apis[name].partial(**self.credential.share_params))
