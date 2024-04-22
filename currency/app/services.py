import re
import requests
import datetime
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from app.models import Currency, Country, BasicCurrencyValues
from django.db.models import F
import plotly.graph_objects as go


countries_numbers_to_currencies = {
    "840": "52148",
    "978": "52170",
    "826": "52146",
    "392": "52246",
    "949": "52158",
    "356": "52238",
    "156": "52207",
}
currencies_to_countries_numbers = {
    "52148": "840",
    "52170": "978",
    "52146": "826",
    "52246": "392",
    "52158": "949",
    "52238": "356",
    "52207": "156",
}


def convert_country_to_currency(country):
    currency = []
    for c in country:
        currency.append(countries_numbers_to_currencies[str(c.number)])
    return currency


def create_currency(
    country=Country.objects.filter(number=840),
    start=datetime.date.today() - relativedelta(years=2),
    end=datetime.date.today(),
):
    currency = set(convert_country_to_currency(country))
    day_start = str(start.day)
    month_start = str(start.month)
    year_start = str(start.year)
    day_end = str(end.day)
    month_end = str(end.month)
    year_end = str(end.year)
    for curr in currency:
        url = (
            f"https://www.finmarket.ru/currency/rates/?"
            f"id=10148&pv=1&cur={int(curr)}&bd={day_start}&bm={month_start}&by={year_start}"
            f"&ed={day_end}&em={month_end}&ey={year_end}&x=37&y=15#archive"
        )

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.find_all("tr")
        base_value = BasicCurrencyValues.objects.get(title=int(curr))
        count = 0
        for tr in table[3:]:
            count +=1
            tr = str(tr)
            tr = re.sub(r"\<[^>]*\>", "-", tr).split("--")[1:-1]

            curr_obj = Currency.objects.update_or_create(
                title=int(curr),
                date=datetime.datetime.strptime(tr[0], "%d.%m.%Y"),
                course=tr[2].replace(",", "."),
                base_value=base_value,
            )
            if count == len(table[3:]):
                add_currency_to_country(
                    int(currencies_to_countries_numbers[curr]), curr_obj[0]
                )


def add_currency_to_country(country, curr_obj):
    Country.objects.filter(number=country).update(currency=curr_obj.id)


def create_countries():
    url = "https://www.iban.ru/currency-codes"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("tr")
    for tr in table[1:]:
        tr = str(tr)
        tr = re.sub(r"\<[^>]*\>", "", tr).split("\n")[1:-1]

        if tr[3] in countries_numbers_to_currencies.keys():
            Country.objects.update_or_create(
                name=tr[0],
                number=int(tr[3]),
            )


def create_basic_currency_values():
    currency = currencies_to_countries_numbers.keys()
    for curr in currency:
        url = (
            f"https://www.finmarket.ru/"
            f"currency/rates/?id=10148&pv=1&cur={int(curr)}&bd=31&bm=12&"
            f"by=2021&ed=1&em=1&ey=2022&x=76&y=11#archive"
        )
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find_all("tr")
        for tr in table[3:]:
            tr = str(tr)
            tr = re.sub(r"\<[^>]*\>", "-", tr).split("--")[1:-1]

            BasicCurrencyValues.objects.update_or_create(
                title=int(curr),
                defaults=dict(
                    title=int(curr),
                    date=datetime.datetime.strptime(tr[0], "%d.%m.%Y"),
                    course=tr[2].replace(",", "."),
                ),
            )



def calculation_of_relative_changes(country, start, end):
    currency = set(convert_country_to_currency(country))
    fig = go.Figure()
    for curr in currency:
        data = Currency.objects.filter(
            title=int(curr), date__range=(start, end)
        ).annotate(division_result=F("course") / F("base_value__course")).values_list("date", "division_result", "country__name")

        figure = add_trc(data, fig)
    chart = build_chart(figure)
    return chart


def add_trc(data, fig):
    x = []
    y = []
    name = set()
    for t in data:
        x.append(t[0])
        y.append(t[1])
        if not t[2] is None:
            name.add(t[2])
    if len(name) > 10:
        count = 0
        name_str = ""
        for n in name:
            count +=1
            if count == 10:
                name_str = name_str + str(n).strip() + ", <br>"
                count = 0
            else:
                name_str = name_str + str(n).strip() + ", "
    else:
        name_str = f", ".join(name)
    name_str += '<br>'
    fig.add_trace(go.Scatter(x=x, y=y, name=name_str, showlegend=True, legendwidth=1200))
    return fig


def build_chart(figure):
    figure.update_layout(legend_orientation="h",
                         legend=dict(
                             y=-0.3, 
                             yanchor="top"
                             ),
                             title="Валюты стран",
                             xaxis_title="Дата",
                             yaxis_title="Относительные изменения курсов валют(в сравнении с 31.12.2021)",
                             height=1000,
                             )

    chart = figure.to_html(full_html=False, config = {'displayModeBar': False})
    return chart
