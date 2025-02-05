from django import forms

class StockSymbolForm(forms.Form):
    text_input = forms.CharField(label='Enter text', max_length=100)
