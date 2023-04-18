# sag_py_auth_brand

[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities](https://snyk.io/test/github/SamhammerAG/sag_py_auth_brand/badge.svg)](https://snyk.io/test/github/SamhammerAG/sag_py_auth_brand)

[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_auth_brand/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_auth_brand?branch=master
[codeclimate-image]:https://api.codeclimate.com/v1/badges/9731a0fe593f7e5f10b6/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_auth_brand/maintainability

This provides a way to secure your fastapi with keycloak jwt bearer authentication.
This library bases on sag_py_auth and adds support for instances/brands.

## What it does
* Secure your api endpoints
* Verifies auth tokens: signature, expiration, issuer, audience
* Verifies the brand/customer over a token role (+ alias support)
* Verifies the instance over a token role
* Verifies the stage over a realm role
* Allows to set additional permissions by specifying further token roles

## How to use

### Installation

pip install sag-py-auth-brand

### Secure your apis

First create the fast api dependency with the auth config:
```python
from sag_py_auth import TokenRole
from sag_py_auth_brand.models import AuthConfig
from sag_py_auth_brand.brand_jwt_auth import BrandJwtAuth
from fastapi import Depends

auth_config = BrandAuthConfig("https://authserver.com/auth/realms/projectName", "myaudience", "myinstance", "mystage")
required_roles = [TokenRole("clientname", "adminrole")]
requires_admin = Depends(BrandJwtAuth(auth_config, required_roles))
```

Afterwards you can use it in your route like that:

```python
@app.post("/posts", dependencies=[requires_admin], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
```

Or if you use sub routes, auth can also be enforced for the entire route like that:

```python
router = APIRouter()
router.include_router(sub_router, tags=["my_api_tag"], prefix="/subroute",dependencies=[requires_admin])
```

### Get brand information

See sag_py_auth to find out how to access the token and user info.

Furthermore you can get the brand by accessing it over the context:
```python
from sag_py_auth_brand.request_brand_context import get_brand as get_brand_from_context
brand = get_brand_from_context()
```

This works in async calls but not in sub threads (without additional changes).

See:
* https://docs.python.org/3/library/contextvars.html
* https://kobybass.medium.com/python-contextvars-and-multithreading-faa33dbe953d

### Log the brand

It is possible to log the brand by adding a filter.

```python
import logging
from sag_py_auth_brand.request_brand_logging_filter import RequestBrandLoggingFilter

console_handler = logging.StreamHandler(sys.stdout)
console_handler.addFilter(RequestBrandLoggingFilter())

```

The filter provides the field request_brand with the brand.

### How a token has to look like

```json
{

    "iss": "https://authserver.com/auth/realms/projectName",
    "aud": ["audienceOne", "audienceTwo"],
    "typ": "Bearer",
    "azp": "public-project-swagger",
    "preferred_username": "preferredUsernameValue",
    .....
    "realm_access": {
        "roles": ["myStage"]
    },
    "resource_access": {
        "role-instance": {
            "roles": ["myInstance"]
        },
        "role-brand": {
            "roles": ["myBrand"]
        },
        "role-endpoint": {
            "roles": ["permissionOne", "permissionTwo"]
        },
        "role-brand-alias": {
            "roles": ["myBrand", "myBrandAliasOne", "myBrandAliasTwo"]
        }
    }
}
```

* role-endpoint is just required for permission checks of the api endpoint
* role-brand-alias is optional for the alias feature. If you don't use aliases it can be left ayway.
* role-brand-alias must contain exactly one original brand together with one or multiple aliases

## How to publish

* Update the version in setup.py and commit your change
* Create a tag with the same version number
* Let github do the rest
