from django import forms

class IntegrationForm(forms.Form):
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')
    
class FormulaEvaluationForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    x_value = forms.FloatField(label='Value of x')

