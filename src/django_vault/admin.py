# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib import admin

from django_vault.models import APIKey, Channel, ChannelPayment, CustomerPaymentVault
from django_vault.utils.api_keys import access_installed, mask_key


@admin.register(CustomerPaymentVault)
class CustomerPaymentVault(admin.ModelAdmin):
    model = CustomerPaymentVault
    list_display = ["id", "customer"]
    list_filter = ["customer"]
    search_fields = ["customer", "first_transaction_id", "ext_customer_id"]
    readonly_fields = ["id", "created_at", "modified_at", "first_transaction_id", "ext_customer_id"]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """Keys show only their last four characters; with django_access installed they are read-only (tokens rule).

    Legacy path: a key's value is shown once, by ``vault-generate-api-key``; a row added here has a random value
    nobody can read back, so create keys with the command and use this page to review or delete them.
    """

    model = APIKey
    list_display = ["id", "masked_key", "created_at", "modified_at"]
    list_filter = ["created_at", "modified_at"]
    readonly_fields = ["id", "masked_key", "created_at", "modified_at"]

    @admin.display(description="key")
    def masked_key(self, obj) -> str:
        return mask_key(obj.key)

    def has_add_permission(self, request) -> bool:
        return not access_installed() and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return not access_installed() and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return not access_installed() and super().has_delete_permission(request, obj)


class ChannelPaymentInline(admin.TabularInline):
    model = ChannelPayment
    readonly_fields = ["id"]
    extra = 0


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    model = Channel
    inlines = [ChannelPaymentInline]
    list_display = ["id", "idx", "created_at", "modified_at"]
    list_filter = ["created_at", "modified_at"]
    search_fields = ["idx"]
    readonly_fields = ["id", "created_at", "modified_at"]
