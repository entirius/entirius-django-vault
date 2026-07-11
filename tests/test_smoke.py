# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Smoke test: every public submodule imports cleanly under a configured Django."""

import importlib

import pytest

MODULES = [
    "django_vault.apps",
    "django_vault.settings",
    "django_vault.bi",
    "django_vault.urls",
    "django_vault.admin",
    "django_vault.models.api_key",
    "django_vault.models.base_model",
    "django_vault.models.channel",
    "django_vault.models.customer_vault",
    "django_vault.domain.dto.card",
    "django_vault.domain.enums",
    "django_vault.domain.payment_provider.payu_payment_vault",
    "django_vault.utils.decorators",
    "django_vault.views.vault_api",
    "django_vault.management.commands.vault-generate-api-key",
]


@pytest.mark.parametrize("module", MODULES)
def test_module_imports(module):
    importlib.import_module(module)
