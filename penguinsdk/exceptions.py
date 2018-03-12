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


class TransactionFailedError(PenguinError):
    def __init__(self, transaction_info, msg='transaction failed'):
        super(TransactionFailedError, self).__init__(msg)
        self.transaction_info = transaction_info


class UnsupporttedApiError(PenguinError):
    def __init__(self, msg):
        super(UnsupporttedApiError, self).__init__(msg)
