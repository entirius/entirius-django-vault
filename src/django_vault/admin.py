# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib import admin

from django_vault.models import APIKey, Channel, ChannelPayment, CustomerPaymentVault


@admin.register(CustomerPaymentVault)
class CustomerPaymentVault(admin.ModelAdmin):
    model = CustomerPaymentVault
    list_display = ["id", "customer"]
    list_filter = ["customer"]
    search_fields = ["customer", "first_transaction_id", "ext_customer_id"]
    readonly_fields = ["id", "created_at", "modified_at", "first_transaction_id", "ext_customer_id"]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    model = APIKey
    list_display = ["id", "key", "created_at", "modified_at"]
    list_filter = ["created_at", "modified_at"]
    search_fields = ["key"]
    readonly_fields = ["id", "created_at", "modified_at"]


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
