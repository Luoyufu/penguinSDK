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

api_3rd_party = Endpoints(
    base_uri='https://api.om.qq.com',
    publish_video='/article/authpubvid',
    transaction_info='/transaction/infoauth',
    media_info='/media/basicinfoauth',
    upload_video_thumbnail='/video/authvideopic',
    apply_for_video_upload='/video/authuploadready',
    upload_video_chunk='/video/authuploadtrunk',
    publish_uploaded_video='/article/authpubvideo',
    publish_article='/article/authpubpic',
    publish_live='/article/authpublive',
    article_list='/article/authlist?')


api_content_site = Endpoints(
    base_uri='https://api.om.qq.com',
    publish_live='/article/clientpublive',
    media_info='/media/basicinfoclient',
    publish_article='/article/clientpubpic',
    publish_video='/article/clientpubvid',
    transaction_info='/transaction/infoclient',
    upload_video_chunk='/video/clientuploadtrunk',
    publish_uploaded_video='/article/clientpubvideo',
    article_list='/article/clientlist?',
    upload_video_thumbnail='/video/clientvideopic',
    apply_for_video_upload='/video/clientuploadready',
    media_stats='/media/statsclient',
    media_daily_stats='/media/dailystatsclient',
    article_stats='/article/statsclient',
    article_daily_stats='/article/dailystatsclient')


def get_url(consumer_name, endpoint_name):
    endpoints = globals()[consumer_name]
    return endpoints.get_url(endpoint_name)
