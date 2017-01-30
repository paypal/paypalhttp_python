from token_service import TokenService


class Injector:
    def __call__(self, request):
        raise NotImplementedError("Injectors must be callable")


class AuthInjector(Injector):
    def __init__(self, environment, refresh_token=None):
        self.environment = environment
        self.refresh_token = refresh_token

        self.access_token = None
        self.token_service = TokenService(environment)

    def __call__(self, r):
        if self.access_token and not self.access_token.is_expired():
            token = self.access_token
        else:
            token = self.token_service.fetch_access_token(refresh_token=self.refresh_token)
            self.access_token = token

        r.headers["Authorization"] = "Bearer " + token.access_token

        return r
