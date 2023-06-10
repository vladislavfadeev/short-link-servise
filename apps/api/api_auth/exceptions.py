import apps.api.api_auth.status as status


class AuthenticationFailed(Exception):
    """
    """   
    def __init__(self, msg=None):
        self.code = status.HTTP_401_UNAUTHORIZED
        self.detail = 'Incorrect authentication credentials.'
        self.default_code = 'authentication_failed'
        if msg:
            self.detail = msg

    def __str__(self):
        return f'{self.detail} - {self.default_code} - CODE [{self.code}]'
