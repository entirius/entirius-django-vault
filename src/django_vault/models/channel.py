# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from django_vault.domain.enums import PaymentProvider
from django_vault.domain.payment_provider.payu_payment_vault import PayUPaymentProvider
from django_vault.models.base_model import BaseModel


class Channel(BaseModel):
    idx = models.CharField(max_length=128, blank=False, null=False, unique=True)
    label = models.CharField(max_length=128, blank=False, null=False, default="", unique=True)
    objects = models.Manager()


class ChannelPayment(BaseModel):
    channel: "Channel" = models.ForeignKey(on_delete=models.deletion.CASCADE, to="Channel")
    additional_data = models.JSONField(blank=True, null=True)
    provider = models.CharField(max_length=24, choices=PaymentProvider.choices, default=PaymentProvider.UNKNOWN)
    objects = models.Manager()

    def _get_provider_cls(self):
        match self.provider:
            case PaymentProvider.PAYU_CARD:
                return PayUPaymentProvider
            case PaymentProvider.PAYU_CARD_ADD:
                return PayUPaymentProvider
            case _:
                return None

    def _get_provider_init_args(self):
        args = [self]
        kwargs = {}
        return args, kwargs

    def get_provider(self):
        args, kwargs = self._get_provider_init_args()
        cls = self._get_provider_cls()
        return cls(*args, **kwargs)
