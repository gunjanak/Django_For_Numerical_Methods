from django import forms

class IntegrationForm(forms.Form):
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')
    
