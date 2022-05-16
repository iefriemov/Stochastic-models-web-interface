from django import forms
from .models import Input, Choose_Model

class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        exclude = ("user", )
        
        
        
class ModelForm(forms.ModelForm):
    class Meta:
        model = Choose_Model
        exclude = ("user", )