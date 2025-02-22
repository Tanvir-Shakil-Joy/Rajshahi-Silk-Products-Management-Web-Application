from django import forms
from .models import SilkProduct

class SilkProductForm(forms.ModelForm):
    class Meta:
        model = SilkProduct
        fields = ['name', 'type', 'price', 'availability']