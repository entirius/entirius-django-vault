# AGENTS.md

Customer payment-card vault with PayU tokenized cards behind an X-API-KEY REST API —
distribution `entirius-django-vault`, Django app `django_vault`.

**Tech:** Python >=3.11, Django >=5.0, entirius-py-payu-sdk, entirius-django-utils
(API decorators), entirius-django-accounts (schema dependency)

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest + pytest-django) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the package / Django app_label / DB table prefix `django_vault` — it is a schema contract.
- Migrations are part of the public contract — never edit an already released migration.
- Default: do not commit — git is the user's call.

## Architecture

```
urls.py  →  views/vault_api.py (get_payment_cards, process_payment_card)
              @authenticate + @authorize_api (X-API-KEY ↔ models.APIKey)
              → models.CustomerPaymentVault (FK django_accounts.Customer, per ChannelPayment)
              → domain/payment_provider/payu_payment_vault.py → payu-sdk (tokenized cards)
```

| Path | Purpose |
|------|---------|
| `models/api_key.py` | `APIKey` — sha256 key for the X-API-KEY header |
| `models/channel.py` | `Channel` + `ChannelPayment` — provider config per channel (JSON `additional_data`) |
| `models/customer_vault.py` | `CustomerPaymentVault` — customer ↔ provider vault record |
| `views/vault_api.py` | REST API: list / add / delete payment cards |
| `domain/payment_provider/` | PayU provider (sandbox flag from `additional_data`) |
| `domain/dto/card.py` | marshmallow-dataclass payloads (add/delete card) |
| `utils/decorators.py` | `authorize_api` — X-API-KEY check |
| `bi.py` | bievents base event (reads `BI_ENVIRONMENT`/`BI_BUSINESS_UNIT` at import) |
| `management/commands/vault-generate-api-key.py` | API-key generator (writes under `DATA_DIR`) |

## Settings

| Setting | Default | Purpose |
|---------|---------|---------|
| `API_BASE_URL` | `"api"` | URL prefix for the vault API |
| `BI_ENVIRONMENT` | — (required) | bievents environment; read at import of `bi.py` |
| `BI_BUSINESS_UNIT` | — (required) | bievents business unit; read at import of `bi.py` |
| `DATA_DIR` | — | target dir for `vault-generate-api-key` without `--file_path` |

Log codes reference: `docs/log_codes.md`; API reference: `docs/vault_docs.md`.

## Gotchas

- `CustomerPaymentVault.customer` is a string-reference FK to `django_accounts.Customer` — no
  Python import, but migration 0001 depends on `django_accounts.0017` (covered by the released
  accounts squash via `replaces`); deptry needs the DEP002 ignore for it.
- `bi.py` reads `settings.BI_ENVIRONMENT`/`BI_BUSINESS_UNIT` at import time — the host must define
  them or module import fails.
- Card tokens in `docs/vault_docs.md` examples are PayU sandbox samples, not secrets.
