# -*- coding: utf-8 -*-

from doclink import Consumer
from ..endpoints import api as endpoints
from .. import utils
from ..exceptions import TransactionFailedError

consumer = Consumer(
    endpoints.base_uri,
    expected_status_code=200)
consumer.resp_hook(utils.preprocess_resp)


@consumer.get(endpoints.media_info)
def media_info(resp):
    """Get media basic info from Penguin.

    Args:
        access_token (str): access_token.
        openid (str): openid.

    Returns:
        dict: the header image, the nick name. For example:
            {
                "header": "http://inews.gtimg.com/newsapp_ls/0/183849551_100100/0",
                "nick": "测试"
            }

    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
    </meta>
    """
    return resp.json_['data']


@consumer.post(endpoints.publish_video)
def publish_video(resp):
    """Upload a video and publish it.

    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - title
                - tags
                - cat
                - md5
                - desc: ''
                - apply:
                    required: False
            multipart: media
    </meta>
    """
    return resp.json_['data']['transaction_id']


@consumer.post(endpoints.publish_uploaded_video)
def publish_uploaded_video(resp):
    """Publish a uploaded video.

    Vid is pointted to the uploaded vidoe.

    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - title
                - tags
                - cat
                - desc: ''
                - apply:
                    required: False
                - vid
    </meta>
    """
    return resp.json_['data']['transaction_id']


@consumer.post(endpoints.upload_video_thumbnail)
def upload_video_thumbnail(resp):
    """
    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - md5
                - vid
            multipart: media
    </meta>
    """
    return resp.json_['data']['transaction_id']


@consumer.get(endpoints.transaction_info)
def transaction_info(resp):
    """
    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - transaction_id
    </meta>
    """
    return resp.json_['data']


@consumer.post(endpoints.apply_for_video_upload)
def apply_for_video_upload(resp):
    """
    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - size
                - md5
                - sha
    </meta>
    """
    return resp.json_['data']['transaction_id']


@consumer.post(endpoints.upload_video_chunk)
def upload_video_chunk(resp):
    """
    <meta>
        args:
            query:
                - access_token
                - openid:
                    required: False
                - transaction_id
                - start_offset: 0
            file: mediatrunk
    </meta>
    """
    return resp.json_['data']
