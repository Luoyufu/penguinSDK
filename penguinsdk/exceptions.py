# -*- coding: utf-8 -*-


class PenguinError(Exception):
    """docstring for PenguinError"""
    pass


class RespWithFailedCodeError(PenguinError):
    def __init__(self, code, resp_json, resp):
        super(RespWithFailedCodeError, self).__init__(
            'penguin resp with error content, code: {}\n'
            'resp_json:{}'.format(code, resp_json))
        self.code = code
        self.resp_json = resp_json
        self.resp = resp


class RespContentValueError(PenguinError):
    def __init__(self, msg=None):
        super(RespContentValueError, self).__init__(
            msg or 'resp content value error')


class CredentialError(PenguinError):
    def __init__(self, msg=None):
        super(CredentialError, self).__init__(
            msg or 'credential error')


class TokenRefreshFailedError(PenguinError):
    def __init__(self, msg='token refresh failed'):
        super(TokenRefreshFailedError, self).__init__(msg)
