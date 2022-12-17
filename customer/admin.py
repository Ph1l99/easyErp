from django.contrib import admin

from customer.models import FidelityCard, Customer


class FidelityCardAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'is_active')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name')


admin.site.register(FidelityCard, FidelityCardAdmin)
admin.site.register(Customer, CustomerAdmin)
