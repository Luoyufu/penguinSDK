# -*- coding: utf-8 -*-

import datetime
from functools import partial
from time import time

from .exceptions import RespWithFailedCodeError
from .exceptions import RespContentValueError

CLOCK_GAP_SECS = 300  # 5 minutes, used to early expired and invoke refresh
CLOCK_GAP = datetime.timedelta(seconds=CLOCK_GAP_SECS)

KIND_3RD_PARTY = '3rd_party'
KIND_CONTENT_SITE = 'content_site'


def check_resp_code(resp_json, resp):
    """Check the code from tencent resp.
    If resp succeed, code in resp_json will be '0'.

    Args:
        resp_json (dict): json from tencest resp.

    Raises:
        RespWithFailedCodeError: if check failed.
    """
    code = resp_json['code']
    if code not in ('0', 0):
        raise RespWithFailedCodeError(code, resp_json, resp)


def utcnow():   # pragma: no cover
    """Returns the current UTC datetime.

    Returns:
        datetime: The current time in UTC.
    """
    return datetime.datetime.utcnow()


def parse_expiry_datetime(expires_in):
    """Parses the expiry field from a response into a datetime.
    Args:
        response_data (Mapping): The JSON-parsed response data.
    Returns:
        Optional[datetime]: The expiration or ``None`` if no expiration was
            specified.
    """
    if expires_in:
        return utcnow() + datetime.timedelta(
            seconds=expires_in)
    else:
        return None


def parse_expiry_timestamp(expires_in):
    """Parses the expiry field from a response into a timestamp.
    Args:
        response_data (Mapping): The JSON-parsed response data.
    Returns:
        Optional[datetime]: The expiration or ``None`` if no expiration was
            specified.
    """
    if expires_in:
        return int(time()) + expires_in
    else:
        return None


def preprocess_resp(resp):
    try:
        resp_json = resp.json()
    except ValueError:
        raise RespContentValueError

    check_resp_code(resp_json, resp)
    resp.json_ = resp_json


def calculate_file_hash(hash_factory, file_obj, read_factor=128):   # pragma: no cover
    file_obj.seek(0)
    hash_obj = hash_factory()
    read_size = read_factor * hash_obj.block_size

    for chunk in iter(partial(file_obj.read, read_size), b''):
        hash_obj.update(chunk)

    return hash_obj.hexdigest()
