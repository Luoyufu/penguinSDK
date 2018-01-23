# -*- coding: utf-8 -*-


class Endpoints(object):
    def __init__(self, base_uri, *args, **kwargs):
        self.base_uri = base_uri
        self._endpoint_map = dict(*args, **kwargs)

    def __getattr__(self, name):
        return self._endpoint_map[name]

    def get_url(self, endpoint_name):
        return self.base_uri + self._endpoint_map[endpoint_name]


auth = Endpoints(
    base_uri='https://auth.om.qq.com',
    authorization='/omoauth2/authorize',
    access_token='/omoauth2/accesstoken',
    refresh_token='/omoauth2/refreshtoken',
    check_token='/omoauth2/checktoken')

api = Endpoints(
    base_uri='https://api.om.qq.com',
    publish_video='/article/authpubvid',
    transaction_info='/transaction/infoauth',
    media_info='/media/basicinfoauth',
    upload_video_thumbnail='/video/authvideopic')


def get_url(consumer_name, endpoint_name):
    endpoints = globals()[consumer_name]
    return endpoints.get_url(endpoint_name)
