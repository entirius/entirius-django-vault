# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import uuid

from django.views.decorators.csrf import csrf_exempt
from django_utils.api.decorators import api_view, authenticate, parse_body, require_authentication, require_http_method
from django_utils.api.exceptions import BadRequest, MethodNotAllowed, NotFound
from django_utils.api.responses import Response
from process_logger.process_logger import ProcessLogger

from django_vault.domain.dto.card import PayUAddCardPayload, PayUDeleteCardPayload
from django_vault.models.channel import ChannelPayment
from django_vault.models.customer_vault import CustomerPaymentVault
from django_vault.utils.decorators import authorize_api


@api_view
@csrf_exempt
@authenticate
@authorize_api
@require_authentication
@require_http_method("GET", "DELETE", "POST")
def process_payment_card(request, channel_idx: str, payment_method_code: str, *args, **kwargs):
    logger = ProcessLogger("DJANGO_VAULT_API - process_payment_card")

    def get_customer_and_provider(request, channel_idx, payment_method_code, create_customer=False):
        customer = request.user.customer if (request.user is not None and request.user.is_customer) else None
        if customer is None:
            logger.set_code(4001)
            logger.error("Customer does not exist.")
            raise NotFound("4001")

        if not customer.email:
            logger.set_code(4002)
            logger.error("Customer does not have email or ext_customer_id.")
            raise NotFound("4002")

        channel = ChannelPayment.objects.filter(
            channel__idx=channel_idx, provider__in=[payment_method_code, f"{payment_method_code}_add"]
        ).first()

        if channel is None:
            logger.set_code(4003)
            logger.error("ChannelPayment does not exist.")
            raise NotFound("4003")
        customer_vault = CustomerPaymentVault.objects.filter(
            customer__user__email=customer.email, channel_for_payment__channel__idx=channel_idx
        ).first()
        first_transaction_id = uuid.uuid4()
        if customer_vault is None and create_customer:
            customer_vault = CustomerPaymentVault.objects.create(customer=customer, channel_for_payment=channel)
            first_transaction_id = customer_vault.first_transaction_id
        elif customer_vault is None:
            return None

        provider = channel.get_provider()
        provider.additional_data = channel.additional_data
        provider.ext_customer_id = customer_vault.ext_customer_id
        provider.first_transaction_id = first_transaction_id
        provider.email = str(customer_vault.customer.email)
        provider.request = request
        return provider

    def get_card_list_for_pm(request, channel_idx: str, payment_method_code: str, *args, **kwargs):
        provider = get_customer_and_provider(request, channel_idx, payment_method_code)
        if provider is None:
            return Response([])

        card_list = provider.get_card_list()
        return Response(card_list)

    @parse_body(PayUAddCardPayload.Schema)
    def add_card_for_pm(request, channel_idx: str, payment_method_code: str, body: PayUAddCardPayload, *args, **kwargs):
        provider = get_customer_and_provider(request, channel_idx, f"{payment_method_code}_add", create_customer=True)
        try:
            is_successfully_added = provider.add_card(body.token)
        except ValueError as e:
            logger.set_code(4004)
            logger.exception(e)
            raise BadRequest("4004")
        except Exception as e:
            logger.set_code(4005)
            logger.exception(e)
            raise NotFound("4005")

        if is_successfully_added:
            return Response({"status": "success"})
        else:
            return Response({"status": "error"})

    @parse_body(PayUDeleteCardPayload.Schema)
    def delete_card_for_pm(
        request, channel_idx: str, payment_method_code: str, body: PayUDeleteCardPayload, *args, **kwargs
    ):
        provider = get_customer_and_provider(request, channel_idx, payment_method_code)
        if provider is None:
            raise NotFound("4006")
        is_successfully_deleted = provider.delete_card(body.token)

        if is_successfully_deleted:
            return Response({"status": "success"})
        else:
            return Response({"status": "error"})

    match request.method:
        case "GET":
            return get_card_list_for_pm(request, channel_idx, payment_method_code, *args, **kwargs)
        case "DELETE":
            return delete_card_for_pm(request, channel_idx, payment_method_code, *args, **kwargs)
        case "POST":
            return add_card_for_pm(request, channel_idx, payment_method_code, *args, **kwargs)
        case _:
            raise MethodNotAllowed


def get_all_card_for_customer(channel_idx, customer):
    customer_vaults = CustomerPaymentVault.objects.filter(
        channel_for_payment__channel__idx=channel_idx, customer=customer
    )
    if not customer_vaults:
        return Response([])

    cards = []
    for customer_vault in customer_vaults:
        provider = customer_vault.channel_for_payment.get_provider()
        provider.additional_data = customer_vault.channel_for_payment.additional_data
        provider.ext_customer_id = customer_vault.ext_customer_id
        provider.email = str(customer_vault.customer.email)
        card_list = provider.get_card_list()
        if card_list:
            cards.append(card_list)
    return cards


@api_view
@csrf_exempt
@authenticate
@authorize_api
@require_authentication
@require_http_method("GET")
def get_payment_cards(request, channel_idx: str, *args, **kwargs):
    logger = ProcessLogger("DJANGO_VAULT_API - get_payment_cards")
    customer = request.user.customer if (request.user is not None and request.user.is_customer) else None
    if customer is None:
        logger.set_code(4001)
        logger.error("Customer does not exist.")
        raise NotFound("4001")

    if not customer.email:
        logger.set_code(4007)
        logger.error("Customer does not have email.")
        raise BadRequest("Customer does not have email.")

    cards = get_all_card_for_customer(channel_idx, customer)
    return Response(cards)
