# entirius-django-vault

A Django module for saved payment cards in Entirius, the open-source modular ecommerce platform. It keeps the
tokenized PayU cards of a customer per sales channel and serves them over a key-protected REST API; card numbers
never reach the database.

[![PyPI](https://img.shields.io/pypi/v/entirius-django-vault.svg)](https://pypi.org/project/entirius-django-vault/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-django-vault.svg)](https://pypi.org/project/entirius-django-vault/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-django-vault/blob/develop/LICENSE)

## What it does

- Lists, adds and deletes the saved payment cards of a signed-in customer.
- Stores only the link between a customer and the payment provider's vault; the cards stay tokenized at PayU.
- Holds the payment provider configuration per sales channel.
- Guards every route with customer authentication and a key in the `X-API-KEY` header.

## Installation

```shell
uv add entirius-django-vault
pip install entirius-django-vault
```

```python
INSTALLED_APPS = [
    ...
    "django_utils",
    "django_accounts",
    "django_vault",
]

# urls.py
urlpatterns = [
    path("", include("django_vault.urls")),
]
```

Required settings: `BI_ENVIRONMENT` and `BI_BUSINESS_UNIT` (read when the module is imported). Reference:
https://github.com/entirius/entirius-django-vault/blob/develop/AGENTS.md (section Settings).

With `django_access` installed the key is an access token with the scope `vault.api`:

```shell
python manage.py access_token create --application <name> --create-application --scope vault.api --channel <idx>
```

Without `django_access`, create the key with `python manage.py vault-generate-api-key [--file_path <path>]`. The key
is printed once and cannot be read back; keys added by hand in the Django admin have a random value nobody sees, so
create them with the command. With `django_access` installed the command refuses: keys are access tokens there.

## Quick start

```python
from django_vault.models import CustomerPaymentVault

vaults = CustomerPaymentVault.objects.filter(customer=customer).select_related("channel_for_payment")
```

The REST routes mount under `{API_BASE_URL}/vault/<version>/<channel_idx>/payment_card/`; requests and responses are
in https://github.com/entirius/entirius-django-vault/blob/develop/docs/vault_docs.md.

## Requirements

- Python 3.11 or newer, Django 5.0 or newer.
- Entirius packages pulled in: `entirius-django-accounts`, `entirius-django-utils`, `entirius-py-payu-sdk`,
  `entirius-py-bievents`, `entirius-py-process-logger`.

## Documentation

- Module docs: https://github.com/entirius/entirius-django-vault/tree/develop/docs
- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-django-vault/blob/develop/CHANGELOG.md

## Part of Entirius

This module runs inside the Entirius backend service (Volkanos), where the checkout uses it for card-on-file
payments.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Sibling modules: https://github.com/entirius/entirius-django-accounts,
  https://github.com/entirius/entirius-django-checkout
- PayU SDK: https://github.com/entirius/entirius-py-payu-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest + pytest-django)
```

Development and agent instructions: https://github.com/entirius/entirius-django-vault/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-django-vault/blob/develop/LICENSE.
