from django.db import models
import datetime


class Currency(models.Model):
    class Curr(models.TextChoices):
        USD = "52148", "Доллар"
        EUR = "52170", "Eвро"
        GBP = "52146", "Фунт"
        JPY = "52246", "Японская йена"
        TRY = "52158", "Турецкая лира"
        INR = "52238", "Индийская рупия"
        CNY = "52207", "Китайский юань"

    title = models.IntegerField(choices=tuple(map(lambda x: (int(x[0]), x[1]),
                                                  Curr.choices)),
                                default=Curr.USD,
                                verbose_name="Название валюты")
    date = models.DateField(verbose_name="Дата", default=datetime.date.today())
    course = models.DecimalField(decimal_places=4, max_digits=8,
                                 verbose_name="Курс", null=True)
    base_value = models.ForeignKey(to="BasicCurrencyValues", on_delete=models.DO_NOTHING,
                                   null=True, default=None,
                                   related_name="current_value", verbose_name="Базовое значение")

    def __str__(self):
        return dict(self.Curr.choices)[str(self.title)] + "   " + str(self.date)

    class Meta:
        ordering = ["title", "-date"]
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название страны")
    number = models.IntegerField(default=840,
                                 verbose_name="Номер")
    currency = models.ForeignKey(to="Currency", on_delete=models.SET_NULL,
                                 default=None, related_name="country",
                                 null=True, verbose_name="Валюта")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class BasicCurrencyValues(models.Model):
    class Curr(models.TextChoices):
        USD = "52148", "Доллар"
        EUR = "52170", "Eвро"
        GBP = "52146", "Фунт"
        JPY = "52246", "Японская йена"
        TRY = "52158", "Турецкая лира"
        INR = "52238", "Индийская рупия"
        CNY = "52207", "Китайский юань"

    title = models.IntegerField(choices=tuple(map(lambda x: (int(x[0]), x[1]),
                                                  Curr.choices)),
                                default=Curr.USD,
                                verbose_name="Название валюты", unique=True)
    date = models.DateField(verbose_name="Дата", default=datetime.date.today())
    course = models.DecimalField(decimal_places=4, max_digits=8,
                                 verbose_name="Курс", null=True)

    def __str__(self):
        return dict(self.Curr.choices)[str(self.title)] + "   " + str(self.date)

    class Meta:
        ordering = ["title", "-date"]
        verbose_name = "Основные значения валюты"
        verbose_name_plural = "Основные значения валют"