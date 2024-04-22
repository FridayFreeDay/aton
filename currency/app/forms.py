import datetime
from django import forms
from app.models import Country


class FilterForm(forms.Form):
    this_year = datetime.date.today().year
    years = tuple(range(this_year - 2, this_year+1))
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=years),
                                 label="Дата | От")
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=years),
                                label="Дата | До",
                                initial=datetime.date.today())

    country = forms.ModelMultipleChoiceField(queryset=Country.objects.all(),
                                widget=forms.CheckboxSelectMultiple,
                                label="Валюта", initial=False)
