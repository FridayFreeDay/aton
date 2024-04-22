from django.contrib import admin

from app.models import Currency, Country, BasicCurrencyValues


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "number", "currency"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "course", "date", "base_value"]


@admin.register(BasicCurrencyValues)
class BasicCurrencyValuesAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "course", "date"]
