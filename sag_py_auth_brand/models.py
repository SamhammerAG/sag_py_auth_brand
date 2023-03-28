from sag_py_auth.models import AuthConfig


class BrandAuthConfig(AuthConfig):
    def __init__(self, issuer: str, audience: str, instance: str, stage: str):
        super().__init__(issuer, audience)
        self.instance = instance
        self.stage = stage
