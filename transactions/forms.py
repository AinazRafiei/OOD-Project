# forms.py
from django import forms


class ChargeForm(forms.Form):
    amount = forms.IntegerField(
        max_value=10000,
        min_value=1,
    )


class WithdrawForm(forms.Form):
    amount = forms.IntegerField(
        max_value=10000,
        min_value=1,
    )