# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
#
#      File: upload.py
#   Project: MVP
#    Author: Luo Yufu
#
#   Copyright (c) 2017 麦禾互动. All rights reserved.

from functools import partial
from hashlib import (
    md5,
    sha1)
import os

import requests

from . import utils
from .doclinks import api
from .exceptions import TransactionFailedError

TRUNK_SIZE = 4 * 1024 * 1024  # 5MB


class Uploader(object):

    def __init__(self, access_token, openid=None):
        self._openid = openid
        self._access_token = access_token

    def upload_video(self, file_path, monitor_callback=print):
        file_size = os.path.getsize(file_path)

        with open(file_path, 'rb') as file_obj:
            transaction_id = self._apply_for_video_upload(file_size, file_obj)
            file_obj.seek(0)

            for result in iter(partial(self._upload_video_trunk, file_obj, transaction_id),
                               StopIteration):
                monitor_callback(result)

            transcation_info_params = dict(access_token=self._access_token,
                                           transaction_id=transaction_id)
            if self._openid:
                transcation_info_params.update(openid=self._openid)

            transaction_info = api.transaction_info(**transcation_info_params)

            if transaction_info['transaction_status'] == u'失败':
                raise TransactionFailedError(transaction_info)

            return transaction_info['vid']

    def _upload_video_trunk(self, file_obj, transaction_id):
        params = {
            'access_token': self._access_token,
            'start_offset': file_obj.tell(),
            'transaction_id': transaction_id,
            'mediatrunk': (file_obj.read(TRUNK_SIZE))
        }

        if self._openid:
            params.update(openid=self._openid)

        result = api.upload_video_chunk(**params)

        if result['end_offset'] == result['start_offset']:
            return StopIteration
        else:
            return result

    def _prepare_apply_params(self, file_size, file_obj):
        md5_hash = utils.calculate_file_hash(md5, file_obj)
        sha1_hash = utils.calculate_file_hash(sha1, file_obj)
        params = {
            'access_token': self._access_token,
            'size': file_size,
            'md5': md5_hash,
            'sha': sha1_hash
        }

        if self._openid:
            params.update(openid=self._openid)
        return params

    def _apply_for_video_upload(self, file_size, file_obj):
        params = self._prepare_apply_params(file_size, file_obj)
        return api.apply_for_video_upload(**params)

    def upload_thumbnail(self, vid, file_pointer):
        try:
            # file_pointer is a file_path
            with open(file_pointer) as file_obj:
                md5_hash = utils.calculate_file_hash(md5, file_obj)
                file_obj.seek(0)
                params = self._prepare_thumbnail_params(vid, md5_hash, file_obj)
                return api.upload_video_thumbnail(**params)
        except (IOError, TypeError):
            # file_pointer is a bytes from file_read or network
            if isinstance(file_pointer, (tuple, list)):
                md5_obj = md5()
                md5_obj.update(file_pointer[1])
                md5_hash = md5_obj.hexdigest()

            params = self._prepare_thumbnail_params(vid, md5_hash, file_pointer)
        else:
            raise ValueError('file_pointer should be a file_path or a tuple(file_name, content)')

    def _prepare_thumbnail_params(self, vid, md5_hash, file_info):
        params = {
            'access_token': self._access_token,
            'vid': vid,
            'md5': md5_hash,
            'media': file_info
        }
        if self._openid:
            params.update(openid=self._openid)

        return params

    def _fetch_thumbnail(self, thumbnail_url):
        return requests.get(thumbnail_url)


def upload_video(access_token, file_path, openid=None):
    return Uploader(access_token, openid).upload_video(file_path)


def upload_thumbnail(access_token, vid, file_pointer, openid=None):
    return Uploader(access_token, openid).upload_thumbnail(vid, file_pointer)
