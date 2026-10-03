# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import secrets

import pytest
from django.apps import apps

CHANNEL_IDXS = ("any-channel", "other-channel")


def import_keys_into_access() -> None:
    """With django_access installed keys are tokens: import the legacy rows as a deploy's migrate does."""
    if apps.is_installed("django_access"):
        from django_access.services.legacy import import_legacy_keys

        import_legacy_keys()


@pytest.fixture
def make_api_key(db):
    """Create an X-API-KEY the module accepts today and return its raw value.

    vault keys carry no channel and no scope, so both arguments are accepted and ignored. The key contract tests
    go through this helper only (with django_access installed it also imports the key as a legacy token), so moving
    the check onto another key store changes this function, never the assertions. Values are random and never printed.
    """
    from django_vault.models import APIKey

    def make_api_key(channel=None, scope: str | None = None) -> str:
        raw = secrets.token_hex(32)
        APIKey.objects.create(key=raw)
        import_keys_into_access()
        return raw

    return make_api_key


@pytest.fixture
def _jwt_backend(settings):
    """The v1 ``@authenticate`` resolves the customer through django.contrib.auth backends."""
    settings.AUTHENTICATION_BACKENDS = [
        "django_accounts.backends.JWTAccessBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]


@pytest.fixture
def payu_channels(db):
    """``payment_card/`` (all cards) answers 500 for a customer without a vault today, so the success pin uses
    ``payment_card/<code>/``, which answers ``[]`` for a channel payment the customer has no vault on."""
    from django_vault.models.channel import Channel, ChannelPayment

    for idx in CHANNEL_IDXS:
        ChannelPayment.objects.create(channel=Channel.objects.create(idx=idx, label=idx), provider="payu_card")


@pytest.fixture
def customer_jwt(db) -> str:
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model
    from django_accounts.models import Customer
    from rest_framework_simplejwt.tokens import RefreshToken

    user = get_user_model().objects.create_user(username="cardholder", email="cardholder@example.com")
    EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
    Customer.objects.create(user=user)
    return str(RefreshToken.for_user(user).access_token)
