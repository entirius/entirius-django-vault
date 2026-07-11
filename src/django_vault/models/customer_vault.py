# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import uuid

from django.db import models

from .base_model import BaseModel


def generate_first_transaction_id():
    first_transaction_id = uuid.uuid4()
    while CustomerPaymentVault.objects.filter(first_transaction_id=first_transaction_id).exists():
        first_transaction_id = uuid.uuid4()
    return first_transaction_id


def generate_ext_customer_id():
    ext_customer_id = uuid.uuid4()
    while CustomerPaymentVault.objects.filter(ext_customer_id=ext_customer_id).exists():
        ext_customer_id = uuid.uuid4()
    return ext_customer_id


class CustomerPaymentVault(BaseModel):
    channel_for_payment = models.ForeignKey("ChannelPayment", on_delete=models.CASCADE, related_name="vault_channel")
    customer = models.ForeignKey("django_accounts.Customer", on_delete=models.CASCADE, related_name="vault_customer")
    first_transaction_id = models.CharField(
        max_length=128, blank=False, null=False, default=generate_first_transaction_id, unique=True
    )
    ext_customer_id = models.CharField(
        max_length=128, blank=False, null=False, default=generate_ext_customer_id, unique=True
    )
    objects = models.Manager()
