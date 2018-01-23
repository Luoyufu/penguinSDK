# -*- coding: utf-8 -*-

import datetime
from time import time

from .exceptions import RespWithFailedCodeError
from .exceptions import RespContentValueError

CLOCK_GAP_SECS = 300  # 5 minutes, used to early expired and invoke refresh
CLOCK_GAP = datetime.timedelta(seconds=CLOCK_GAP_SECS)


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


def utcnow():
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
        return time() + expires_in
    else:
        return None


def preprocess_resp(resp):
    try:
        resp_json = resp.json()
    except ValueError:
        raise RespContentValueError

    check_resp_code(resp_json, resp)
    resp.json_ = resp_json
