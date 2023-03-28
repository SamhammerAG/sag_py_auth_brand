import logging
from typing import Optional

from fastapi import Header
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from sag_py_auth import JwtAuth, Token, TokenRole
from .request_brand_context import set_brand as set_brand_to_context, set_brand_alias as set_brand_alias_to_context
from .models import BrandAuthConfig

logger = logging.getLogger(__name__)


class BrandJwtAuth(JwtAuth):
    def __init__(
            self,
            auth_config: BrandAuthConfig,
            required_role: Optional[str]):
        super().__init__(
            auth_config,
            required_roles=[
                TokenRole('role-instance', auth_config.instance),
                TokenRole('role-endpoint', required_role)
            ],
            required_realm_roles=[auth_config.stage])

    async def __call__(self, request: Request, brand: str = Header(...)) -> Token:
        token = await super(BrandJwtAuth, self).__call__(request)
        self._verifyBrand(token, brand)
        set_brand_to_context(brand)
        return token

    def _verifyBrand(self, token: Token, brand: str):
        if not token.has_role('role-brand', brand) and not self._brand_has_accessible_alias(token, brand):
            self._raise_auth_error(HTTP_403_FORBIDDEN, "Missing brand.")

    def _brand_has_accessible_alias(self, token: Token, brand: str):
        brand_aliases = token.get_roles('role-brand-alias')

        # Check if the given brand is defined as alias for the brand it should be replaced by.
        if len(brand_aliases) < 1:
            logger.debug("Brand %s is not in list of accessible brand aliases.", brand)
            return False

        # Find indices of all detected brand aliases accessible for the current client or user
        # (i.e. compare accessible brands with brand aliases in token because
        # user access is configured via brands (not via brand alias)):
        accessible_brand_alias_ids = [
            id for id, val in enumerate(
                brand_alias in token.get_roles('role-brand')
                for brand_alias in brand_aliases
            ) if val
        ]

        # Set alias only if there is exactly one match
        # (one user must have access to 0 or 1 brand that corresponds to a brand alias):
        if len(accessible_brand_alias_ids) > 1:
            logger.warning("Unambiguous role association: user has access to more than one brand alias.")
            return False
        if len(accessible_brand_alias_ids) == 0:
            logger.warning("Unambiguous role association: brand is not associated with any brand aliases.")
            return False

        brand_alias = brand_aliases[0]
        set_brand_alias_to_context(brand_alias)
        return True
