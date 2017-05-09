__author__ = 'igor'
from django import forms


class SearchForm(forms.Form):
    enter_company = forms.CharField(
        label='Enter GitHub User',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
