# -*- coding: utf-8 -*-

from hashlib import md5

from .utils import calculate_file_hash
from doclink.utils import guess_filename
from doclinks import api


class Publisher(object):
    def __init__(self, access_token, openid=None):
        self._access_token = access_token
        self._openid = openid

    def publish_video(self, upload_info, file_pointer):
        """Publish vidoe.

        Args:
            upload_info (dict): Info for publish
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
        def prepare_params(upload_info, md5_hash, file_param):
            """Nested function to prepare params."""
            params = dict(upload_info, access_token=self._access_token)
            if self._openid:
                params.update(openid=self._openid)
            params.update(media=file_param, md5=md5_hash)

        #  file_pointer is file_path
        if isinstance(file_pointer, str):
            with open(file_pointer) as file_obj:
                file_name = guess_filename(file_obj)
                md5_hash = calculate_file_hash(md5, file_obj)
                file_obj.seek(0)

                return api.upload_video_thumbnail(
                    **prepare_params(upload_info, md5_hash, (file_name, file_obj)))
        #  file_pointer is tuple of file info
        elif isinstance(file_pointer, (list, tuple)):
            file_obj = file_pointer[1]
            md5_hash = calculate_file_hash(md5, file_obj)
            file_obj.seek(0)

            return api.upload_video_thumbnail(
                **prepare_params(upload_info, md5_hash, file_pointer))
        # file_pointer is file object
        else:
            file_name = guess_filename(file_pointer)
            md5_hash = calculate_file_hash(md5, file_pointer)
            file_pointer.seek(0)

            return api.upload_video_thumbnail(
                **prepare_params(upload_info, md5_hash, file_pointer))

    def publish_uploaded_video(self, upload_info, vid):
        """Publish an uploaded video by its video.

        Args:
            upload_info (dict): Info for publish.
            vid (str): Vid pointed to the uploade video.

        Returns:
            str: Transaction of this publishment.
        """

        def prepare_params(upload_info, vid):
            """Nested function to prepare params."""
            params = dict(upload_info, vid=vid, access_token=self._access_token)
            if self._openid:
                params.update(openid=self._openid)

        return api.publish_uploaded_video(**prepare_params(upload_info, vid))
