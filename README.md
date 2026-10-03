# Django Vault

Customer payment-card vault for the Volkanos ecommerce platform. Stores tokenized PayU cards per
customer and channel, exposed through an X-API-KEY-protected REST API — companion module to
[entirius-django-accounts](https://github.com/entirius/entirius-django-accounts).

## Installation

```shell
pip install entirius-django-vault
```

Add the app to your project:

```python
INSTALLED_APPS = [
    ...
    "django_vault",
]
```

Requires `django_accounts` in `INSTALLED_APPS` (schema dependency) and the host settings
`BI_ENVIRONMENT` + `BI_BUSINESS_UNIT`. Include the API with your URLconf:

```python
urlpatterns += [path("", include("django_vault.urls"))]
```

## Usage

Generate an API key and call the vault API (see [docs/vault_docs.md](docs/vault_docs.md)):

```bash
python manage.py vault-generate-api-key [--file_path <path>]
```

The key is printed once and cannot be read back; keys added by hand in the Django admin have a random value
nobody sees, so create them with the command.

With django-access installed the command refuses: keys are access tokens there
(`manage.py access_token create --scope vault.api --application <name> --expires-days <days>`).

Log codes reference: [docs/log_codes.md](docs/log_codes.md).

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest + pytest-django)
```

Architecture and settings reference: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
