# -*- coding: utf-8 -*-

from hashlib import md5
import os

from .utils import calculate_file_hash
from doclink.utils import guess_filename


class Publisher(object):
    def __init__(self, consumer, access_token, openid=None):
        self._consumer = consumer
        self._access_token = access_token
        self._openid = openid

    def publish_video(self, publish_info, file_pointer):
        """Publish vidoe.

        Args:
            publish_info (dict): Info for publish
            file_pointer (str/file_object/tuple): Point to a file.
                It could be one of the below types.

                str:
                    File path of video.
                file_object:
                    File object return from open.
                tuple:
                    2-tuple, (file_name, file_object).
                    3-tuple, (file_name, file_object, Content-Type)
                    4-tuple, (file_name, file_object, Content-Type, headers)

        Returns:
            str: Transaction id of this publishment.
        """
        def prepare_params(publish_info, md5_hash, file_param):
            """Nested function to prepare params."""
            params = dict(publish_info, access_token=self._access_token)
            if self._openid:
                params.update(openid=self._openid)
            params.update(media=file_param, md5=md5_hash)

            return params

        #  file_pointer is tuple of file info
        if isinstance(file_pointer, (list, tuple)):
            file_obj = file_pointer[1]
            md5_hash = calculate_file_hash(md5, file_obj)
            file_obj.seek(0)

            return self._consumer.publish_video(
                **prepare_params(publish_info, md5_hash, file_pointer))
        else:
            try:
                # file_pointer is file path
                file_obj = None
                file_obj = open(file_pointer, 'rb')
            except (IOError, TypeError) as e:
                # file_pointer is file object
                file_name = guess_filename(file_pointer)
                md5_hash = calculate_file_hash(md5, file_pointer)
                file_pointer.seek(0)

                return self._consumer.publish_video(
                    **prepare_params(publish_info, md5_hash, file_pointer))
            else:
                file_name = os.path.basename(file_pointer)
                md5_hash = calculate_file_hash(md5, file_obj)
                file_obj.seek(0)

                return self._consumer.publish_video(
                    **prepare_params(publish_info, md5_hash, (file_name, file_obj)))
            finally:
                if file_obj:
                    file_obj.close()

    def publish_uploaded_video(self, publish_info, vid):
        """Publish an uploaded video by its video.

        Args:
            publish_info (dict): Info for publish.
            vid (str): Vid pointed to the uploade video.

        Returns:
            str: Transaction of this publishment.
        """

        def prepare_params(publish_info, vid):
            """Nested function to prepare params."""
            params = dict(publish_info, vid=vid, access_token=self._access_token)
            if self._openid:
                params.update(openid=self._openid)

            return params

        return self._consumer.publish_uploaded_video(**prepare_params(publish_info, vid))


def publish_video(consumer, access_token, publish_info, file_pointer, openid=None):
    return Publisher(consumer, access_token, openid).publish_video(publish_info, file_pointer)


def publish_uploaded_video(consumer, access_token, publish_info, vid, openid=None):
    return Publisher(consumer, access_token, openid).publish_uploaded_video(publish_info, vid)
