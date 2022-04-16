from django import forms
from .models import Input

class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        exclude = ("user", )