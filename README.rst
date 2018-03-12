************
PenguinSDK(腾讯内容开放平台SDK)
************

.. image:: https://travis-ci.org/Luoyufu/penguinSDK.svg?branch=master
    :target: https://travis-ci.org/Luoyufu/penguinSDK

.. image:: https://codecov.io/gh/Luoyufu/penguinSDK/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Luoyufu/penguinSDK

.. image:: https://img.shields.io/pypi/v/penguinSDK.svg
  :target: https://pypi.python.org/pypi/penguinSDK

.. image:: https://img.shields.io/pypi/pyversions/penguinSDK.svg
  :target: https://pypi.python.org/pypi/penguinSDK


`腾讯内容开放平台API <https://open.om.qq.com/resources/resourcesCenter>`_ 的Python SDK。

概述
========
PenguinSDK实现了腾讯内容开放平台的全部API：

* 授权/oauth API
* 第三方服务API
* 内容网站API

SDK基于声明式API框架 `doclink <https://github.com/Luoyufu/doclink>`_ 实现

使用
====
内容网站API
--------
* 获取credential(授权凭证)
.. code-block:: python

    from penguinsdk import Penguin


    penguin = Penguin('client_id', 'client_secret')
    penguin.build_content_site_credential()

    >>> print(penguin.credential)
    access_token:<access_token>
    openid:<openid>
    refresh_token:None
    client_id:<client_id>
    expiry:1520766527

* 通过access_token构建credential
.. code-block:: python

    penguin = Penguin('client_id', 'client_secret')
    penguin.build_content_site_credential(access_token='access_token')

    >>> print(penguin.credential)
    access_token:access_token
    openid:None
    refresh_token:None
    client_id:client_id
    expiry:None

* 调用API
credential构建好之后，就可以通过Penguin对象调用内容网站API
.. code-block:: python

    penguin = Penguin('client_id', 'client_secret')
    penguin.build_content_site_credential()

    media_info = penguin.media_info()  # 获取自媒体基本信息

    >>> print(media_info)
    {'nick': '青铜味', 'header': 'http://inews.gtimg.com/newsapp_ls/0/2720632941_200200/0'}

第三方服务
-----

第三方服务需要通过oauth2协议获取用户许可

* oauth流程：oauth_flow

1. 获取授权页地址

.. code-block:: python

    from penguinsdk import Penguin

    penguin = Penguin('client_id', 'client_secret')
    oauth2_flow = penguin.oauth2_flow
    authorization_url = oauth2_flow.get_authorization_url(redirect_uri='redirect_uri', state='state')

    >>> print(authorization_url)
    'https://auth.om.qq.com/omoauth2/authorize?response_type=code&client_id=client_id&redirect_uri=redirect_uri&state=state'

2. 客户端在上一步的授权地址获得用户授权，将向redirect_uri回调授权码code

3. 通过code交换access_token并获得credential实例。credential中包含access_token, refresh_token, openid, expiry可以保存下来以便后续使用。

.. code-block:: python

    penguin = Penguin('client_id', 'client_secret')

    code = 'auth_code'
    penguin.build_3rd_party_credential(code)

    >>> print(penguin.credential)
    access_token:<access_token>
    openid:<openid>
    refresh_token:<refresh_token>
    client_id:<client_id>
    expiry:1520766527

4. 通过已有授权信息构建credentials

.. code-block:: python

    penguin = Penguin('client_id', 'client_secret')
    penguin.build_3rd_party_credential(
        access_token='access_token',
        refresh_token='refresh_token',
        openid='openid',
        expiry=1520766527)

    >>> print(penguin.credential)
    access_token:'access_token'
    openid:'openid'
    refresh_token:'refresh_token'
    client_id:'client_id'
    expiry:1520766527

5. 调用API

credential构建好之后，就可以通过Penguin对象调用第三方服务的API

.. code-block:: python

    penguin = Penguin('client_id', 'client_secret')
    penguin.build_3rd_party_credential(
        access_token='access_token',
        refresh_token='refresh_token',
        openid='openid',
        expiry=1520766527)

    penguin.media_info()

    >>> print(media_info)
    {'nick': '青铜味', 'header': 'http://inews.gtimg.com/newsapp_ls/0/2720632941_200200/0'}

API汇总
=====
内容网站API
-------

调用时，penguin将自动传入access_token, 其余参数通过命名参数方式传入

