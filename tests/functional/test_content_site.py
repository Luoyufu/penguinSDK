# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from os import path

import pytest

from penguinsdk import Penguin
from . import utils

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']


@pytest.fixture(scope='module')
def credential():
    return Penguin(client_id,
                   client_secret).oauth2_flow.get_access_token()


@pytest.fixture(scope='module')
def penguin(credential):
    penguin = Penguin(client_id, client_secret)
    penguin.credential = credential

    return penguin


class TestContentSite:
    def test_check_token(self, credential):
        assert credential.check_token()

    def test_publish_video(self, penguin):
        media_path = path.join(
            path.dirname(path.abspath(__file__)), 'media', 'video.mkv')

        transaction_id = penguin.publish_video({
            'title': u'超级搞笑的绿头鹦鹉高能扭头' + utils.now_str(),
            'desc': u'一只绿头鹦鹉瞬间高能转头,十分搞笑',
            'tags': u'搞笑 萌宠',
            'cat': 700}, media_path)

        print(transaction_id)

    def test_get_media_info(self, penguin):
        media_info = penguin.media_info()

        print(media_info)
        assert 'nick' in media_info
        assert 'header' in media_info

    @pytest.mark.skip(reason="no suitable rtmp_url")
    def test_publish_live(self, penguin):
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        penguin.publish_live(
            title=u'精品直播放送，欢迎围观' + utils.now_str(),
            start_time=start_time.strftime('%y-%m-%d %H:%M:%S'),
            end_time=end_time.strftime('%y-%m-%d %H:%M:%S'),
            cover_pic='http://cms-bucket.nosdn.127.net/'
            'be6a67cdbe8f4ce7851bab7c5d72d14820180308222319.jpg',
            rtmp_url='rtmp://live.hkstv.hk.lxdns.com/live/hks')

    def test_publish_article(self, penguin):
        penguin.publish_article(
            title=u'一些有趣的社会实验，探寻心灵的启迪' + utils.now_str(),
            content=u'这些都是来自国内外真实的社会实验，能打动你我的心。'.encode('utf-8'),
            cover_pic='http://cms-bucket.nosdn.127.net/'
            'be6a67cdbe8f4ce7851bab7c5d72d14820180308222319.jpg')

    def test_publish_video_by_chunk(self, penguin):
        video_path = path.join(
            path.dirname(path.abspath(__file__)), 'media', 'video.mkv')
        pic_path = path.join(
            path.dirname(path.abspath(__file__)), 'media', 'pic.jpg')

        vid = penguin.upload_video(video_path)
        penguin.upload_thumbnail(vid, pic_path)
        publish_tid = penguin.publish_uploaded_video(
            {
                'title': u'超级搞笑的绿头鹦鹉高能扭头' + utils.now_str(),
                'desc': u'一只绿头鹦鹉瞬间高能转头,十分搞笑',
                'tags': u'搞笑 萌宠',
                'cat': 700
            },
            vid)
        print(penguin.transaction_info(transaction_id=publish_tid))

    def test_media_stats(self, penguin):
        print(penguin.media_stats())

    @pytest.mark.skip(u'企鹅号返回404')
    def test_media_daily_stats(self, penguin):
        print(penguin.media_daily_stats())

    def test_article_stats(self, penguin):
        print(penguin.article_stats(article_id='20180311A0F1OI00'))

    @pytest.mark.skip(u'企鹅号返回404')
    def test_article_daily_stats(self, penguin):
        print(penguin.article_daily_stats(article_id='20180311A0F1OI00'))
