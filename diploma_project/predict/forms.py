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
        widgets = { 
                    'A': forms.NumberInput(attrs={'style': 'width: 270px'}),
                    'b': forms.NumberInput(attrs={'style': 'width: 270px'}),
                    'w': forms.NumberInput(attrs={'style': 'width: 270px'}),
                    'T': forms.NumberInput(attrs={'style': 'width: 270px'})
                    }