# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import include, path

from django_vault import settings
from django_vault.views.vault_api import get_payment_cards, process_payment_card

api_paths = [
    path("payment_card/<str:payment_method_code>/", process_payment_card, name="process_payment_card"),
    path("payment_card/", get_payment_cards, name="get_payment_cards"),
]

urlpatterns = [path(f"{settings.BASE_URL}/vault/<str:version>/<str:channel_idx>/", include(api_paths))]
