from typing import Any

from sag_py_auth.models import Token

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.models import BrandAuthConfig


def build_sample_auth_config() -> BrandAuthConfig:
    return BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName",
        "myAudience",
        "myInstance",
        "myStage",
    )


def build_sample_jwt_auth(roles: list[str] | None) -> BrandJwtAuth:
    auth_config: BrandAuthConfig = build_sample_auth_config()
    return BrandJwtAuth(auth_config, roles)


def get_token(
    realm_access: dict[str, Any] | None, resource_access: dict[str, Any] | None
) -> Token:
    token_dict: dict[str, Any] = {
        "exp": 1679924012,
        "iat": 1679923712,
        "auth_time": 1679923711,
        "jti": "d21e91b2-ad94-4564-b183-261f84517e04",
        "iss": "https://authserver.com/auth/realms/projectName",
        "aud": ["audienceOne", "audienceTwo"],
        "sub": "138e7422-751f-4184-972a-f54938dba104",
        "typ": "Bearer",
        "azp": "public-project-swagger",
        "session_state": "cded04d5-b630-43db-a7b1-c0065ba52fdf",
        "allowed-origins": ["https://myproject.com", "http://myproject.de"],
        "scope": "scopeOne scopeTwo",
        "sid": "ceed04d5-b630-43db-a7b1-90065ba52fdd",
        "email_verified": False,
        "preferred_username": "preferredUsernameValue",
    }

    if realm_access is not None:
        token_dict["realm_access"] = realm_access

    if resource_access is not None:
        token_dict["resource_access"] = resource_access

    return Token(token_dict)
