# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from dataclasses import asdict

from payu_sdk import PayU

from django_vault.domain.dto.card import Card

logger = logging.getLogger(__name__)
logger_process = logging.getLogger("process")


class PayUPaymentProvider:
    email = None
    request = None
    ext_customer_id = None
    first_transaction_id = None
    additional_data = {}
    payu = None

    def __init__(self, additional_data: str) -> None:
        self.additional_data = additional_data

    def get_use_sandbox_setting(self) -> bool:
        if "use_sandbox" in self.additional_data and isinstance(self.additional_data["use_sandbox"], bool):
            return self.additional_data["use_sandbox"]
        else:
            return True

    def check_connection_data(self):
        if (
            "client_id" not in self.additional_data
            or "client_secret" not in self.additional_data
            or not self.ext_customer_id
            or not self.email
        ):
            raise AttributeError("No connection data in payment method")

    def process_authorization(self):
        self.check_connection_data()
        self.payu = PayU(
            client_id=self.additional_data["client_id"],
            client_secret=self.additional_data["client_secret"],
            pos_id=self.additional_data["pos_id"],
            email=self.email,
            ext_customer_id=self.ext_customer_id,
        )
        self.payu.use_sandbox(self.get_use_sandbox_setting())
        self.payu.authorize()

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_card_list(self):
        self.process_authorization()
        payments_method = self.payu.get_payment()
        card_list = []
        for card in payments_method["cardTokens"]:
            card.pop("preferred")
            card_list.append(asdict(Card.Schema().load(card)))
        return card_list

    def add_card(self, token):
        self.process_authorization()
        ip = self.get_client_ip()
        return self.payu.add_card(token, ip, self.first_transaction_id)

    def delete_card(self, token):
        self.process_authorization()
        return self.payu.delete_card(token)
