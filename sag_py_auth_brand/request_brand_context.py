from typing import Optional

from contextvars import ContextVar

brand: ContextVar[Optional[str]] = ContextVar('brand', default=None)
brand_alias: ContextVar[Optional[str]] = ContextVar('brand_alias', default=None)


def get_brand() -> str:
    """Gets the context local brand. See library contextvars for details.

    Returns: The brand
    """
    current_brand_alias = brand_alias.get('')
    current_brand = brand.get('')
    return current_brand_alias if current_brand_alias != "" else current_brand


def set_brand(brand_to_set: str):
    """Sets the context local brand. See library contextvars for details.
    """
    brand.set(brand_to_set)


def set_brand_alias(brand_alias_to_set: str):
    """Sets the context local brand. See library contextvars for details.
    """
    brand_alias.set(brand_alias_to_set)
