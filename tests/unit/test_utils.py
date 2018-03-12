# -*- coding: utf-8 -*-

import pytest

from penguinsdk import utils
from penguinsdk.exceptions import (
    RespWithFailedCodeError,
    RespContentValueError)


def test_check_resp_code_success():
    resp_json = {'code': 0}
    resp = object()

    utils.check_resp_code(resp_json, resp)


def test_check_resp_code_failed():
    resp_json = {'code': 1}
    resp = object()

    with pytest.raises(RespWithFailedCodeError):
        utils.check_resp_code(resp_json, resp)


def test_parse_expiry_datetime_without_expires_in(mocker):
    assert utils.parse_expiry_datetime(expires_in=None) is None


def test_parse_expiry_datetime_with_expires_in(mocker):
    mocker.patch.object(utils, 'utcnow', authspec=True,
                        return_value=1000)
    mocker.patch('datetime.timedelta', authspec=True,
                 return_value=1000)

    assert utils.parse_expiry_datetime(1000) == 2000


def test_parse_expiry_timestamp_without_expires_in():
    assert utils.parse_expiry_timestamp(expires_in=None) is None


def test_parse_expiry_timestamp_with_expires_in(mocker):
    mocker.patch.object(utils, 'time',
                        return_value=1000)

    assert utils.parse_expiry_timestamp(1000) == 2000


def test_preprocess_resp_no_json():
    class resp:
        @classmethod
        def json(cls):
            raise ValueError

    with pytest.raises(RespContentValueError):
        utils.preprocess_resp(resp)


def test_preprocess_resp_with_json(mocker):
    class resp:
        @classmethod
        def json(cls):
            return {'code': 0}

    mock = mocker.patch.object(utils,
                               'check_resp_code',
                               authspec=True)

    utils.preprocess_resp(resp)

    assert mock.called
    assert resp.json_ == {'code': 0}
