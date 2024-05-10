from django import forms
from .models import sells

class SellsForm(forms.ModelForm):
    class Meta:
        model = sells
        fields = ('sells',)