.. code-block:: python

    from doclink import Consumer
    from ..endpoints import api_content_site as endpoints
    from .. import utils

    consumer = Consumer(
        endpoints.base_uri,
        expected_status_code=200)
    consumer.resp_hook(utils.preprocess_resp)


    @consumer.get(endpoints.media_info)
    def media_info(resp):
        """
        <meta>
            args:
                query:
                    - access_token
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.transaction_info)
    def transaction_info(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - transaction_id
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.article_list)
    def article_list(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - page
                    - limit: 10
        </meta>
        """


    @consumer.post(endpoints.publish_live)
    def publish_live(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - title
                    - start_time
                    - end_time
                    - cover_pic
                    - rtmp_url
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.post(endpoints.publish_article)
    def publish_article(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - title
                    - content
                    - cover_pic
                    - apply:
                        required: False
                    - original_platform:
                        required: False
                    - original_url:
                        required: False
                    - original_author:
                        required: False
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.post(endpoints.publish_video)
    def publish_video(resp):
        """Upload a video and publish it.

        <meta>
            args:
                query:
                    - access_token
                    - title
                    - tags
                    - cat
                    - md5
                    - desc
                    - apply:
                        required: False
                multipart: media
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.post(endpoints.apply_for_video_upload)
    def apply_for_video_upload(resp):
        """
        <meta>
            args:
                query:
                    - access_token
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
                    - transaction_id
                    - start_offset: 0
                file: mediatrunk
        </meta>
        """
        return resp.json_['data']


    @consumer.post(endpoints.publish_uploaded_video)
    def publish_uploaded_video(resp):
        """Publish a uploaded video.

        Vid is pointted to the uploaded vidoe.

        <meta>
            args:
                query:
                    - access_token
                    - title
                    - tags
                    - cat
                    - desc
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
                    - md5
                    - vid
                file: media
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.get(endpoints.media_stats)
    def media_stats(resp):
        """
        <meta>
            args:
                query:
                    - access_token
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.media_daily_stats)
    def media_daily_stats(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - begin_date:
                        required: False
                    - end_date:
                        required: False
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.article_stats)
    def article_stats(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - article_id
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.article_daily_stats)
    def article_daily_stats(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - article_id
                    - begin_date:
                        required: False
                    - end_date:
                        required: False
        </meta>
        """
        return resp.json_['data']

第三方服务API
--------

调用时，penguin将自动传入access_token和openid, 其余参数通过命名参数方式传入

.. code-block:: python

    from doclink import Consumer
    from ..endpoints import api_3rd_party as endpoints
    from .. import utils

    consumer = Consumer(
        endpoints.base_uri,
        expected_status_code=200)
    consumer.resp_hook(utils.preprocess_resp)


    @consumer.get(endpoints.media_info)
    def media_info(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.transaction_info)
    def transaction_info(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
                    - transaction_id
        </meta>
        """
        return resp.json_['data']


    @consumer.get(endpoints.article_list)
    def article_list(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
                    - page
                    - limit: 10
        </meta>
        """


    @consumer.post(endpoints.publish_live)
    def publish_live(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
                    - title
                    - start_time
                    - end_time
                    - cover_pic
                    - rtmp_url
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.post(endpoints.publish_article)
    def publish_article(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
                    - title
                    - content
                    - cover_pic
                    - apply:
                        required: False
                    - original_platform:
                        required: False
                    - original_url:
                        required: False
                    - original_author:
                        required: False
        </meta>
        """
        return resp.json_['data']['transaction_id']


    @consumer.post(endpoints.publish_video)
    def publish_video(resp):
        """Upload a video and publish it.

        <meta>
            args:
                query:
                    - access_token
                    - openid
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


    @consumer.post(endpoints.apply_for_video_upload)
    def apply_for_video_upload(resp):
        """
        <meta>
            args:
                query:
                    - access_token
                    - openid
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
                    - openid
                    - transaction_id
                    - start_offset: 0
                file: mediatrunk
        </meta>
        """
        return resp.json_['data']


    @consumer.post(endpoints.publish_uploaded_video)
    def publish_uploaded_video(resp):
        """Publish a uploaded video.

        Vid is pointted to the uploaded vidoe.

        <meta>
            args:
                query:
                    - access_token
                    - openid
                    - title
                    - tags
                    - cat
                    - desc
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
                    - openid
                    - md5
                    - vid
                file: media
        </meta>
        """
        return resp.json_['data']['transaction_id']
