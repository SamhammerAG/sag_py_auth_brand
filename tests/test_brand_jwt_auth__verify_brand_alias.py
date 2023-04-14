from typing import Any, Dict, List, Optional

import pytest
from fastapi import HTTPException
from pytest import MonkeyPatch
from sag_py_auth.models import Token

from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from sag_py_auth_brand.models import BrandAuthConfig

from .helpers import get_token

context_brand: Optional[str] = None
context_brand_alias: Optional[str] = None


def set_brand_to_context_mock(brand_to_set: Optional[str]) -> None:
    global context_brand
    context_brand = brand_to_set


def set_brand_alias_to_context_mock(brand_alias_to_set: Optional[str]) -> None:
    global context_brand_alias
    context_brand_alias = brand_alias_to_set


def test__verify_brand__where_user_has_brand_alias(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    brand_jwt_auth: BrandJwtAuth = _build_sample_jwt_auth(["myRequiredRole"])

    resource_access: Optional[Dict[str, Any]] = {
        "role-brand": {"roles": ["mybrandone"]},
        "role-brand-alias": {"roles": ["mybrandone", "firstalias", "secondalias"]},
    }

    token: Token = get_token(None, resource_access)

    monkeypatch.setattr("sag_py_auth_brand.brand_jwt_auth.set_request_brand_to_context", set_brand_to_context_mock)
    monkeypatch.setattr(
        "sag_py_auth_brand.brand_jwt_auth.set_request_brand_alias_to_context", set_brand_alias_to_context_mock
    )

    # Act
    try:
        brand_jwt_auth._verify_brand(token, "secondalias")
    except Exception:
        pytest.fail("No exception expected if the brand is present in the token")

    # Assert

    # Has to be the brand of the request
    assert context_brand == "secondalias"
    # Has to be the alias of the brand from the request.
    # The alias is the brand that has originally had access to the api
    # It is used in the entire background logic as brand
    assert context_brand_alias == "mybrandone"


def test__verify_brand__where_brand_aliases_is_missing_role_brand(monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(HTTPException) as exception:
        # Arrange
        brand_jwt_auth: BrandJwtAuth = _build_sample_jwt_auth(["myRequiredRole"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone"]},
            "role-brand-alias": {"roles": ["firstalias", "secondalias"]},
        }

        token: Token = get_token(None, resource_access)

        monkeypatch.setattr("sag_py_auth_brand.brand_jwt_auth.set_request_brand_to_context", set_brand_to_context_mock)
        monkeypatch.setattr(
            "sag_py_auth_brand.brand_jwt_auth.set_request_brand_alias_to_context", set_brand_alias_to_context_mock
        )

        # Act
        brand_jwt_auth._verify_brand(token, "secondalias")

    assert exception.value.status_code == 403
    assert exception.value.detail == "Missing brand."
    assert context_brand is None
    assert context_brand_alias is None


def test__verify_brand__where_brand_aliases_have_multiple_role_brands(monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(HTTPException) as exception:
        # Arrange
        brand_jwt_auth: BrandJwtAuth = _build_sample_jwt_auth(["myRequiredRole"])

        resource_access: Optional[Dict[str, Any]] = {
            "role-brand": {"roles": ["mybrandone", "mybrandtwo"]},
            "role-brand-alias": {"roles": ["mybrandone", "mybrandtwo", "firstalias", "secondalias"]},
        }

        token: Token = get_token(None, resource_access)

        monkeypatch.setattr("sag_py_auth_brand.brand_jwt_auth.set_request_brand_to_context", set_brand_to_context_mock)
        monkeypatch.setattr(
            "sag_py_auth_brand.brand_jwt_auth.set_request_brand_alias_to_context", set_brand_alias_to_context_mock
        )

        # Act
        brand_jwt_auth._verify_brand(token, "secondalias")

    assert exception.value.status_code == 403
    assert exception.value.detail == "Missing brand."
    assert context_brand is None
    assert context_brand_alias is None


def _build_sample_jwt_auth(roles: List[str]) -> BrandJwtAuth:
    auth_config = BrandAuthConfig(
        "https://authserver.com/auth/realms/projectName", "myAudience", "myInstance", "myStage"
    )
    return BrandJwtAuth(auth_config, roles)
