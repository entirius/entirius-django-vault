# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import unique

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


@unique
class PaymentProvider(TextChoices):
    UNKNOWN = "unknown", _("unknown")
    PAYU_CARD = "payu_card", _("PayU Card")
    PAYU_CARD_ADD = "payu_card_add", _("PayU Card Add")
