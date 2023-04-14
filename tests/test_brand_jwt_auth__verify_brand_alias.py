from typing import Any, Dict, Optional
from unittest import TestCase, main

import pytest
from fastapi import HTTPException
from sag_py_auth.models import Token

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.constants import LogMessages
from sag_py_auth_brand.models import BrandAuthConfig

from .helpers import get_token


class TestVerifyBrandAlias(TestCase):

    def test__verify_brand__where_user_has_brand_alias(self) -> None:
        # Arrange
        auth_config = BrandAuthConfig(
            "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
        )
        brand_jwt_auth = BrandJwtAuth(auth_config, ["myEndpoint"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone"]},
            "role-brand-alias": {"roles": ["mybrandone", "firstalias", "secondalias"]},
        }

        token: Token = get_token(None, resource_access)

        # Act
        try:
            brand_jwt_auth._verify_brand(token, "secondalias")
        except Exception:
            pytest.fail("No exception expected if the brand is present in the token")

    def test__verify_brand__with_missing_brand_alias(self) -> None:
        # Arrange
        auth_config = BrandAuthConfig(
            "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
        )
        brand_jwt_auth = BrandJwtAuth(auth_config, ["myEndpoint"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone"]},
            "role-brand-alias": {"roles": []},
        }

        token: Token = get_token(None, resource_access)

        # Act
        with pytest.raises(HTTPException) as exception, self.assertLogs(level='DEBUG') as log_watcher:
            brand_jwt_auth._verify_brand(token, "secondalias")

        # Assert
        self.assertTrue(LogMessages.MISSING_BRAND_ALIAS in ''.join(log_watcher.output))
        assert exception.value.status_code == 403
        assert exception.value.detail == "Missing brand."

    def test__verify_brand__where_brand_aliases_is_missing_role_brand(self) -> None:
        # Arrange
        auth_config = BrandAuthConfig(
            "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
        )
        brand_jwt_auth = BrandJwtAuth(auth_config, ["myEndpoint"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone"]},
            "role-brand-alias": {"roles": ["firstalias", "secondalias"]},
        }

        token: Token = get_token(None, resource_access)

        # Act
        with pytest.raises(HTTPException) as exception, self.assertLogs() as log_watcher:
            brand_jwt_auth._verify_brand(token, "secondalias")

        # Assert
        self.assertTrue(LogMessages.MISSING_COMPOUND_BRAND in ''.join(log_watcher.output))
        assert exception.value.status_code == 403
        assert exception.value.detail == "Missing brand."

    def test__verify_brand__where_brand_aliases_have_multiple_role_brands(self) -> None:
        # Arrange
        auth_config = BrandAuthConfig(
            "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
        )
        brand_jwt_auth = BrandJwtAuth(auth_config, ["myEndpoint"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone", "mybrandtwo"]},
            "role-brand-alias": {"roles": ["mybrandone", "mybrandtwo", "firstalias", "secondalias"]},
        }

        token: Token = get_token(None, resource_access)

        # Act
        with pytest.raises(HTTPException) as exception, self.assertLogs() as log_watcher:
            brand_jwt_auth._verify_brand(token, "secondalias")

        # Assert
        self.assertTrue(LogMessages.UNAMBIGUOUS_BRAND_ALIAS in ''.join(log_watcher.output))
        assert exception.value.status_code == 403
        assert exception.value.detail == "Missing brand."


if __name__ == '__main__':
    main()