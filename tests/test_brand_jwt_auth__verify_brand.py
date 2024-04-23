from typing import Any, Dict, Optional
from unittest import TestCase, main

import mock
import pytest
from mock import Mock
from sag_py_auth.models import Token

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth

from .helpers import build_sample_jwt_auth, get_token


class TestVerifyBrand(TestCase):
    @mock.patch("sag_py_auth_brand.brand_jwt_auth.set_request_brand_to_context")
    def test__verify_brand__where_user_has_brand(self, mock_set_brand_to_context: Mock) -> None:
        # Arrange
        brand_jwt_auth: BrandJwtAuth = build_sample_jwt_auth(["myEndpoint"])

        resource_access: Optional[Dict[str, Any]] = {"role-brand": {"roles": ["mybrandone", "mybrandtwo"]}}

        token: Token = get_token(None, resource_access)

        # Act
        try:
            brand_jwt_auth._verify_brand(token, "mybrandone")
        except Exception:
            pytest.fail("No exception expected if the brand is present in the token")

        # Assert
        mock_set_brand_to_context.assert_called_once_with("mybrandone")


if __name__ == "__main__":
    main()
