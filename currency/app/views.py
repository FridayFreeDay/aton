from django.shortcuts import render, redirect
from app.forms import FilterForm
from app.services import (create_currency,
                          create_countries,
                          create_basic_currency_values,
                          calculation_of_relative_changes)


def upload(request):
    create_countries()
    create_basic_currency_values()
    return redirect("home")


def start(request):
    return render(request, template_name="start.html")


def home(request):
    data_for_chart = "Необходимо выбрать страну"
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            create_currency(country=f["country"],
                         start=f["start_date"],
                         end=f["end_date"])
            data_for_chart = calculation_of_relative_changes(country=f["country"],
                         start=f["start_date"],
                         end=f["end_date"])
            # print(data_for_chart)
    else:
        form = FilterForm()
    data = {
        "form": form,
        "chart": data_for_chart,
    }
    return render(request, template_name="home.html", context=data)
