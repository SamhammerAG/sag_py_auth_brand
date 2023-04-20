from logging import LogRecord

from sag_py_auth.models import AuthConfig


class BrandAuthConfig(AuthConfig):
    def __init__(self, issuer: str, audience: str, instance: str, stage: str) -> None:
        super().__init__(issuer, audience)
        self.instance: str = instance
        self.stage: str = stage


class BrandLogRecord(LogRecord):
    # This is the brand for backend logic
    brand: str
    # The original brand of the request
    request_brand: str
    # The brand used in backend logic in case of aliasing
    request_brand_alias: str
