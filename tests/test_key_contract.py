# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Characterization of today's vault key contract (X-API-KEY + customer JWT).

Keyed views stack ``@authenticate @authorize_api @require_authentication``: the key is checked before the
customer, and keys carry no channel. Pins what they answer — quirks included — so moving the key check onto
another key store cannot change a status or a body. Keys come only from the ``make_api_key`` helper.

The module has no key-free public route: both ``payment_card`` routes are keyed.
"""

import secrets

import pytest
from rest_framework.test import APIClient

CARDS_URL = "/api/vault/1/{channel_idx}/payment_card/payu_card/"
pytestmark = pytest.mark.usefixtures("payu_channels")


def _cards(key: str | None, jwt: str | None = None, channel_idx: str = "any-channel"):
    headers = {}
    if key is not None:
        headers["HTTP_X_API_KEY"] = key
    if jwt is not None:
        headers["HTTP_AUTHORIZATION"] = f"Bearer {jwt}"
    return APIClient().get(CARDS_URL.format(channel_idx=channel_idx), **headers)


def _refusal(response) -> tuple[int, str, object]:
    body = response.json()
    return response.status_code, body["meta"]["status"], body["data"]


@pytest.fixture(autouse=True)
def _live_key(make_api_key):
    """Valid keys exist in every test, so a refusal proves the lookup, not an empty key store."""
    make_api_key()


@pytest.mark.django_db
class TestAuthorizeApi:
    def test_no_key_and_no_jwt_is_401(self):
        assert _refusal(_cards(None)) == (401, "UNAUTHORIZED", "Invalid api key")

    def test_wrong_key_with_customer_jwt_is_401(self, customer_jwt):
        wrong_key = secrets.token_hex(32)
        response = _cards(wrong_key, jwt=customer_jwt)
        assert _refusal(response) == (401, "UNAUTHORIZED", "Invalid api key")
        assert wrong_key not in response.content.decode()

    def test_right_key_without_customer_jwt_is_401(self, make_api_key):
        assert _refusal(_cards(make_api_key())) == (401, "UNAUTHORIZED", {})

    def test_right_key_with_customer_jwt_lists_cards(self, customer_jwt, make_api_key):
        response = _cards(make_api_key(), jwt=customer_jwt)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_key_is_not_bound_to_a_channel(self, customer_jwt, make_api_key):
        assert _cards(make_api_key(), jwt=customer_jwt, channel_idx="other-channel").status_code == 200
