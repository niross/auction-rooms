from django.contrib import admin
from .models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'symbol'
    )

admin.site.register(Currency, CurrencyAdmin)
