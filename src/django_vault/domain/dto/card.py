# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from marshmallow_dataclass import add_schema, dataclass


@add_schema
@dataclass
class PayUAddCardPayload:
    token: str


@add_schema
@dataclass
class PayUDeleteCardPayload:
    token: str


@add_schema
@dataclass
class Card:
    value: str
    brandImageUrl: str
    status: str
    cardExpirationYear: int
    cardExpirationMonth: int
    cardNumberMasked: str
    cardScheme: str
    cardBrand: str
